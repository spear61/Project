from pico2d import *

import SMB_state
import game_framework
import game_world
import logo_state

import main_state

name = "WorldStartState"
image = None
logo_time = 0.0


def enter():
    global image
    image = load_image('world_start_image.png')


def exit():
    global image
    del (image)


def update():
    global logo_time

    if (logo_time > 1.5):
        logo_time = 0
        if SMB_state.mario_life < 0:
            SMB_state.mario_life = 1
            game_framework.change_state(logo_state)
        else:
            game_framework.change_state(main_state)

    logo_time += game_framework.frame_time


def draw():
    global image

    clear_canvas()
    image.draw(256, 240)
    if SMB_state.mario_life < 0:
        debug_print('   GAME OVER    ')
    else:
        debug_print('   stage : 1 - ' + str(SMB_state.map_state) + '    life : ' + str(SMB_state.mario_life))
    update_canvas()

def handle_events():
    events = get_events()

