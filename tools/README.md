# Tools

## generate_map.ps1

Regenerates the whole political map by reassigning every vanilla HOI4 state to its
Cyberpunk-world successor tag (per [docs/03](../docs/03_GLOBAL_POLITICAL_MAP.md) and the canon map),
and (re)creates the new country tags, definitions, localisation, and history files.

**Reads:** the installed game at `E:\SteamLibrary\steamapps\common\Hearts of Iron IV`
(`map/definition.csv` + `history/states/*.txt`).
**Writes into the mod:** `history/states/` overrides, `common/countries/`, `common/country_tags/`,
`history/countries/`, `localisation/english/cyberpunk_countries_l_english.yml`.

It does **not** touch the two hand-authored histories (`NUS`, `USR`) or the bookmarks.

Run from PowerShell:

```
& ".\tools\generate_map.ps1"
```

Mapping logic lives in the `Get-Target` function (continent + vanilla owner + state-name keywords).
Edit that function to refine assignments, then re-run.
