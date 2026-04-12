from db.migrations import safety_gate


def test_safety_gate_passes_when_all_checks_pass(monkeypatch):
    monkeypatch.setattr(safety_gate, "run_preflight", lambda strict: 0)
    monkeypatch.setattr(safety_gate, "run_schema_drift_check", lambda: 0)
    monkeypatch.setattr(safety_gate, "run_validation", lambda: 0)
    monkeypatch.setattr(safety_gate, "run_monitoring", lambda: 0)

    assert safety_gate.run_safety_gate() == 0


def test_safety_gate_fails_when_any_check_fails(monkeypatch):
    monkeypatch.setattr(safety_gate, "run_preflight", lambda strict: 2)
    monkeypatch.setattr(safety_gate, "run_schema_drift_check", lambda: 0)
    monkeypatch.setattr(safety_gate, "run_validation", lambda: 0)
    monkeypatch.setattr(safety_gate, "run_monitoring", lambda: 0)

    assert safety_gate.run_safety_gate() == 2


def test_safety_gate_uses_non_strict_preflight_when_configured(monkeypatch):
    observed_strict_values: list[bool] = []

    def _fake_preflight(strict: bool) -> int:
        observed_strict_values.append(strict)
        return 0

    monkeypatch.setattr(safety_gate, "run_preflight", _fake_preflight)
    monkeypatch.setattr(safety_gate, "run_schema_drift_check", lambda: 0)
    monkeypatch.setattr(safety_gate, "run_validation", lambda: 0)
    monkeypatch.setattr(safety_gate, "run_monitoring", lambda: 0)
    monkeypatch.setenv("MIGRATION_PREFLIGHT_STRICT", "false")

    assert safety_gate.run_safety_gate() == 0
    assert observed_strict_values == [False]
