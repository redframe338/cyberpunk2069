"""Install an image as the HOI4 frontend background without distorting it."""

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


SIZES = {
    "load_cyberpunk_bg.dds": (1920, 1440),
    "load_cyberpunk_bg_small.dds": (192, 144),
}


def compose(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    # Fill the 4:3 engine texture with a subdued extension of the supplied
    # widescreen artwork, then center the complete uncropped image over it.
    background = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS)
    blur_radius = max(2, round(size[0] / 70))
    background = background.filter(ImageFilter.GaussianBlur(blur_radius))
    background = ImageEnhance.Brightness(background).enhance(0.55)

    foreground = ImageOps.contain(source, size, method=Image.Resampling.LANCZOS)
    x = (size[0] - foreground.width) // 2
    y = (size[1] - foreground.height) // 2
    background.paste(foreground, (x, y))
    return background.convert("RGBA")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()

    source = Image.open(args.source).convert("RGB")
    args.output_directory.mkdir(parents=True, exist_ok=True)

    rendered: dict[str, Image.Image] = {}
    for filename, size in SIZES.items():
        image = compose(source, size)
        image.save(args.output_directory / filename, pixel_format="DXT5")
        rendered[filename] = image

    if args.preview:
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        rendered["load_cyberpunk_bg.dds"].convert("RGB").resize(
            (960, 720), Image.Resampling.LANCZOS
        ).save(args.preview)

    print("Installed main-menu background textures.")


if __name__ == "__main__":
    main()
