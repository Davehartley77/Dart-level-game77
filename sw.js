/* Saved by the Bull: works offline once installed. VERSION is stamped at each publish. */
const VERSION = "20260913-185448";
const SHELL_CACHE = "shell-" + VERSION;
const ASSET_CACHE = "assets-v1";
const SHELL = ["./", "./index.html", "./manifest.json", "./images/icon.png", "./images/icon-192.png", "./images/icon-512.png", "./images/icon-maskable.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(SHELL_CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("shell-") && k !== SHELL_CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("message", e => { if (e.data === "skipWaiting") self.skipWaiting(); });

// Safari asks for audio in byte ranges; serve a 206 slice out of the cached file.
async function rangeResponse(request, full) {
  const range = request.headers.get("range");
  const buf = await full.arrayBuffer();
  const m = /bytes=(\d+)-(\d*)/.exec(range || "");
  if (!m) return new Response(buf, { status: 200, headers: full.headers });
  const start = +m[1], end = m[2] ? +m[2] : buf.byteLength - 1;
  const slice = buf.slice(start, end + 1);
  const headers = new Headers(full.headers);
  headers.set("Content-Range", `bytes ${start}-${end}/${buf.byteLength}`);
  headers.set("Content-Length", String(slice.byteLength));
  headers.set("Accept-Ranges", "bytes");
  return new Response(slice, { status: 206, headers });
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const isShell = url.origin === location.origin && (url.pathname.endsWith("/") || url.pathname.endsWith("/index.html"));
  if (isShell) {
    // the page itself: network first so updates arrive, cache when offline
    e.respondWith(fetch(req).then(r => { const copy = r.clone(); caches.open(SHELL_CACHE).then(c => c.put("./index.html", copy)); return r; })
      .catch(() => caches.match("./index.html")));
    return;
  }
  // lists (the voice manifest and names): network first so new phrases are picked up, cache when offline
  if (url.origin === location.origin && /\.(txt|json)$/.test(url.pathname)) {
    e.respondWith(fetch(req).then(r => { if (r.ok) { const copy = r.clone(); caches.open(ASSET_CACHE).then(c => c.put(new Request(url.href), copy)); } return r; })
      .catch(() => caches.match(new Request(url.href)).then(r => r || new Response("", { status: 504 }))));
    return;
  }
  // everything else (voice clips, icons, fonts): cache first, then network and keep it
  e.respondWith((async () => {
    const key = new Request(url.href, { method: "GET" });
    const hit = await caches.match(key);
    if (hit) return req.headers.has("range") ? rangeResponse(req, hit) : hit;
    try {
      const r = await fetch(key);
      if (r.ok && (url.origin === location.origin || /fonts\.(googleapis|gstatic)\.com/.test(url.host))) { const copy = r.clone(); caches.open(ASSET_CACHE).then(c => c.put(key, copy)); }
      return req.headers.has("range") ? rangeResponse(req, r) : r;
    } catch (err) {
      return new Response("", { status: 504 });
    }
  })());
});
