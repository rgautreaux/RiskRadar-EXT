"""Tests for notification provider selection and fallback behavior."""

from notifications.provider import get_notification_provider


def test_default_provider_is_noop(monkeypatch):
    monkeypatch.setattr("config.settings.settings.NOTIFICATION_PROVIDER", "")
    provider = get_notification_provider()
    assert provider.name == "noop"


def test_expo_falls_back_without_token(monkeypatch):
    monkeypatch.setattr("config.settings.settings.NOTIFICATION_PROVIDER", "expo")
    monkeypatch.setattr("config.settings.settings.EXPO_ACCESS_TOKEN", "")
    provider = get_notification_provider()
    assert provider.name == "noop"


def test_expo_provider_selected_with_token(monkeypatch):
    monkeypatch.setattr("config.settings.settings.NOTIFICATION_PROVIDER", "expo")
    monkeypatch.setattr("config.settings.settings.EXPO_ACCESS_TOKEN", "token")
    provider = get_notification_provider()
    assert provider.name == "expo"


def test_fcm_falls_back_without_credentials(monkeypatch):
    monkeypatch.setattr("config.settings.settings.NOTIFICATION_PROVIDER", "fcm")
    monkeypatch.setattr("config.settings.settings.FCM_SERVER_KEY", "")
    monkeypatch.setattr("config.settings.settings.FCM_PROJECT_ID", "")
    provider = get_notification_provider()
    assert provider.name == "noop"


def test_fcm_provider_selected_with_credentials(monkeypatch):
    monkeypatch.setattr("config.settings.settings.NOTIFICATION_PROVIDER", "fcm")
    monkeypatch.setattr("config.settings.settings.FCM_SERVER_KEY", "server-key")
    monkeypatch.setattr("config.settings.settings.FCM_PROJECT_ID", "project-id")
    provider = get_notification_provider()
    assert provider.name == "fcm"
