"""Create EEC and Neo-Soviet institutional country-leader portraits."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[1]
PORTRAITS = (
    (
        "european_parliament",
        ROOT / "assets" / "european_parliament_source.png",
        ROOT / "mod" / "gfx" / "leaders" / "EEC" / "portrait_EEC_european_parliament.dds",
        (4, 24, 59),
    ),
    (
        "supreme_soviet",
        ROOT / "assets" / "supreme_soviet_source.png",
        ROOT / "mod" / "gfx" / "leaders" / "USR" / "portrait_USR_supreme_soviet.dds",
        (118, 0, 0),
    ),
)
PREVIEW = ROOT / "assets" / "institutional_leader_portraits_preview.png"


def make_portrait(source_path: Path, background: tuple[int, int, int]) -> Image.Image:
    source = Image.open(source_path).convert("RGB")
    source = ImageEnhance.Contrast(source).enhance(1.04)
    emblem = ImageOps.contain(source, (156, 156), Image.Resampling.LANCZOS)
    portrait = Image.new("RGB", (156, 210), background)
    portrait.paste(emblem, ((156 - emblem.width) // 2, 27))
    return portrait


def main() -> None:
    previews: list[Image.Image] = []
    for _, source, output, background in PORTRAITS:
        portrait = make_portrait(source, background)
        output.parent.mkdir(parents=True, exist_ok=True)
        portrait.save(output, format="DDS", pixel_format="DXT5")
        previews.append(portrait.resize((468, 630), Image.Resampling.NEAREST))
        print(output)
    sheet = Image.new("RGB", (936, 630), (6, 7, 11))
    for index, portrait in enumerate(previews):
        sheet.paste(portrait, (index * 468, 0))
    sheet.save(PREVIEW)
    print(PREVIEW)


if __name__ == "__main__":
    main()
