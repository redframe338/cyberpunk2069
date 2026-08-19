"""Create Nicolo Loggagia's HOI4 country-leader portrait."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "nicolo_loggagia_source.jpeg"
OUTPUT = ROOT / "mod" / "gfx" / "leaders" / "BIO" / "portrait_BIO_nicolo_loggagia.dds"
PREVIEW = ROOT / "assets" / "nicolo_loggagia_portrait_preview.png"


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    portrait = ImageOps.fit(
        source,
        (156, 210),
        method=Image.Resampling.LANCZOS,
        centering=(0.52, 0.27),
    )
    portrait = ImageEnhance.Contrast(portrait).enhance(1.06)
    portrait = ImageEnhance.Sharpness(portrait).enhance(1.10)
    portrait = portrait.filter(
        ImageFilter.UnsharpMask(radius=0.6, percent=30, threshold=3)
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    portrait.save(OUTPUT, format="DDS", pixel_format="DXT5")
    portrait.resize((468, 630), Image.Resampling.NEAREST).save(PREVIEW)
    print(OUTPUT)


if __name__ == "__main__":
    main()
