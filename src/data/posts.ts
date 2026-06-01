import parentingRebelHtml from "../article-html/posts/parenting-rebel-switch.html?raw";
import lettingGoResponsibleHtml from "../article-html/posts/letting-go-responsible-attitude.html?raw";
import type { CategoryId } from "./categories";

export interface Post {
  title: string;
  slug: string;
  date: string;
  kicker: string;
  excerpt: string;
  categories: CategoryId[];
  coverImage?: string;
  coverAlt?: string;
  relatedPosts: string[];
  body: string;
}

export const posts = [
  {
    title: "原來放手，才是更負責的態度",
    slug: "letting-go-responsible-attitude",
    date: "2026-06-01",
    kicker: "KC 育兒手記",
    excerpt:
      "孩子需要大量低風險的小衝突練習，父母真正的負責不是立刻介入，而是留出孩子能練習的空間。",
    categories: ["parents", "core"],
    coverImage: "/images/ai-education-hero.png",
    coverAlt: "溫暖書桌上的筆記本、平板、教育書籍與 AI 學習網絡概念圖像",
    relatedPosts: ["parenting-rebel-switch"],
    body: lettingGoResponsibleHtml
  },
  {
    title: "輕鬆育兒的開關——家長先離經叛道",
    slug: "parenting-rebel-switch",
    date: "2026-05-29",
    kicker: "KC 育兒手記",
    excerpt:
      "輕鬆育兒不是少做，而是先看見問題的上游，敢在別人覺得奇怪的地方提前做決定。",
    categories: ["parents", "core"],
    coverImage: "/images/ai-education-hero.png",
    coverAlt: "溫暖書桌上的筆記本、平板、教育書籍與 AI 學習網絡概念圖像",
    relatedPosts: ["letting-go-responsible-attitude"],
    body: parentingRebelHtml
  }
] satisfies Post[];

export const postsBySlug = new Map(posts.map((post) => [post.slug, post]));

export function getPostsByCategory(categoryId: CategoryId) {
  return posts.filter((post) => post.categories.includes(categoryId));
}

export function formatPostDate(date: string) {
  return new Intl.DateTimeFormat("zh-TW", {
    year: "numeric",
    month: "long",
    day: "numeric"
  }).format(new Date(`${date}T00:00:00+08:00`));
}
