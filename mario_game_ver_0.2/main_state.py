import random
import json
import os

from pico2d import *
import game_framework
import game_world
import logo_state
import world_start_state
import SMB_state

from mario import Mario
from gumba import Gumba
from piranha_plant import Piranha_plant
from stage import Stage_1_1, Stage_1_2, Floor


name = "MainState"

mario = None
gumba = None
piranha_plant = None
stage_1_1 = None
stage_1_2 = None
floors = []


def enter():
    if SMB_state.font == None:
        SMB_state.font = load_font('mario_text.TTF', 16)
    global mario
    mario = Mario()
    game_world.add_object(mario, 1)

    global gumba
    gumba = Gumba()
    game_world.add_object(gumba, 1)

    global piranha_plant
    piranha_plant = Piranha_plant()
    game_world.add_object(piranha_plant, 1)

    if SMB_state.map_state == 1:
        global stage_1_1
        stage_1_1 = Stage_1_1()
        game_world.add_object(stage_1_1, 0)

    if SMB_state.map_state == 2:
        global stage_1_2
        stage_1_2 = Stage_1_2()
        game_world.add_object(stage_1_2, 0)

    global floor
    floors = [Floor() for i in range(3)]
    if SMB_state.map_state == 1:
        floors[0].x = 2252
        floors[0].gap = 66
        floors[1].x = 2807
        floors[1].gap = 98
        floors[2].x = 4994
        floors[2].gap = 65
    game_world.add_objects(floors, 1)




def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DELETE:
            game_framework.change_state(world_start_state)
        else:
            mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    # if not collide(mario, grass):
    #     mario.y += mario.gravity_speed // -2 * (mario.timer ** 2)
    for game_over_zone in floors:
        if collide(game_over_zone, mario):
            game_framework.change_state(world_start_state)
            SMB_state.mario_life -= 1
            if SMB_state.mario_life < 0:
                game_framework.change_state(world_start_state)
            pass
    # delay(0.013)
    # fill here


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
