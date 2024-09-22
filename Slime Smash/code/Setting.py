import pygame
import os

SCALAR = 2
SCREEN_WIDTH = 480 * SCALAR
SCREEN_HEIGHT = 360 * SCALAR
SCREEN_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

GROUND_Y = SCREEN_HEIGHT - 200
GRAVITY = 2500

if os.path.exists("Highscore.txt"):
    with open("Highscore.txt", "r") as file:
        HIGHSCORE = int(file.read())
else:
    HIGHSCORE = 0