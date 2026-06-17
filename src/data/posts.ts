import vibeCodingRadarHtml from "../article-html/posts/vibe-coding-radar.html?raw";
import shouldKidsFollowTemplatesInExamsHtml from "../article-html/posts/should-kids-follow-templates-in-exams.html?raw";
import boundaryOfLettingGoHtml from "../article-html/posts/boundary-of-letting-go.html?raw";
import mxShellGrowingOwnMethodHtml from "../article-html/posts/mx-shell-growing-own-method.html?raw";
import notTechDifficultyButUncertaintyHtml from "../article-html/posts/not-tech-difficulty-but-uncertainty.html?raw";
import protectorParadoxHtml from "../article-html/posts/protector-paradox.html?raw";
import notAllHarmIsBullyingHtml from "../article-html/posts/not-all-harm-is-bullying.html?raw";
import schoolAndWorkplaceBullyingHtml from "../article-html/posts/school-and-workplace-bullying.html?raw";
import notEveryCorrectWordShouldBeSaidHtml from "../article-html/posts/not-every-correct-word-should-be-said.html?raw";
import pityingChildhoodVsAdulthoodHtml from "../article-html/posts/pitying-childhood-vs-adulthood.html?raw";
import talkingMoralsToKidsHtml from "../article-html/posts/talking-morals-to-kids.html?raw";
import kidsDontDisobeyOnPurposeHtml from "../article-html/posts/kids-dont-disobey-on-purpose.html?raw";
import iDontReplyHtml from "../article-html/posts/i-dont-reply.html?raw";
import goldenBowlOrHandcuffsHtml from "../article-html/posts/golden-bowl-or-handcuffs.html?raw";
import watchingEnglishCartoonsIsntLearningHtml from "../article-html/posts/watching-english-cartoons-isnt-learning.html?raw";
import noPunishmentIsHardHtml from "../article-html/posts/no-punishment-is-hard.html?raw";
import parentingRebelHtml from "../article-html/posts/parenting-rebel-switch.html?raw";
import lettingGoResponsibleHtml from "../article-html/posts/letting-go-responsible-attitude.html?raw";
import moneyCantBuyTrustHtml from "../article-html/posts/money-cant-buy-trust.html?raw";
import teachKidEmotionalRecognitionHtml from "../article-html/posts/teach-kid-emotional-recognition.html?raw";
import gratitudePracticeLettingGoHtml from "../article-html/posts/gratitude-practice-letting-go.html?raw";
import shouldKidsLearnCodingHtml from "../article-html/posts/should-kids-learn-coding.html?raw";
import howHighCanAnUnswayedPersonGoHtml from "../article-html/posts/how-high-can-an-unswayed-person-go.html?raw";
import ironFistEducationIntroHtml from "../article-html/posts/iron-fist-education-intro.html?raw";
import ironFistEducationP1Html from "../article-html/posts/iron-fist-education-p1.html?raw";
import ironFistEducationP2Html from "../article-html/posts/iron-fist-education-p2.html?raw";
import ironFistEducationP3Html from "../article-html/posts/iron-fist-education-p3.html?raw";
import ironFistEducationP4Html from "../article-html/posts/iron-fist-education-p4.html?raw";
import ironFistEducationP5Html from "../article-html/posts/iron-fist-education-p5.html?raw";
import ironFistEducationP6Html from "../article-html/posts/iron-fist-education-p6.html?raw";
import ironFistEducationP7Html from "../article-html/posts/iron-fist-education-p7.html?raw";
import ironFistEducationP8Html from "../article-html/posts/iron-fist-education-p8.html?raw";
import ironFistEducationP9Html from "../article-html/posts/iron-fist-education-p9.html?raw";
import ironFistEducationP10Html from "../article-html/posts/iron-fist-education-p10.html?raw";
import minimumEffortInfiniteFutureHtml from "../article-html/posts/minimum-effort-infinite-future.html?raw";
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

const vibeCodingRadarGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/vibe-coding-radar";

const vibeCodingRadarGraphics = Array.from({ length: 3 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${vibeCodingRadarGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `給家長和孩子的 AI 編程入門圖文解析 ${page}/3`
  };
});

const shouldKidsFollowTemplatesInExamsGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/should-kids-follow-templates-in-exams";

const shouldKidsFollowTemplatesInExamsGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${shouldKidsFollowTemplatesInExamsGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `應試教育裡，孩子一定要「照這個來」嗎？圖文解析 ${page}/10`
  };
});

const boundaryOfLettingGoGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/boundary-of-letting-go";

const boundaryOfLettingGoGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${boundaryOfLettingGoGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `放手的邊界——什麼時候該讓孩子自己「發現」，什麼時候不行圖文解析 ${page}/10`
  };
});

const mxShellGrowingOwnMethodGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/mx-shell-growing-own-method";

const mxShellGrowingOwnMethodGraphics = Array.from({ length: 8 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${mxShellGrowingOwnMethodGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `自學的終點不是學會別人的方法，而是長出自己的方法圖文解析 ${page}/8`
  };
});

const notTechDifficultyButUncertaintyGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/not-tech-difficulty-but-uncertainty";

const notTechDifficultyButUncertaintyGraphics = Array.from({ length: 13 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${notTechDifficultyButUncertaintyGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `不是技術難才值錢，是你敢碰的不確定性越深越值錢圖文解析 ${page}/13`
  };
});

const protectorParadoxGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/protector-paradox";

const protectorParadoxGraphics = Array.from({ length: 12 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${protectorParadoxGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `保護者悖論圖文解析 ${page}/12`
  };
});

const notAllHarmIsBullyingGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/not-all-harm-is-bullying";

const notAllHarmIsBullyingGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${notAllHarmIsBullyingGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `不是所有傷害都叫霸凌：孩子要先學會分辨這三件事圖文解析 ${page}/10`
  };
});

const schoolAndWorkplaceBullyingGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/school-and-workplace-bullying";

const schoolAndWorkplaceBullyingGraphics = Array.from({ length: 12 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${schoolAndWorkplaceBullyingGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `學校與職場的霸凌層出不窮：我們到底少教了孩子什麼圖文解析 ${page}/12`
  };
});

const noPunishmentIsHardGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/no-punishment-is-hard";

const noPunishmentIsHardGraphics = Array.from({ length: 18 }, (_, index) => {
  const page = index + 1;

  return {
    src: `${noPunishmentIsHardGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `不想處罰孩子，但真的很難圖文解析 ${page}/18`
  };
});

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

const notEveryCorrectWordShouldBeSaidGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/not-every-correct-word-should-be-said";

const notEveryCorrectWordShouldBeSaidGraphics = Array.from({ length: 8 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${notEveryCorrectWordShouldBeSaidGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `不是每句正確的話，都適合說出口圖文解析 ${page}/8`
  };
});

const pityingChildhoodVsAdulthoodGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/pitying-childhood-vs-adulthood";

const pityingChildhoodVsAdulthoodGraphics = Array.from({ length: 9 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${pityingChildhoodVsAdulthoodGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `你心疼現在的她，但你心疼長大後的她嗎？圖文解析 ${page}/9`
  };
});

const talkingMoralsToKidsGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/talking-morals-to-kids";

const talkingMoralsToKidsGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${talkingMoralsToKidsGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `你跟孩子講道德，她聽了嗎？圖文解析 ${page}/10`
  };
});

const kidsDontDisobeyOnPurposeGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/kids-dont-disobey-on-purpose";

const kidsDontDisobeyOnPurposeGraphics = Array.from({ length: 12 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${kidsDontDisobeyOnPurposeGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `孩子不是故意不聽話圖文解析 ${page}/12`
  };
});

const iDontReplyGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/i-dont-reply";

const iDontReplyGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${iDontReplyGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `「我不回」圖文解析 ${page}/10`
  };
});

const goldenBowlOrHandcuffsGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/golden-bowl-or-handcuffs";

const goldenBowlOrHandcuffsGraphics = Array.from({ length: 14 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${goldenBowlOrHandcuffsGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `是金飯碗，還是金手銬——為什麼最有保障的人，反而最不敢說話？圖文解析 ${page}/14`
  };
});

const watchingEnglishCartoonsIsntLearningGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/watching-english-cartoons-isnt-learning";

const watchingEnglishCartoonsIsntLearningGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${watchingEnglishCartoonsIsntLearningGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `看英文卡通不等於學英語圖文解析 ${page}/10`
  };
});

const howHighCanAnUnswayedPersonGoGraphicBase =
  "/images/posts/how-high-can-an-unswayed-person-go";

const howHighCanAnUnswayedPersonGoGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${howHighCanAnUnswayedPersonGoGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `不被左右的人，能走到什麼高度？圖文解析 ${page}/10`
  };
});

const ironFistEducationIntroGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-intro";

const ironFistEducationIntroGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationIntroGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》系列導讀：為什麼我們明明知道要管，卻管不動？圖文解析 ${page}/10`
  };
});

const ironFistEducationP1GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p1";

const ironFistEducationP1Graphics = Array.from({ length: 9 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP1GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第1篇：真正刺痛人的，不是拳頭，而是制度沒有牙齒圖文解析 ${page}/9`
  };
});

const ironFistEducationP2GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p2";

const ironFistEducationP2Graphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP2GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第2篇：孩子為什麼會守規矩？先看五個底層槓桿圖文解析 ${page}/10`
  };
});

const ironFistEducationP3GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p3";

const ironFistEducationP3Graphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP3GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第3篇：孩子是怎麼一步一步變得什麼都不在乎的？圖文解析 ${page}/10`
  };
});

const ironFistEducationP4GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p4";

const ironFistEducationP4Graphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP4GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第4篇：孩子不是只缺規矩，也缺練習圖文解析 ${page}/10`
  };
});

const ironFistEducationP5GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p5";

const ironFistEducationP5Graphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP5GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第5篇：日常秩序都不配合的孩子，到底是不能，還是不願意？圖文解析 ${page}/10`
  };
});

const ironFistEducationP6GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p6";

const ironFistEducationP6Graphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP6GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第6篇：為什麼老師越來越無力？圖文解析 ${page}/10`
  };
});

const ironFistEducationP7GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p7";

const ironFistEducationP7Graphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP7GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第7篇：灰色秩序消失後，正式制度補上了嗎？圖文解析 ${page}/10`
  };
});

const ironFistEducationP8GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p8";

const ironFistEducationP8Graphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP8GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第8篇：不是木匠，也不能放任圖文解析 ${page}/10`
  };
});

const ironFistEducationP9GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p9";

const ironFistEducationP9Graphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP9GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第9篇：好制度不是要求老師更強，而是給老師後勤圖文解析 ${page}/10`
  };
});

const ironFistEducationP10GraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/iron-fist-education-p10";

const ironFistEducationP10Graphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${ironFistEducationP10GraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `《鐵拳教育》第10篇：不要等孩子什麼都不怕，才開始問怎麼管圖文解析 ${page}/10`
  };
});

const minimumEffortInfiniteFutureGraphicBase =
  "https://pub-0eb2a942d02b407091b3e88d3d56fd63.r2.dev/posts/minimum-effort-infinite-future";

const minimumEffortInfiniteFutureGraphics = Array.from({ length: 10 }, (_, index) => {
  const page = index + 1;
  return {
    src: `${minimumEffortInfiniteFutureGraphicBase}/graphic-${String(page).padStart(2, "0")}.webp`,
    alt: `花最小努力，換孩子無限未來圖文解析 ${page}/10`
  };
});

export const posts = [
  {
    title: "花最小努力，換孩子無限未來",
    slug: "minimum-effort-infinite-future",
    date: "2026-06-17",
    kicker: "KC 育兒手記",
    excerpt:
      "為什麼最簡單的三件事，大多數父母反而做不到 前幾天跟一個年輕同事聊天，聊到我對孩子的期待。 我說，我希望花最小的努力——包含時間和金錢——但又希望孩子有無限的未來。 他愣了一下，然後說了一句很厲害的話：那就要有方法。 對，方法。方法對了，就會相對輕鬆...",
    categories: ["parents", "core"],
    coverImage: minimumEffortInfiniteFutureGraphics[0].src,
    coverAlt: minimumEffortInfiniteFutureGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: minimumEffortInfiniteFutureGraphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p1", "iron-fist-education-p2"],
    body: minimumEffortInfiniteFutureHtml
  },

  {
    title: "《鐵拳教育》系列導讀：為什麼我們明明知道要管，卻管不動？",
    slug: "iron-fist-education-intro",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 系列導讀",
    excerpt:
      "你知道該管。 孩子賴在地上不起來，你知道不能就這樣算了。孩子在餐廳尖叫，你知道該設界線。孩子對你翻白眼，你知道不能假裝沒看見。 你都知道。 但管了沒用。提醒三次，安靜兩分鐘，又來了。設了界線，守不住。跟老師溝通，老師說他也沒辦法。你回家想了一整晚，第...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationIntroGraphics[0].src,
    coverAlt: ironFistEducationIntroGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationIntroGraphics
    },
    relatedPosts: ["iron-fist-education-p1", "iron-fist-education-p10", "iron-fist-education-p2", "minimum-effort-infinite-future"],
    body: ironFistEducationIntroHtml
  },
  {
    title: "《鐵拳教育》第1篇：真正刺痛人的，不是拳頭，而是制度沒有牙齒",
    slug: "iron-fist-education-p1",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第1篇",
    excerpt:
      "2026年6月5日，Netflix上線了一部韓劇。IMDb 8.6，上線一週橫掃25個國家和地區熱播榜首。 劇名叫《鐵拳教育》。 劇情設定很粗暴：韓國全面實施《禁止體罰法》之後，法規意外成了霸凌者的保護傘——未滿14歲的施暴者免予刑責，教師正常管教遭...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP1Graphics[0].src,
    coverAlt: ironFistEducationP1Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP1Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p2", "minimum-effort-infinite-future"],
    body: ironFistEducationP1Html
  },
  {
    title: "《鐵拳教育》第2篇：孩子為什麼會守規矩？先看五個底層槓桿",
    slug: "iron-fist-education-p2",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第2篇",
    excerpt:
      "上一篇我們留了一個問題：人為什麼會守規矩？ 你可能會說：因為善良。因為有教養。因為知道什麼是對、什麼是錯。 這些答案都對，但都不完整。 說白了，善良只是守規矩的原因之一。一個孩子守規矩，通常不是因為單一的力量，而是因為好幾種力量同時在拉住他。 有些力...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP2Graphics[0].src,
    coverAlt: ironFistEducationP2Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP2Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p1", "iron-fist-education-p3", "minimum-effort-infinite-future"],
    body: ironFistEducationP2Html
  },
  {
    title: "《鐵拳教育》第3篇：孩子是怎麼一步一步變得什麼都不在乎的？",
    slug: "iron-fist-education-p3",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第3篇",
    excerpt:
      "上一篇我們說了：五個底層槓桿撐住一個孩子守規矩的結構。也說了：槓桿撐不住沒有固定順序，但會有結構性的連鎖反應。 那這個「連鎖反應」到底長什麼樣？一個孩子從「還算守規矩」走到「什麼都不在乎」，中間發生了什麼？ 這篇我們來拆這個過程。 不過先說清楚：不是...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP3Graphics[0].src,
    coverAlt: ironFistEducationP3Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP3Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p2", "iron-fist-education-p4"],
    body: ironFistEducationP3Html
  },
  {
    title: "《鐵拳教育》第4篇：孩子不是只缺規矩，也缺練習",
    slug: "iron-fist-education-p4",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第4篇",
    excerpt:
      "上一篇我們拆了三條崩塌路徑。其中第三條最讓人心酸：有些孩子不是槓桿斷了，是從來就沒有撐起來過。規矩這件事，從來就沒有真正長出來過。 但為什麼？為什麼現在的孩子，比以前更容易走到這一步？ 不是孩子變了。是練習場消失了。",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP4Graphics[0].src,
    coverAlt: ironFistEducationP4Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP4Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p3", "iron-fist-education-p5"],
    body: ironFistEducationP4Html
  },
  {
    title: "《鐵拳教育》第5篇：日常秩序都不配合的孩子，到底是不能，還是不願意？",
    slug: "iron-fist-education-p5",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第5篇",
    excerpt:
      "上一篇我們說了三條崩塌路徑，也說了四種不配合類型。 但四型裡有一條分界線，比其他所有區分都重要： 這個孩子是不能，還是不願？ 你可能覺得這不難分。不配合就是不配合，誰分不清？ 先別急——做一個判斷。 一個國小三年級的男生，上課不聽，作業不寫，老師講了...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP5Graphics[0].src,
    coverAlt: ironFistEducationP5Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP5Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p4", "iron-fist-education-p6"],
    body: ironFistEducationP5Html
  },
  {
    title: "《鐵拳教育》第6篇：為什麼老師越來越無力？",
    slug: "iron-fist-education-p6",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第6篇",
    excerpt:
      "上一篇我們留了一個問號：一個班三十個孩子，有一個持續不配合的，老師的精力就被吃掉大半。如果同時有兩三個——老師能補嗎？補不了的部分，誰來扛？ 答案很殘酷：沒有人扛。 你可能會說：制度都在啊——學校有輔導室、有學務處、有校安通報系統，老師為什麼不管？ ...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP6Graphics[0].src,
    coverAlt: ironFistEducationP6Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP6Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p5", "iron-fist-education-p7"],
    body: ironFistEducationP6Html
  },
  {
    title: "《鐵拳教育》第7篇：灰色秩序消失後，正式制度補上了嗎？",
    slug: "iron-fist-education-p7",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第7篇",
    excerpt:
      "上一篇我們留了一個問號：灰色秩序消失了，正式制度補上了嗎？ 你可能會說：以前的校園不是更亂嗎？有體罰、有教官、有黑幫滲透，怎麼可能比現在好？ 這句話暗含一個判斷：以前更差，現在至少有制度。 但如果你看完這篇，你可能會改口：以前確實亂，但以前有制衡；現...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP7Graphics[0].src,
    coverAlt: ironFistEducationP7Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP7Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p6", "iron-fist-education-p8"],
    body: ironFistEducationP7Html
  },
  {
    title: "《鐵拳教育》第8篇：不是木匠，也不能放任",
    slug: "iron-fist-education-p8",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第8篇",
    excerpt:
      "建制度之前，有一個更根本的問題要先回答：教育的界線到底在哪裡？ 你可能會說：蒙特梭利不是說了嗎？給孩子自由。高普尼克不是也說了嗎？做園丁，不做木匠。所以結論就是界線要軟、後果要少、讓孩子自己長。 這句話，兩個人都被誤讀了。 蒙特梭利有牙齒。高普尼克有...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP8Graphics[0].src,
    coverAlt: ironFistEducationP8Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP8Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p7", "iron-fist-education-p9"],
    body: ironFistEducationP8Html
  },
  {
    title: "《鐵拳教育》第9篇：好制度不是要求老師更強，而是給老師後勤",
    slug: "iron-fist-education-p9",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第9篇",
    excerpt:
      "我們已經拆解了孩子不守規矩的底層邏輯，也看見了灰色秩序消失後的真空。現在，必須面對最核心的問題：教育不能回到拳頭，但如果我們拒絕拳頭，拿什麼來補位？ 當舊的威權工具被拿掉，我們補上了很多「正向管教」的理念，卻沒有給老師「後勤」。 這正是現在教育現場最...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP9Graphics[0].src,
    coverAlt: ironFistEducationP9Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP9Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p10", "iron-fist-education-p8"],
    body: ironFistEducationP9Html
  },
  {
    title: "《鐵拳教育》第10篇：不要等孩子什麼都不怕，才開始問怎麼管",
    slug: "iron-fist-education-p10",
    date: "2026-06-15",
    kicker: "鐵拳教育 · 第10篇",
    excerpt:
      "愛要穩，界線要硬。 只有愛沒有界線是縱容，只有界線沒有愛是壓迫。 這句話，你可能聽過無數遍。但聽過和做到之間，隔著一條巨大的溝。 《家庭教育藍皮書2024》調查了上百萬個家庭，數據很刺眼：80%的家長對孩子的學業表現感到焦慮，60%時刻擔心孩子出意外...",
    categories: ["iron-fist-education", "parents", "core"],
    coverImage: ironFistEducationP10Graphics[0].src,
    coverAlt: ironFistEducationP10Graphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: ironFistEducationP10Graphics
    },
    relatedPosts: ["iron-fist-education-intro", "iron-fist-education-p9"],
    body: ironFistEducationP10Html
  },

  {
    title: "給家長和孩子的 AI 編程入門",
    slug: "vibe-coding-radar",
    date: "2026-06-10",
    kicker: "家長推薦",
    excerpt:
      "給家長和孩子的 AI 編程入門：為什麼你需要一個「先照著做」的導航站？",
    categories: ["parents", "core"],
    coverImage: vibeCodingRadarGraphics[0].src,
    coverAlt: vibeCodingRadarGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: vibeCodingRadarGraphics
    },
    relatedPosts: ["should-kids-learn-coding", "should-kids-follow-templates-in-exams", "mx-shell-growing-own-method"],
    body: vibeCodingRadarHtml
  },
  {
    title: "應試教育裡，孩子一定要「照這個來」嗎？",
    slug: "should-kids-follow-templates-in-exams",
    date: "2026-06-10",
    kicker: "KC 育兒思考",
    excerpt:
      "應試教育本身就是一張孩子不能不照著來的參考圖。但在應試教育裡，孩子一定要「照這個來」嗎？我們該如何透過「指導淡出」與建立「圖式（Schema）」，讓孩子既能過關，又不會永遠只會照著套模板？",
    categories: ["parents", "core"],
    coverImage: shouldKidsFollowTemplatesInExamsGraphics[0].src,
    coverAlt: shouldKidsFollowTemplatesInExamsGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: shouldKidsFollowTemplatesInExamsGraphics
    },
    relatedPosts: ["vibe-coding-radar", "boundary-of-letting-go", "not-tech-difficulty-but-uncertainty", "kids-dont-disobey-on-purpose"],
    body: shouldKidsFollowTemplatesInExamsHtml
  },
  {
    title: "放手的邊界——什麼時候該讓孩子自己「發現」，什麼時候不行",
    slug: "boundary-of-letting-go",
    date: "2026-06-09",
    kicker: "KC 育兒手記",
    excerpt:
      "放手的邊界——什麼時候該讓孩子自己「發現」，什麼時候不行？從認知科學與圖式（Schema）理論，看透放手的核心判斷依據與指導淡出的藝術。",
    categories: ["parents", "core"],
    coverImage: boundaryOfLettingGoGraphics[0].src,
    coverAlt: boundaryOfLettingGoGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: boundaryOfLettingGoGraphics
    },
    relatedPosts: ["should-kids-follow-templates-in-exams", "mx-shell-growing-own-method", "letting-go-responsible-attitude", "pitying-childhood-vs-adulthood"],
    body: boundaryOfLettingGoHtml
  },
  {
    title: "自學的終點不是學會別人的方法，而是長出自己的方法",
    slug: "mx-shell-growing-own-method",
    date: "2026-06-09",
    kicker: "自學思考",
    excerpt:
      "自學的終點不是學會別人的方法，而是長出自己的方法。從自學AI做出好萊塢驚嘆短片的Mx-Shell身上，看見「照這個來」與「朝這個去」的學習姿態。",
    categories: ["parents", "core"],
    coverImage: mxShellGrowingOwnMethodGraphics[0].src,
    coverAlt: mxShellGrowingOwnMethodGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: mxShellGrowingOwnMethodGraphics
    },
    relatedPosts: ["vibe-coding-radar", "boundary-of-letting-go", "not-tech-difficulty-but-uncertainty", "should-kids-learn-coding", "watching-english-cartoons-isnt-learning"],
    body: mxShellGrowingOwnMethodHtml
  },
  {
    title: "不是技術難才值錢，是你敢碰的不確定性越深越值錢",
    slug: "not-tech-difficulty-but-uncertainty",
    date: "2026-06-08",
    kicker: "職場觀察 · 育兒思考",
    excerpt:
      "從一個工程師的認知翻轉，到一個父親的育兒醒悟：不是技術難才值錢，是你敢碰的不確定性越深越值錢。",
    categories: ["parents", "core"],
    coverImage: notTechDifficultyButUncertaintyGraphics[0].src,
    coverAlt: notTechDifficultyButUncertaintyGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: notTechDifficultyButUncertaintyGraphics
    },
    relatedPosts: ["should-kids-follow-templates-in-exams", "mx-shell-growing-own-method", "protector-paradox", "letting-go-responsible-attitude", "should-kids-learn-coding"],
    body: notTechDifficultyButUncertaintyHtml
  },
  {
    title: "保護者悖論",
    slug: "protector-paradox",
    date: "2026-06-08",
    kicker: "KC 育兒手記",
    excerpt:
      "過度的保護，往往會演變成無形的控制與限制。當我們試圖消除孩子生命中所有的風險，我們是否也同步消除了她長出力量與適應未來的可能性？",
    categories: ["parents", "core"],
    coverImage: protectorParadoxGraphics[0].src,
    coverAlt: protectorParadoxGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: protectorParadoxGraphics
    },
    relatedPosts: ["not-tech-difficulty-but-uncertainty", "letting-go-responsible-attitude", "pitying-childhood-vs-adulthood", "not-all-harm-is-bullying"],
    body: protectorParadoxHtml
  },
  {
    title: "學校與職場的霸凌層出不窮：我們到底少教了孩子什麼？",
    slug: "school-and-workplace-bullying",
    date: "2026-06-04",
    kicker: "面對霸凌三部曲 · 第一部",
    excerpt:
      "霸凌層出不窮的背後，往往是集體沉默與旁觀的共犯機制。我們需要教給孩子的，不是簡單的對與錯，而是看見體制與人性的盲點，並長出採取行動的智慧與勇氣。",
    categories: ["society", "core", "facing-bullying"],
    coverImage: schoolAndWorkplaceBullyingGraphics[0].src,
    coverAlt: schoolAndWorkplaceBullyingGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: schoolAndWorkplaceBullyingGraphics
    },
    relatedPosts: ["not-all-harm-is-bullying", "money-cant-buy-trust", "golden-bowl-or-handcuffs", "parenting-rebel-switch", "how-high-can-an-unswayed-person-go"],
    body: schoolAndWorkplaceBullyingHtml
  },
  {
    title: "不是所有傷害都叫霸凌：孩子要先學會分辨這三件事",
    slug: "not-all-harm-is-bullying",
    date: "2026-06-04",
    kicker: "面對霸凌三部曲 · 第二部",
    excerpt:
      "在談論霸凌前，我們應先協助孩子釐清「同儕衝突」、「惡意挑釁」與「霸凌」的關鍵差異。唯有正確識別傷害的本質，才能採取最適當的自我保護策略。",
    categories: ["parents", "core", "facing-bullying"],
    coverImage: notAllHarmIsBullyingGraphics[0].src,
    coverAlt: notAllHarmIsBullyingGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: notAllHarmIsBullyingGraphics
    },
    relatedPosts: ["protector-paradox", "school-and-workplace-bullying", "kids-dont-disobey-on-purpose", "teach-kid-emotional-recognition", "how-high-can-an-unswayed-person-go"],
    body: notAllHarmIsBullyingHtml
  },
  {
    title: "不被左右的人，能走到什麼高度？",
    slug: "how-high-can-an-unswayed-person-go",
    date: "2026-06-04",
    kicker: "面對霸凌三部曲 · 第三部",
    excerpt:
      "真正自由的人，不是沒人能冒犯他，而是不把每個笨人的行為都放進心裡。放下不是忍受，是不讓不值得的事佔用你的心。",
    categories: ["parents", "core", "facing-bullying"],
    coverImage: howHighCanAnUnswayedPersonGoGraphics[0].src,
    coverAlt: howHighCanAnUnswayedPersonGoGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: howHighCanAnUnswayedPersonGoGraphics
    },
    relatedPosts: ["not-all-harm-is-bullying", "school-and-workplace-bullying"],
    body: howHighCanAnUnswayedPersonGoHtml
  },
  {
    title: "不是每句正確的話，都適合說出口",
    slug: "not-every-correct-word-should-be-said",
    date: "2026-06-04",
    kicker: "KC 育兒手記",
    excerpt:
      "有時候，我們說的都是對的，但聽的人卻關上了耳朵。在關係裡，比起「正確」，看見對方的處境與情緒，才是溝通真正開始的起點。",
    categories: ["parents", "core"],
    coverImage: notEveryCorrectWordShouldBeSaidGraphics[0].src,
    coverAlt: notEveryCorrectWordShouldBeSaidGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: notEveryCorrectWordShouldBeSaidGraphics
    },
    relatedPosts: ["teach-kid-emotional-recognition", "gratitude-practice-letting-go", "no-punishment-is-hard", "talking-morals-to-kids"],
    body: notEveryCorrectWordShouldBeSaidHtml
  },
  {
    title: "你心疼現在的她，但你心疼長大後的她嗎？",
    slug: "pitying-childhood-vs-adulthood",
    date: "2026-06-04",
    kicker: "KC 育兒手記",
    excerpt:
      "當孩子遇到挫折、流淚時，我們本能地想要伸出援手。但現在的心疼，是否會剝奪她未來長出韌性與能力的機會？放手，需要更大的勇氣。",
    categories: ["parents", "core"],
    coverImage: pityingChildhoodVsAdulthoodGraphics[0].src,
    coverAlt: pityingChildhoodVsAdulthoodGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: pityingChildhoodVsAdulthoodGraphics
    },
    relatedPosts: ["boundary-of-letting-go", "protector-paradox", "letting-go-responsible-attitude", "gratitude-practice-letting-go", "no-punishment-is-hard", "watching-english-cartoons-isnt-learning"],
    body: pityingChildhoodVsAdulthoodHtml
  },
  {
    title: "你跟孩子講道德，她聽了嗎？",
    slug: "talking-morals-to-kids",
    date: "2026-06-04",
    kicker: "KC 育兒手記",
    excerpt:
      "用抽象的道德教條管教孩子，往往只會換來反彈或敷衍。唯有連結孩子的真實體驗與需求，道德才會從規範轉化為內在的生命力。",
    categories: ["parents", "core"],
    coverImage: talkingMoralsToKidsGraphics[0].src,
    coverAlt: talkingMoralsToKidsGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: talkingMoralsToKidsGraphics
    },
    relatedPosts: ["no-punishment-is-hard", "teach-kid-emotional-recognition", "not-every-correct-word-should-be-said", "kids-dont-disobey-on-purpose"],
    body: talkingMoralsToKidsHtml
  },
  {
    title: "孩子不是故意不聽話",
    slug: "kids-dont-disobey-on-purpose",
    date: "2026-06-04",
    kicker: "KC 育兒手記",
    excerpt:
      "當孩子頻頻出現脫序行為，她可能不是在反抗，而是大腦與身體的發展尚未跟上要求。理解她的局限，建立外在秩序，才是引導的良方。",
    categories: ["parents", "core"],
    coverImage: kidsDontDisobeyOnPurposeGraphics[0].src,
    coverAlt: kidsDontDisobeyOnPurposeGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: kidsDontDisobeyOnPurposeGraphics
    },
    relatedPosts: ["should-kids-follow-templates-in-exams", "not-all-harm-is-bullying", "no-punishment-is-hard", "teach-kid-emotional-recognition", "talking-morals-to-kids"],
    body: kidsDontDisobeyOnPurposeHtml
  },
  {
    title: "「我不回」",
    slug: "i-dont-reply",
    date: "2026-06-04",
    kicker: "KC 育兒手記",
    excerpt:
      "面對負面質疑或情緒化的反饋，選擇「不回覆」並非怯懦，而是保留自身心力、守護內部秩序的智慧境界。",
    categories: ["parents", "core"],
    coverImage: iDontReplyGraphics[0].src,
    coverAlt: iDontReplyGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: iDontReplyGraphics
    },
    relatedPosts: ["not-every-correct-word-should-be-said", "gratitude-practice-letting-go", "parenting-rebel-switch"],
    body: iDontReplyHtml
  },
  {
    title: "是金飯碗，還是金手銬——為什麼最有保障的人，反而最不敢說話？",
    slug: "golden-bowl-or-handcuffs",
    date: "2026-06-04",
    kicker: "KC 育兒思考",
    excerpt:
      "體制帶來的終身保障，有時反而化為沉重的束縛，讓最有能力推動改變的人選擇沉默。我們該如何打破沉默，為教育現場帶入活水？",
    categories: ["society", "core"],
    coverImage: goldenBowlOrHandcuffsGraphics[0].src,
    coverAlt: goldenBowlOrHandcuffsGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: goldenBowlOrHandcuffsGraphics
    },
    relatedPosts: ["school-and-workplace-bullying", "money-cant-buy-trust", "should-kids-learn-coding", "parenting-rebel-switch"],
    body: goldenBowlOrHandcuffsHtml
  },
  {
    title: "看英文卡通不等於學英語",
    slug: "watching-english-cartoons-isnt-learning",
    date: "2026-06-04",
    kicker: "KC 育兒手記",
    excerpt:
      "僅靠被動的螢幕吸收，無法讓孩子長出真正的語言表達能力。英語學習需要雙向互動與有意義的對話情境連結。",
    categories: ["parents", "core"],
    coverImage: watchingEnglishCartoonsIsntLearningGraphics[0].src,
    coverAlt: watchingEnglishCartoonsIsntLearningGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: watchingEnglishCartoonsIsntLearningGraphics
    },
    relatedPosts: ["mx-shell-growing-own-method", "should-kids-learn-coding", "pitying-childhood-vs-adulthood", "talking-morals-to-kids"],
    body: watchingEnglishCartoonsIsntLearningHtml
  },

  {
    title: "不想處罰孩子，但真的很難",
    slug: "no-punishment-is-hard",
    date: "2026-06-03",
    kicker: "KC 育兒手記",
    excerpt:
      "連續兩天被告狀，大人的壓力很真實。蒙特梭利指出服從是意志發展的最後階段，而許多行為問題其實是心理畸變的身體表現。找出孩子卡在哪一步，方案才會準。",
    categories: ["parents", "core"],
    coverImage: noPunishmentIsHardGraphics[0].src,
    coverAlt: noPunishmentIsHardGraphics[0].alt,
    gallery: {
      label: "<圖文解析>",
      images: noPunishmentIsHardGraphics
    },
    relatedPosts: ["should-kids-learn-coding", "teach-kid-emotional-recognition", "gratitude-practice-letting-go", "not-every-correct-word-should-be-said", "pitying-childhood-vs-adulthood", "talking-morals-to-kids", "kids-dont-disobey-on-purpose"],
    body: noPunishmentIsHardHtml
  },
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
    relatedPosts: ["vibe-coding-radar", "mx-shell-growing-own-method", "not-tech-difficulty-but-uncertainty", "no-punishment-is-hard", "teach-kid-emotional-recognition", "gratitude-practice-letting-go", "money-cant-buy-trust", "golden-bowl-or-handcuffs", "watching-english-cartoons-isnt-learning"],
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
    relatedPosts: ["no-punishment-is-hard", "teach-kid-emotional-recognition", "letting-go-responsible-attitude", "parenting-rebel-switch", "should-kids-learn-coding", "not-every-correct-word-should-be-said", "pitying-childhood-vs-adulthood", "i-dont-reply"],
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
    relatedPosts: ["not-all-harm-is-bullying", "no-punishment-is-hard", "letting-go-responsible-attitude", "parenting-rebel-switch", "gratitude-practice-letting-go", "should-kids-learn-coding", "not-every-correct-word-should-be-said", "talking-morals-to-kids", "kids-dont-disobey-on-purpose"],
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
    relatedPosts: ["school-and-workplace-bullying", "letting-go-responsible-attitude", "parenting-rebel-switch", "teach-kid-emotional-recognition", "gratitude-practice-letting-go", "should-kids-learn-coding", "golden-bowl-or-handcuffs"],
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
    relatedPosts: ["boundary-of-letting-go", "not-tech-difficulty-but-uncertainty", "protector-paradox", "parenting-rebel-switch", "money-cant-buy-trust", "teach-kid-emotional-recognition", "gratitude-practice-letting-go", "should-kids-learn-coding", "pitying-childhood-vs-adulthood"],
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
    relatedPosts: ["school-and-workplace-bullying", "letting-go-responsible-attitude", "money-cant-buy-trust", "teach-kid-emotional-recognition", "gratitude-practice-letting-go", "should-kids-learn-coding", "i-dont-reply", "golden-bowl-or-handcuffs"],
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