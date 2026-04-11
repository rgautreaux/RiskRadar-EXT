"""Notification provider abstraction for backend dispatch.

This module intentionally defaults to a no-op provider so backend logic can be
validated safely before integrating external push services.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from config.settings import settings


class NotificationProvider(Protocol):
    """Protocol for provider-specific push delivery adapters."""

    name: str

    def send(self, device_token: str, title: str, body: str) -> bool:
        """Send a push notification to a single device token."""


@dataclass(frozen=True)
class NoopNotificationProvider:
    """Safe default provider that records intent but performs no outbound calls."""

    name: str = "noop"

    def send(self, device_token: str, title: str, body: str) -> bool:
        # Intentionally succeeds to keep the dispatch pipeline deterministic in tests.
        _ = (device_token, title, body)
        return True


def get_notification_provider() -> NotificationProvider:
    """Return the configured notification provider adapter."""
    provider = settings.NOTIFICATION_PROVIDER.strip().lower()
    if provider in {"", "noop"}:
        return NoopNotificationProvider()

    # Keep unknown provider values safe and explicit until integration is added.
    return NoopNotificationProvider()
