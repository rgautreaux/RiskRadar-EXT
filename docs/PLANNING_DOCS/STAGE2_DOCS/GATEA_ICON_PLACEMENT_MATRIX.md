# Gate A Icon Placement Matrix

Status: Draft
Owner: Rebecca (Layout Lane)
Last Updated: 2026-03-17

## Purpose

Define where icons appear by page and region, with asset type and size conventions, so icon treatment remains consistent during Phase 1 and Phase 2 implementation.

## Icon Sizing Convention

- icon-sm: 16x16
- icon-md: 24x24
- icon-lg: 32x32
- icon-xl: 48x48

## Asset Type Rules

- PNG: Branded, illustrative, and named wireframe assets.
- CSS badge: Repeated status/chip indicators where custom image is not required.

## Icon Placement Matrix

| Page | Region | Icon Asset | Asset Type | Target Size Class | Fallback Rule | Notes |
|---|---|---|---|---|---|---|
| Home Dashboard | Local Risk Snapshot | wireframe_icons/RiskRadar_Local_Icon.png | PNG | icon-lg | If missing, render text badge Local | Pair with local risk cards |
| Home Dashboard | Global Risk Snapshot | wireframe_icons/RiskRadar_DEST_Global_Icon.png | PNG | icon-lg | If missing, render text badge Global | Use one global marker per panel |
| Alerts | Alerts Header | wireframe_icons/RiskRadar_ALERT_NotifIcon.png | PNG | icon-md | If missing, use CSS bell badge | Header marker only |
| Alerts | Notification Window | wireframe_icons/RiskRadar_ALERT_NotifWindow.png | PNG | icon-xl | If missing, show bordered placeholder block | Window shell indicator |
| Summaries | Summary Metadata | wireframe_icons/RiskRadar_DataHeader_Format.png | PNG | icon-md | If missing, preserve metadata text row | Metadata region marker |
| Profile | Header Branding | wireframe_icons/RiskRadar_STND_Logo.png | PNG | icon-lg | If missing, use text logo RiskRadar | Branding only |
| Login | Auth Header | wireframe_icons/RiskRadar_STND_Text.png | PNG | icon-lg | If missing, render plain title text | Keep auth shell minimal |
| Register | Auth Header | wireframe_icons/RiskRadar_STND_Text.png | PNG | icon-lg | If missing, render plain title text | Match login treatment |
| Risk | Local EQ/Flood/Fire/Wind rows | wireframe_icons/RiskRadar_LocalEQ_Icon.png; wireframe_icons/RiskRadar_LocalFlood_Icon.png; wireframe_icons/RiskRadar_LocalFIre_Icon.png; wireframe_icons/RiskRadar_LocalWindEvent_Icon.png | PNG | icon-md | If missing, use CSS category chip | Preserve row ordering |
| Risk | Global EQ/Flood/Fire/Wind rows | wireframe_icons/RiskRadar_GlobalEQ_Icon.png; wireframe_icons/RiskRadar_GlobalFlood_Icon.png; wireframe_icons/RiskRadar_GlobalFire_Icon.png; wireframe_icons/RiskRadar_GlobalWindEvent_Icon.png | PNG | icon-md | If missing, use CSS category chip | Preserve row ordering |
| Risk | Environmental rows | wireframe_icons/RiskRadar_AirQuality_Icon.png; wireframe_icons/RiskRadar_Pollen_Icon.png; wireframe_icons/RiskRadar_Pollution_Icon.png; wireframe_icons/RiskRadar_Weather_Icon.png | PNG | icon-md | If missing, use CSS environmental chip | Match wireframe grouping |
| Map | Page Header | wireframe_icons/RiskRadar_STND_HomeBttn.png | PNG | icon-sm | If missing, omit icon and keep label | Shell-only page |
| Forecast | Page Header | wireframe_icons/RiskRadar_STND_HomeBttn.png | PNG | icon-sm | If missing, omit icon and keep label | Shell-only page |
| Assistant | Header | wireframe_icons/RiskRadar_Assistant_Icon.png | PNG | icon-md | If missing, use CSS assistant badge | Shell-only page |
| Alert Detail | Detail Header | wireframe_icons/RiskRadar_ALERT_Text.png | PNG | icon-md | If missing, render plain section title | Detail shell parity |
| Summary Detail | Detail Header | wireframe_icons/RiskRadar_STND_Text.png | PNG | icon-md | If missing, render plain section title | Detail shell parity |

## Completion Checklist

- [ ] Icon entries exist for all in-scope pages
- [ ] Size class assigned for each placement
- [ ] Fallback rule assigned for each placement
- [ ] PNG vs CSS-badge usage follows hybrid strategy

## Naming Consistency Pass (2026-03-17)

Result: Completed with corrections.

Corrections applied:
1. Normalized icon asset references to include the wireframe_icons/ prefix across all rows.

No remaining naming mismatches found between page names in this file and GATEA_WIREFRAME_MAPPING_MATRIX.md.
