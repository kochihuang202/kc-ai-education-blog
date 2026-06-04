import fs from 'fs';
import path from 'path';

// Define paths
const postsFilePath = path.resolve('src/data/posts.ts');
const publicDir = path.resolve('public');
const sitemapPath = path.join(publicDir, 'sitemap.xml');

// Read posts.ts content
const postsContent = fs.readFileSync(postsFilePath, 'utf8');

// Match slugs using regex
const slugRegex = /slug:\s*["']([^"']+)["']/g;
const slugs = [];
let match;
while ((match = slugRegex.exec(postsContent)) !== null) {
  // Deduplicate and filter out interface declarations (which won't match quotes anyway)
  if (!slugs.includes(match[1])) {
    slugs.push(match[1]);
  }
}

// Domain configuration
const siteUrl = 'https://kc-ai-education-blog.ji3cp31p4.workers.dev';

// Construct XML sitemap
let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${siteUrl}/</loc>
    <priority>1.0</priority>
    <changefreq>daily</changefreq>
  </url>
  <url>
    <loc>${siteUrl}/admin/</loc>
    <priority>0.1</priority>
    <changefreq>monthly</changefreq>
  </url>
`;

slugs.forEach(slug => {
  xml += `  <url>
    <loc>${siteUrl}/posts/${slug}/</loc>
    <priority>0.8</priority>
    <changefreq>weekly</changefreq>
  </url>\n`;
});

xml += `</urlset>`;

// Write output
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}
fs.writeFileSync(sitemapPath, xml, 'utf8');
console.log(`[SEO] Successfully generated sitemap.xml with ${slugs.length} posts.`);
