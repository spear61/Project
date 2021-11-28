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
    if SMB_state.font == None:
        SMB_state.font = load_font('mario_text.TTF', 16)


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
    SMB_state.font.draw(0, 470, 'MARIO            WORLD     TIME', (255, 255, 255))
    SMB_state.font.draw(0,450, str(SMB_state.mario_score)+'         x' + str(SMB_state.mario_coin)+'      1-'+str(SMB_state.map_state),(255,255,255))
    if SMB_state.mario_life < 0:
        SMB_state.font.draw(175,240, 'GAME OVER', (255,255,255))
    else:
        SMB_state.font.draw(256,240,'x'+str(SMB_state.mario_life),(255,255,255))

    update_canvas()

def handle_events():
    events = get_events()

