# 14 — Vertical Slice Roadmap

Development order. The guiding principle: **build the global skeleton and the four-power vertical
slice before deep regional content.** Night City content comes *after* the Neo-Soviet and European
systems, not before.

## Phase 1 — Global skeleton

Create the political map and minimal setup for the four core regions:

- North America
- Europe
- the Neo-Soviet sphere
- East Asia

The rest of the world receives simplified placeholder setup (generic states, tags, minimal history).

**Deliverables:** a loadable mod (`descriptor.mod`), country tags for all Tier One + Tier Two powers,
a working `map/` with provinces/states for the four core regions, boot to the 1 Jan 2069 bookmark
without errors.

**Exit criterion:** the mod loads to the main menu and starts a game on the bookmark with the four
regions populated.

## Phase 2 — Four-power vertical slice

Basic playable content for the four principal powers:

- NUSA
- Neo-Soviet Union
- one major European state **or** the EEC framework
- Japan **and** Arasaka

Each power gets:

- initial political setup (parties, leader, starting laws),
- a **20–30 focus prototype**,
- starting military structure (OOB, templates),
- an economic identity,
- **one unique mechanic** in prototype form,
- diplomatic interactions with the other three powers.

**Exit criterion:** each of the four is playable end-to-end through its focus prototype, its unique
mechanic functions, and the four can interact diplomatically.

## Phase 3 — Complete Neo-Soviet and European systems

Before heavily developing Night City:

- Neo-Soviet **union cohesion** (full crisis events, tiers),
- **SovOil–state** ladder (all five positions),
- **cybernetic / all economic** paths,
- European **integration** system (EEC),
- European **national sovereignty** paths,
- European **corporate influence**,
- **Eurasian energy diplomacy**.

**Exit criterion:** the Eurasian Settlement and European Crisis campaigns are fully playable.

## Phase 4 — North American regional conflict

Then build the North American theater in depth:

- NUSA reunification,
- Militech,
- Free States,
- Texas,
- Night City,
- Arasaka's return to North America.

**Exit criterion:** the Reunification of America campaign is fully playable and interlocks with the
Pacific and Atlantic axes.

## Cross-phase tracks (continuous)

- **Localisation:** every added key gets English localisation in the same change (`15`).
- **Diplomacy & tech systems** (`12`, `13`): stubbed in Phase 2, deepened alongside Phases 3–4.
- **Corporate sovereignty** (`06`): prototype in Phase 2 (Arasaka), generalized in Phases 3–4.

## Definition of done per power

A power is "launch-complete" when it has: full focus tree, its unique mechanic fully implemented,
starting history + OOB, economic identity via laws/spirits, localisation, and at least one scripted
crisis tied to a global conflict axis (`01` §4).
