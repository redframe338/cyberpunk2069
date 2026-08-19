"""Build frontend-only HOI4 menu textures from the Cyberpunk 2069 artwork."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


FRONTEND_SIZE = (1920, 1440)
BUTTON_SIZE = (320, 62)
MENU_PANEL_SIZE = (448, 600)
ROSTER_PANEL_SIZE = (1120, 700)
COUNTRY_CARD_FRAME_SIZE = (150, 274)
NEON = (239, 75, 85)       # signal red
CYAN = (103, 219, 225)     # pale data cyan
MAGENTA = (159, 53, 64)    # muted structural red
INK = (6, 7, 11)
BURGUNDY = (27, 10, 17)


def compose_frontend(source: Image.Image) -> Image.Image:
    """Preserve the full 16:9 artwork inside HOI4's 4:3 frontend texture."""
    background = ImageOps.fit(source, FRONTEND_SIZE, method=Image.Resampling.LANCZOS)
    background = background.filter(ImageFilter.GaussianBlur(28))
    background = ImageEnhance.Brightness(background).enhance(0.45)

    foreground = ImageOps.contain(source, FRONTEND_SIZE, method=Image.Resampling.LANCZOS)
    x = (FRONTEND_SIZE[0] - foreground.width) // 2
    y = (FRONTEND_SIZE[1] - foreground.height) // 2
    background.paste(foreground, (x, y))
    return background.convert("RGBA")


def menu_button_strip() -> Image.Image:
    """Cyberdeck navigation rows modelled on the reference menu."""
    width, height = BUTTON_SIZE
    strip = Image.new("RGBA", (width * 3, height), (0, 0, 0, 0))

    def frame(state: int) -> Image.Image:
        image = Image.new("RGBA", BUTTON_SIZE, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        shape = ((1, 9), (10, 1), (294, 1), (319, 18), (319, 51),
                 (308, 61), (1, 61))
        fills = ((*BURGUNDY, 105), (14, 35, 39, 235), (112, 31, 42, 245))
        edges = ((*NEON, 90), (*CYAN, 255), (*NEON, 255))
        draw.polygon(shape, fill=fills[state], outline=edges[state])
        # Left selector rail and the reference's bright boxed interaction state.
        draw.rectangle((1, 9, 8, 60), fill=((*NEON, 125), (*CYAN, 255), (*NEON, 255))[state])
        draw.line((17, 7, 273, 7), fill=((*NEON, 75), (*CYAN, 225), (*NEON, 210))[state])
        draw.line((17, 55, 302, 55), fill=((*NEON, 55), (*CYAN, 185), (*NEON, 150))[state])
        # Status cell and telemetry bars on the right end of every row.
        draw.rectangle((275, 11, 309, 49), outline=(*CYAN, 165 if state else 70))
        for y in (17, 22, 27, 36):
            draw.line((281, y, 301 if y != 36 else 293, y), fill=(*CYAN, 190 if state else 75))
        draw.polygon(((309, 19), (317, 27), (317, 41), (309, 49)), fill=(*MAGENTA, 200))
        for x in range(18, 66, 8):
            draw.rectangle((x, 12, x + 3, 14), fill=(*NEON, 95 + state * 60))
        return image

    for state in range(3):
        image = frame(state)
        strip.paste(image, (width * state, 0), image)
    return strip


def angular_button_strip(size: tuple[int, int], frames: int = 3) -> Image.Image:
    """Generate a scalable cyberpunk button strip for compact setup controls."""
    width, height = size
    strip = Image.new("RGBA", (width * frames, height), (0, 0, 0, 0))
    cut = max(5, min(14, height // 3))
    for state in range(frames):
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        shape = ((1, cut), (cut, 1), (width - cut * 2, 1),
                 (width - 1, cut), (width - 1, height - cut),
                 (width - cut, height - 1), (cut * 2, height - 1),
                 (1, height - cut))
        fills = ((*INK, 245), (*BURGUNDY, 250), (55, 17, 27, 255))
        edge = ((*NEON, 205), (*CYAN, 255), (*NEON, 255))[state]
        draw.polygon(shape, fill=fills[state], outline=edge)
        draw.line((cut + 5, 5, width - cut * 2 - 4, 5), fill=(*CYAN, 110 + state * 55), width=1)
        draw.rectangle((width - cut - 9, height // 2 - 2,
                        width - cut - 5, height // 2 + 2), fill=(*MAGENTA, 210))
        strip.paste(image, (state * width, 0), image)
    return strip


def checkbox_strip() -> Image.Image:
    """Two-frame neon checkbox with an unmistakable active state."""
    frame_size = (34, 30)
    strip = Image.new("RGBA", (68, 30), (0, 0, 0, 0))
    for state in range(2):
        image = Image.new("RGBA", frame_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.polygon(((3, 8), (10, 2), (31, 2), (31, 23), (24, 29), (3, 29)),
                     fill=(*INK, 250), outline=(*NEON, 235))
        draw.rectangle((8, 7, 26, 24), outline=(*CYAN, 145), width=1)
        if state:
            draw.line((9, 15, 15, 22, 27, 7), fill=(*NEON, 255), width=3)
            draw.rectangle((28, 5, 31, 8), fill=(*MAGENTA, 255))
        strip.paste(image, (state * frame_size[0], 0), image)
    return strip


def difficulty_strip() -> Image.Image:
    """Two-frame selector backing used beneath each difficulty label."""
    return angular_button_strip((116, 35), 2)


def terminal_row(size: tuple[int, int], header: bool = False) -> Image.Image:
    width, height = size
    row = Image.new("RGBA", size, (*BURGUNDY, 225 if not header else 245))
    draw = ImageDraw.Draw(row)
    draw.rectangle((1, 1, width - 2, height - 2), outline=(*NEON, 115 if not header else 220), width=1)
    draw.line((10, height - 3, width - 40, height - 3), fill=(*CYAN, 85), width=1)
    draw.polygon(((width - 32, 1), (width - 1, 1), (width - 1, height - 1)),
                 fill=(*NEON, 65 if not header else 140))
    draw.rectangle((7, 7, 10, height - 8), fill=(*MAGENTA, 175))
    for x in range(width - 92, width - 22, 9):
        draw.rectangle((x, 7, x + 3, 9), fill=(*CYAN, 130))
    return row


def framed_panel(size: tuple[int, int], alpha: int = 235) -> Image.Image:
    """Detailed cyberdeck chassis shared by frontend and setup screens."""
    width, height = size
    panel = Image.new("RGBA", size, (*INK, alpha))
    draw = ImageDraw.Draw(panel)
    outline = ((4, 28), (28, 4), (width - 58, 4), (width - 4, 48),
               (width - 4, height - 32), (width - 32, height - 4),
               (44, height - 4), (4, height - 42))
    draw.line((*outline, outline[0]), fill=(*NEON, 205), width=2, joint="curve")
    inner = ((14, 32), (33, 14), (width - 62, 14), (width - 14, 53),
             (width - 14, height - 37), (width - 37, height - 14),
             (49, height - 14), (14, height - 47))
    draw.line((*inner, inner[0]), fill=(*NEON, 75), width=1)
    draw.line((38, 27, width - 90, 27), fill=(*CYAN, 150), width=2)
    draw.line((63, height - 27, width - 55, height - 27), fill=(*MAGENTA, 145), width=2)
    draw.polygon(((width - 88, 4), (width - 58, 4), (width - 23, 33),
                  (width - 69, 24)), fill=(*NEON, 185))
    draw.polygon(((4, height - 70), (4, height - 42), (36, height - 10),
                  (22, height - 55)), fill=(*CYAN, 145))
    for y in range(82, height - 65, 42):
        draw.line((19, y, 31, y), fill=(*NEON, 130), width=1)
        draw.ellipse((width - 30, y - 2, width - 26, y + 2), fill=(*MAGENTA, 200))
    # Reference-style vertical navigation rail, micro-grid, and diagnostic footer.
    draw.line((38, 26, 38, height - 31), fill=(*NEON, 115), width=1)
    draw.line((42, 70, 42, height - 78), fill=(*CYAN, 45), width=1)
    for y in range(78, height - 82, 13):
        draw.line((24, y, 33 if y % 26 else 36, y), fill=(*NEON, 100), width=1)
    for x in range(56, width - 50, 16):
        draw.rectangle((x, 43, x + 5, 45), fill=(*CYAN, 55 if x % 32 else 120))
    draw.rectangle((55, height - 66, width - 52, height - 42), outline=(*NEON, 75))
    for x in range(64, width - 65, 12):
        draw.line((x, height - 59, x + 6, height - 59), fill=(*CYAN, 80))
    # The large bookmark chassis gets two purpose-built section separators.
    if width >= 1000 and height >= 650:
        for y in (42, 337):
            draw.line((76, y, width - 76, y), fill=(*NEON, 150), width=1)
            draw.line((width - 180, y - 4, width - 82, y - 4), fill=(*CYAN, 170), width=2)
        draw.rectangle((52, 52, width - 52, height - 54), outline=(*CYAN, 35))
    # Circuit traces and system-status blocks keep large panels visually active.
    draw.line((24, 62, 70, 62, 84, 48, 145, 48), fill=(*NEON, 80), width=1)
    draw.line((width - 24, height - 88, width - 74, height - 88,
               width - 91, height - 71, width - 160, height - 71),
              fill=(*CYAN, 85), width=1)
    return panel


def country_card_strip() -> Image.Image:
    """Create normal and hover frames for featured leader/flag cards."""
    width, height = COUNTRY_CARD_FRAME_SIZE
    strip = Image.new("RGBA", (width * 2, height), (0, 0, 0, 0))

    def frame(hovered: bool) -> Image.Image:
        card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card)
        edge = (*CYAN, 255) if hovered else (*NEON, 220)
        inner = (*NEON, 150 if hovered else 75)
        # Only the chassis is opaque. Portrait and flag apertures remain fully
        # transparent so HOI4's leader and flag textures retain their brightness.
        chassis = ((2, 24), (24, 2), (126, 2), (148, 24),
                   (148, 252), (128, 272), (20, 272), (2, 254))
        draw.polygon(chassis, fill=(*INK, 240))
        draw.rectangle((14, 18, width - 15, 183), fill=(0, 0, 0, 0))
        draw.rectangle((24, 189, 125, 239), fill=(0, 0, 0, 0))
        draw.rectangle((2, 2, width - 3, height - 3), outline=edge, width=3)
        draw.rectangle((8, 8, width - 9, height - 9), outline=inner, width=1)

        # Portrait viewport, flag bay, and country-name terminal plate.
        draw.rectangle((14, 18, width - 15, 183), outline=(*NEON, 170), width=2)
        draw.line((9, 188, width - 10, 188), fill=edge, width=2)
        draw.rectangle((24, 189, 125, 239), outline=(*CYAN, 170), width=2)
        draw.rectangle((8, 241, width - 9, height - 9), fill=(*BURGUNDY, 245), outline=inner, width=1)
        # Small scan/status deck above and below the portrait aperture.
        draw.rectangle((32, 8, 118, 13), outline=(*CYAN, 75))
        for x in range(37, 113, 9):
            draw.rectangle((x, 10, x + 3, 11), fill=(*CYAN, 130))
        draw.rectangle((13, 245, 18, 266), fill=(*MAGENTA, 180))
        draw.rectangle((132, 245, 137, 266), fill=(*CYAN, 135))

        # Angular cyberpunk corner cuts and small telemetry marks.
        draw.polygon(((2, 2), (25, 2), (2, 25)), fill=(0, 0, 0, 0))
        draw.line((3, 25, 25, 3), fill=edge, width=3)
        draw.polygon(((width - 3, 2), (width - 26, 2), (width - 3, 25)), fill=(0, 0, 0, 0))
        draw.line((width - 4, 25, width - 26, 3), fill=edge, width=3)
        for y in (46, 82, 118, 154, 218):
            draw.line((5, y, 10, y), fill=inner, width=1)
            draw.line((width - 11, y, width - 6, y), fill=inner, width=1)
        if hovered:
            draw.rectangle((11, 11, width - 12, height - 12), outline=(*CYAN, 170), width=2)
            draw.line((18, 187, width - 19, 187), fill=(*CYAN, 240), width=2)
        return card

    normal = frame(False)
    hover = frame(True)
    strip.paste(normal, (0, 0), normal)
    strip.paste(hover, (width, 0), hover)
    return strip


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--setup-source", type=Path)
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()

    source = Image.open(args.source).convert("RGB")
    args.output_directory.mkdir(parents=True, exist_ok=True)

    frontend = compose_frontend(source)
    frontend.save(
        args.output_directory / "cyberpunk_main_menu.dds", pixel_format="DXT5"
    )
    menu_button_strip().save(
        args.output_directory / "cyberpunk_menu_button.dds", pixel_format="DXT5"
    )
    framed_panel(MENU_PANEL_SIZE, 245).save(
        args.output_directory / "cyberpunk_menu_panel.dds", pixel_format="DXT5"
    )
    framed_panel(ROSTER_PANEL_SIZE, 220).save(
        args.output_directory / "cyberpunk_roster_panel.dds", pixel_format="DXT5"
    )
    country_card_strip().save(
        args.output_directory / "cyberpunk_country_entry.dds", pixel_format="DXT5"
    )
    # Country-selection map and gameplay-settings interface kit.
    for filename, size, alpha in (
        ("cyberpunk_setup_bar_top.dds", (484, 128), 238),
        ("cyberpunk_setup_bar_bottom.dds", (484, 128), 238),
        ("cyberpunk_game_settings_panel.dds", (484, 97), 245),
        ("cyberpunk_gameplay_panel.dds", (598, 250), 242),
        ("cyberpunk_country_details_panel.dds", (492, 301), 242),
        ("cyberpunk_rules_panel.dds", (678, 600), 248),
        ("cyberpunk_random_panel.dds", (500, 400), 248),
        ("cyberpunk_dropdown_panel.dds", (300, 300), 250),
    ):
        framed_panel(size, alpha).save(args.output_directory / filename, pixel_format="DXT5")

    for filename, size in (
        ("cyberpunk_compact_button.dds", (261, 34)),
        ("cyberpunk_small_button.dds", (148, 38)),
        ("cyberpunk_tiny_button.dds", (123, 34)),
        ("cyberpunk_play_button.dds", (241, 60)),
    ):
        angular_button_strip(size, 3).save(args.output_directory / filename, pixel_format="DXT5")

    angular_button_strip((241, 60), 1).save(
        args.output_directory / "cyberpunk_play_button_ready.dds", pixel_format="DXT5"
    )
    angular_button_strip((232, 35), 2).save(
        args.output_directory / "cyberpunk_custom_settings_button.dds", pixel_format="DXT5"
    )
    checkbox_strip().save(
        args.output_directory / "cyberpunk_checkbox.dds", pixel_format="DXT5"
    )
    difficulty_strip().save(
        args.output_directory / "cyberpunk_difficulty_button.dds", pixel_format="DXT5"
    )
    terminal_row((630, 40)).save(
        args.output_directory / "cyberpunk_rule_row.dds", pixel_format="DXT5"
    )
    terminal_row((636, 40), True).save(
        args.output_directory / "cyberpunk_rule_header.dds", pixel_format="DXT5"
    )
    terminal_row((300, 32)).save(
        args.output_directory / "cyberpunk_dropdown_bg.dds", pixel_format="DXT5"
    )

    if args.setup_source:
        setup_source = Image.open(args.setup_source).convert("RGB")
        setup_background = ImageOps.fit(
            setup_source, (1920, 1080), method=Image.Resampling.LANCZOS
        ).convert("RGBA")
        setup_background.save(
            args.output_directory / "cyberpunk_country_setup.dds", pixel_format="DXT5"
        )

    if args.preview:
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        frontend.convert("RGB").resize((960, 720), Image.Resampling.LANCZOS).save(
            args.preview
        )

    print("Built frontend-only background and functional menu overlays.")


if __name__ == "__main__":
    main()
