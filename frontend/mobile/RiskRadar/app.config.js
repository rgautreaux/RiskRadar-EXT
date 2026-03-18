// Dynamic Expo config that merges the static app.json values with runtime
// environment overrides. The API base URL is intentionally NOT hard-coded
// here so each developer/environment can supply the correct value:
//
//   iOS simulator:      http://127.0.0.1:8000  (default code fallback)
//   Android emulator:   http://10.0.2.2:8000
//   Physical device:    http://<your-machine-ip>:8000
//
// Set the environment variable before starting the dev server:
//   API_BASE_URL=http://10.0.2.2:8000 npx expo start --android

/** @param {{ config: import('@expo/config-types').ExpoConfig }} ctx */
module.exports = ({ config }) => ({
  ...config,
  extra: {
    ...config.extra,
    // When API_BASE_URL is not set the value is undefined, which causes
    // riskService.ts to fall through to its own platform-appropriate default.
    apiBaseUrl: process.env.API_BASE_URL,
  },
});
