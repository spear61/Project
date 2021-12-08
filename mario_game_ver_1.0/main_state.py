import random
import json
import os

from pico2d import *
import game_framework
import game_world
import logo_state
import mario
import world_start_state
import SMB_state

from mario import Mario, Bottom_mario
    # Top_mario, Bottom_mario
from gumba import Gumba
from koopa_troopa import Koopa_troopa
from piranha_plant import Piranha_plant
from stage import Stage_1_1, Stage_1_2, Floor, Floor_draw
from objects import Tunnel,Block

name = "MainState"


def enter():
    if SMB_state.font == None:
        SMB_state.font = load_font('mario_text.TTF', 16)



    # SMB_state.top_mario = Top_mario()
    # game_world.add_object(SMB_state.top_mario, 1)
    #


    if SMB_state.map_state == 1:
        with open('block_1_1.json', 'r') as f:
            block_data_list = json.load(f)
        for data in block_data_list:
            block = Block(data['x'],data['y'],data['prop'],data['item'])
            game_world.add_object(block, 1)
        with open('tunnel_1_1.json', 'r') as f:
            tunnel_data_list = json.load(f)
        for data in tunnel_data_list:
            tunnel = Tunnel(data['x'], data['y'])
            game_world.add_object(tunnel, 1)
        SMB_state.stage_1_1 = Stage_1_1()
        game_world.add_object(SMB_state.stage_1_1, 0)
        with open('floor_1_1.json', 'r') as f:
            floor_data_list = json.load(f)
        for data in floor_data_list:
            floor = Floor(data['x'], data['width'])
            game_world.add_object(floor, 1)
        SMB_state.floor_draw = Floor_draw()
        game_world.add_object(SMB_state.floor_draw, 1)
        # SMB_state.gumba = Gumba()
        # game_world.add_object(SMB_state.gumba, 1)
        with open('gumba_1_1.json', 'r') as f:
            gumba_data_list = json.load(f)
        for data in gumba_data_list:
            gumba = Gumba(data['x'], data['y'], data['dir'])
            game_world.add_object(gumba, 0)
        # SMB_state.koopa_troopa = Koopa_troopa()
        # game_world.add_object(SMB_state.koopa_troopa, 1)
        # with open('troopa_1_1.json', 'r') as f:
        #     troopa_data_list = json.load(f)
        # for data in troopa_data_list:
        #     koopa_troopa = Koopa_troopa(data['x'], data['y'], data['dir'])
        #     game_world.add_object(koopa_troopa, 1)
        # # SMB_state.piranha_plant = Piranha_plant()
        # # game_world.add_object(SMB_state.piranha_plant, 1)
        # with open('piranha_1_1.json', 'r') as f:
        #     piranha_data_list = json.load(f)
        # for data in piranha_data_list:
        #     piranha_plant = Piranha_plant(data['x'], data['y'])
        #     game_world.add_object(piranha_plant, 1)

    if SMB_state.map_state == 2:
        SMB_state.stage_1_2 = Stage_1_2()
        game_world.add_object(SMB_state.stage_1_2, 0)

    SMB_state.mario = Mario()
    game_world.add_object(SMB_state.mario, 1)
    SMB_state.bottom_mario = Bottom_mario()
    game_world.add_object(SMB_state.bottom_mario, 1)




def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DELETE:
            game_framework.change_state(world_start_state)
        elif event == SDL_KEYDOWN and event.key == SDLK_BACKSPACE:
            SMB_state.mario.add_event(mario.GameOverState)
        else:
            SMB_state.mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    # if not collide(mario, grass):
    #     mario.y += mario.gravity_speed // -2 * (mario.timer ** 2)
    # for Floor in SMB_state.floors:
    #     if collide(Floor, SMB_state.mario):
    #         game_framework.change_state(world_start_state)
    #         SMB_state.mario_life -= 1
    #         if SMB_state.mario_life < 0:
    #             game_framework.change_state(world_start_state)
    #         pass
    # delay(0.013)
    # fill here


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
