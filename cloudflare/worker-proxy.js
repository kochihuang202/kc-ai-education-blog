const RAW_BASE = "https://raw.githubusercontent.com/kochihuang202/kc-ai-education-blog/main/dist";

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
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

const DEPLOY_VERSION = "v_2026_07_31_10_35";

async function fetchAsset(pathname) {
  const assetPath = resolveAssetPath(pathname);
  const upstream = await fetch(`${RAW_BASE}${assetPath}?v=${DEPLOY_VERSION}`, {
    headers: { "User-Agent": "kc-ai-education-blog-worker" },
    cf: { cacheTtl: 300, cacheEverything: true }
  });

  if (!upstream.ok && assetPath !== "/404.html") {
    const notFound = await fetch(`${RAW_BASE}/404.html?v=${DEPLOY_VERSION}`, {
      headers: { "User-Agent": "kc-ai-education-blog-worker" },
      cf: { cacheTtl: 300, cacheEverything: true }
    });

    return new Response(notFound.body, {
      status: 404,
      headers: {
        "content-type": "text/html; charset=utf-8",
        "cache-control": "public, max-age=60",
        "x-worker-version": DEPLOY_VERSION
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
  headers.set("x-worker-version", DEPLOY_VERSION);

  return new Response(upstream.body, { status: upstream.status, headers });
}

const STATUS_JSON_URL = "https://raw.githubusercontent.com/kochihuang202/kc-ai-education-blog/main/src/data/fb-status.json";

async function getLiveStatus(env) {
  let statusStr = null;
  if (env.KC_BLOG_KV) {
    statusStr = await env.KC_BLOG_KV.get("fb_status");
  }
  
  if (statusStr) {
    return JSON.parse(statusStr);
  }
  
  // Fallback to GitHub raw status file
  try {
    const response = await fetch(STATUS_JSON_URL, {
      headers: { "User-Agent": "kc-ai-education-blog-worker" }
    });
    if (response.ok) {
      const status = await response.json();
      // Cache it in KV for next times
      if (env.KC_BLOG_KV) {
        await env.KC_BLOG_KV.put("fb_status", JSON.stringify(status));
      }
      return status;
    }
  } catch (err) {
    console.error("Failed to fetch fallback fb-status.json:", err);
  }
  
  return {};
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // API Endpoint: GET /api/fb-status
    if (url.pathname === "/api/fb-status" && request.method === "GET") {
      const status = await getLiveStatus(env);
      return new Response(JSON.stringify(status), {
        status: 200,
        headers: {
          "content-type": "application/json; charset=utf-8",
          "cache-control": "no-store"
        }
      });
    }

    // API Endpoint: POST /api/toggle-fb
    if (url.pathname === "/api/toggle-fb" && request.method === "POST") {
      // 1. Password Verification
      const authHeader = request.headers.get("Authorization");
      if (!env.ADMIN_PASSWORD || authHeader !== env.ADMIN_PASSWORD) {
        return new Response(JSON.stringify({ error: "Unauthorized" }), {
          status: 401,
          headers: {
            "content-type": "application/json; charset=utf-8",
            "cache-control": "no-store"
          }
        });
      }

      // 2. Parse Body & Update KV
      try {
        const { slug, checked } = await request.json();
        if (!slug) {
          return new Response(JSON.stringify({ error: "Missing slug" }), {
            status: 400,
            headers: { "content-type": "application/json" }
          });
        }

        const status = await getLiveStatus(env);
        status[slug] = checked;

        if (env.KC_BLOG_KV) {
          await env.KC_BLOG_KV.put("fb_status", JSON.stringify(status));
        }

        return new Response(JSON.stringify({ success: true }), {
          status: 200,
          headers: {
            "content-type": "application/json; charset=utf-8",
            "cache-control": "no-store"
          }
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), {
          status: 500,
          headers: { "content-type": "application/json" }
        });
      }
    }

    // Static Assets serving (GET/HEAD)
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method Not Allowed", { status: 405 });
    }

    return fetchAsset(url.pathname);
  }
};
