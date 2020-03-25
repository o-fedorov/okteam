"""Automation tasks.

See http://www.pyinvoke.org/ for details.
"""
from math import ceil
from pathlib import Path

from invoke import Exit, task


@task
def crop(ctx, path, nx=1, ny=4):
    """Crop a sprite sheet."""
    from PIL import Image

    path = Path(path)
    image = Image.open(path)
    step_x = ceil(image.width / nx)
    step_y = ceil(image.height / ny)

    for i, y in enumerate(range(0, image.height, step_y)):
        for j, x in enumerate(range(0, image.width, step_x)):
            cropped = image.crop(
                (x, y, min(x + step_x, image.width), min(y + step_y, image.height))
            )
            cropped_name = path.parent / f"{ path.stem }_{i}_{j}{ path.suffix }"
            print("Saving", cropped_name)
            cropped.save(cropped_name)


@task
def resize(ctx, path, width=None, height=None, output=None):
    """Resize all images in a directory."""
    from PIL import Image, UnidentifiedImageError

    if width is None and height is None:
        raise Exit("At least --with or --height is expected.")

    path = Path(path)
    output = (path / "resized") if output is None else Path(output)
    output.mkdir(parents=True, exist_ok=True)

    for image_path in path.glob("*"):
        if image_path.is_dir():
            continue

        try:
            image = Image.open(image_path)
        except UnidentifiedImageError:
            print("Skipping", image_path)
            continue

        if height is None:
            new_height = ceil(image.height * int(width) / image.width)
            new_width = int(width)
        elif width is None:
            new_width = ceil(image.width * int(height) / image.height)
            new_height = int(height)
        else:
            new_height = int(height)
            new_width = int(width)

        resized_name = output / image_path.name
        print("Saving", resized_name)
        image.resize((new_width, new_height)).save(resized_name)


@task
def build(ctx):
    """Package the game."""
    ctx.run("poetry export --format requirements.txt --output requirements.txt --without-hashes")
    try:
        version = ctx.run(f"poetry version").stdout.strip()
        name = "-".join(version.split())
        ctx.run(f"poetry run python ./create-upload.py { name }")
    finally:
        ctx.run("rm requirements.txt")


@task
def fmt(ctx):
    """Apply automatic code formatting."""
    ctx.run("poetry run isort -rc .")
    ctx.run("poetry run black .")
