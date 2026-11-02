
import pygame
import random
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 760
WORLD_W = 900
PANEL_X = WORLD_W
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ECOSYSTEM - A Living World")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 17)
SMALL = pygame.font.SysFont("arial", 13)
MEDIUM = pygame.font.SysFont("arial", 22, bold=True)
LARGE = pygame.font.SysFont("arial", 42, bold=True)

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

state = "menu"
paused = False
speed = 1
day = 1
day_timer = 0
weather = "Sunny"
season_index = 0
seasons = ["Spring", "Summer", "Autumn", "Winter"]
pollution = 0
event_message = "Your ecosystem is ready!"
event_timer = 240
selected_tool = "select"

plants = []
trees = []
rabbits = []
foxes = []
deer = []
birds = []
history = {"rabbits": [], "foxes": [], "deer": [], "plants": []}


def clamp(value, low, high):
    return max(low, min(high, value))


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def draw_text(surface, text, x, y, font=FONT, color=WHITE):
    surface.blit(font.render(str(text), True, color), (x, y))


def set_message(message):
    global event_message, event_timer
    event_message = message
    event_timer = 240


def random_world_position():
    return random.randint(25, WORLD_W - 25), random.randint(80, HEIGHT - 25)


class Plant:
    def __init__(self, x=None, y=None):
        if x is None or y is None:
            x, y = random_world_position()
        self.x = x
        self.y = y
        self.size = random.randint(4, 8)
        self.growth = 0

    def update(self):
        self.growth = min(1, self.growth + 0.002 * speed)

    def draw(self):
        size = max(2, int(self.size * self.growth))
        pygame.draw.circle(screen, LIGHT_GREEN, (int(self.x), int(self.y)), size)


class Tree:
    def __init__(self, x=None, y=None):
        if x is None or y is None:
            x, y = random_world_position()
        self.x = x
        self.y = y
        self.size = random.randint(13, 23)

    def draw(self):
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, BROWN, (x - 3, y, 6, 16))
        pygame.draw.circle(screen, DARK_GREEN, (x, y - 5), self.size)
        pygame.draw.circle(screen, GREEN, (x - 5, y - 10), self.size // 2)


class Animal:
    def __init__(self, x=None, y=None, color=WHITE, size=7, kind="animal"):
        if x is None or y is None:
            x, y = random_world_position()
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.size = size
        self.kind = kind
        self.energy = random.randint(60, 100)
        self.direction = random.random() * math.tau
        self.age = 0

    def update(self):
        self.age += speed
        self.energy -= 0.012 * speed

        if random.random() < 0.04:
            self.direction += random.uniform(-1, 1)

        self.x += math.cos(self.direction) * speed
        self.y += math.sin(self.direction) * speed

        if self.x < 15 or self.x > WORLD_W - 15:
            self.direction = math.pi - self.direction

        if self.y < 70 or self.y > HEIGHT - 15:
            self.direction = -self.direction

        self.x = clamp(self.x, 15, WORLD_W - 15)
        self.y = clamp(self.y, 70, HEIGHT - 15)

    def draw(self):
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, self.color, (x, y), self.size)

        if self.kind == "rabbit":
            pygame.draw.circle(screen, self.color, (x - 3, y - 8), 3)
            pygame.draw.circle(screen, self.color, (x + 3, y - 8), 3)
        elif self.kind == "fox":
            pygame.draw.polygon(screen, RED, [
                (x - 5, y - 4), (x, y - 10), (x + 5, y - 4)
            ])
        elif self.kind == "deer":
            pygame.draw.line(screen, BROWN, (x - 3, y - 5), (x - 6, y - 10), 2)
            pygame.draw.line(screen, BROWN, (x + 3, y - 5), (x + 6, y - 10), 2)
        elif self.kind == "bird":
            pygame.draw.circle(screen, YELLOW, (x + 2, y - 2), 2)


def make_animal(kind):
    settings = {
        "rabbit": (WHITE, 7),
        "fox": (RED, 9),
        "deer": (BROWN, 10),
        "bird": (BLUE, 5)
    }
    color, size = settings[kind]
    return Animal(color=color, size=size, kind=kind)


def reset_world():
    global plants, trees, rabbits, foxes, deer, birds
    global day, day_timer, weather, season_index, pollution
    global paused, history

    plants = [Plant() for _ in range(100)]
    trees = [Tree() for _ in range(18)]
    rabbits = [make_animal("rabbit") for _ in range(12)]
    foxes = [make_animal("fox") for _ in range(3)]
    deer = [make_animal("deer") for _ in range(5)]
    birds = [make_animal("bird") for _ in range(8)]

    day = 1
    day_timer = 0
    weather = "Sunny"
    season_index = 0
    pollution = 0
    paused = False
    history = {"rabbits": [], "foxes": [], "deer": [], "plants": []}
    set_message("A new ecosystem has begun!")


def draw_world():
    screen.fill(BG)

    # Grass patches
    for i in range(35):
        x = (i * 137 + 37) % WORLD_W
        y = (i * 83 + 100) % HEIGHT
        pygame.draw.circle(screen, (24, 42, 33), (x, y), 22)

    for tree in trees:
        tree.draw()

    for plant in plants:
        plant.draw()

    for animal_list in (rabbits, foxes, deer, birds):
        for animal in animal_list:
            animal.draw()

    # World border
    pygame.draw.line(screen, PANEL_LIGHT, (WORLD_W - 1, 0),
                     (WORLD_W - 1, HEIGHT), 3)


def draw_panel():
    pygame.draw.rect(screen, PANEL, (PANEL_X, 0, WIDTH - PANEL_X, HEIGHT))

    x = PANEL_X + 20
    y = 20

    draw_text(screen, "ECOSYSTEM", x, y, MEDIUM, LIGHT_GREEN)
    y += 35
    draw_text(screen, "A LIVING WORLD", x, y, SMALL, MUTED)
    y += 35

    draw_text(screen, f"Day: {day}", x, y, FONT)
    y += 27
    draw_text(screen, f"Season: {seasons[season_index]}", x, y)
    y += 27
    draw_text(screen, f"Weather: {weather}", x, y)
    y += 35

    pygame.draw.line(screen, PANEL_LIGHT, (x, y), (WIDTH - 20, y), 2)
    y += 15

    draw_text(screen, "POPULATION", x, y, MEDIUM, YELLOW)
    y += 32

    stats = [
        ("Plants", len(plants), LIGHT_GREEN),
        ("Trees", len(trees), GREEN),
        ("Rabbits", len(rabbits), WHITE),
        ("Foxes", len(foxes), RED),
        ("Deer", len(deer), BROWN),
        ("Birds", len(birds), BLUE)
    ]

    for name, count, color in stats:
        pygame.draw.circle(screen, color, (x + 5, y + 9), 5)
        draw_text(screen, f"{name}: {count}", x + 18, y)
        y += 25

    y += 10
    pygame.draw.line(screen, PANEL_LIGHT, (x, y), (WIDTH - 20, y), 2)
    y += 15

    draw_text(screen, "CONTROLS", x, y, MEDIUM, YELLOW)
    y += 32

    controls = [
        "SPACE - Pause / Resume",
        "1 - Add plants",
        "2 - Add rabbits",
        "3 - Add foxes",
        "4 - Add deer",
        "5 - Add trees",
        "6 - Add birds",
        "R - Rain",
        "N - New ecosystem",
        "+ / - - Simulation speed",
        "Click world to add selected",
        "ESC - Quit"
    ]

    for line in controls:
        draw_text(screen, line, x, y, SMALL, MUTED)
        y += 22

    y = HEIGHT - 55
    message = event_message[:27]
    draw_text(screen, message, x, y, SMALL, YELLOW)

    if paused:
        draw_text(screen, "PAUSED", x, y - 24, FONT, RED)


def add_selected(x, y):
    global pollution

    if x >= WORLD_W or y < 60:
        return

    if selected_tool == "plants":
        plants.append(Plant(x, y))
        set_message("A new plant was added!")
    elif selected_tool == "rabbits":
        rabbits.append(make_animal("rabbit"))
        rabbits[-1].x, rabbits[-1].y = x, y
        set_message("A rabbit joined the ecosystem!")
    elif selected_tool == "foxes":
        foxes.append(make_animal("fox"))
        foxes[-1].x, foxes[-1].y = x, y
        set_message("A fox joined the ecosystem!")
    elif selected_tool == "deer":
        deer.append(make_animal("deer"))
        deer[-1].x, deer[-1].y = x, y
        set_message("A deer joined the ecosystem!")
    elif selected_tool == "trees":
        trees.append(Tree(x, y))
        set_message("A tree was planted!")
    elif selected_tool == "birds":
        birds.append(make_animal("bird"))
        birds[-1].x, birds[-1].y = x, y
        set_message("A bird joined the ecosystem!")


def update_world():
    global day, day_timer, season_index, weather, event_timer

    if paused:
        return

    day_timer += 1

    if day_timer >= 600:
        day_timer = 0
        day += 1

        if day % 10 == 0:
            season_index = (season_index + 1) % len(seasons)
            set_message(f"Season changed to {seasons[season_index]}!")

        if random.random() < 0.35:
            weather = random.choice(["Sunny", "Rainy", "Cloudy"])
            set_message(f"The weather is now {weather.lower()}.")

    for plant in plants:
        plant.update()

    for animal_list in (rabbits, foxes, deer, birds):
        for animal in animal_list[:]:
            animal.update()
            if animal.energy <= 0:
                animal_list.remove(animal)

    # Animals need food to survive.
    for rabbit in rabbits[:]:
        nearby = next(
            (plant for plant in plants if distance(rabbit, plant) < 18),
            None
        )
        if nearby:
            plants.remove(nearby)
            rabbit.energy = min(100, rabbit.energy + 30)

    for animal in deer:
        if random.random() < 0.002 * speed and len(plants) < 250:
            plants.append(Plant())

    # Animals reproduce when the ecosystem has enough food.
    if len(rabbits) < 60 and plants and random.random() < 0.003 * speed:
        rabbits.append(make_animal("rabbit"))

    if len(foxes) < 20 and len(rabbits) > 5:
        if random.random() < 0.0008 * speed:
            foxes.append(make_animal("fox"))

    if len(deer) < 30 and plants and random.random() < 0.0005 * speed:
        deer.append(make_animal("deer"))

    if len(birds) < 40 and random.random() < 0.0008 * speed:
        birds.append(make_animal("bird"))

    # Foxes hunt nearby rabbits.
    for fox in foxes:
        target = next(
            (rabbit for rabbit in rabbits if distance(fox, rabbit) < 12),
            None
        )
        if target:
            rabbits.remove(target)
            fox.energy = min(100, fox.energy + 35)

    # Rain encourages plant growth.
    if weather == "Rainy" and len(plants) < 250:
        if random.random() < 0.03 * speed:
            plants.append(Plant())

    if len(plants) < 10 and random.random() < 0.04:
        plants.append(Plant())

    if event_timer > 0:
        event_timer -= 1


def draw_menu():
    screen.fill(BG)

    for i in range(60):
        x = (i * 173 + 40) % WIDTH
        y = (i * 97 + 30) % HEIGHT
        pygame.draw.circle(screen, (32, 55, 39), (x, y), 3)

    title = LARGE.render("ECOSYSTEM", True, LIGHT_GREEN)
    subtitle = MEDIUM.render("A LIVING WORLD", True, WHITE)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, 230)))
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 285)))

    draw_text(screen, "Watch nature grow, survive, and change.", 390, 340,
              FONT, MUTED)

    button = pygame.Rect(455, 405, 290, 60)
    pygame.draw.rect(screen, GREEN, button, border_radius=10)
    label = MEDIUM.render("START SIMULATION", True, WHITE)
    screen.blit(label, label.get_rect(center=button.center))

    draw_text(screen, "Click START or press ENTER", 460, 490, FONT, MUTED)
    draw_text(screen, "ESC to quit", 540, 520, SMALL, MUTED)

    return button


running = True
menu_button = pygame.Rect(455, 405, 290, 60)

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif state == "menu":
                if event.key == pygame.K_RETURN:
                    reset_world()
                    state = "game"

            else:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                elif event.key == pygame.K_n:
                    reset_world()

                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS,
                                   pygame.K_KP_PLUS):
                    speed = min(5, speed + 1)

                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    speed = max(1, speed - 1)

                elif event.key == pygame.K_1:
                    selected_tool = "plants"
                    set_message("Selected: plants")
                elif event.key == pygame.K_2:
                    selected_tool = "rabbits"
                    set_message("Selected: rabbits")
                elif event.key == pygame.K_3:
                    selected_tool = "foxes"
                    set_message("Selected: foxes")
                elif event.key == pygame.K_4:
                    selected_tool = "deer"
                    set_message("Selected: deer")
                elif event.key == pygame.K_5:
                    selected_tool = "trees"
                    set_message("Selected: trees")
                elif event.key == pygame.K_6:
                    selected_tool = "birds"
                    set_message("Selected: birds")
                elif event.key == pygame.K_r:
                    weather = "Rainy"
                    set_message("Rain is helping the plants grow!")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "menu":
                if menu_button.collidepoint(event.pos):
                    reset_world()
                    state = "game"
            else:
                add_selected(*event.pos)

    if state == "menu":
        menu_button = draw_menu()
    else:
        update_world()
        draw_world()
        draw_panel()

        draw_text(screen, f"Speed: {speed}x", 15, 15, SMALL, YELLOW)

        if paused:
            draw_text(screen, "PAUSED", 15, 38, MEDIUM, RED)

    pygame.display.flip()

pygame.quit()
sys.exit()
