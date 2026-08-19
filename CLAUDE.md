# The Fractured World, 2069 — HOI4 Total Conversion Mod

## What this is
A Hearts of Iron IV total-conversion mod set in the Cyberpunk 2077 universe, start date 1 January 2069.

## Repository layout
```
cyberpunk mod/
  mod/              <- the actual HOI4 mod (game files, descriptor.mod)
  assets/           <- source images, reference art
  docs/             <- design documents
  tools/            <- build scripts
  disabled_content/ <- shelved content for later
```

## CRITICAL CONSTRAINTS — never violate these

### Files that must NEVER be overwritten
- `mod/gfx/interface/cyberpunk_main_menu.dds` — custom main menu background, NO BACKUP
- `mod/gfx/interface/cyberpunk_country_setup.dds` — custom country setup background, NO BACKUP
- If either file needs changes, make a backup first and ask the user before touching them.

### Descriptor safety
- **NEVER** add `replace_path="common/national_focus"` to `descriptor.mod` — causes ACCESS_VIOLATION crash

### State ID limit
- HOI4 hard cap: state IDs must be ≤ 1081
- All 1081 slots are used. No new states can be created, only existing ones reassigned.

### Color scheme
- **Primary**: NEON RED (#FF3030) on black background, white text
- **Accents**: Blue/cyan
- **Country names on map**: NEON YELLOW (#FFFF00)
- **NO purple** anywhere except Petrochem (PET), which is explicitly purple
- **NO yellow** anywhere except country map names, HRE (neon yellow), and Petrochem
- Top bar icons: vanilla HOI4 icons tinted neon yellow (luminance-preserving tint)

### HOI4 game path (platform-dependent)
- **Windows**: `E:\SteamLibrary\steamapps\common\Hearts of Iron IV`
- **macOS**: `~/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV`
  (verify on first use — may also be in `/Applications` or another Steam library)

### HOI4 mod install path (platform-dependent)
- **Windows**: the `mod/` subfolder here IS the mod. Symlink or copy to
  `C:\Users\<user>\Documents\Paradox Interactive\Hearts of Iron IV\mod\`
- **macOS**: `~/Documents/Paradox Interactive/Hearts of Iron IV/mod/`

## HOI4 modding reference

### File formats
- **DDS**: Uncompressed A8R8G8B8 with 128-byte header, BGRA pixel data
- **TGA**: 18-byte header + BGRA pixel data, bottom-left origin (header[17]=0x08), rows bottom-to-top
- **Flag sizes**: 82×52 (main `gfx/flags/`), 41×26 (`gfx/flags/medium/`), 10×7 (`gfx/flags/small/`)
- **Localisation**: UTF-8 with BOM, `l_english:` header, every key prefixed with space + key colon + number colon + space + quoted value

### Focus tree syntax
- `prerequisite = { focus = A focus = B }` = A **OR** B
- Multiple `prerequisite = { }` blocks = **AND** (all must be satisfied)
- `mutually_exclusive` blocks go **inside** focus definitions
- Same focus ID in same tree = crash. Always check for duplicates.

### Cosmetic tags
- `set_cosmetic_tag = TAG_NAME` changes name/flag/color at runtime
- Requires: color entry in `common/countries/colors.txt`, localisation, and flag TGA files named `TAG_NAME.tga`

### Civil wars
- `start_civil_war = { ideology = X size = 0.5 }` with variable checks for corporate allegiance
- Militech/Petrochem influence variables determine which side each corp joins

## Country tags (29 + PET = 30)
NUS, USR, WCS, FSA, TEX, OAS, EEC, GRN, KOR, URB, ASN, IDN, UAR, PAC, UNW,
MOR, ALG, AZA, NIR, SIR, ARK, SVO, MLT, BIO, MTC, KGT, GAZ, HRE, PET

Key cosmetic tags: USR_eurasian_empire, USR_corporate_eurasia, USR_sovoil_eurasia,
USR_russian_federation, USR_commonwealth_states, USR_soviet_empire,
NUS_empire_america, NUS_corporate_confederation, NUS_american_federation, NUS_socialist_states

## NUS civil war paths
1. **Fascist → Empire of America** — `NUS_empire_america` cosmetic tag
2. **Accelerationist → Confederation of Corporate States** — `NUS_corporate_confederation`
3. **Federalist → American Federation** — `NUS_american_federation`
4. **Communist → USSA** — `NUS_socialist_states`

Militech (MLT) and Petrochem (PET) are NUS subjects that join whichever civil war
side accumulated the most influence over them via focus tree choices.

## DDS neon-yellow tinting method
Luminance-preserving: compute `L = 0.299*R + 0.587*G + 0.114*B`, then set `R=L, G=L, B=0`.
Preserves icon detail/shading while making everything yellow. Keep alpha channel intact.

## Current state (as of August 2026)
- USR focus tree: complete (all paths + OGAS sub-tree)
- NUS focus tree: complete (96 focuses, 4 civil war paths, shared branches)
- NUS events: 13 civil war events with Militech/Petrochem allegiance logic
- Top bar icons: 19 vanilla icons tinted neon yellow
- All civil war flags converted from source images
- Petrochem (PET) set up as playable country (purple, Louisiana/Oklahoma)
- Note: dual Petrochem representation exists (PET country + older internal NUS event chain in `events/petrochem.txt`) — may want to consolidate
