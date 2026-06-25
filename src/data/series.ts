export interface SeriesItem {
  slug: string;
  title: string;
  label?: string;
}

export interface SeriesConfig {
  id: string;
  name: string;
  accent: string;
  steps: SeriesItem[];
}

export const seriesList: SeriesConfig[] = [
  {
    id: "facing-bullying",
    name: "面對霸凌三部曲",
    accent: "#B84A39",
    steps: [
      { slug: "school-and-workplace-bullying", title: "第一部：有手段 ｜ 學校與職場的霸凌層出不窮：我們到底少教了孩子什麼？", label: "1" },
      { slug: "not-all-harm-is-bullying", title: "第二部：會分辨 ｜ 不是所有傷害都叫霸凌：孩子要先學會分辨這三件事", label: "2" },
      { slug: "how-high-can-an-unswayed-person-go", title: "第三部：放得下 ｜ 不被左右的人，能走到什麼高度？", label: "3" }
    ]
  },
  {
    id: "iron-fist-education",
    name: "鐵拳教育（共 11 篇）",
    accent: "#C0512F",
    steps: [
      { slug: "iron-fist-education-intro", title: "導讀 ｜ 為什麼我們明明知道要管，卻管不動？", label: "導" },
      { slug: "iron-fist-education-p1", title: "第1篇 ｜ 真正刺痛人的，不是拳頭，而是制度沒有牙齒", label: "1" },
      { slug: "iron-fist-education-p2", title: "第2篇 ｜ 孩子為什麼會守規矩？先看五個底層槓桿", label: "2" },
      { slug: "iron-fist-education-p3", title: "第3篇 ｜ 孩子是怎麼一步一步變得什麼都不在乎的？", label: "3" },
      { slug: "iron-fist-education-p4", title: "第4篇 ｜ 孩子不是只缺規矩，也缺練習", label: "4" },
      { slug: "iron-fist-education-p5", title: "第5篇 ｜ 日常秩序都不配合的孩子，到底是不能，還是不願意？", label: "5" },
      { slug: "iron-fist-education-p6", title: "第6篇 ｜ 為什麼老師越來越無力？", label: "6" },
      { slug: "iron-fist-education-p7", title: "第7篇 ｜ 灰色秩序消失後，正式制度補上了嗎？", label: "7" },
      { slug: "iron-fist-education-p8", title: "第8篇 ｜ 不是木匠，也不能放任", label: "8" },
      { slug: "iron-fist-education-p9", title: "第9篇 ｜ 好制度不是要求老師更強，而是給老師後勤", label: "9" },
      { slug: "iron-fist-education-p10", title: "第10篇 ｜ 不要等孩子什麼都不怕，才開始問怎麼管", label: "10" }
    ]
  },
  {
    id: "memory-science",
    name: "記憶學專題系列",
    accent: "#4A6FA5",
    steps: [
      { slug: "is-memory-unimportant-in-ai-era", title: "第一篇 ｜ AI時代，記憶力不重要？說這話的人不是蠢就是壞", label: "1" },
      { slug: "memory-science-is-misunderstood", title: "第二篇 ｜ 記憶學被冤枉了", label: "2" },
      { slug: "how-to-train-memory-since-childhood", title: "第三篇 ｜ 記憶學實操前傳——從小怎麼練", label: "3" },
      { slug: "memory-science-is-misunderstood-p4", title: "第四篇 ｜ 教孩子認字，大人先掌握學習方法", label: "4" },
      { slug: "memory-science-is-misunderstood-p5", title: "第五篇 ｜ 象形字圖卡，認字的第一步", label: "5" },
      { slug: "memory-science-is-misunderstood-p6", title: "第六篇 ｜ 象形字圖卡（二）：人物姿態與動物飛禽", label: "6" },
      { slug: "memory-science-is-misunderstood-p7", title: "第七篇 ｜ 象形字圖卡（三）：植物草木與器物建築", label: "7" },
      { slug: "memory-science-is-misunderstood-p8", title: "第八篇 ｜ 拆字實戰：二十幾個字，帶你走一遍", label: "8" },
      { slug: "memory-science-is-misunderstood-p9", title: "第九篇 ｜ 拆字進階：核心觀點與更多範例", label: "9" }
    ]
  },
  {
    id: "memory-science-app",
    name: "記憶學_應用系列",
    accent: "#3E8E7E",
    steps: [
      { slug: "how-would-you-remember-fruits-of-four-seasons", title: "第一篇 ｜ 四季的水果，你會怎麼記", label: "1" },
      { slug: "how-to-actually-use-memory-science", title: "第二篇 ｜ 記憶學到底怎麼用——一個同事的四次試錯", label: "2" }
    ]
  }
];
