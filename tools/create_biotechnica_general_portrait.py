"""Create the shared large/small portrait used by Biotechnica's command staff."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "biotechnica_generals_source.jpeg"
LARGE = ROOT / "mod" / "gfx" / "leaders" / "BIO" / "portrait_BIO_corporate_commander.dds"
SMALL = ROOT / "mod" / "gfx" / "interface" / "ideas" / "portrait_BIO_corporate_commander_small.dds"
PREVIEW = ROOT / "assets" / "biotechnica_general_portrait_preview.png"


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    portrait = ImageOps.fit(
        source,
        (156, 210),
        method=Image.Resampling.LANCZOS,
        centering=(0.50, 0.31),
    )
    portrait = ImageEnhance.Contrast(portrait).enhance(1.08)
    portrait = ImageEnhance.Sharpness(portrait).enhance(1.10)
    portrait = portrait.filter(
        ImageFilter.UnsharpMask(radius=0.6, percent=35, threshold=3)
    )
    LARGE.parent.mkdir(parents=True, exist_ok=True)
    SMALL.parent.mkdir(parents=True, exist_ok=True)
    portrait.save(LARGE, format="DDS", pixel_format="DXT5")
    portrait.resize((65, 67), Image.Resampling.LANCZOS).save(
        SMALL, format="DDS", pixel_format="DXT5"
    )
    portrait.resize((468, 630), Image.Resampling.NEAREST).save(PREVIEW)
    print(LARGE)
    print(SMALL)


if __name__ == "__main__":
    main()
