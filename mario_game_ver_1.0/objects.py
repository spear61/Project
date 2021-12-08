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
        self.width = 32

    def update(self):
        if SMB_state.map_move == True and self.x < 6784 - 512:
            self.x -= SMB_state.map_x_velocity * game_framework.frame_time
        # if collision.collide(SMB_state.mario, self):
        #     if SMB_state.mario.x < self.x:
        #         # SMB_state.mario.x = clamp(0,SMB_state.mario.x, self.x - SMB_state.mario.front_width)
        #         SMB_state.mario.x = self.x - SMB_state.mario.front_width
        #     else:
        #         SMB_state.mario.x = clamp(self.x + self.width + SMB_state.mario.back_width, SMB_state.mario.x, 512)
        # elif collision.collide(SMB_state.bottom_mario, self):
        #     # if SMB_state.mario.cur_state is mario.JumpState:
        #     if SMB_state.mario.jump_enable is True:
        #         SMB_state.mario.add_event(mario.TO_IDLE)
        #         SMB_state.mario.velocity = 0
        #         SMB_state.mario.jump_enable = False
        #         SMB_state.mario_collide_object = 'tunnel'
        #     if SMB_state.mario.jump_enable is False and SMB_state.mario.cur_state is not mario.JumpState:
        #         SMB_state.mario.y = self.y + 16 + SMB_state.mario.height // 2
        if SMB_state.mario.y > self.y + 32 and collision.collide(SMB_state.bottom_mario, self):
            SMB_state.mario.y = clamp(self.y + 32 + SMB_state.mario.height // 2, SMB_state.mario.y, 480)
            SMB_state.mario.collide_object = 'block'
            if SMB_state.mario.last_state == 'Run' or SMB_state.mario.last_state == 'RunDash':
                SMB_state.mario.add_event(mario.TO_RUN)
            elif SMB_state.mario.last_state == 'Dash':
                SMB_state.mario.add_event(mario.TO_DASH)
            elif SMB_state.mario.last_state == 'Idle' or SMB_state.mario.last_state == 'IdleDash':
                SMB_state.mario.add_event(mario.TO_IDLE)
                SMB_state.mario.velocity = 0
        if collision.collide(SMB_state.mario, self) and SMB_state.mario.y < self.y + 32:
            if SMB_state.mario.x < self.x:
                # SMB_state.mario.x = clamp(0,SMB_state.mario.x, self.x - SMB_state.mario.front_width)
                SMB_state.mario.x = self.x - SMB_state.mario.front_width
            else:
                SMB_state.mario.x = clamp(self.x + self.width + SMB_state.mario.back_width, SMB_state.mario.x, 512)
        pass

    def draw(self):
        if self.prop == 'question':
            self.image.clip_draw_to_origin(0, 96, 32, 32, self.x, self.y)
        elif self.prop == 'normal':
            self.image.clip_draw_to_origin(96, 96, 32, 32, self.x, self.y)
        elif self.prop == 'brick':
            self.image.clip_draw_to_origin(160, 96, 32, 32, self.x, self.y)
        elif self.prop == 'stair':
            self.image.clip_draw_to_origin(320, 0, 32, 32, self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x, self.y, self.x + 32, self.y + 32


class Tunnel:
    image = None

    def __init__(self, x=896, y=-14):
        if Tunnel.image == None:
            Tunnel.image = load_image('tunnel.png')
        self.x, self.y = x, y
        self.height = 128
        self.width = 64

    def update(self):
        if SMB_state.map_move == True and self.x < 6784 - 512:
            self.x -= SMB_state.map_x_velocity * game_framework.frame_time

        # if collision.collide(SMB_state.mario, self):
        #     if SMB_state.mario.x < self.x:
        #         # SMB_state.mario.x = clamp(0,SMB_state.mario.x, self.x - SMB_state.mario.front_width)
        #         SMB_state.mario.x = self.x - SMB_state.mario.front_width
        #     else:
        #         SMB_state.mario.x = clamp(self.x + self.width + SMB_state.mario.back_width, SMB_state.mario.x, 512)
        # elif collision.collide(SMB_state.bottom_mario, self):
        #     # if SMB_state.mario.cur_state is mario.JumpState:
        #     if SMB_state.mario.jump_enable is True:
        #         SMB_state.mario.add_event(mario.TO_IDLE)
        #         SMB_state.mario.velocity = 0
        #         SMB_state.mario.jump_enable = False
        #         SMB_state.mario_collide_object = 'tunnel'
        #     if SMB_state.mario.jump_enable is False and SMB_state.mario.cur_state is not mario.JumpState:
        #         SMB_state.mario.y = self.y + 128 + SMB_state.mario.height // 2

        # if collision.collide(SMB_state.mario, self) == 'bottom' and SMB_state.mario.cur_state == mario.JumpState:
        #     SMB_state.mario.collide_object = 'tunnel'
        #     if SMB_state.mario.last_state == 'Run' or SMB_state.mario.last_state == 'RunDash':
        #         SMB_state.mario.add_event(mario.TO_RUN)
        #     elif SMB_state.mario.last_state == 'Dash':
        #         SMB_state.mario.add_event(mario.TO_DASH)
        #     elif SMB_state.mario.last_state == 'Idle' or SMB_state.mario.last_state == 'IdleDash':
        #         SMB_state.mario.add_event(mario.TO_IDLE)
        #         SMB_state.mario.velocity = 0
        # if SMB_state.mario.cur_state != mario.JumpState and SMB_state.mario.collide_object == 'floor':
        #     if collision.collide(SMB_state.mario, self) == 'right':
        #         SMB_state.mario.x = self.x - SMB_state.mario.front_width
        #     elif collision.collide(SMB_state.mario, self) == 'left':
        #         SMB_state.mario.x = self.x + SMB_state.mario.back_width
            # elif collision.collide(SMB_state.mario, self) == 'top':
            #     SMB_state.mario.y = clamp(0, SMB_state.mario.y, self.y)
            # if SMB_state.mario.collide_object == 'tunnel':
        if SMB_state.mario.y > self.y + 128 and collision.collide(SMB_state.mario, self) and SMB_state.mario.collide_object != 'tunnel' :
            SMB_state.mario.y = clamp(self.y + 128 + SMB_state.mario.height // 2, SMB_state.mario.y, 480)
            SMB_state.mario.collide_object = 'tunnel'
            if SMB_state.mario.last_state == 'Run' or SMB_state.mario.last_state == 'RunDash':
                SMB_state.mario.add_event(mario.TO_RUN)
            elif SMB_state.mario.last_state == 'Dash':
                SMB_state.mario.add_event(mario.TO_DASH)
            elif SMB_state.mario.last_state == 'Idle' or SMB_state.mario.last_state == 'IdleDash':
                SMB_state.mario.add_event(mario.TO_IDLE)
                SMB_state.mario.velocity = 0
        if collision.collide(SMB_state.mario, self) and SMB_state.mario.y < self.y+ 128:
            if SMB_state.mario.x < self.x:
                # SMB_state.mario.x = clamp(0,SMB_state.mario.x, self.x - SMB_state.mario.front_width)
                SMB_state.mario.x = self.x - SMB_state.mario.front_width
            else:
                SMB_state.mario.x = clamp(self.x + self.width + SMB_state.mario.back_width, SMB_state.mario.x, 512)



    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 64, 128, self.x, self.y)
        # draw_rectangle(*(self.get_bb()))

    def get_bb(self):
        return self.x, self.y, self.x + 64, self.y + 128
