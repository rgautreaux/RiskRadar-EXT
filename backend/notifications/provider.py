"""Notification provider abstraction for backend dispatch.

This module intentionally defaults to a no-op provider so backend logic can be
validated safely before integrating external push services.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


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


@dataclass(frozen=True)
class ExpoNotificationProvider:
    """Scaffold provider for future Expo push integration."""

    name: str = "expo"

    def send(self, device_token: str, title: str, body: str) -> bool:
        # Integration scaffold only: intentionally no outbound API call yet.
        _ = (device_token, title, body)
        return False


@dataclass(frozen=True)
class FcmNotificationProvider:
    """Scaffold provider for future Firebase Cloud Messaging integration."""

    name: str = "fcm"

    def send(self, device_token: str, title: str, body: str) -> bool:
        # Integration scaffold only: intentionally no outbound API call yet.
        _ = (device_token, title, body)
        return False


def get_notification_provider() -> NotificationProvider:
    """Return the configured notification provider adapter."""
    provider = settings.NOTIFICATION_PROVIDER.strip().lower()
    if provider in {"", "noop"}:
        return NoopNotificationProvider()

    if provider == "expo":
        if settings.EXPO_ACCESS_TOKEN:
            return ExpoNotificationProvider()
        logger.warning("notifications.provider_fallback provider=expo reason=missing_access_token")
        return NoopNotificationProvider()

    if provider == "fcm":
        if settings.FCM_SERVER_KEY and settings.FCM_PROJECT_ID:
            return FcmNotificationProvider()
        logger.warning("notifications.provider_fallback provider=fcm reason=missing_credentials")
        return NoopNotificationProvider()

    # Keep unknown provider values safe and explicit until integration is added.
    logger.warning("notifications.provider_fallback provider=%s reason=unknown", provider)
    return NoopNotificationProvider()
