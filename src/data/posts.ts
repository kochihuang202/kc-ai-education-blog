import parentingRebelHtml from "../article-html/posts/parenting-rebel-switch.html?raw";
import lettingGoResponsibleHtml from "../article-html/posts/letting-go-responsible-attitude.html?raw";
import moneyCantBuyTrustHtml from "../article-html/posts/money-cant-buy-trust.html?raw";
import teachKidEmotionalRecognitionHtml from "../article-html/posts/teach-kid-emotional-recognition.html?raw";
import gratitudePracticeLettingGoHtml from "../article-html/posts/gratitude-practice-letting-go.html?raw";
import shouldKidsLearnCodingHtml from "../article-html/posts/should-kids-learn-coding.html?raw";
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
  gallery?: {
    label: string;
    images: Array<{
      src: string;
      alt: string;
    }>;
  };
  relatedPosts: string[];
  body: string;
}

const lettingGoGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/letting-go-responsible-attitude";

const lettingGoGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;

  return {
    src: `${lettingGoGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `原來放手，才是更負責的態度圖文解析 ${page}/10`
  };
});

const moneyCantBuyTrustGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/money-cant-buy-trust";

const moneyCantBuyTrustGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;

  return {
    src: `${moneyCantBuyTrustGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `發錢救不了信不過圖文解析 ${page}/10`
  };
});

const teachKidEmotionalRecognitionGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/teach-kid-emotional-recognition";

const teachKidEmotionalRecognitionGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;

  return {
    src: `${teachKidEmotionalRecognitionGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `你以為在教孩子控制情緒，但她其實早已失控圖文解析 ${page}/10`
  };
});

const gratitudePracticeLettingGoGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/gratitude-practice-letting-go";

const gratitudePracticeLettingGoGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;

  return {
    src: `${gratitudePracticeLettingGoGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `感謝是放下執念的日常練習圖文解析 ${page}/10`
  };
});

const shouldKidsLearnCodingGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/should-kids-learn-coding";

const shouldKidsLearnCodingGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;

  return {
    src: `${shouldKidsLearnCodingGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `AI能寫程式了，你的孩子該學什麼？圖文解析 ${page}/10`
  };
});

export const posts = [
  {
    title: "AI能寫程式了，你的孩子該學什麼？",
    slug: "should-kids-learn-coding",
    date: "2026-06-02",
    kicker: "KC 育兒思考",
    excerpt:
      "當AI能三秒鐘寫出程式，孩子學程式的意義早已不是背語法，而是訓練兩層能力：說清楚需求的表達力，與看透系統的判斷力。判斷力，才是真正不被替代的護城河。",
    categories: ["parents", "core"],
    coverImage: shouldKidsLearnCodingGraphics[0].src,
    coverAlt: shouldKidsLearnCodingGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: shouldKidsLearnCodingGraphics
    },
    relatedPosts: ["teach-kid-emotional-recognition", "gratitude-practice-letting-go", "money-cant-buy-trust"],
    body: shouldKidsLearnCodingHtml
  },
  {
    title: "感謝是放下執念的日常練習",
    slug: "gratitude-practice-letting-go",
    date: "2026-06-02",
    kicker: "KC 育兒手記",
    excerpt:
      "孩子犯錯處理完後，我額外做了一個延伸：感謝她願意坦白。感謝不是縱容，而是看見信任的瞬間，更是幫孩子和父母自己一步步往上走、放下執念的日常修煉。",
    categories: ["parents", "core"],
    coverImage: gratitudePracticeLettingGoGraphics[0].src,
    coverAlt: gratitudePracticeLettingGoGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: gratitudePracticeLettingGoGraphics
    },
    relatedPosts: ["teach-kid-emotional-recognition", "letting-go-responsible-attitude", "parenting-rebel-switch", "should-kids-learn-coding"],
    body: gratitudePracticeLettingGoHtml
  },
  {
    title: "你以為在教孩子控制情緒，但她其實早已失控",
    slug: "teach-kid-emotional-recognition",
    date: "2026-06-02",
    kicker: "KC 育兒手記",
    excerpt:
      "女兒在學校動手打了人，理智線快斷的當下我沒有進行常規處罰，而是做了一個「禁水果甜食」的對照實驗，並意識到在教導情緒控制（剎車）前，應先協助孩子預防失控（降坡度）。",
    categories: ["parents", "core"],
    coverImage: teachKidEmotionalRecognitionGraphics[0].src,
    coverAlt: teachKidEmotionalRecognitionGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: teachKidEmotionalRecognitionGraphics
    },
    relatedPosts: ["letting-go-responsible-attitude", "parenting-rebel-switch", "gratitude-practice-letting-go", "should-kids-learn-coding"],
    body: teachKidEmotionalRecognitionHtml
  },
  {
    title: "發錢救不了信不過",
    slug: "money-cant-buy-trust",
    date: "2026-06-01",
    kicker: "KC 育兒思考",
    excerpt:
      "2000億津貼買不到安心，如果教育現場的信任崩塌、老師留不住，再多現金也只是往漏水的水桶裡倒水。",
    categories: ["society", "core"],
    coverImage: moneyCantBuyTrustGraphics[0].src,
    coverAlt: moneyCantBuyTrustGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: moneyCantBuyTrustGraphics
    },
    relatedPosts: ["letting-go-responsible-attitude", "parenting-rebel-switch", "teach-kid-emotional-recognition", "gratitude-practice-letting-go", "should-kids-learn-coding"],
    body: moneyCantBuyTrustHtml
  },
  {
    title: "原來放手，才是更負責的態度",
    slug: "letting-go-responsible-attitude",
    date: "2026-06-01",
    kicker: "KC 育兒手記",
    excerpt:
      "孩子需要大量低風險的小衝突練習，父母真正的負責不是立刻介入，而是留出孩子能練習的空間。",
    categories: ["parents", "core"],
    coverImage: lettingGoGraphics[0].src,
    coverAlt: lettingGoGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: lettingGoGraphics
    },
    relatedPosts: ["parenting-rebel-switch", "money-cant-buy-trust", "teach-kid-emotional-recognition", "gratitude-practice-letting-go", "should-kids-learn-coding"],
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
    coverAlt: "溫慢書桌上的筆記本、平板、教育書籍與 AI 學習網絡概念圖像",
    relatedPosts: ["letting-go-responsible-attitude", "money-cant-buy-trust", "teach-kid-emotional-recognition", "gratitude-practice-letting-go", "should-kids-learn-coding"],
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
