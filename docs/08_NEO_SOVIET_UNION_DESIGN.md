# 08 — Neo-Soviet Union Design

> **Design law.** The Neo-Soviet Union must never be treated as a minor regional faction or merely
> as the political shell of SovOil. It is a major sovereign superpower with its own institutions,
> ideological possibilities, military strategy, economic systems, and global ambitions. Its focus
> tree is among the largest and most developed in the mod, comparable to the NUSA and to Europe.

This document sits immediately after the NUSA (`07`) and ahead of every regional faction, by design.

## 1. Identity

A reconsolidated Eurasian socialist federation that survived the collapse of the old order and
rebuilt itself as a first-tier superpower. It is defined by four tensions the player resolves through
play:

**Is the Neo-Soviet Union a sovereign socialist federation, an authoritarian security state, an
energy empire, or a state increasingly captured by SovOil and its industrial networks?**

Starting posture (1 Jan 2069): powerful, resource-rich, and technologically capable, but strained by
uneven **union cohesion**, an unresolved relationship with **SovOil**, and competition for Eurasian
influence against China, Europe, and NUSA-aligned interests.

## 2. The three core mechanics

The Neo-Soviet Union feels structurally different from the NUSA because of three interlocking systems.

### 2.1 Union cohesion

A national value (0–100) representing Moscow's ability to mobilize the whole federation. The union
contains multiple republics and regional interests; cohesion measures how well the center can
command them.

**High cohesion provides:** manpower access, industrial coordination bonuses, political stability,
stronger federal control (decisions unlocked), improved military logistics.

**Low cohesion causes:** republican resistance, separatist politics, industrial disobedience
(construction/production penalties), ethnic and regional crises (events), openings for foreign
interference.

Implementation notes:
- Model as a hidden-modifier-backed variable plus a visible national spirit that swaps tiers
  (e.g. `NSU_cohesion_high/med/low/crisis`).
- Cohesion is spent and earned: federal centralization decisions raise it at a legitimacy cost;
  republican concessions lower federal reach but reduce unrest.
- Foreign powers can attack cohesion via intelligence/cyber operations (`12`).

### 2.2 SovOil relationship

The government and SovOil are **connected but not identical**. A ladder tracks the balance of power
between the state and the corporation:

1. **State-controlled enterprise** — SovOil is a nationalized ministry-arm.
2. **Strategic partnership** — aligned but distinct interests.
3. **Corporate autonomy** — SovOil operates with substantial independence.
4. **Corporate–state parity** — dual power; SovOil co-governs energy regions.
5. **SovOil domination** — the corporation has captured the state (petro-state end).

Player levers: **nationalize** SovOil; **grant limited autonomy**; **merge** state planning with
corporate management; **allow capture**; **break up** SovOil into regional enterprises; **weaponize**
it as an instrument of foreign policy (energy leverage over Europe and neighbors).

The ladder position gates focuses, economic laws, and diplomatic tools, and interacts with cohesion
(SovOil dominance in energy republics can either buy stability or provoke separatism).

**Implemented vertical slice:** SovOil is playable as tag `SVO`, beginning under the Union through
the custom **Strategic State Corporation** relationship. Its variable
`sovoil_state_influence` uses six gameplay tiers from Administrative Agency to Energy State.
Unlike Arasaka, this system is built around extraction, refining, infrastructure, logistics,
exports, and wartime fuel mobilization rather than espionage or political subversion.

SovOil directly administers eleven existing-map energy and logistics districts: Tyumen (capital),
western Siberia, Yamal, the Caspian extraction zone, the Nenets Arctic offshore base, the Volga
petrochemical complex, the strategic pipeline headquarters, the major refinery district, Crimea's
Black Sea export complex, the Caucasus energy-security zone, and the Chukotka Arctic resource zone.
The Union retains cores and sovereignty claims on every district. No new state IDs are created.

### 2.3 Economic model (planning ↔ market coordination)

The Neo-Soviet economy has its own mechanic distinct from generic HOI4 economy laws. Selectable /
evolvable models:

- **Centralized state planning** — max coordination, low adaptability.
- **Cybernetic planning** — AI/network-assisted coordination (see the Cybernetic Socialism path).
- **State-directed market socialism** — hybrid flexibility.
- **Mixed strategic economy** — strategic sectors planned, rest liberalized.
- **Corporate energy capitalism** — SovOil-dominant, petro-driven.
- **Military mobilization economy** — total war footing.

Each model reshapes construction speed, resource output, consumer-goods pressure, and stability.

### 2.4 Eurasian influence

A competition layer (shared with `12_GLOBAL_DIPLOMACY_DESIGN.md`) over: Eastern Europe, Central Asia,
the Caucasus, the Arctic, the Middle East, Mongolia, and parts of East Asia.

Influence is expanded through: energy agreements, military guarantees, infrastructure construction,
intelligence operations, political support, debt arrangements, cyber operations, and direct
intervention. Contested primarily by China, Europe, and NUSA-aligned actors.

## 3. Political paths (focus-tree branches)

Six major branches. Each is a distinct answer to the central question; each unlocks characteristic
economic models, SovOil ladder positions, and cohesion strategies.

### 3.1 Renewal of the Union
Strengthen federal institutions · modernize the union treaty · balance the republics · rebuild public
services · limit SovOil · build a stable multinational federation.
→ Democratic-federal socialist end. High cohesion via legitimacy, not coercion.

### 3.2 Cybernetic Socialism
Revive automated economic coordination · establish national data networks · integrate AI-assisted
planning · expand public cybernetics · suppress corporate price manipulation · build a technologically
advanced planned economy.
→ Draws conceptual inspiration from Soviet cybernetic-planning history (OGAS-style) **without**
recreating the twentieth-century USSR. Ties into control of the new Net (`13`). Economic model:
Cybernetic planning.

### 3.3 Security-State Restoration
Empower the intelligence services · militarize the borderlands · centralize political authority ·
suppress separatism · expand strategic industries · rebuild a Eurasian military bloc.
→ Authoritarian security-state end. Cohesion enforced by coercion; strong military, brittle
legitimacy.

### 3.4 SovOil Ascendancy
Grant SovOil administrative authority · privatize regional infrastructure · create energy-security
zones · place corporate executives in government · build a transcontinental petro-state.
→ Corporate-capture end (SovOil domination on the ladder). Economic model: Corporate energy
capitalism.

### 3.5 Republican Confederation
Decentralize authority · expand republican sovereignty · loosen the union into a confederation ·
allow distinct regional economic systems · preserve common defense and foreign policy.
→ Low central cohesion by design, traded for resilience and legitimacy; unique diplomacy with
constituent republics as near-sovereign actors.

### 3.6 Revolutionary Internationalism
Oppose both Western corporations and domestic oligarchic structures · support socialist movements
abroad · organize anti-corporate governments · build an alternative international economic system ·
attempt a new global socialist bloc.
→ Aggressive ideological-export end; creates a rival faction/alliance system on the world stage.

## 4. Military identity

- Large conscript-capable manpower base **gated by cohesion**.
- Strong strategic/heavy industry and missile/space sectors; advanced military science.
- Doctrine emphasis: deep-battle / mass-mobilization plus a modern cyber-electronic warfare layer.
- A **Eurasian military bloc** (faction) is buildable via Security-State or Revolutionary paths.

## 5. Constituent republics

The union is a federation, not a unitary state. Per the canon map, it is **vast**: Russia (core) plus
SSRs for Ukraine, Belarus, Moldova, the **Baltics** (Lithuania/Latvia/Estonia), the Caucasus
(Georgia/Armenia/Azerbaijan), **all of Central Asia**, and **Afghanistan and Iran**. Represent major
republics as regional interests with cohesion stakes; the separately-tagged groupings (`UKR`, `BLR`,
`BAL`, `CAU`, `KAZ`, `PER`, `AFG` — see `03` §2.3) can become **playable Tier Two** actors under
Republican Confederation or on union breakup. **Ukraine** is the most contested western republic.
Exact republic list and borders are fixed in `03_GLOBAL_POLITICAL_MAP.md`.

> **Name / tag (resolved, hybrid — `02` D5, `03` §5.0):** the union's in-game full name is the canon
> *Union of Sovereign Soviet Republics*, tag **`USR`**. "Neo-Soviet" is retained as the mod's shorthand
> adjective (and this doc's working title): e.g. *Neo-Soviet factions*, *Neo-Soviet military*.

## 6. Starting situation (1 Jan 2069) — summary

- Cohesion: medium, trending fragile in energy and borderland republics.
- SovOil ladder: **Strategic partnership** (position 2), contestable in either direction.
- Economic model: **Mixed strategic economy**, evolvable.
- Open crises: separatist pressure in at least one republic; a Eurasian influence contest with China;
  an energy-leverage decision toward Europe.

## 7. Content scope for launch (vertical slice → full)

Vertical slice (Phase 2, see `14`): initial political setup, 20–30 focus prototype spanning the six
branch *entrances*, starting military structure, the cohesion + SovOil mechanics in prototype, and
diplomatic hooks to the NUSA, a European power, and Japan/Arasaka.

Full (Phase 3): complete all six branches, full cohesion crisis events, full SovOil ladder, all six
economic models, Eurasian influence system, and playable-republic breakup paths.

## 8. Open design questions

- Exact map treatment of the union's western border and which republics are separately playable.
- Whether Cybernetic Socialism and Renewal of the Union can partially combine.
- How SovOil's foreign energy leverage interacts mechanically with the European integration struggle
  (`09`) — likely a shared "energy dependency" modifier on European states.
