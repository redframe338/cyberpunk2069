"""Create Ling Xiaohan's HOI4 country-leader portrait."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "ling_xiaohan_source.jpeg"
OUTPUT = ROOT / "mod" / "gfx" / "leaders" / "KGT" / "portrait_KGT_ling_xiaohan.dds"
PREVIEW = ROOT / "assets" / "ling_xiaohan_portrait_preview.png"


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    width, height = source.size
    upper_body = source.crop((
        int(width * 0.11),
        int(height * 0.035),
        int(width * 0.89),
        int(height * 0.64),
    ))
    portrait = ImageOps.fit(
        upper_body,
        (156, 210),
        method=Image.Resampling.LANCZOS,
        centering=(0.50, 0.42),
    )
    portrait = ImageEnhance.Contrast(portrait).enhance(1.10)
    portrait = ImageEnhance.Sharpness(portrait).enhance(1.12)
    portrait = portrait.filter(
        ImageFilter.UnsharpMask(radius=0.6, percent=35, threshold=3)
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    portrait.save(OUTPUT, format="DDS", pixel_format="DXT5")
    portrait.resize((468, 630), Image.Resampling.NEAREST).save(PREVIEW)
    print(OUTPUT)


if __name__ == "__main__":
    main()
