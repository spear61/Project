import random
import json
import os

from pico2d import *

name = "MainState"

# mario = None
# platform = None
# map = None

map_location = 800
enemy_move = 0
map_update_a = 0
map_update_b = 0


class Map:
    def __init__(self):
        self.image = load_image('bg-1-1.png')
        self.map_x = 800

    def update(self):
        global map_location
        global enemy_move
        if map_update_a == 1 and map_update_b == 1:
            self.map_x += 10
            map_location += 10
            enemy_move = 10
        else:
            enemy_move = 0
        if self.map_x > 3392:
            self.map_x = 3392

    def draw(self):
        self.image.clip_draw(self.map_x - 800, 236, 800, 600, 400, 300)


class Mario:
    def __init__(self):
        self.image = load_image('characters.png')
        self.x = 400
        self.y = 80
        self.frame = 0

    def update(self):
        global direction
        global map_update_a
        if direction == 0:
            self.x += 10
        elif direction == 2:
            self.x -= 10
        self.frame = (self.frame + 1) % 3
        if self.x > 400:
            self.x = 400
            map_update_a = 1
        else:
            map_update_a = 0
        if self.x <= 20:
            self.x = 20

    def draw(self):
        if direction == 0:
            self.image.clip_draw(self.frame * 18 + 293, 365, 18, 34, self.x, self.y)
        elif direction == 1:
            self.image.clip_draw(255, 365, 18, 34, self.x, self.y)
        elif direction == 2:
            self.image.clip_draw(self.frame * 18 + 164, 365, 18, 34, self.x, self.y)
        elif direction == 3:
            self.image.clip_draw(237, 365, 18, 34, self.x, self.y)


class Gumba:
    def __init__(self):
        self.image = load_image('characters.png')
        self.spawn = 500  # random.randint(0, 3392)
        self.x = self.spawn;
        self.y = 70;
        self.frame = 0;

    def update(self):
        self.frame = (self.frame + 1) % 2
        if map_location < 3392:
            self.x = self.x - enemy_move

    def draw(self):
        global map_location
        if (self.spawn <= map_location) and (self.spawn + 800 >= map_location):
            self.image.clip_draw(self.frame * 18 + 293, 194, 18, 20, self.x, self.y)


class Turtle:
    def __init__(self):
        self.image = load_image('characters.png')
        self.spawn = 520  # random.randint(0, 3392)
        self.x = self.spawn;
        self.y = 76;
        self.frame = 0;

    def update(self):
        self.frame = (self.frame + 1) % 2
        if map_location < 3392:
            self.x = self.x - enemy_move

    def draw(self):
        global map_location
        if (self.spawn <= map_location) and (self.spawn + 800 >= map_location):
            self.image.clip_draw(self.frame * 18 + 293, 171, 18, 22, self.x, self.y)


class Flower:
    def __init__(self):
        self.image = load_image('characters.png')
        self.spawn = 540  # random.randint(0, 3392)
        self.x = self.spawn;
        self.y = 74;
        self.frame = 0;

    def update(self):
        self.frame = (self.frame + 1) % 2
        if map_location < 3392:
            self.x = self.x - enemy_move

    def draw(self):
        global map_location
        if (self.spawn <= map_location) and (self.spawn + 800 >= map_location):
            self.image.clip_draw(self.frame * 19 + 123, 194, 19, 25, self.x, self.y)


def handle_events():
    global running
    global direction
    global map_update_b
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            direction = 0
            map_update_b = 1
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            direction = 1
            map_update_b = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            direction = 2
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            direction = 3


open_canvas()
mario = Mario()
map = Map()
# gumbas = [Gumba() for i in range(10)]
# turtles = [Turtle() for i in range(10)]
gumba = Gumba()
turtle = Turtle()
flower = Flower()
running = True
direction = 1

# game main loop code

while running:
    delay(0.05)
    handle_events()

    # Game logic
    mario.update()
    map.update()
    gumba.update()
    turtle.update()
    flower.update()
    # for Gumba in gumbas:
    #     Gumba.update()
    # for Turtle in turtles:
    #     Turtle.update()
    # Game drawing
    clear_canvas()
    map.draw()
    mario.draw()
    gumba.draw()
    turtle.draw()
    flower.draw()
    # for Gumba in gumbas:
    #     Gumba.draw()
    # for Turtle in turtles:
    #     Turtle.draw()
    update_canvas()

# finalization code
