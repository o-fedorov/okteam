from . import tsurka
from .settings import BACKGROUND, HEIGHT, TITLE, WIDTH


def draw():
    screen.fill(BACKGROUND)
    tsurka.draw()


def update(dt):
    tsurka.update(dt)
