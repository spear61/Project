from pico2d import *
import game_framework
import game_world

import world_start_state

name = "LogoState"
image = None



def enter():
    global image
    image = load_image('SMB_Title_512.png')


def exit():
    global image
    del (image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_state(world_start_state)


def update():
    pass


def draw():
    global image
    clear_canvas()
    image.draw(256, 240)
    update_canvas()
