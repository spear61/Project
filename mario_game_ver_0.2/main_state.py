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
from stage import Stage_1_1, Stage_1_2, Game_over_zone

name = "MainState"

mario = None
stage_1_1 = None
stage_1_2 = None
game_over_zones = []


def enter():
    if SMB_state.font == None:
        SMB_state.font = load_font('mario_text.TTF', 16)
    global mario
    mario = Mario()
    game_world.add_object(mario, 1)

    if SMB_state.map_state == 1:
        global stage_1_1
        stage_1_1 = Stage_1_1()
        game_world.add_object(stage_1_1, 0)

    if SMB_state.map_state == 2:
        global stage_1_2
        stage_1_2 = Stage_1_2()
        game_world.add_object(stage_1_2, 0)

    global game_over_zones
    game_over_zones = [Game_over_zone() for i in range(3)]
    if SMB_state.map_state == 1:
        game_over_zones[0].x = 2252
        game_over_zones[0].gap = 66
        game_over_zones[1].x = 2807
        game_over_zones[1].gap = 98
        game_over_zones[2].x = 4994
        game_over_zones[2].gap = 65
    game_world.add_objects(game_over_zones, 1)




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
    for game_over_zone in game_over_zones:
        if collide(game_over_zone, mario):
            game_framework.change_state(world_start_state)
            SMB_state.mario_life -= 1
            if SMB_state.mario_life < 0:
                game_framework.change_state(world_start_state)
            pass
    delay(0.013)
    # fill here


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
