const STATIC_CACHE = 'riskradar-static-v1';
const API_CACHE = 'riskradar-api-v1';

const STATIC_ASSETS = [
  '/assets/app.css',
  '/assets/theme.css',
  '/assets/rr-web-ux.css',
  '/assets/rr-web-ux.js',
  '/login.php',
  '/index.php',
  '/alerts.php',
  '/assistant.php',
  '/map.php'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.addAll(STATIC_ASSETS)).catch(() => Promise.resolve())
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys
        .filter((key) => key !== STATIC_CACHE && key !== API_CACHE)
        .map((key) => caches.delete(key))
    ))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  if (req.method !== 'GET') {
    return;
  }

  if (url.pathname.includes('/api/v1/')) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(API_CACHE).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then((cached) => cached || new Response(JSON.stringify({ offline: true }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        })))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) {
        return cached;
      }

      return fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(STATIC_CACHE).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match('/login.php'));
    })
  );
});
