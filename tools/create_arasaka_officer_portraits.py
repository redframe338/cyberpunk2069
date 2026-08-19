"""Create large and small HOI4 portraits for Arasaka's officer corps."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets" / "arasaka_officers"
LARGE_DIR = ROOT / "mod" / "gfx" / "leaders" / "ARK"
SMALL_DIR = ROOT / "mod" / "gfx" / "interface" / "ideas"
PREVIEW = ROOT / "assets" / "arasaka_officer_portraits_preview.png"

OFFICERS = (
    ("masato_kuroda", "IMG_6649.jpeg", (0.50, 0.38)),
    ("akira_shibata", "IMG_6651.jpeg", (0.50, 0.34)),
    ("naoki_hasegawa", "IMG_6652.jpeg", (0.51, 0.36)),
    ("ryo_hayashi", "IMG_6650.jpeg", (0.50, 0.42)),
    ("kazuki_arai", "IMG_6648.jpeg", (0.50, 0.28)),
    ("takeshi_ono", "IMG_6647.jpeg", (0.50, 0.30)),
    ("shun_okamoto", "IMG_6544.jpeg", (0.50, 0.24)),
    ("tatsuya_fujii", "IMG_6587.jpeg", (0.50, 0.30)),
    # Eight supplied images cover ten officers; use alternate crops of the
    # first two armored operators so every commander still has a portrait.
    ("kohei_matsuda", "IMG_6649.jpeg", (0.43, 0.35)),
    ("isamu_nishimura", "IMG_6651.jpeg", (0.57, 0.31)),
)


def main() -> None:
    LARGE_DIR.mkdir(parents=True, exist_ok=True)
    SMALL_DIR.mkdir(parents=True, exist_ok=True)
    preview_tiles = []

    for officer_id, filename, centering in OFFICERS:
        source = Image.open(SOURCE_DIR / filename).convert("RGB")
        portrait = ImageOps.fit(
            source,
            (156, 210),
            method=Image.Resampling.LANCZOS,
            centering=centering,
        )
        portrait = ImageEnhance.Contrast(portrait).enhance(1.06)
        portrait = ImageEnhance.Sharpness(portrait).enhance(1.08)
        portrait = portrait.filter(
            ImageFilter.UnsharpMask(radius=0.6, percent=30, threshold=3)
        )
        large = LARGE_DIR / f"portrait_ARK_{officer_id}.dds"
        small = SMALL_DIR / f"portrait_ARK_{officer_id}_small.dds"
        portrait.save(large, format="DDS", pixel_format="DXT5")
        portrait.resize((65, 67), Image.Resampling.LANCZOS).save(
            small, format="DDS", pixel_format="DXT5"
        )
        preview_tiles.append(portrait.resize((234, 315), Image.Resampling.LANCZOS))

    sheet = Image.new("RGB", (234 * 5, 315 * 2), (5, 5, 7))
    for index, tile in enumerate(preview_tiles):
        sheet.paste(tile, ((index % 5) * 234, (index // 5) * 315))
    sheet.save(PREVIEW)
    print(f"Generated {len(OFFICERS)} Arasaka officer portrait sets.")
    print(PREVIEW)


if __name__ == "__main__":
    main()
