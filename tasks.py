"""Automation tasks.

See http://www.pyinvoke.org/ for details.
"""
from math import ceil
from pathlib import Path

from invoke import task


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
