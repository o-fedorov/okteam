from pgzero.builtins import Actor

from .settings import BACKGROUND, HEIGHT, TITLE, WIDTH

alice = Actor("walk0")
alice.midright = (WIDTH, HEIGHT / 2)


def draw():
    screen.fill(BACKGROUND)
    alice.draw()
