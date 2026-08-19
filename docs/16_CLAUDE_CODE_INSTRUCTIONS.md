# 16 — Claude Code Instructions

Operating instructions for AI-assisted development on this project. This is the contract for how work
proceeds so that a large, multi-session build stays coherent.

## 1. Read order at the start of any session

1. `01_GLOBAL_DESIGN_BIBLE.md` — the non-negotiable rules.
2. `04_MAJOR_POWER_MATRIX.md` — what makes each power distinct.
3. `14_VERTICAL_SLICE_ROADMAP.md` — what phase we are in and what is in scope.
4. The design doc for whatever power/system the task touches.

## 2. Non-negotiable rules (never violate)

- **V does not appear.** No 2077-protagonist content.
- **Night City is a flashpoint, not the center.** Do not build the campaign around it.
- **The Neo-Soviet Union is a first-tier superpower**, never a minor faction or a SovOil shell.
- **Six independent power centers.** No single North American storyline defines the global campaign.
- Respect the **source hierarchy** in `02`; record deliberate divergences there.

## 3. Working method

- **Stay in phase.** Do not build Phase 4 (Night City / North American depth) content before Phases
  1–3 are complete, unless the user explicitly redirects.
- **One power/system per task** where possible; keep changes reviewable.
- **Localise as you go** — every new player-facing key gets English text in the same change (`15`).
- **Namespace everything** with the prefixes in `15` to avoid collisions.
- **Update the docs** when you make a design decision in code: new tags → `03`; new divergence → `02`;
  new mechanic detail → the relevant design doc.

## 4. Definition of done for a coding task

- Files placed in the correct `mod/` subfolder per `15`.
- Localisation present for all added keys.
- Namespacing and formatting conform to `15`.
- If the mod is test-loadable in this environment, it loads with a clean `error.log`; if not, say so
  explicitly rather than claiming verification.
- Docs updated for any design decision made.

## 5. Verification honesty

State plainly what was and was not verified. HOI4 cannot necessarily be launched in this environment;
if a change was **not** loaded and tested in-game, say so. Never report untested script as
"working."

## 6. Test-load workflow (finalized)

HOI4 **is** installed on this machine:

- **Game install:** `E:\SteamLibrary\steamapps\common\Hearts of Iron IV` (`hoi4.exe`).
- **Game version:** `1.19.2` ("Operation Postern"). `descriptor.mod` targets `supported_version="1.19.*"`.
- **Paradox user dir:** `C:\Users\victo\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV`
  (note: **OneDrive-redirected** Documents).

**Chosen workflow — pointer `.mod` file (no copy, no symlink).** A loose descriptor lives at
`…\Paradox Interactive\Hearts of Iron IV\mod\cyberpunk_2069.mod` containing a
`path="C:/Users/victo/cyberpunk mod/mod"` line pointing at this repo's `mod/` folder. The launcher
reads mod content directly from the repo, so edits here are picked up on the next game launch — no
sync step.

- To test: launch HOI4 → in the launcher, enable **"The Fractured World, 2069"** → Play.
- If the launcher does not show it, the v2 launcher may need the mod registered in
  `launcher-v2.sqlite`; re-open the launcher first (it scans `mod\*.mod` on startup).
- After a test, read the error log at
  `…\Paradox Interactive\Hearts of Iron IV\logs\error.log` — a clean log is the baseline bar (`15`).

**Reference mod present:** *The New World Order* is installed in the user's mod folder — a useful
geopolitical-conversion reference for map/tag/focus patterns.

## 7. When unsure

Escalate to the design bible's central questions and the five conflict axes. If a proposed detail
serves none of the six power centers or five axes, it is probably out of scope for launch — flag it
rather than building it.

## 8. Task tracking

Track multi-step work visibly (todo list). Prefer finishing a vertical, playable increment (a working
focus prototype + its mechanic + localisation) over broad half-built breadth.
