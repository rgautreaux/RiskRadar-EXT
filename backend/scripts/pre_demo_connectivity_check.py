"""Pre-demo connectivity preflight for RiskRadar.

Purpose:
- Fail fast when frontend/backend/API wiring is broken before running demos.
- Enforce a canonical local topology by default:
  - Backend API: http://127.0.0.1:8001
  - Frontend PHP: http://127.0.0.1:8080

Usage (from repository root):
    python backend/scripts/pre_demo_connectivity_check.py

Optional:
    python backend/scripts/pre_demo_connectivity_check.py --no-enforce-canonical
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_BACKEND_URL = "http://127.0.0.1:8001"
DEFAULT_API_PREFIX = "/api/v1"
DEFAULT_FRONTEND_URL = "http://127.0.0.1:8080/index.php"
DEFAULT_MAP_URL = "http://127.0.0.1:8080/map.php"
DEFAULT_TIMEOUT_SECONDS = 6.0


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str


def _normalize_base_url(value: str) -> str:
    return value.rstrip("/")


def _normalize_prefix(value: str) -> str:
    if not value:
        return DEFAULT_API_PREFIX
    value = value.strip()
    if not value.startswith("/"):
        value = "/" + value
    return value.rstrip("/") or DEFAULT_API_PREFIX


def _http_request(url: str, timeout: float, method: str = "GET", headers: dict[str, str] | None = None) -> tuple[int, str, dict[str, str]]:
    request = Request(url=url, method=method, headers=headers or {})
    with urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
        response_headers = {k.lower(): v for (k, v) in response.headers.items()}
        return response.status, body, response_headers


def _check_json_endpoint(name: str, url: str, timeout: float) -> CheckResult:
    try:
        status, body, _ = _http_request(url, timeout=timeout)
    except HTTPError as error:
        return CheckResult(name=name, ok=False, details=f"HTTP {error.code} from {url}")
    except (URLError, TimeoutError, OSError) as error:
        reason = getattr(error, "reason", str(error))
        return CheckResult(name=name, ok=False, details=f"Connection error to {url}: {reason}")

    if status != 200:
        return CheckResult(name=name, ok=False, details=f"Expected HTTP 200, got {status} from {url}")

    try:
        json.loads(body)
    except json.JSONDecodeError:
        return CheckResult(name=name, ok=False, details=f"Response from {url} is not valid JSON")

    return CheckResult(name=name, ok=True, details=f"OK ({url})")


def _check_assistant_user_lookup(base_url: str, api_prefix: str, timeout: float) -> CheckResult:
    url = f"{base_url}{api_prefix}/assistant/respond"
    payload = json.dumps(
        {
            "message": "connectivity probe",
            "page_context": "assistant",
            "user_id": 1,
            "location": "Baton Rouge",
        }
    ).encode("utf-8")

    request = Request(
        url=url,
        method="POST",
        data=payload,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
    except HTTPError as error:
        status = error.code
        body = error.read().decode("utf-8", errors="replace") if error.fp is not None else ""
    except (URLError, TimeoutError, OSError) as error:
        reason = getattr(error, "reason", str(error))
        return CheckResult(
            name="assistant user lookup",
            ok=False,
            details=f"Connection error to {url}: {reason}",
        )

    if status >= 500:
        return CheckResult(
            name="assistant user lookup",
            ok=False,
            details=(
                f"Received HTTP {status} from {url}. "
                "This usually indicates backend/db schema drift (for example missing users columns)."
            ),
        )

    # Any non-5xx response keeps connectivity health green; auth/validation can vary by environment.
    try:
        if body:
            json.loads(body)
    except json.JSONDecodeError:
        return CheckResult(
            name="assistant user lookup",
            ok=False,
            details=f"Response from {url} is not valid JSON",
        )

    return CheckResult(name="assistant user lookup", ok=True, details=f"OK (HTTP {status})")


def _load_frontend_api_config() -> dict[str, Any]:
    php_expression = (
        "$config = require 'frontend/web/config/app.php';"
        "if (!is_array($config)) { fwrite(STDERR, 'config-not-array'); exit(2); }"
        "echo json_encode($config);"
    )

    completed = subprocess.run(
        ["php", "-r", php_expression],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )

    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip() or "unknown php error"
        raise RuntimeError(f"Unable to load frontend config via PHP CLI: {stderr}")

    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Frontend config output was not valid JSON: {error}") from error

    if not isinstance(parsed, dict):
        raise RuntimeError("Frontend config root is not an object")

    return cast(dict[str, Any], parsed)


def _frontend_origin(frontend_url: str) -> str:
    parsed = urlparse(frontend_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid frontend URL: {frontend_url}")
    return f"{parsed.scheme}://{parsed.netloc}"


def run_preflight(enforce_canonical: bool, timeout_seconds: float) -> int:
    results: list[CheckResult] = []

    try:
        config = _load_frontend_api_config()
    except RuntimeError as error:
        print(f"FAIL: frontend config load: {error}")
        return 1

    api_raw = config.get("api")
    api: dict[str, Any] = cast(dict[str, Any], api_raw) if isinstance(api_raw, dict) else {}
    configured_base_url = _normalize_base_url(str(api.get("base_url") or DEFAULT_BACKEND_URL))
    configured_prefix = _normalize_prefix(str(api.get("prefix") or DEFAULT_API_PREFIX))

    if enforce_canonical:
        canonical_base = _normalize_base_url(DEFAULT_BACKEND_URL)
        canonical_prefix = _normalize_prefix(DEFAULT_API_PREFIX)

        if configured_base_url != canonical_base:
            results.append(
                CheckResult(
                    name="canonical backend base",
                    ok=False,
                    details=(
                        f"Configured frontend API base_url is {configured_base_url}, expected {canonical_base}. "
                        "Update frontend/web/config/app.php, config.local.php, or RISKRADAR_API_BASE_URL."
                    ),
                )
            )
        else:
            results.append(CheckResult(name="canonical backend base", ok=True, details=f"OK ({configured_base_url})"))

        if configured_prefix != canonical_prefix:
            results.append(
                CheckResult(
                    name="canonical API prefix",
                    ok=False,
                    details=f"Configured API prefix is {configured_prefix}, expected {canonical_prefix}",
                )
            )
        else:
            results.append(CheckResult(name="canonical API prefix", ok=True, details=f"OK ({configured_prefix})"))

    # Backend root and representative API routes.
    results.append(_check_json_endpoint("backend root", f"{configured_base_url}/", timeout_seconds))
    results.append(_check_json_endpoint("readiness API", f"{configured_base_url}{configured_prefix}/health/ready", timeout_seconds))
    results.append(_check_json_endpoint("alerts API", f"{configured_base_url}{configured_prefix}/alerts?limit=1", timeout_seconds))
    results.append(
        _check_json_endpoint(
            "forecast API",
            f"{configured_base_url}{configured_prefix}/forecast?lat=34.0522&lon=-118.2437",
            timeout_seconds,
        )
    )
    results.append(_check_assistant_user_lookup(configured_base_url, configured_prefix, timeout_seconds))

    # Frontend pages should render and map page should include API endpoints.
    for label, page_url in (("frontend index", DEFAULT_FRONTEND_URL), ("frontend map", DEFAULT_MAP_URL)):
        try:
            status, body, _ = _http_request(page_url, timeout=timeout_seconds)
        except HTTPError as error:
            results.append(CheckResult(name=label, ok=False, details=f"HTTP {error.code} from {page_url}"))
            continue
        except (URLError, TimeoutError, OSError) as error:
            reason = getattr(error, "reason", str(error))
            results.append(CheckResult(name=label, ok=False, details=f"Connection error to {page_url}: {reason}"))
            continue

        if status != 200:
            results.append(CheckResult(name=label, ok=False, details=f"Expected HTTP 200, got {status}"))
            continue

        if label == "frontend map":
            expected_alerts_url = f"{configured_base_url}{configured_prefix}/alerts/map"
            expected_risk_url = f"{configured_base_url}{configured_prefix}/risk/map"
            expected_alerts_url_escaped = expected_alerts_url.replace("/", "\\/")
            expected_risk_url_escaped = expected_risk_url.replace("/", "\\/")
            map_ok = (
                (expected_alerts_url in body or expected_alerts_url_escaped in body)
                and (expected_risk_url in body or expected_risk_url_escaped in body)
            )
            details = (
                "Map page includes configured API endpoints"
                if map_ok
                else (
                    "Map page did not include configured API endpoints. "
                    f"Expected markers for {expected_alerts_url} and {expected_risk_url}"
                )
            )
            results.append(CheckResult(name="frontend map API wiring", ok=map_ok, details=details))
        else:
            results.append(CheckResult(name=label, ok=True, details=f"OK ({page_url})"))

    # CORS preflight from frontend origin to backend.
    origin = _frontend_origin(DEFAULT_FRONTEND_URL)
    preflight_url = f"{configured_base_url}{configured_prefix}/alerts"
    try:
        status, _, headers = _http_request(
            preflight_url,
            timeout=timeout_seconds,
            method="OPTIONS",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
            },
        )
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        results.append(CheckResult(name="CORS preflight", ok=False, details=f"Preflight request failed: {error}"))
    else:
        cors_origin = headers.get("access-control-allow-origin", "")
        cors_ok = status == 200 and cors_origin == origin
        results.append(
            CheckResult(
                name="CORS preflight",
                ok=cors_ok,
                details=(
                    f"OK (allow-origin={cors_origin})"
                    if cors_ok
                    else f"Expected HTTP 200 + allow-origin={origin}, got status={status}, allow-origin={cors_origin}"
                ),
            )
        )

    print("RiskRadar pre-demo connectivity preflight")
    print(f"Configured frontend backend base: {configured_base_url}")
    print(f"Configured frontend API prefix:  {configured_prefix}")
    print("")

    failed = False
    for result in results:
        icon = "PASS" if result.ok else "FAIL"
        print(f"[{icon}] {result.name}: {result.details}")
        failed = failed or (not result.ok)

    print("")
    if failed:
        print("Connectivity preflight failed. Resolve the failed checks before running demos.")
        return 1

    print("Connectivity preflight passed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run pre-demo connectivity checks for frontend/backend/API wiring.")
    parser.add_argument(
        "--no-enforce-canonical",
        action="store_true",
        help="Do not fail when frontend config differs from canonical local backend base/prefix.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="HTTP timeout in seconds for each probe.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return run_preflight(enforce_canonical=not args.no_enforce_canonical, timeout_seconds=args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
