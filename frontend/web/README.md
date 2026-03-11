# Web Frontend

This directory is the designated location for the CMPS 357 PHP web-app extension.

## Intended Structure

- `views/` — page templates and routed screens
- `components/` — reusable UI fragments
- `services/` — backend API wrappers and normalization helpers
- `public/` — public assets and entry files
- `config/` — environment and runtime configuration templates

## Purpose

The web frontend is intentionally separate from the existing mobile frontend in `frontend/mobile/` so both frontends can develop independently while sharing the same backend in `backend/`.
