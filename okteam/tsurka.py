from typing import Tuple

from pgzero.builtins import Actor
from pygame import Vector2

from .settings import ANIMATION_SPEED, HEIGHT, SPEED, WALK_IMAGES, WIDTH

_TIME = 0.0

ALL = {}
X = Vector2(1, 0)
Y = Vector2(0, 1)


def add(direction: Tuple[int, int]):
    actor = Actor(WALK_IMAGES[0])
    ALL[actor] = Vector2(direction)
    return actor


add((1, 0)).midright = (WIDTH, HEIGHT / 2)
add((0, 1)).midbottom = (WIDTH / 2, HEIGHT)


def draw():
    for actor in ALL:
        actor.draw()


def update(dt):
    global _TIME
    _TIME += dt

    for actor in ALL:
        update_one(actor, dt)


def update_one(actor, dt):
    image_num = int(_TIME * ANIMATION_SPEED) % len(WALK_IMAGES)
    actor.image = WALK_IMAGES[image_num]
    if not image_num:
        return

    direction = ALL[actor]
    delta = direction * SPEED * dt

    if actor.left + delta.x <= 0 or actor.right + delta.x >= WIDTH:
        ALL[actor] = direction.reflect(X)
        delta = delta.reflect(X)

    if actor.top + delta.y <= 0 or actor.bottom + delta.y >= HEIGHT:
        ALL[actor] = direction.reflect(Y)
        delta = delta.reflect(Y)

    actor.x += delta.x
    actor.y += delta.y
