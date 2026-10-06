/* Offline cache for presentation mode (scope: present/).
 *
 * Pages, posters and videos are cache-first: a lecture never waits for the
 * network once a deck has been opened. Manifests and HTML are network-first,
 * so a republished deck replaces the cached one when online. Range requests
 * (Safari's video playback) are answered from the cached full response with
 * 206 Partial Content.
 */
"use strict";

const CACHE = "plasma-present-v1";
const fresh = (url) => /\.(json|html|webmanifest|js|css)$/.test(url.pathname) || url.pathname.endsWith("/");

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));

async function ranged(request, response) {
  const header = request.headers.get("range");
  const m = /^bytes=(\d*)-(\d*)$/.exec(header || "");
  if (!m) return response;
  const blob = await response.blob();
  const size = blob.size;
  let start = m[1] === "" ? size - Number(m[2]) : Number(m[1]);
  let end = m[1] !== "" && m[2] !== "" ? Number(m[2]) : size - 1;
  start = Math.max(0, start);
  end = Math.min(size - 1, end);
  if (start > end) {
    return new Response(null, { status: 416, headers: { "Content-Range": `bytes */${size}` } });
  }
  return new Response(blob.slice(start, end + 1), {
    status: 206,
    statusText: "Partial Content",
    headers: {
      "Content-Type": response.headers.get("Content-Type") || "video/mp4",
      "Content-Range": `bytes ${start}-${end}/${size}`,
      "Content-Length": String(end - start + 1),
      "Accept-Ranges": "bytes",
    },
  });
}

async function cacheFirst(request) {
  const cache = await caches.open(CACHE);
  const key = request.url;
  let hit = await cache.match(key);
  if (!hit) {
    // Fetch the whole file (no Range header), keep it, then answer the range.
    const res = await fetch(key, { credentials: "same-origin" });
    if (!res.ok) return res;
    await cache.put(key, res.clone());
    hit = res;
  }
  return request.headers.has("range") ? ranged(request, hit) : hit;
}

async function networkFirst(request) {
  const cache = await caches.open(CACHE);
  try {
    const res = await fetch(request);
    if (res.ok) await cache.put(request.url.split("#")[0], res.clone());
    return res;
  } catch {
    const hit = await cache.match(request.url.split("#")[0], { ignoreSearch: true });
    if (hit) return hit;
    throw new Error("offline and not cached: " + request.url);
  }
}

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  if (!url.pathname.startsWith(new URL("./", self.registration.scope).pathname)) return;
  e.respondWith(fresh(url) ? networkFirst(e.request) : cacheFirst(e.request));
});

// The player posts the URLs of the open deck; store any that are missing.
self.addEventListener("message", (e) => {
  if (e.data?.type !== "cache") return;
  e.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    let failed = 0;
    await Promise.all(e.data.urls.map(async (u) => {
      try {
        const url = new URL(u);
        if (!fresh(url) && await cache.match(u)) return;
        const res = await fetch(u, { cache: "no-cache" });
        if (res.ok) await cache.put(u.split("#")[0], res);
        else failed += 1;
      } catch { failed += 1; }
    }));
    e.source?.postMessage({ type: "cached", failed });
  })());
});
