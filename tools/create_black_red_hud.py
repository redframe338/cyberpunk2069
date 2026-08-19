"""Build the unified Cyberpunk 2069 burgundy/red/cyan interface skin.

Only structural UI textures are targeted. Portraits, flags, equipment art,
technology art, focus icons, and map symbols keep their original colours.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[1]
VANILLA_GFX = Path(r"E:\SteamLibrary\steamapps\common\Hearts of Iron IV\gfx")
VANILLA = VANILLA_GFX / "interface"
OUTPUT_GFX = ROOT / "mod" / "gfx"
OUTPUT = OUTPUT_GFX / "interface"
MASTER_PATH = ROOT / "assets" / "cyberdeck_ui_master.png"

# The only UI colours introduced by this builder. Original alpha is retained.
INK = (6, 7, 11)
BLACK = (9, 8, 12)
BURGUNDY = (27, 10, 17)
BURGUNDY_LIT = (55, 17, 27)
RED_DARK = (112, 31, 42)
RED = (159, 53, 64)
SIGNAL_RED = (239, 75, 85)
CYAN_DARK = (35, 105, 111)
CYAN = (103, 219, 225)

STRUCTURAL_TOKENS = {
    "bg", "background", "header", "window", "panel", "frame", "entry",
    "item", "tab", "button", "footer", "top", "bottom", "overlay",
    "tooltip", "list", "screen", "bar", "slider", "checkbox", "browser",
    "container", "divider", "separator", "progress", "filter", "title",
    "slot", "row", "box", "popup", "view", "ribbon", "strip", "tile",
}

# Complete gameplay screen families. Files still need a structural token, which
# prevents illustrative content in these folders from being recoloured.
SYSTEM_DIRS = {
    "abilitylist", "airview", "alerts", "autonomy", "bop", "construction",
    "decisions", "decisionview", "divisiondesigner", "doctrines",
    "equipmentdesigner", "events", "factions", "focusview",
    "government_in_exile", "intel_ledger", "international_market",
    "landcombat", "military_industrial_organization", "navalcombat",
    "navalrepairview", "naviesview", "occupation", "officer_corp",
    "operations", "peace_conference", "popup_window", "special_project",
    "stateview", "strategicair", "strategicnavy", "techtree", "theater",
    "topbar", "tradeview", "unitcontrol",
}

EXCLUDED_TOKENS = {
    "portrait", "leader", "photo", "flag", "insignia", "medal", "terrain",
    "mapicon", "map_icon", "goal_icon", "focus_icon", "technology_icon",
    "equipment_icon", "album_art", "painting", "news_picture", "country_pic",
}

TEXTICON_TEXTURES = (
    "texticons/army_experience_20x20.dds",
    "texticons/navy_experience_20x20.dds",
    "texticons/air_experience_20x20.dds",
    "texticons/command_power_20x20.dds",
)

SHARED_PANEL_SPRITES = {
    "GFX_header_bg", "GFX_main_screens_bottom", "GFX_tiled_bg",
    "GFX_tiled_plain_bg", "GFX_tiled_window_1b_thin_border",
    "GFX_tiled_window_1b_border", "GFX_tiled_window2_1b_border",
    "GFX_construction_screen_top_bg", "GFX_construction_header_bg",
    "GFX_constructions_bg4", "GFX_production_win_top",
    "GFX_repair_queue_title_bg", "GFX_pol_view_bg", "GFX_pol_goal_bg",
    "GFX_leading_pol_party_bg", "GFX_diplo_upper_win_bg",
    "GFX_diplo_upper_diplo_bg", "GFX_diplo_filter_area_bg",
    "GFX_diplo_actions_bg", "GFX_diplo_relations_bg",
    "GFX_diplo_nat_spirits_bg", "GFX_diplo_details_header",
    "GFX_tech_info_top_win", "GFX_infantry_techtree_bg",
    "GFX_support_techtree_bg", "GFX_armortech_bg",
    "GFX_artillery_techtree_bg", "GFX_naval_techtree_bg",
    "GFX_air_techtree_bg", "GFX_industry_techtree_bg",
    "GFX_engineering_techtree_bg", "GFX_wonderweapons_bg",
    "GFX_subview_header_bg_375x101", "GFX_unit_list_header",
    "GFX_tiled_generic_bg_1", "GFX_generic_box_96",
    "GFX_generic_box_smallest", "GFX_tiled_plain_bg2",
    "GFX_tiled_focus_bg", "GFX_tiled_window_thin_border2",
    "GFX_tiled_paper_bg2", "GFX_tiled_window_transparent",
    "GFX_focus_tooltip", "GFX_mini_tooltip", "GFX_FOCUS_FILTER_FIND_BG",
    "GFX_generic_bg_307x113", "GFX_ongoing_focus_goal",
    "GFX_highlight_focus_goal", "GFX_technology_unavailable_item_bg",
    "GFX_goal_unknown",
}


def words(path: Path) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", path.stem.lower()))


def should_theme(relative: Path) -> bool:
    normalized = relative.as_posix().lower()
    if any(token in normalized for token in EXCLUDED_TOKENS):
        return False
    if not words(relative).intersection(STRUCTURAL_TOKENS):
        return False
    if len(relative.parts) == 1:
        return True
    return relative.parts[0].lower() in SYSTEM_DIRS


def shared_panel_textures() -> set[Path]:
    definitions = VANILLA.parents[1] / "interface"
    resolved: set[Path] = set()
    block_pattern = re.compile(
        r"(?:spriteType|corneredTileSpriteType)\s*=\s*\{.*?\}",
        re.IGNORECASE | re.DOTALL,
    )
    for definition in definitions.rglob("*.gfx"):
        text = definition.read_text(encoding="utf-8", errors="ignore")
        for block in block_pattern.findall(text):
            name = re.search(r'name\s*=\s*"([^"]+)"', block, re.IGNORECASE)
            texture = re.search(
                r'texturefile\s*=\s*"([^"]+)"', block, re.IGNORECASE
            )
            if not name or not texture or name.group(1) not in SHARED_PANEL_SPRITES:
                continue
            path = texture.group(1).replace("\\", "/").replace("//", "/")
            prefix = "gfx/interface/"
            if path.lower().startswith(prefix):
                path = path[len(prefix):]
            if path.lower().endswith(".dds"):
                resolved.add(Path(path))
    return resolved


def all_structural_textures() -> list[Path]:
    selected = {
        path.relative_to(VANILLA)
        for path in VANILLA.rglob("*.dds")
        if should_theme(path.relative_to(VANILLA))
    }
    selected.update(shared_panel_textures())
    return sorted(selected, key=lambda p: p.as_posix().lower())


def palette_map(luma: Image.Image, accent: str) -> Image.Image:
    """Map luminance into the strict cyberdeck ramp."""
    channels: list[list[int]] = [[], [], []]
    for value in range(256):
        if value < 55:
            amount, lo, hi = value / 55, INK, BURGUNDY
        elif value < 145:
            amount, lo, hi = (value - 55) / 90, BURGUNDY, BURGUNDY_LIT
        elif value < 220:
            amount = (value - 145) / 75
            lo, hi = BURGUNDY_LIT, RED if accent == "red" else CYAN_DARK
        else:
            amount = (value - 220) / 35
            lo = RED if accent == "red" else CYAN_DARK
            hi = SIGNAL_RED if accent == "red" else CYAN
        colour = tuple(round(a + (b - a) * amount) for a, b in zip(lo, hi))
        for channel, component in zip(channels, colour):
            channel.append(component)
    return Image.merge(
        "RGB",
        (luma.point(channels[0]), luma.point(channels[1]), luma.point(channels[2])),
    )


def is_control(relative: Path) -> bool:
    name = relative.stem.lower()
    return any(token in name for token in (
        "button", "checkbox", "slider", "progress", "selected", "active",
        "highlight", "ongoing", "available", "filter", "tab",
    ))


def add_hud_detail(image: Image.Image) -> Image.Image:
    width, height = image.size
    if width < 96 or height < 24:
        return image
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    red = (*SIGNAL_RED, 150)
    cyan = (*CYAN, 135)
    cut = max(4, min(12, min(width, height) // 8))
    draw.line([(0, cut), (cut, 0), (min(width - 1, width // 3), 0)], fill=red)
    draw.line(
        [(width - 1, height - cut), (width - cut, height - 1),
         (max(0, width * 2 // 3), height - 1)], fill=red
    )
    if width >= 220:
        draw.line([(width - 54, 2), (width - 14, 2)], fill=cyan)
        for x in range(width - 50, width - 10, 8):
            draw.rectangle((x, 5, x + 2, 6), fill=cyan)
    if height >= 80:
        for y in range(5, height, 5):
            draw.line((1, y, width - 2, y), fill=(239, 75, 85, 7))
    return Image.alpha_composite(image, overlay)


def cyberdeck_style(source: Image.Image, relative: Path, master: Image.Image) -> Image.Image:
    rgba = source.convert("RGBA")
    alpha = rgba.getchannel("A")
    luma = ImageOps.grayscale(rgba)
    luma = ImageEnhance.Contrast(luma).enhance(1.35)
    luma = ImageEnhance.Brightness(luma).enhance(0.86)
    accent = "cyan" if is_control(relative) else "red"
    recoloured = palette_map(luma, accent).convert("RGBA")
    recoloured.putalpha(alpha)
    width, height = rgba.size
    if width >= 640 and height >= 240:
        backdrop = ImageOps.fit(master, (width, height), Image.Resampling.LANCZOS)
        backdrop.putalpha(Image.new("L", (width, height), 36))
        composed = Image.alpha_composite(recoloured, backdrop)
        composed.putalpha(alpha)
        recoloured = composed
    return add_hud_detail(recoloured)


def save_dds(image: Image.Image, output: Path, relative: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    codec = "DXT3" if relative.as_posix().lower() in {
        "topbar/background.dds", "topbar/background_extended.dds"
    } else "DXT5"
    image.save(output, format="DDS", pixel_format=codec)


def make_preview(paths: list[Path]) -> Path:
    cards: list[Image.Image] = []
    for relative in paths:
        path = OUTPUT / relative
        if not path.exists():
            continue
        image = Image.open(path).convert("RGBA")
        canvas = Image.new("RGBA", (800, 190), BLACK + (255,))
        fitted = ImageOps.contain(image, (780, 170), Image.Resampling.LANCZOS)
        canvas.alpha_composite(
            fitted, ((800 - fitted.width) // 2, (190 - fitted.height) // 2)
        )
        cards.append(canvas)
    preview = Image.new("RGB", (820, max(210, len(cards) * 210)), INK)
    y = 10
    for card in cards:
        preview.paste(card.convert("RGB"), (10, y))
        y += 210
    path = ROOT / "assets" / "cyberdeck_full_ui_preview.png"
    preview.save(path, quality=95)
    return path


def main() -> None:
    if not MASTER_PATH.exists():
        raise FileNotFoundError(f"Missing generated master texture: {MASTER_PATH}")
    master = Image.open(MASTER_PATH).convert("RGBA")
    generated: list[Path] = []
    skipped: list[tuple[Path, str]] = []
    counts: Counter[str] = Counter()
    for relative in all_structural_textures():
        source_path = VANILLA / relative
        if not source_path.exists():
            skipped.append((source_path, "missing"))
            continue
        try:
            styled = cyberdeck_style(Image.open(source_path), relative, master)
            save_dds(styled, OUTPUT / relative, relative)
        except Exception as exc:
            skipped.append((source_path, type(exc).__name__))
            continue
        generated.append(relative)
        counts[relative.parts[0] if len(relative.parts) > 1 else "core"] += 1

    for relative_name in TEXTICON_TEXTURES:
        relative = Path(relative_name)
        source_path = VANILLA_GFX / relative
        if source_path.exists():
            styled = cyberdeck_style(Image.open(source_path), relative, master)
            save_dds(styled, OUTPUT_GFX / relative, relative)

    preview = make_preview([
        Path("topbar/background.dds"), Path("construction_screen_top.dds"),
        Path("production_win_top.dds"), Path("diplo_upper_win_bg.dds"),
        Path("decisionview/decision_item_bg.dds"),
        Path("tradeview/trade_header.dds"),
        Path("focusview/titlebar/focus_can_start_bg.dds"),
        Path("division_designer_bg.dds"),
    ])
    print(f"Generated {len(generated)} cyberdeck UI texture overrides.")
    print("Systems: " + ", ".join(
        f"{name}={count}" for name, count in counts.most_common()
    ))
    if skipped:
        print(f"Skipped {len(skipped)} missing or unsupported vanilla textures.")
    print(preview)


if __name__ == "__main__":
    main()
