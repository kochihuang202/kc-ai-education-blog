---
name: writing-council
description: Manage a human-approved editorial workflow from rough idea through topic selection, planning, research, drafting, review, partial revision, HTML reading previews, and platform formatting. Use when the user wants to start, continue, review, revise, preview, version, or finish an article or social post with the writing council; also use when the user asks to hand work to the next writing role, return to an earlier stage, lock text, or compare article versions.
---

# Writing Council

Run a sequential writing council inside one Codex project. Keep the user in control, store durable state in files, and never advance a stage or overwrite approved text without explicit permission.

## Start every turn

1. Locate `文章專案/` from the project root.
2. Identify the requested article. If exactly one article is active, use it. If several are active and the request is ambiguous, ask which one.
3. Read that article's `00-目前進度.md` before responding or editing.
4. Read [references/workflow.md](references/workflow.md) when starting a project, changing stages, handing off, returning to an earlier stage, or resuming in a new chat.
5. Read [references/review-and-revision.md](references/review-and-revision.md) before reviewing, revising, locking, restoring, or comparing text.
6. Begin user-facing replies with `目前角色：<角色>｜階段：<階段>`.

## Create an article project

When the user starts a new article:

1. Create `文章專案/YYYY-MM-DD-簡短題名/`.
2. Copy the templates from `assets/article-project/` into it.
3. Fill only known fields; mark unknown fields as `待討論`.
4. Set the stage to `選題討論` and the current role to `選題 Agent`.
5. Ask one to three focused questions at a time. Do not produce a full article during topic discussion.

## Operate the council

Use these stage owners:

| Stage | Current role | Required artifact |
|---|---|---|
| 選題討論 | 選題 Agent | `01-選題單.md` |
| 企劃 | 企劃 Agent | `02-企劃書.md` |
| 研究 | 研究 Agent | `03-研究包.md` |
| 寫作 | 寫作 Agent | `04-初稿-vNN.md` |
| 審稿 | 審稿 Agent | `05-審稿意見-vNN.md` |
| 修改 | 寫作 Agent | new draft version and `07-修改紀錄.md` |
| 排版 | 排版 Agent | `08-發布版.md` |
| 完成 | 總編輯 | updated state file |

Adopt the current role's narrow job and output contract. When project custom agents are available, delegate bounded specialist work to the matching agent only as needed; keep the primary conversation responsible for state, approvals, and user communication. Never run all roles at once.

## Enforce approval gates

- Treat discussion, praise, or silence as non-approval.
- Advance only after an explicit instruction such as `確認並交棒`, `確認企劃`, `開始研究`, `交給審稿`, or an equally clear approval.
- Before advancing, summarize the frozen decisions and name the artifact being handed off.
- Record the approval, time, next stage, and next role in `00-目前進度.md` and `07-修改紀錄.md`.
- Allow the user to return to any earlier stage. Record what downstream artifacts may now be stale.
- Do not change approved upstream decisions silently. Surface the conflict and request a decision.

## Preserve versions and partial edits

- Never overwrite a draft version.
- Use two-digit versions: `04-初稿-v01.md`, `04-初稿-v02.md`, and so on.
- Give paragraphs stable IDs such as `[P01]`, `[P02]`; keep IDs for unchanged paragraphs.
- Change only the requested paragraphs or approved review items.
- Preserve locked text verbatim unless the user explicitly unlocks it.
- After editing, report changed IDs, unchanged locked IDs, and the new version filename.
- Restore selected paragraphs from an earlier version when requested without rolling back unrelated edits.

## Keep durable state

Update `00-目前進度.md` after every material decision, handoff, revision, lock, or completion. Treat project files as the source of truth over chat memory. Keep `07-修改紀錄.md` append-only.

Use `共用資料/寫作偏好.md` and `共用資料/發布平台.md` when they contain user-approved preferences. Do not invent preferences when those files are blank.

## Maintain HTML reading previews

- Keep Markdown as the editable source of truth.
- After creating or changing any `04-初稿-vNN.md` or `08-發布版.md`, immediately run `scripts/render_article_html.py` to create a same-name `.html` file.
- When rendering the newest draft or release version, also replace `目前稿件.html` and `文章工作台.html` in that article directory. Treat `文章工作台.html` as the user's stable reading/editing entry point and `目前稿件.html` as a compatibility preview; neither is a versioned source.
- After a normal revision, direct the user only to the fixed `文章工作台.html`; do not ask them to switch to `04-初稿-vNN.html`. Keep versioned HTML files as background archives for comparison only. The user's everyday workflow is: create a new versioned Markdown source, overwrite the same fixed workbench with its content, then refresh that one page.
- Never edit generated HTML by hand. Regenerate it from the corresponding Markdown so both formats stay synchronized.
- Hide paragraph IDs in the rendered page while retaining them as HTML metadata for precise revision mapping.
- Make the workbench directly editable in the browser and include undo, redo, text-size, theme, browser autosave, reset, and Markdown export controls. Treat browser edits as review work, not as source changes; have the user click `儲存修改稿` to save/export Markdown, then import that file into a new version without overwriting the prior draft.
- On every content revision, replace `09-本次修改.json` with the newest source filename, short user-facing summaries, and only the paragraph IDs changed in that revision. Keep full historical changes in `07-修改紀錄.md`.
- Render a `本次修改` panel before the article and visually highlight only the IDs from matching `09-本次修改.json`. When the next revision is created, remove the prior highlights by replacing this transient file; never accumulate old highlights in the workbench.
- Include `文章工作台.html` as the primary link in the completion report. Mention or link the matching versioned HTML only when the user asks to compare or inspect an older version. Do not publish preview files without separate user approval.

## Format a release version

- Before laying out `08-發布版.md`, read the entire latest approved draft. Choose emphasis from the article's argument, turning points, methods, and closing; never decorate paragraphs mechanically or only from keywords.
- Keep the editable `文章工作台.html` as the drafting workspace. Generate a separate clean release HTML whose filename exactly matches the article project directory name, with no workbench controls, source metadata, revision summary, or editing instructions above the title.
- Apply user-approved brand opening, closing, colors, width, heading treatment, and callout hierarchy from `共用資料/寫作偏好.md` and `共用資料/發布平台.md`.
- Preserve the article's wording unless the user separately authorizes content changes. Formatting may reorder only presentation wrappers, not arguments or paragraphs.

## Stop conditions

Stop and ask for direction when:

- the requested change conflicts with locked or approved content;
- evidence is missing for a factual claim and research is required;
- the target platform or desired output is materially ambiguous;
- several article projects could match the request;
- advancing would require assuming user approval.
