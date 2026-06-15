export const categories = [
  {
    id: "parents",
    label: "給父母",
    summary: "陪孩子長大，也讓自己少一點焦慮。",
    accent: "#A85B40"
  },
  {
    id: "educators",
    label: "給教育工作者",
    summary: "看見教室、學習與 AI 之間的新可能。",
    accent: "#2F6F73"
  },
  {
    id: "society",
    label: "給社會",
    summary: "把教育放回更大的公共討論裡。",
    accent: "#5E6F42"
  },
  {
    id: "core",
    label: "核心思想",
    summary: "整理 KC 對教育、判斷與人的底層觀點。",
    accent: "#5A5F91"
  },
  {
    id: "facing-bullying",
    label: "面對霸凌",
    summary: "從手段、分辨到放下，陪伴家長與孩子系統化面對同儕霸凌。",
    accent: "#B84A39"
  },
  {
    id: "iron-fist-education",
    label: "鐵拳教育",
    summary: "十篇文章拆解一個核心命題：拒絕拳頭，我們有沒有一套足夠強韌的制度？",
    accent: "#C0512F"
  },
] as const;

export type CategoryId = (typeof categories)[number]["id"];

export function getCategory(id: CategoryId) {
  return categories.find((category) => category.id === id);
}
