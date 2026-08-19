const fs = require("fs");
const path = require("path");

const mod = "C:\\Users\\victo\\cyberpunk mod\\mod";
const game = "E:\\SteamLibrary\\steamapps\\common\\Hearts of Iron IV";
const errors = [];

function filesRecursive(directory) {
  const output = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const full = path.join(directory, entry.name);
    if (entry.isDirectory()) output.push(...filesRecursive(full));
    else output.push(full);
  }
  return output;
}

function stateRecords(directory) {
  const records = [];
  for (const file of fs.readdirSync(directory).filter((name) => name.endsWith(".txt"))) {
    const full = path.join(directory, file);
    const text = fs.readFileSync(full, "utf8");
    const id = text.match(/^\s*id\s*=\s*(\d+)/m);
    if (!id) continue;
    const provinces = text.match(/provinces\s*=\s*\{([\d\s]+)\}/m);
    records.push({
      id: Number(id[1]),
      file: full,
      text,
      provinces: provinces ? provinces[1].trim().split(/\s+/).map(Number) : [],
    });
  }
  return records;
}

// Text syntax and encoding.
for (const file of filesRecursive(mod)) {
  const extension = path.extname(file).toLowerCase();
  if (![".txt", ".gfx", ".mod", ".shader", ".fxh", ".yml"].includes(extension)) continue;
  const bytes = fs.readFileSync(file);
  const hasBom = bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf;
  if (extension === ".yml" && !hasBom) errors.push(`Localisation lacks BOM: ${file}`);
  if (extension !== ".yml" && hasBom) errors.push(`Non-localisation file has BOM: ${file}`);
  const text = bytes.toString("utf8");
  const opens = (text.match(/\{/g) || []).length;
  const closes = (text.match(/\}/g) || []).length;
  if (opens !== closes) errors.push(`Brace mismatch ${opens}/${closes}: ${file}`);
}

// Duplicate IDs in the mod and duplicate provinces in the effective map.
const vanillaStates = stateRecords(path.join(game, "history", "states"));
const modStates = stateRecords(path.join(mod, "history", "states"));
const vanillaFilesById = new Map(vanillaStates.map((state) => [
  state.id,
  path.basename(state.file).toLowerCase(),
]));
const modIds = new Map();
for (const state of modStates) {
  if (modIds.has(state.id)) errors.push(`Duplicate mod state ID ${state.id}: ${modIds.get(state.id)} and ${state.file}`);
  modIds.set(state.id, state.file);
  const vanillaFilename = vanillaFilesById.get(state.id);
  const modFilename = path.basename(state.file).toLowerCase();
  if (vanillaFilename && vanillaFilename !== modFilename) {
    errors.push(
      `State ${state.id} does not override vanilla by filename: ${path.basename(state.file)} != ${vanillaFilename}`,
    );
  }
}

const effective = new Map(vanillaStates.map((state) => [state.id, state]));
for (const state of modStates) effective.set(state.id, state);
const provinceOwners = new Map();
for (const state of effective.values()) {
  for (const province of state.provinces) {
    if (provinceOwners.has(province)) {
      errors.push(`Province ${province} appears in states ${provinceOwners.get(province)} and ${state.id}`);
    } else {
      provinceOwners.set(province, state.id);
    }
  }
}

// SovOil-specific ownership and reference checks.
const energyStates = [
  137, 229, 232, 233, 234, 235, 236, 237, 239, 251, 403, 405,
  571, 577, 578, 581, 582, 655, 821, 822, 824, 825, 829,
];
for (const id of energyStates) {
  const state = effective.get(id);
  if (!state) {
    errors.push(`Missing SovOil state ${id}`);
    continue;
  }
  if (!/\bowner\s*=\s*SVO\b/.test(state.text)) errors.push(`State ${id} is not owned by SVO`);
  if (!/\badd_core_of\s*=\s*SVO\b/.test(state.text)) errors.push(`State ${id} lacks SVO core`);
  if (!/\badd_core_of\s*=\s*USR\b/.test(state.text)) errors.push(`State ${id} lacks USR core`);
}

// Modern Chinese borders: unify every historical Chinese-tag state and the
// former treaty-port/island states that belong to the PRC in 2069.
const historicalChinaTags = new Set([
  "CHI", "XSM", "MAN", "SIK", "GXC", "PRC", "MEN", "SHX",
  "YUN", "TIB", "SIN", "CGX", "CSX", "CYN", "CHC",
]);
const requiredChineseStates = new Set([
  322, 326, 328, 524, 591, 609, 617, 716, 728, 729, 745,
]);
// Kang Tao administers only compact corporate enclaves. China remains the
// sovereign state and therefore must retain cores on every one of them.
const kangTaoStates = new Set([326, 597, 598, 606, 608, 613, 614, 743, 745, 749, 1034, 1035, 1038]);
for (const state of vanillaStates) {
  const owner = state.text.match(/^\s*owner\s*=\s*(\w+)/m);
  if (owner && historicalChinaTags.has(owner[1])) requiredChineseStates.add(state.id);
}
for (const id of kangTaoStates) requiredChineseStates.add(id);
for (const id of requiredChineseStates) {
  const state = effective.get(id);
  if (!state) {
    errors.push(`Missing Chinese state ${id}`);
    continue;
  }
  const expectedOwner = kangTaoStates.has(id) ? "KGT" : "CHI";
  if (!new RegExp(`\\bowner\\s*=\\s*${expectedOwner}\\b`).test(state.text)) {
    errors.push(`State ${id} is not owned by ${expectedOwner}`);
  }
  if (!/\badd_core_of\s*=\s*CHI\b/.test(state.text)) errors.push(`State ${id} lacks CHI core`);
  if (kangTaoStates.has(id) && !/\badd_core_of\s*=\s*KGT\b/.test(state.text)) {
    errors.push(`Kang Tao enclave ${id} lacks KGT core`);
  }
}

// Japan should hold only its real home-island states. Corporate Japanese
// enclaves use ARK and are validated separately by the Arasaka package.
const japaneseHomeStates = new Set([
  282, 528, 529, 531, 533, 535, 536, 645, 648, 1018, 1019,
]);
for (const state of effective.values()) {
  if (/\bowner\s*=\s*JAP\b/.test(state.text) && !japaneseHomeStates.has(state.id)) {
    errors.push(`Non-home-island state ${state.id} is incorrectly owned by JAP`);
  }
}

const allText = filesRecursive(mod)
  .filter((file) => [".txt", ".yml", ".gfx", ".mod"].includes(path.extname(file).toLowerCase()))
  .map((file) => fs.readFileSync(file, "utf8"))
  .join("\n");
if (/\b(?:1082|1083|1084|1085|1086)\b\s*=\s*\{/.test(allText)) {
  errors.push("Obsolete Arasaka state IDs are still used as state scopes");
}
if (/set_state_owner_to/.test(allText)) errors.push("Invalid set_state_owner_to effect remains");

console.log(`Effective states: ${effective.size}`);
console.log(`Effective assigned provinces: ${provinceOwners.size}`);
console.log(`Mod state overrides: ${modStates.length}`);
console.log(`SovOil energy states: ${energyStates.length}`);
console.log(`Chinese border states: ${requiredChineseStates.size}`);
if (errors.length) {
  console.error(`Validation failed with ${errors.length} issue(s):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}
console.log("Validation passed with no structural or SovOil ownership errors.");
