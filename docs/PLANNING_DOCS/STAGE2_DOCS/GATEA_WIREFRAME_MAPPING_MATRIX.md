# Gate A Wireframe Mapping Matrix

Status: Draft
Owner: Rebecca (Layout Lane)
Last Updated: 2026-03-17

## Purpose

Map each in-scope page to wireframe regions, section hierarchy, and shared shell dependencies so Phase 1 implementation can proceed with a stable baseline.

## Canonical Page Scope

| Page | View File | In Scope |
|---|---|---|
| Home Dashboard | frontend/web/views/dashboard.php | Yes |
| Alerts | frontend/web/views/alerts.php | Yes |
| Summaries | frontend/web/views/summaries.php | Yes |
| Profile | frontend/web/views/profile.php | Yes |
| Login | frontend/web/views/login.php | Yes |
| Register | frontend/web/views/register.php | Yes |
| Risk | frontend/web/views/risk.php | Yes |
| Map | frontend/web/views/map.php | Yes |
| Forecast | frontend/web/views/forecast.php | Yes |
| Assistant | frontend/web/views/assistant.php | Yes |
| Alert Detail | frontend/web/views/alert_detail.php | Yes |
| Summary Detail | frontend/web/views/summary_detail.php | Yes |

## Wireframe Mapping Matrix

| Page | Required Regions (Ordered) | Existing Template | Shared Layout Dependency | Gap Notes |
|---|---|---|---|---|
| Home Dashboard | Topbar -> Primary Nav -> Local Risk Snapshot -> Global Risk Snapshot -> Alerts Preview -> Summaries Preview | frontend/web/views/dashboard.php | frontend/web/components/layout.php | Validate final card order against wireframe panels |
| Alerts | Topbar -> Primary Nav -> Alerts Header -> Notification List -> Filter/Meta Row | frontend/web/views/alerts.php | frontend/web/components/layout.php | Confirm alert grouping hierarchy |
| Summaries | Topbar -> Primary Nav -> Summaries Header -> Summary Cards -> Meta/Source Rows | frontend/web/views/summaries.php | frontend/web/components/layout.php | Confirm preview length and metadata position |
| Profile | Topbar -> Primary Nav -> Profile Header -> User Info Panel -> Preferences Panel | frontend/web/views/profile.php | frontend/web/components/layout.php | Confirm form section ordering |
| Login | Topbar (minimal) -> Auth Header -> Login Form -> Action Row | frontend/web/views/login.php | frontend/web/components/layout.php | Confirm minimal nav behavior for auth views |
| Register | Topbar (minimal) -> Auth Header -> Register Form -> Action Row | frontend/web/views/register.php | frontend/web/components/layout.php | Confirm field grouping in form grid |
| Risk | Topbar -> Primary Nav -> Risk Header -> Local vs Global Panels -> Supporting Metrics | frontend/web/views/risk.php | frontend/web/components/layout.php | Keep Stage 2 scaffold boundary intact |
| Map | Topbar -> Primary Nav -> Map Header -> Map Placeholder Region -> Legend/Meta | frontend/web/views/map.php | frontend/web/components/layout.php | Shell only; no functional expansion |
| Forecast | Topbar -> Primary Nav -> Forecast Header -> Forecast Panels -> Source/Time Meta | frontend/web/views/forecast.php | frontend/web/components/layout.php | Shell only; verify section hierarchy |
| Assistant | Topbar -> Primary Nav -> Assistant Header -> Prompt/Input Region -> Response Region | frontend/web/views/assistant.php | frontend/web/components/layout.php | Shell only; avoid feature behavior changes |
| Alert Detail | Topbar -> Primary Nav -> Detail Header -> Detail Body -> Related Actions | frontend/web/views/alert_detail.php | frontend/web/components/layout.php | Confirm detail metadata grouping |
| Summary Detail | Topbar -> Primary Nav -> Detail Header -> Summary Body -> Related Context | frontend/web/views/summary_detail.php | frontend/web/components/layout.php | Confirm hierarchy mirrors wireframe detail shell |

## Global Section Taxonomy (Layout Lane)

1. Topbar
2. Primary Navigation
3. Page Header
4. Primary Content Panel(s)
5. Metadata Row(s)
6. Action Row(s)

## Completion Checklist

- [ ] All in-scope pages included
- [ ] Region order verified against web wireframe
- [ ] Shared layout dependencies confirmed
- [ ] Gap notes resolved or intentionally deferred
