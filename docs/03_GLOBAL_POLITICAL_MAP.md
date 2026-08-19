# 03 — Global Political Map

> **Status: Draft (canon-aligned).** Authoritative registry of country tags, borders, and
> mod-original names. Once a tag or name is used in code it is **frozen** here. Territory and bloc
> membership follow the **"World of Cyberpunk 2077" canon map** (`02` source #2); keep a copy at
> `docs/reference/cyberpunk_world_map.png`.

## 0. Canon alignment note

This document was reconciled to the franchise canon map. Where the map and our earlier placeholder
defaults disagreed, **canon wins**. Reversals from the pre-map draft:

- **Baltics, Moldova, Caucasus, all Central Asia, Afghanistan, and Iran are INSIDE the union** as
  SSRs — not independent. (Reverses the earlier "Baltics independent" default.)
- **Poland and the Balkans are in the ECC**, not on the USSR frontier as independents.
- **"Pacifica Confederation" is dropped**; canon's **Western Corporate States (WCS)** takes the West
  Coast corporate zone instead.
- **Latin America is one bloc, the OAS**, not an independent Mexico + placeholder.
- The union's in-game name is the canon **Union of Sovereign Soviet Republics** (tag `USR`); "Neo-Soviet"
  is retained as mod shorthand (resolved, `02` D5).

## 1. Tag conventions

Three-letter uppercase (`15`). Mod-original entities get distinctive codes; surviving canon nations
repurpose recognizable codes; corporations get tags but start as non-landholding **operators** (§6).
Two internal clashes resolved: **AUT** = Austria, **AST** = Australia; **SOV** = SovOil (the union is
not `SOV`).

## 2. Core-region tag registry (Phase 1 detail)

The four core regions get full detail. **Landholding** = owns states at the 2069 start.

### 2.1 North America

| Tag | Entity | Tier | Landholding | Canon territory |
|-----|--------|------|-------------|-----------------|
| NUS | New United States of America | 1 | Yes | ~40 states: NE, Midwest, South, + Alaska, Hawaii, **Southern California (incl. Night City)** |
| WCS | Western Corporate States | 2 | Yes | Idaho, Oregon, Washington (corporate-run) |
| FSA | Free States | 2 | Yes | Montana, Wyoming, Colorado, New Mexico, Arizona, Nevada, Northern California |
| TEX | Republic of Texas | 2 | Yes | Texas |
| CAN | Federal Republic of Canada | 2 | Yes | Canada (strong, unified) |
| NCT | Night City (contested flashpoint) | 2 | No (release) | NUSA state at start; breakaway release tag → independence or Arasaka (§5.0, `07`) |
| MLT | Militech Corporation | 1 | Yes | Ten dispersed federal defense enclaves (`06`, `07`) |
| MTC | MetaCorp Technologies | 1 | Yes | Ten compact technology enclaves inside NUSA territory (`17`) |
| PTC | Petrochem | 2 | Operator | — |

### 2.2 Europe — ECC members, associates, and independents

**ECC members** (in the European Economic Community framework, `09`):

| Tag | Nation | Tag | Nation |
|-----|--------|-----|--------|
| GER | Germany | CZE | Czechoslovakia |
| FRA | France | AUT | Austria |
| ITA | Italy | HUN | Hungary |
| SPA | Spain | ROM | Romania |
| POR | Portugal | BUL | Bulgaria |
| BEN | Benelux | YUG | Yugoslavia |
| DEN | Denmark | GRE | Greece |
| IRE | Ireland | POL | Poland |

**ECC associates:** `NOR` Norway · `SWE` Sweden · `FIN` Finland · `ICL` Iceland · `GRN` Greenland.

**Independent Europe:** `ENG` United Kingdom (**outside** the ECC) · `TUR` Turkey · (`SWI` Switzerland
if needed).

**European corporate/institutional actors:** `EEC` European Economic Community (overlay, non-territorial,
Tier One in mechanical weight) · `ESA` European Space Agency (operator) · `EBM` Euro Business Machines
(operator) · `BIO` Biotechnica (operator).

### 2.3 USSR sphere

Union tag: **`USR`** — in-game name *Union of Sovereign Soviet Republics*; "Neo-Soviet" is mod shorthand
(resolved, `02` D5).

**Constituent SSRs owned by the union at start** (canon list): Russia (core) + Ukraine, Belarus,
Moldova, Lithuania, Latvia, Estonia, Georgia, Armenia, Azerbaijan, Kazakhstan, Uzbekistan, Kyrgyzstan,
Tajikistan, Turkmenistan, Afghanistan, Iran.

**Separately-tagged republics** (playable on Republican-Confederation / union breakup, `08` §3.5, §5):

| Tag | Republic (SSR grouping) |
|-----|--------------------------|
| UKR | SSR Ukraine |
| BLR | SSR Belarus (+ Moldova) |
| BAL | Baltic SSRs (Lithuania, Latvia, Estonia) |
| CAU | Transcaucasian SSRs (Georgia, Armenia, Azerbaijan) |
| KAZ | Central Asian SSRs (Kazakhstan-led: Uzbekistan, Kyrgyzstan, Tajikistan, Turkmenistan) |
| PER | SSR Iran |
| AFG | SSR Afghanistan |

Other sphere actors: `SOV` SovOil (operator, `06`/`08`) · `MON` Mongolia (**independent**, not in the
union).

### 2.4 East Asia & Pacific

| Tag | Entity | Tier | Landholding | Notes |
|-----|--------|------|-------------|-------|
| CHI | People's Republic of China | 1 | Yes | — |
| JAP | Japan | 1 | Yes | Distinct from Arasaka |
| ARA | Arasaka | 1 | Operator | Global security-tech corp (`10`) |
| KTO | Kang Tao | 2 | Operator | Chinese smart-weapons corp |
| KOR | Korea | 2 | Yes | Not shown on map; assumed independent — **verify** |
| ORB | Orbital Air | 3 | Operator | Global space-launch corp |

## 3. World-bloc registry (canon blocs, mostly Phase-1 placeholder)

The map defines several great blocs outside the four core regions. Recorded here with canon members;
individual member tags are assigned when Rest-of-World is developed (`14`). Blocs are modeled as
factions/frameworks with a leader tag.

| Bloc tag | Bloc | Canon members (leader **bold**) |
|----------|------|--------------------------------|
| OAS | Organization of American States | **Mexico**, Cuba, Haiti–Dominicana union, Jamaica, Bahamas, Fed. Rep. of Central America, Colombia, Venezuela, United Guyanas, Suriname, **Brazil**, Ecuador, Peru, Bolivia, Chile, Argentina, Uruguay, Paraguay |
| PAC | Pan-African Confederation | Egypt, Sudan, Ethiopia, Niger, Nigeria, CAR, Congo, Kenya, Uganda, Rwanda, Burundi, Tanzania, Angola, Zimbabwe, Zambia, Madagascar, N. Namibia, Cape's Republic, Orania, Lesotho, Eswatini, Natal |
| UNW | Union of North-West Africa (UNWA) | Benin, Togo, Ghana, Ivory Coast, Liberia, Sierra Leone, Burkina Faso, Guinea, Guinea-Bissau, Senegal, Gambia, Mali, Mauritania |
| ASN | ASEAN | Burma, Thailand, Laos, Vietnam, Cambodia, Malaysia, Brunei, Singapore, New Philippines |
| URB | United Republic of Bharat | **India**, Nepal, Bhutan, Bangladesh, Pakistan (+ contested Afghan/Iranian territory) |
| UAR | United Arab Republic | Syria, Jordan, Iraq, Kuwait, Kurdistan (+ contested Iranian territory) |

**Independent single states (RoW):** `IDN` Indonesia · `AST` Australia · `NZL` New Zealand · `TUR`
Turkey · `MON` Mongolia · North African monarchies `MOR` Morocco, `ALG` Algeria, `AZA` Azawad.

> **Contested overlaps (canon):** Afghanistan and Iran appear under the USSR *and* under URB/UAR —
> canon reflects divided/contested territory there. Model as split ownership or as war-goal flashpoints
> when those regions are developed.

## 4. Reserved tag block

Claimed mod-original / mod-redefined tags (add new ones here in the same change that introduces them):

```
Core:   NUS WCS FSA TEX CAN NCT MIL PTC
Europe: GER FRA ITA SPA POR BEN DEN IRE POL CZE AUT HUN ROM BUL YUG GRE
        NOR SWE FIN ICL GRN ENG TUR SWI  EEC ESA EBM BIO
USSR:   USR UKR BLR BAL CAU KAZ PER AFG SOV MON
E.Asia: CHI JAP ARA KTO KOR ORB
Blocs:  OAS PAC UNW ASN URB UAR  IDN AST NZL MOR ALG AZA
```

## 5. Map interpretation decisions

### 5.0 Resolved core decisions
1. **Union name/tag — RESOLVED (hybrid):** in-game name *Union of Sovereign Soviet Republics*, tag
   **`USR`**; "Neo-Soviet" retained as mod shorthand/adjective (`02` D5).
2. **Night City — RESOLVED (contested state):** Southern California (incl. Night City) is **NUSA
   territory at start**. Night City is a scripted **flashpoint** that can break away to independence or
   Arasaka via events; tag **`NCT`** is reserved for the released state (`02` D3, `07`).

### 5.1 North America — canon
- **NUS** holds its large canon core; reunification targets are **WCS, Free States, Texas** (Canada is
  a separate strong power, not a reunification target).
- **WCS** is the corporate-controlled Pacific NW — a natural early theatre for the corporate-sovereignty
  axis (`06`).

### 5.2 Europe — UNIFIED EEC COUNTRY (user decision)
- **EEC** is a **single unified country** (`EEC`, European blue) owning all of continental Europe —
  Germany, France, Italy, Iberia, Benelux, Poland, Czechoslovakia, Austria, Hungary, Romania, Bulgaria,
  Yugoslavia, Greece, Ireland, Denmark, Norway, Sweden, Finland, Iceland, and Switzerland.
- **Independent, outside the EEC:** the **United Kingdom** (`ENG`), **Turkey** (`TUR`), and the **USSR**
  (`USR`).
- Individual European nations are **not separately playable** at the 2069 start (supersedes the earlier
  separate-members plan; `02` D2). Their vanilla tags become defunct (own nothing).
- Generator rule: continent-1 states → `EEC`, except `ENG` (kept) and `SOV`/Baltics (→ `USR`).

### 5.3 USSR — canon
- The union owns the full canon SSR set (§2.3), including the Baltics, Caucasus, Central Asia,
  Afghanistan, and Iran. **Mongolia is independent.** Ukraine remains the most contested western
  republic for breakaway paths (`08`).

### 5.4 East Asia & Pacific — canon
- **CHI**, **JAP**, **MON** independent; **ASEAN** and **Indonesia** as separate SE-Asian actors;
  Korea assumed independent pending verification.

## 6. How corporations hold territory

Corporations tagged **operators** (`MIL SOV ARA KTO PTC BIO ORB EBM ESA`) start owning **no states**;
they act through the corporate-sovereignty ladder (`06`) and economic ownership-share (`05`), gaining
territory only via a sovereignty path. **Exception to watch:** the **WCS** is a *state* that is
corporate-run — a landholding country expressing corporate power directly, distinct from the operator
corps. The **EEC** is the non-territorial special case on the state side (`09`).

## 7. Remaining open questions (non-blocking for core Phase 1)

- Korea's status (independent vs. absorbed) — not on the map; verify against other canon.
- Arabian peninsula and North African micro-state breakdown — map detail unclear; resolve when Africa/
  Middle East are developed.
- Modeling of contested Afghanistan/Iran (split ownership vs. flashpoint) (§3).
- Whether OAS/PAC/ASEAN/URB/UAR are single mega-tags or factions of member tags at launch — default
  **faction of members**, finalized during RoW development.

_Once §5.0's two **[decide]** items are settled, this document is ready to drive
`common/country_tags/`, `history/countries/`, and `history/states/` for the core regions._
