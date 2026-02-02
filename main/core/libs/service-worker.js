var CACHE_VERSION = "v1";
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open("my-pwa-cache-" + CACHE_VERSION).then((cache) => {
      return cache.addAll([
        "/",
      ]);
    })
  );
  self.skipWaiting();
});

self.addEventListener("fetch", (event) => {
  var url = event.request.url;
  // Скрипты темы и app.js всегда с сети, чтобы не отдавать старый кэш
  if (url.indexOf("app.js") !== -1 || (url.indexOf("/core/theme/") !== -1 && url.indexOf(".js") !== -1)) {
    event.respondWith(fetch(event.request));
    return;
  }
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
  