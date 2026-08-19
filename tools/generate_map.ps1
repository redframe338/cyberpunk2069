# Cyberpunk 2077 map generator — reassigns every vanilla HOI4 state to its
# Cyberpunk-world successor tag (per docs/03 + canon map) and creates the new
# country tags/definitions/localisation/history. Same Earth geography, new owners.

# RETIRED AFTER THE INITIAL MAP PASS:
# The live mod now contains hand-authored Iran, Switzerland, Korea, Arabian
# wasteland, and Arasaka state/history changes. A blind full regeneration would
# overwrite those stable files. Run only when intentionally rebuilding the map
# from vanilla and prepared to reapply all post-generation content.
param(
  [switch]$UnsafeFullRegeneration
)

if (-not $UnsafeFullRegeneration) {
  throw "Full regeneration is disabled because it would overwrite hand-authored Cyberpunk states and country history. Use -UnsafeFullRegeneration only for a deliberate rebuild."
}

$ErrorActionPreference = 'Stop'
$game = "E:\SteamLibrary\steamapps\common\Hearts of Iron IV"
$mod  = "C:\Users\victo\cyberpunk mod\mod"

# --- province -> continent map ---
$prov2cont = @{}
foreach ($line in [System.IO.File]::ReadAllLines("$game\map\definition.csv")) {
  $f = $line.Split(';'); if ($f.Count -ge 8) { $prov2cont[$f[0]] = $f[7] }
}

# Chinese warlord/successor tags that unify into CHI
$chinaTags = @('CHI','XSM','MAN','SIK','GXC','PRC','MEN','SHX','YUN','TIB','SIN','CGX','CSX','CYN','CHC')

function Get-Target($owner, $cont, $f) {
  $f = $f.ToLower()
  if ($f -match 'hawaii') { return 'NUS' }
  if ($f -match 'greenland') { return 'GRN' }
  switch ($cont) {
    '1' { # Europe
      if ($owner -eq 'SOV') { return 'USR' }
      if ($owner -in @('EST','LAT','LIT')) { return 'USR' }
      if ($owner -eq 'ENG') { return 'ENG' } # United Kingdom stays independent
      return 'EEC' # all other continental Europe unifies into the EEC
    }
    '2' { # North America
      if ($owner -eq 'CAN') { return 'CAN' }
      if ($f -match 'newfoundland|labrador|bermuda|pierre and miquelon') { return 'CAN' }
      if ($owner -eq 'MEX') { return 'OAS' }
      if ($owner -eq 'USA') {
        if ($f -match 'idaho|oregon|washington') { return 'WCS' }
        if ($f -match 'montana|wyoming|colorado|new mexico|arizona|nevada') { return 'FSA' }
        if ($f -match 'texas') { return 'TEX' }
        return 'NUS'
      }
      return 'OAS' # Central America / Caribbean minors
    }
    '3' { return 'OAS' } # South America
    '4' { # Australasia
      if ($owner -eq 'NZL') { return 'NZL' }
      if ($owner -eq 'CHL') { return 'OAS' }
      if ($owner -eq 'INS') { return 'IDN' }
      return 'AST'
    }
    '5' { # Africa
      if ($f -match 'morocco|sidi ifni|rio de oro|spanish africa') { return 'MOR' }
      if ($f -match 'algeria|tunisia') { return 'ALG' }
      if ($f -match 'tombouctou|gao') { return 'AZA' }
      if ($f -match 'liberia|sierra leone|gambia|cape verde|dahomey|togo|upper volta|ivory coast|guinea|niger|nigeria|benue|borno|sokoto|mali|mauritania|kayes|senegal') { return 'UNW' }
      return 'PAC'
    }
    '6' { # Asia
      if ($owner -in @('SOV','AFG','TAN')) { return 'USR' }
      if ($owner -in @('RAJ','NEP','BHU')) { return 'URB' }
      if ($f -match 'goa') { return 'URB' }
      if ($owner -eq 'MON') { return 'MON' }
      if ($owner -in $chinaTags) { return 'CHI' }
      if ($f -match 'formosa|taiwan|hong ?kong|macau|hainan|guangzhouwan') { return 'CHI' }
      if ($owner -eq 'JAP') {
        if ($f -match 'korea|chosen|seoul|keijo|heijo|pyongyang|kanko|rashin|chosun') { return 'KOR' }
        return 'JAP'
      }
      if ($owner -eq 'USA') { if ($f -match 'guam|wake|midway') { return 'NUS' }; return 'ASN' }
      if ($owner -in @('INS','HOL')) { return 'IDN' }
      return 'ASN' # FRA/ENG/MAL/BRM/SIA/PHI/POR colonial SE Asia
    }
    '7' { # Middle East
      if ($owner -in @('PER','SOV','AFG')) { return 'USR' }
      if ($owner -eq 'TUR') { return 'TUR' }
      if ($owner -eq 'RAJ') { return 'URB' }
      if ($owner -in @('SAU','YEM','OMA')) { return $owner } # Arabia stays independent
      if ($f -match 'cairo|sinai|egypt') { return 'PAC' }
      return 'UAR'
    }
    default { return $owner }
  }
}

# --- pass 1: decide + write state overrides ---
if (-not (Test-Path "$mod\history\states")) { New-Item -ItemType Directory -Force "$mod\history\states" | Out-Null }
$tagStates = @{}
$changed = 0; $total = 0
foreach ($file in Get-ChildItem "$game\history\states" -Filter *.txt) {
  $total++
  $t = [System.IO.File]::ReadAllText($file.FullName)
  $owner = if ($t -match 'owner\s*=\s*([A-Z0-9]{3})') { $Matches[1] } else { '' }
  $id    = if ($t -match 'id\s*=\s*(\d+)') { [int]$Matches[1] } else { 0 }
  $cont  = ''
  if ($t -match 'provinces\s*=\s*\{\s*([\d\s]+?)\}') {
    $fp = ($Matches[1].Trim() -split '\s+')[0]
    if ($prov2cont.ContainsKey($fp)) { $cont = $prov2cont[$fp] }
  }
  if (-not $owner) { continue }               # unowned stays unowned
  $target = Get-Target $owner $cont $file.Name
  if (-not $tagStates.ContainsKey($target)) { $tagStates[$target] = New-Object System.Collections.Generic.List[int] }
  $tagStates[$target].Add($id)
  if ($target -eq $owner) { continue }        # survivor, keep vanilla file
  $t2 = $t -replace 'owner\s*=\s*[A-Z0-9]{3}', "owner = $target"
  $t2 = $t2 -replace 'controller\s*=\s*[A-Z0-9]{3}', "controller = $target"
  $t2 = $t2 -replace 'add_core_of\s*=\s*[A-Z0-9]{3}', "add_core_of = $target"
  $t2 = $t2 -replace 'add_claim_by\s*=\s*[A-Z0-9]{3}\s*', ''
  $hdr = "# AUTO-GENERATED map override: $owner -> $target (Cyberpunk conversion). See docs/03.`r`n"
  [System.IO.File]::WriteAllText("$mod\history\states\$($file.Name)", $hdr + $t2, (New-Object System.Text.UTF8Encoding($false)))
  $changed++
}
"state files written (changed): $changed of $total total"

# --- new tag metadata (NUS/USR already hand-authored, excluded here) ---
$new = [ordered]@{
  WCS = @{n="Western Corporate States"; a="Corporate";     c="western_european"; col="120 170 210"; cap=386}
  FSA = @{n="Free States";              a="Free States";    c="western_european"; col="175 205 230"; cap=382}
  TEX = @{n="Republic of Texas";        a="Texan";          c="western_european"; col="205 95 70";   cap=375}
  OAS = @{n="Organization of American States"; a="American"; c="southamerican";   col="90 150 210";  cap=277}
  EEC = @{n="European Economic Community"; a="European";     c="western_european"; col="45 100 205";  cap=64}
  GRN = @{n="Greenland";                a="Greenlandic";    c="western_european"; col="120 130 150"; cap=101}
  KOR = @{n="Korea";                    a="Korean";         c="asian";            col="180 140 200"; cap=0}
  URB = @{n="United Republic of Bharat"; a="Bharati";       c="asian";            col="210 150 90";  cap=0}
  ASN = @{n="ASEAN";                    a="ASEAN";          c="asian";            col="230 100 160"; cap=0}
  IDN = @{n="Indonesia";               a="Indonesian";     c="asian";            col="235 130 180"; cap=0}
  UAR = @{n="United Arab Republic";     a="Arab";           c="middle_eastern";   col="150 170 90";  cap=291}
  PAC = @{n="Pan-African Confederation"; a="African";       c="african";          col="60 150 70";   cap=907}
  UNW = @{n="Union of North-West Africa"; a="West African"; c="african";          col="240 200 90";  cap=558}
  MOR = @{n="Morocco";                  a="Moroccan";       c="middle_eastern";   col="140 45 45";   cap=461}
  ALG = @{n="Algeria";                  a="Algerian";       c="middle_eastern";   col="110 60 60";   cap=459}
  AZA = @{n="Azawad";                   a="Azawadi";        c="african";          col="200 120 60";  cap=782}
}

# --- country_tags (new tags + the two hand-authored) ---
$tagLines = @("# Cyberpunk conversion country tags. See docs/03_GLOBAL_POLITICAL_MAP.md.",
  'NUS = "countries/New United States of America.txt"',
  'USR = "countries/Union of Sovereign Soviet Republics.txt"')
foreach ($k in $new.Keys) { $tagLines += ('{0} = "countries/{1}.txt"' -f $k, $new[$k].n) }
[System.IO.File]::WriteAllLines("$mod\common\country_tags\00_cyberpunk.txt", $tagLines)

# --- country definition files + history ---
foreach ($k in $new.Keys) {
  $m = $new[$k]
  $def = "graphical_culture = $($m.c)_gfx`r`ngraphical_culture_2d = $($m.c)_2d`r`n`r`ncolor = { $($m.col) }`r`n"
  [System.IO.File]::WriteAllText("$mod\common\countries\$($m.n).txt", $def, (New-Object System.Text.UTF8Encoding($false)))
  $cap = $m.cap
  if ($cap -eq 0) { if ($tagStates.ContainsKey($k) -and $tagStates[$k].Count -gt 0) { $cap = ($tagStates[$k] | Sort-Object)[0] } else { $cap = 1 } }
  $hist = @"
# $($m.n) — 2069 starting setup (auto-generated first pass; placeholder government).
capital = $cap

set_research_slots = 3
set_stability = 0.50
set_war_support = 0.40

set_politics = {
	ruling_party = neutrality
	last_election = "2064.01.01"
	election_frequency = 48
	elections_allowed = no
}

set_popularities = {
	democratic = 25
	neutrality = 60
	fascism = 10
	communism = 5
}
"@
  [System.IO.File]::WriteAllText("$mod\history\countries\$k - $($m.n).txt", $hist, (New-Object System.Text.UTF8Encoding($false)))
}

# --- localisation (UTF-8 WITH BOM) ---
$loc = New-Object System.Collections.Generic.List[string]
$loc.Add('l_english:')
$loc.Add(' NUS:0 "New United States of America"'); $loc.Add(' NUS_DEF:0 "the New United States of America"'); $loc.Add(' NUS_ADJ:0 "American"')
$loc.Add(' USR:0 "Union of Sovereign Soviet Republics"'); $loc.Add(' USR_DEF:0 "the Union of Sovereign Soviet Republics"'); $loc.Add(' USR_ADJ:0 "Neo-Soviet"')
foreach ($k in $new.Keys) {
  $m = $new[$k]
  $loc.Add((' {0}:0 "{1}"' -f $k, $m.n)); $loc.Add((' {0}_DEF:0 "{1}"' -f $k, $m.n)); $loc.Add((' {0}_ADJ:0 "{1}"' -f $k, $m.a))
}
[System.IO.File]::WriteAllText("$mod\localisation\english\cyberpunk_countries_l_english.yml", ($loc -join "`r`n") + "`r`n", (New-Object System.Text.UTF8Encoding($true)))

# --- summary ---
"`n=== states per Cyberpunk tag (top 30) ==="
$tagStates.GetEnumerator() | Sort-Object { $_.Value.Count } -Descending | Select-Object -First 30 | ForEach-Object { "{0,5}  {1}" -f $_.Value.Count, $_.Key }
