/* SoulSkill PWA service worker.
 * Cache only the app shell and same-origin static assets. Never cache API,
 * authorization-bearing, or non-GET requests.
 */
const CACHE_PREFIX = 'soulskill-pwa-';
const SHELL_CACHE = CACHE_PREFIX + 'shell-v2';
const RUNTIME_CACHE = CACHE_PREFIX + 'runtime-v2';
const SHELL_FILES = [
  './',
  './index.html',
  './offline.html',
  './manifest.json',
  './favicon.png',
  './icons/Icon-192.png',
  './icons/Icon-512.png',
  './icons/Icon-maskable-192.png',
  './icons/Icon-512.svg',
  './icons/Icon-maskable-512.svg'
];
const STATIC_FILE = /\.(?:js|mjs|css|json|wasm|bin|dat|png|jpe?g|svg|webp|ico|woff2?|ttf|otf)$/i;
const API_PATH = /\/(?:api|auth|v1|health)(?:\/|$)/i;

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL_CACHE);
    await Promise.all(SHELL_FILES.map(async (file) => {
      try {
        await cache.add(file);
      } catch (error) {
        // Optional icons or generated files may not exist in every build.
        console.warn('SoulSkill shell asset was not cached:', file, error);
      }
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const cacheNames = await caches.keys();
    const currentCaches = [SHELL_CACHE, RUNTIME_CACHE];
    await Promise.all(
      cacheNames
        .filter((name) => name.startsWith(CACHE_PREFIX) && !currentCaches.includes(name))
        .map((name) => caches.delete(name))
    );
    await self.clients.claim();
  })());
});

async function trimRuntimeCache(cache, maxEntries = 120) {
  const keys = await cache.keys();
  if (keys.length <= maxEntries) return;
  await Promise.all(keys.slice(0, keys.length - maxEntries).map((key) => cache.delete(key)));
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET' || request.headers.has('authorization') || request.headers.has('range')) return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin || API_PATH.test(url.pathname)) return;
  if (/\/version\.json$/i.test(url.pathname)) return;

  const isNavigation = request.mode === 'navigate';
  const isStaticAsset = STATIC_FILE.test(url.pathname)
    || url.pathname.includes('/assets/')
    || url.pathname.includes('/canvaskit/');

  if (isNavigation) {
    event.respondWith((async () => {
      try {
        const response = await fetch(request);
        if (response.ok && response.type === 'basic' && !/no-store|private/i.test(response.headers.get('cache-control') || '')) {
          const cache = await caches.open(SHELL_CACHE);
          await cache.put('./index.html', response.clone());
        }
        return response;
      } catch (_) {
        return (await caches.match('./index.html'))
          || (await caches.match('./offline.html'))
          || new Response('You are offline. Reconnect and try again.', {
            status: 503,
            headers: { 'Content-Type': 'text/plain; charset=utf-8' }
          });
      }
    })());
    return;
  }

  if (!isStaticAsset) return;
  event.respondWith((async () => {
    const cache = await caches.open(RUNTIME_CACHE);
    try {
      const response = await fetch(request);
      if (response.ok && response.type === 'basic' && !/no-store|private/i.test(response.headers.get('cache-control') || '')) {
        await cache.put(request, response.clone());
        await trimRuntimeCache(cache);
      }
      return response;
    } catch (_) {
      return (await cache.match(request)) || (await caches.match(request)) || Response.error();
    }
  })());
});
