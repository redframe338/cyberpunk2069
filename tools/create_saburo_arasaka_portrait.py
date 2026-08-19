"""Create Saburo Arasaka's HOI4 country-leader portrait."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "saburo_arasaka_source.jpeg"
OUTPUT = ROOT / "mod" / "gfx" / "leaders" / "ARK" / "portrait_ARK_saburo_arasaka.dds"
PREVIEW = ROOT / "assets" / "saburo_arasaka_portrait_preview.png"


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")

    # Centered executive portrait retaining Saburo's face and formal clothing.
    portrait = source.crop((290, 0, 708, 562))
    portrait = portrait.resize((156, 210), Image.Resampling.LANCZOS)
    portrait = ImageEnhance.Contrast(portrait).enhance(1.04)
    portrait = ImageEnhance.Sharpness(portrait).enhance(1.08)
    portrait = portrait.filter(
        ImageFilter.UnsharpMask(radius=0.6, percent=35, threshold=3)
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    portrait.save(OUTPUT, format="DDS", pixel_format="DXT5")
    portrait.resize((468, 630), Image.Resampling.NEAREST).save(PREVIEW)
    print(OUTPUT)


if __name__ == "__main__":
    main()
