"""Create HOI4 commander portraits from the supplied Adam Smasher artwork."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "adam_smasher_source.jpeg"
LARGE = ROOT / "mod" / "gfx" / "leaders" / "ARK" / "portrait_ARK_adam_smasher.dds"
SMALL = (
    ROOT
    / "mod"
    / "gfx"
    / "interface"
    / "ideas"
    / "portrait_ARK_adam_smasher_small.dds"
)
PREVIEW = ROOT / "assets" / "adam_smasher_portrait_preview.png"


def crop_to_ratio(
    image: Image.Image, box: tuple[int, int, int, int], size: tuple[int, int]
) -> Image.Image:
    portrait = image.crop(box).convert("RGB")
    portrait = portrait.resize(size, Image.Resampling.LANCZOS)
    portrait = ImageEnhance.Contrast(portrait).enhance(1.04)
    portrait = ImageEnhance.Sharpness(portrait).enhance(1.08)
    return portrait.filter(ImageFilter.UnsharpMask(radius=0.6, percent=35, threshold=3))


def main() -> None:
    source = Image.open(SOURCE)

    # Full commander framing: head, cybernetics, shoulders and chest armor.
    large = crop_to_ratio(source, (100, 0, 1120, 1373), (156, 210))
    # Roster framing: tighter face crop for the 65x67 selection icon.
    small = crop_to_ratio(source, (220, 80, 1020, 905), (65, 67))

    LARGE.parent.mkdir(parents=True, exist_ok=True)
    SMALL.parent.mkdir(parents=True, exist_ok=True)
    large.save(LARGE, format="DDS", pixel_format="DXT5")
    small.save(SMALL, format="DDS", pixel_format="DXT5")

    preview = large.resize((468, 630), Image.Resampling.NEAREST)
    preview.save(PREVIEW)
    print(LARGE)
    print(SMALL)


if __name__ == "__main__":
    main()
