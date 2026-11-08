/* SoulSkill PWA service worker. API and authenticated requests are never cached. */
const CACHE_PREFIX = 'soulskill-pwa-';
const SHELL_CACHE = CACHE_PREFIX + 'shell-v1';
const RUNTIME_CACHE = CACHE_PREFIX + 'runtime-v1';
const SHELL_FILES = [
  './', './index.html', './manifest.json', './favicon.png',
  './icons/Icon-192.png', './icons/Icon-512.png',
  './icons/Icon-maskable-192.png', './icons/Icon-512.svg', './icons/Icon-maskable-512.svg'
];
const STATIC_FILE = /\.(?:js|mjs|css|json|wasm|bin|dat|png|jpe?g|svg|webp|ico|woff2?|ttf|otf)$/i;
self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL_CACHE);
    await Promise.all(SHELL_FILES.map(async (file) => {
      try { await cache.add(file); } catch (error) { console.warn('SoulSkill shell asset was not cached:', file, error); }
    }));
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const cacheNames = await caches.keys();
    await Promise.all(cacheNames.filter((name) => name.startsWith(CACHE_PREFIX)
      && ![SHELL_CACHE, RUNTIME_CACHE].includes(name)).map((name) => caches.delete(name)));
    await self.clients.claim();
  })());
});
self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET' || request.headers.has('authorization')) return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (/\/(?:api|auth|v1|health)(?:\/|$)/i.test(url.pathname) || /\/version\.json$/i.test(url.pathname)) return;
  const isNavigation = request.mode === 'navigate';
  const isStaticAsset = STATIC_FILE.test(url.pathname) || url.pathname.includes('/assets/') || url.pathname.includes('/canvaskit/');
  if (!isNavigation && !isStaticAsset) return;
  if (isNavigation) {
    event.respondWith((async () => {
      try {
        const response = await fetch(request);
        if (response.ok && response.type === 'basic') {
          const cache = await caches.open(SHELL_CACHE);
          await cache.put('./index.html', response.clone());
        }
        return response;
      } catch (_) { return (await caches.match('./index.html')) || Response.error(); }
    })());
    return;
  }
  event.respondWith((async () => {
    const cache = await caches.open(RUNTIME_CACHE);
    try {
      const response = await fetch(request);
      if (response.ok && response.type === 'basic') await cache.put(request, response.clone());
      return response;
    } catch (_) { return (await cache.match(request)) || (await caches.match(request)) || Response.error(); }
  })());
});
