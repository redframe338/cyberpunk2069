# 02 — Canon and Source Hierarchy

How to resolve lore questions and conflicts. When sources disagree, higher tiers win.

## Source hierarchy (highest authority first)

1. **This mod's design bible (`01`) and design documents.** Where the mod deliberately diverges from
   franchise canon (e.g. elevating the Neo-Soviet Union to a first-tier superpower), the mod's
   documents govern. Divergences must be recorded in the "Deliberate divergences" section below.
2. **The "World of Cyberpunk 2077" geopolitical map** — the franchise reference for the late-century
   global bloc structure (NUSA, WCS, Free States, USSR, ECC, OAS, PAC, UNWA, ASEAN, URB, UAR, and the
   member-state lists of each). This is the **authoritative source for who owns what territory** and
   the names of the great blocs. A copy should be kept at `docs/reference/cyberpunk_world_map.png`.
   Territory and bloc membership from this map **override** any placeholder map assumptions made
   before it was available (see `03` §0).
3. **Cyberpunk RED tabletop material** (2045 setting) — the closest canonical treatment of the
   post-corporate-war, post-DataKrash world and the primary reference for the 2069 era's institutions,
   corporations, and the internal politics of the blocs above.
4. **Cyberpunk 2020 tabletop material** — foundational worldbuilding, corporations, nations, and the
   Fourth Corporate War.
5. **Cyberpunk 2077 / Phantom Liberty** — used for texture, technology, and the NUSA/Arasaka/Militech
   state of play, but **not** as a source of protagonist storylines. V and 2077's personal
   narratives are out of scope.
6. **Real-world 2020s geopolitics, geography, and economics** — used to fill gaps plausibly where
   franchise canon is silent (internal detail of blocs the map names but does not break down).

## Handling the 2069 date

The franchise does not richly document 2069 specifically. Treat 2069 as an **extrapolation** forward
from the RED/2077 baseline:

- Corporate power has partially reconsolidated after the Fourth Corporate War.
- The NUSA reunification project is underway but incomplete.
- The new Net is being rebuilt under contested governance.
- The **Neo-Soviet Union** is a mod-specific extrapolation: a reconsolidated Eurasian socialist
  federation. This is a **deliberate divergence** (see below) and is developed in `08`.

## Deliberate divergences from franchise canon

Record every intentional departure here so contributors do not "correct" them.

| # | Divergence | Rationale |
|---|-----------|-----------|
| D1 | Elevating the union to a **first-tier sovereign superpower** with full internal institutions and factions, not merely SovOil's sphere. (Consistent with canon: the map shows a vast USSR.) | Core to the mod's four-power global structure (`01`, `08`). |
| D2 | Modeling the **EEC as a single unified country** (`EEC`) absorbing continental Europe (incl. Scandinavia and the Balkans), with the **UK, Turkey, and USSR independent**. (Supersedes the earlier "separate playable members" plan — user decision.) | Matches the canon map's single blue European bloc; individual members are not separately playable at the 2069 start (`03` §5.2, `09`). |
| D3 | **Night City is a NUSA state at start** (canon), but a scripted **contested flashpoint** that can break away to independence or Arasaka via events. Tag `NCT` is reserved for the released state; NUSA owns the territory at start. | Honors the canon map while keeping NC a playable flashpoint (`01`, `03` §5.0, `07`). |
| D4 | The **2069 start date** and its parallel crises are a mod extrapolation forward from the map's 2077 baseline. | Chosen for maximum simultaneous geopolitical tension (`01`, `14`). |
| D5 | **Resolved — hybrid naming.** The union's in-game full name is the canon **"Union of Sovereign Soviet Republics"** (tag `USR`); the mod keeps **"Neo-Soviet"** as shorthand/adjective (e.g. Neo-Soviet factions) and as doc `08`'s working title. | Canon-faithful name + retained mod branding. |

## Naming conventions for canon vs. mod-original

- Prefer canonical names where they exist (Arasaka, Militech, SovOil, Kang Tao, NUSA, Night City).
- Mod-original entities (e.g. specific Neo-Soviet republics or European coalition governments) get
  names recorded in `03_GLOBAL_POLITICAL_MAP.md` and, once used, are frozen — do not rename in code
  without updating the map document.

## When in doubt

Escalate to the design bible's central questions. If a proposed detail does not serve one of the five
conflict axes or the six power centers, it is probably out of scope for the launch version.
