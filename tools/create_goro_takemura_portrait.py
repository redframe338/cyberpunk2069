"""Create HOI4 commander portraits from the supplied Goro Takemura artwork."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "goro_takemura_source.jpg"
LARGE = ROOT / "mod" / "gfx" / "leaders" / "ARK" / "portrait_ARK_goro_takemura.dds"
SMALL = (
    ROOT
    / "mod"
    / "gfx"
    / "interface"
    / "ideas"
    / "portrait_ARK_goro_takemura_small.dds"
)
PREVIEW = ROOT / "assets" / "goro_takemura_portrait_preview.png"


def make_portrait(
    image: Image.Image, box: tuple[int, int, int, int], size: tuple[int, int]
) -> Image.Image:
    portrait = image.crop(box).convert("RGB")
    portrait = portrait.resize(size, Image.Resampling.LANCZOS)
    portrait = ImageEnhance.Contrast(portrait).enhance(1.04)
    portrait = ImageEnhance.Sharpness(portrait).enhance(1.08)
    return portrait.filter(ImageFilter.UnsharpMask(radius=0.6, percent=35, threshold=3))


def main() -> None:
    source = Image.open(SOURCE)

    # Full commander frame: face, cybernetic neck, Arasaka armor and shoulders.
    large = make_portrait(source, (0, 18, 736, 1008), (156, 210))
    # Tighter roster portrait so the face remains clear at 65x67.
    small = make_portrait(source, (120, 55, 610, 560), (65, 67))

    LARGE.parent.mkdir(parents=True, exist_ok=True)
    SMALL.parent.mkdir(parents=True, exist_ok=True)
    large.save(LARGE, format="DDS", pixel_format="DXT5")
    small.save(SMALL, format="DDS", pixel_format="DXT5")
    large.resize((468, 630), Image.Resampling.NEAREST).save(PREVIEW)

    print(LARGE)
    print(SMALL)


if __name__ == "__main__":
    main()
