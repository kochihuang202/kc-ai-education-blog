const RAW_BASE = "https://raw.githubusercontent.com/kochihuang202/kc-ai-education-blog/main/dist";

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml; charset=utf-8",
  ".ico": "image/x-icon"
};

function ext(pathname) {
  const match = pathname.match(/\.[^.\/]+$/);
  return match ? match[0].toLowerCase() : ".html";
}

function resolveAssetPath(pathname) {
  if (pathname === "/") return "/index.html";
  if (pathname.endsWith("/")) return `${pathname}index.html`;
  return pathname;
}

async function fetchAsset(pathname) {
  const assetPath = resolveAssetPath(pathname);
  const upstream = await fetch(`${RAW_BASE}${assetPath}`, {
    headers: { "User-Agent": "kc-ai-education-blog-worker" },
    cf: { cacheTtl: 300, cacheEverything: true }
  });

  if (!upstream.ok && assetPath !== "/404.html") {
    const notFound = await fetch(`${RAW_BASE}/404.html`, {
      headers: { "User-Agent": "kc-ai-education-blog-worker" },
      cf: { cacheTtl: 300, cacheEverything: true }
    });

    return new Response(notFound.body, {
      status: 404,
      headers: {
        "content-type": "text/html; charset=utf-8",
        "cache-control": "public, max-age=60"
      }
    });
  }

  const headers = new Headers();
  headers.set("content-type", TYPES[ext(assetPath)] || "application/octet-stream");
  headers.set(
    "cache-control",
    assetPath.includes("/_astro/") || assetPath.includes("/images/")
      ? "public, max-age=31536000, immutable"
      : "public, max-age=60"
  );

  return new Response(upstream.body, { status: upstream.status, headers });
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method Not Allowed", { status: 405 });
    }

    return fetchAsset(url.pathname);
  }
};
