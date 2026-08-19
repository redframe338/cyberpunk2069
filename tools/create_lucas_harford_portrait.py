"""Create Lucas Harford's HOI4 country-leader portrait."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "lucas_harford_source.jpeg"
OUTPUT = ROOT / "mod" / "gfx" / "leaders" / "MLT" / "portrait_MLT_lucas_harford.dds"
PREVIEW = ROOT / "assets" / "lucas_harford_portrait_preview.png"


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")

    # Tight executive crop retaining Harford's face, suit, and red-lit chair.
    portrait = source.crop((338, 0, 840, 675))
    portrait = portrait.resize((156, 210), Image.Resampling.LANCZOS)
    portrait = ImageEnhance.Contrast(portrait).enhance(1.08)
    portrait = ImageEnhance.Sharpness(portrait).enhance(1.10)
    portrait = portrait.filter(
        ImageFilter.UnsharpMask(radius=0.6, percent=35, threshold=3)
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    portrait.save(OUTPUT, format="DDS", pixel_format="DXT5")
    portrait.resize((468, 630), Image.Resampling.NEAREST).save(PREVIEW)
    print(OUTPUT)


if __name__ == "__main__":
    main()
