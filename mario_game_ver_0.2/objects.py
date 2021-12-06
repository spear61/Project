from pico2d import *

import collision
import game_framework
import SMB_state
import mario
import world_start_state


class Block:
    image = None

    def __init__(self, x, y, prop, item):
        if Block.image == None:
            Block.image = load_image('blocks.png')
        self.x, self.y = x, y
        self.prop = prop
        self.item = item

    def update(self):
        pass

    def draw(self):
        if self.prop == 'question':
            self.image.clip_draw_to_origin(0, 96, 32, 32, self.x, self.y)
        elif self.prop == 'normal':
            self.image.clip_draw_to_origin(96, 96, 32, 32, self.x, self.y)
        elif self.prop == 'brick':
            self.image.clip_draw_to_origin(160, 96, 32, 32, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x, self.y, self.x + 32, self.y + 32


class Tunnel:
    image = None

    def __init__(self, x=896, y=-14):
        if Tunnel.image == None:
            Tunnel.image = load_image('tunnel.png')
        self.x, self.y = x, y
        self.width = 64

    def update(self):
        if SMB_state.map_move == True and self.x < 6784 - 512:
            self.x -= SMB_state.map_x_velocity * game_framework.frame_time

        if collision.collide(SMB_state.mario, self):
            if SMB_state.mario.x < self.x:
                # SMB_state.mario.x = clamp(0,SMB_state.mario.x, self.x - SMB_state.mario.front_width)
                SMB_state.mario.x = self.x - SMB_state.mario.front_width
            else:
                SMB_state.mario.x = clamp(self.x + self.width + SMB_state.mario.back_width, SMB_state.mario.x, 512)
        elif collision.collide(SMB_state.bottom_mario, self):
            # if SMB_state.mario.cur_state is mario.JumpState:
            if SMB_state.mario.jump_enable is False:
                SMB_state.mario.add_event(mario.TO_IDLE)
                SMB_state.mario.velocity = 0
                SMB_state.mario.jump_enable = False
            if SMB_state.mario.jump_enable is not True and SMB_state.mario.cur_state is not mario.JumpState:
                SMB_state.mario.y = self.y + 128 + SMB_state.mario.height // 2

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 64, 128, self.x, self.y)
        draw_rectangle(*(self.get_bb()))

    def get_bb(self):
        return self.x, self.y, self.x + 64, self.y + 128
