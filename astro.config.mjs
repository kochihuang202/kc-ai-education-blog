import { defineConfig } from "astro/config";
import fs from "node:fs";
import path from "node:path";

export default defineConfig({
  site: "https://kc-ai-education-blog.pages.dev",
  vite: {
    plugins: [
      {
        name: "save-fb-status",
        configureServer(server) {
          server.middlewares.use((req, res, next) => {
            if (req.url === "/api/fb-status" && req.method === "GET") {
              try {
                const jsonPath = path.resolve("src/data/fb-status.json");
                let status = {};
                if (fs.existsSync(jsonPath)) {
                  status = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
                }
                res.writeHead(200, { "Content-Type": "application/json" });
                res.end(JSON.stringify(status));
              } catch (err) {
                res.writeHead(500, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ error: err.message }));
              }
            } else if (req.method === "POST" && req.url === "/api/toggle-fb") {
              let body = "";
              req.on("data", (chunk) => {
                body += chunk;
              });
              req.on("end", () => {
                try {
                  const { slug, checked } = JSON.parse(body);
                  const jsonPath = path.resolve("src/data/fb-status.json");

                  // Read existing status
                  let status = {};
                  if (fs.existsSync(jsonPath)) {
                    status = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
                  }

                  // Update status
                  status[slug] = checked;

                  // Write back to file
                  fs.writeFileSync(jsonPath, JSON.stringify(status, null, 2), "utf8");

                  res.writeHead(200, { "Content-Type": "application/json" });
                  res.end(JSON.stringify({ success: true }));
                } catch (err) {
                  res.writeHead(500, { "Content-Type": "application/json" });
                  res.end(JSON.stringify({ error: err.message }));
                }
              });
            } else {
              next();
            }
          });
        }
      }
    ]
  }
});
