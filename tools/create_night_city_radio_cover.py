"""Create HOI4's two-frame station cover for Night City Radio."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "night_city_radio_cover_source.png"
OUTPUT = (
    ROOT
    / "mod"
    / "gfx"
    / "interface"
    / "topbar"
    / "musicplayer"
    / "night_city_radio_album_art.dds"
)
PREVIEW = ROOT / "assets" / "night_city_radio_cover_preview.png"


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    # A 5:4 crop retains the car, large station title, and central character.
    width, height = source.size
    crop_height = min(height, int(width / 1.25))
    top = max(0, min(height - crop_height, int(height * 0.10)))
    cover = source.crop((0, top, width, top + crop_height))
    cover = cover.resize((152, 120), Image.Resampling.LANCZOS).convert("RGBA")
    cover.putalpha(Image.new("L", cover.size, 255))

    selected = ImageEnhance.Brightness(cover).enhance(1.12)
    selected = ImageEnhance.Contrast(selected).enhance(1.08)
    draw = ImageDraw.Draw(selected)
    draw.rectangle((0, 0, 151, 119), outline=(255, 12, 82), width=3)

    sheet = Image.new("RGBA", (304, 120), (0, 0, 0, 255))
    sheet.paste(cover, (0, 0))
    sheet.paste(selected, (152, 0))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUTPUT, format="DDS", pixel_format="DXT5")
    sheet.resize((912, 360), Image.Resampling.NEAREST).save(PREVIEW)

    # A dedicated now-playing thumbnail makes the cover visible in the compact
    # topbar player too, not only in the station-selection grid.
    now_playing = ImageOps.fit(cover, (46, 46), Image.Resampling.LANCZOS)
    now_playing.putalpha(Image.new("L", now_playing.size, 255))
    now_playing.save(
        OUTPUT.with_name("night_city_radio_now_playing.dds"),
        format="DDS", pixel_format="DXT5"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
