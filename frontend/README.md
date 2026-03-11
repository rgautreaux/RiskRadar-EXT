# Frontend Directory

This repository now separates the two frontend surfaces so they can evolve independently while sharing the same backend in `backend/`.

## Structure

- `mobile/` — existing Expo/React Native mobile application assets for RiskRadar.
- `web/` — dedicated CMPS 357 PHP web-app extension workspace.

## Shared Backend

Both frontend surfaces are intended to consume the same FastAPI backend and API routes implemented in `backend/`.

## Entry Points

- See `mobile/README.md` for the mobile frontend layout.
- See `web/README.md` for the web frontend scaffold and intended structure.
