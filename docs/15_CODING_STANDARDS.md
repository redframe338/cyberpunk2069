# 15 — Coding Standards

Conventions for the HOI4 mod files under `mod/`. HOI4 uses Paradox's Clausewitz scripting (`.txt`
files in a bracketed key-value format) plus YAML localisation. Consistency here keeps a large mod
maintainable.

## 1. File and folder layout

Standard HOI4 structure under `mod/`:

```
mod/
  descriptor.mod
  common/
    countries/            country definitions + colors
    country_tags/         tag -> file mapping
    ideas/                national spirits, laws, designers
    national_focus/       focus trees
    ideologies/           ideology definitions
    scripted_effects/     reusable effects
    scripted_triggers/    reusable triggers
    on_actions/           hooks
    characters/           leaders, advisors, generals
    decisions/            decision categories + decisions
    dynamic_modifiers/    e.g. union cohesion tiers
  events/                 event files
  history/
    countries/            starting state per country
    states/               state ownership/buildings
    units/                orders of battle (OOB)
  map/                    provinces, definition, states (Phase 1)
  localisation/
    english/              *_l_english.yml
  gfx/                    flags, focus icons, GUI art
  interface/              GUI definitions
```

## 2. Naming conventions

- **Country tags:** three-letter uppercase. Reserve a documented block for mod tags to avoid vanilla
  collisions. Record every tag in `03_GLOBAL_POLITICAL_MAP.md`.
  - `NUS` = New United States of America
  - `NSU` = Neo-Soviet Union
  - `ARA` = Arasaka · `MIL` = Militech · `SOV` = SovOil · `KTO` = Kang Tao
  - `TEX` = Republic of Texas · `NCT` = Night City (finalize the full list in `03`).
- **Prefixes:** namespace all mod-authored ideas, focuses, events, and variables with a short prefix
  so they never collide with vanilla or each other:
  - Focuses: `NSU_focus_...`, `NUS_focus_...`
  - Ideas / spirits: `NSU_cohesion_high`, `NUS_reunification_pressure`
  - Events: `nsu.1`, `nsu.2` (namespace per country/system)
  - Variables: `nsu_cohesion`, `sovoil_ladder`
  - Scripted effects/triggers: `nsu_add_cohesion_effect`, `nsu_has_high_cohesion`
- **Localisation keys** match the object key exactly, plus vanilla suffix conventions
  (`_desc`, `_tt`, focus `_focus`).

## 3. Formatting

- **Indentation:** one tab per nesting level (Paradox convention). Be consistent within a file.
- **Braces:** opening brace on the same line as the key: `key = {`.
- **One statement per line** inside blocks where practical.
- **Comments:** `#` line comments. Comment the *intent* of non-obvious triggers/effects, not the
  syntax.
- **Encoding:** localisation `.yml` files **must** be UTF-8 **with BOM** (HOI4 requirement). Script
  `.txt` files: UTF-8.

## 4. Localisation rules

- Every player-facing key added in a change gets an English string in the **same** change. No orphan
  keys.
- Format: `key:0 "Text"` under a `l_english:` header.
- Keep tone consistent with `01` (grounded geopolitics). Avoid neon-noir pastiche in official
  strings.

## 5. Scripting hygiene

- **Reuse** via `scripted_effects` / `scripted_triggers` rather than copy-pasting logic (e.g. cohesion
  changes, SovOil ladder shifts).
- Prefer **dynamic modifiers** for tiered values (union cohesion) over many hard-coded spirits.
- Guard expensive `on_actions` and event triggers with cheap pre-checks first.
- Keep OOB and history edits data-only; put logic in effects/decisions.

## 6. Validation before commit

- Load the mod and check the **error.log** (`Documents/Paradox Interactive/Hearts of Iron IV/logs/`)
  — a clean load is the baseline bar.
- No missing-localisation warnings for keys you added.
- New focus trees render without overlap in the focus UI.

## 7. Version control

- The project root (`cyberpunk mod/`) is the repo. `mod/` and `docs/` are tracked.
- Commit messages: imperative, scoped, e.g. `NSU: add union cohesion dynamic modifier tiers`.
- Do not commit local Paradox launcher junk; add a `.gitignore` when the repo is initialized.

## 8. Symlink / test-load workflow

For live testing, the mod must be visible to the launcher. Either develop directly in
`Documents/Paradox Interactive/Hearts of Iron IV/mod/` or symlink `mod/` there. Record the chosen
workflow in `16_CLAUDE_CODE_INSTRUCTIONS.md`.
