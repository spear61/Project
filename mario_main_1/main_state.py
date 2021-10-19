import random
import json
import os

from pico2d import *

name = "MainState"

#mario = None
#platform = None
#map = None

map_update_a = 0
map_update_b = 0


class Map:
    def __init__(self):
        self.image = load_image('bg-1-1.png')
        self.map_x = 0

    def update(self):
        if map_update_a == 1 and map_update_b == 1:
            self.map_x += 10
        if self.map_x > 2592:
            self.map_x = 2592

    def draw(self):
        self.image.clip_draw(self.map_x, 236, 800, 600, 400, 300)


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
            self.image.clip_draw(self.frame * 18+293, 365, 18, 34, self.x, self.y)
        elif direction == 1:
            self.image.clip_draw(255, 365, 18, 34, self.x, self.y)
        elif direction == 2:
            self.image.clip_draw(self.frame * 18+164, 365, 18, 34, self.x, self.y)
        elif direction == 3:
            self.image.clip_draw(237, 365, 18, 34, self.x, self.y)


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
running = True
direction = 1

# game main loop code

while running:
    delay(0.05)
    handle_events()

    # Game logic
    mario.update()
    map.update()
    # Game drawing
    clear_canvas()
    map.draw()
    mario.draw()
    update_canvas()

# finalization code
