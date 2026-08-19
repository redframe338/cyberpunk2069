"""Install one supplied image as every required HOI4 flag variant."""

import argparse
import struct
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FLAGS = ROOT / "mod" / "gfx" / "flags"
SIZES = {"": (82, 52), "medium": (41, 26), "small": (10, 7)}
VARIANTS = ("", "_communism", "_democratic", "_fascism", "_neutrality")


def save_hoi4_tga(image: Image.Image, size: tuple[int, int], path: Path) -> None:
    resized = image.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    width, height = size
    header = bytearray(18)
    header[2] = 2  # Uncompressed true-color image.
    header[12:14] = struct.pack("<H", width)
    header[14:16] = struct.pack("<H", height)
    header[16] = 24
    header[17] = 0  # Bottom-left origin, matching vanilla HOI4 flags.

    pixels = bytearray()
    for y in range(height - 1, -1, -1):
        for red, green, blue in (resized.getpixel((x, y)) for x in range(width)):
            pixels.extend((blue, green, red))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(header + pixels)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("tag")
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()

    image = Image.open(args.source)
    for folder, size in SIZES.items():
        destination = FLAGS / folder
        for suffix in VARIANTS:
            save_hoi4_tga(image, size, destination / f"{args.tag}{suffix}.tga")

    if args.preview:
        preview = Image.open(FLAGS / f"{args.tag}.tga").convert("RGB")
        preview.resize((820, 520), Image.Resampling.NEAREST).save(args.preview)

    print(f"Installed 15 flag files for {args.tag}.")


if __name__ == "__main__":
    main()
