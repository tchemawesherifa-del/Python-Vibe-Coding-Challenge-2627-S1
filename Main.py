import pygame
import random
import math
import sys

# ============================================================
# ECOSYSTEM: A LIVING WORLD
# One-file Python/Pygame simulation. No extra image files needed.
# ============================================================

pygame.init()

WIDTH, HEIGHT = 1200, 760
WORLD_W = 900
PANEL_X = WORLD_W
PANEL_W = WIDTH - WORLD_W
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ECOSYSTEM - A Living World")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 17)
SMALL = pygame.font.SysFont("arial", 13)
MEDIUM = pygame.font.SysFont("arial", 22, bold=True)
LARGE = pygame.font.SysFont("arial", 42, bold=True)

# Colours
BG = (19, 31, 29)
PANEL = (25, 39, 36)
PANEL_LIGHT = (36, 54, 47)
WHITE = (239, 241, 226)
MUTED = (166, 184, 166)
GREEN = (75, 137, 72)
DARK_GREEN = (43, 91, 53)
LIGHT_GREEN = (126, 178, 83)
YELLOW = (244, 207, 105)
BLUE = (104, 174, 220)
RED = (215, 100, 79)
BROWN = (111, 78, 52)

# Simulation settings
state = "menu"
paused = False
speed = 1
day = 1
day_timer = 0
weather = "Sunny"
season_index = 0
seasons = ["Spring", "Summer", "Autumn", "Winter"]
pollution = 0
rain_timer = 0
event_message = "Your ecosystem is ready!"
event_timer = 300
selected_tool = "select"
show_help = False

plants = []
trees = []
rabbits = []
foxes = []
deer = []
birds = []
particles = []
history = {"rabbits": [], "foxes": [], "deer": [], "plants": []}
history_timer = 0

# Small helper functions
def clamp(value, low, high):
    return max(low, min(high, value))


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def draw_text(surface, text, x, y, font=FONT, color=WHITE):
    image = font.render(str(text), True, color)
    surface.blit(image, (x, y))


def set_message(message):
    global event_message, event_timer
    event_message = message
    event_timer = 240


def random_world_position(margin=25):
    return (random.randint(margin, WORLD_W - margin),
            random.randint(65, HEIGHT - 25))


class Plant:
    def __init__(self, x=None, y=None, kind=None):
        if x is None or y is None:
            x, y = random_world_position()