from pico2d import *
import game_framework
import SMB_state
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

    def __init__(self, x = 896, y = -14):
        if Tunnel.image == None:
            Tunnel.image = load_image('tunnel.png')
        self.x, self.y = x, y

    def update(self):
        if SMB_state.map_move == True and self.x < 6784 - 512:
            self.x -= SMB_state.map_x_velocity * game_framework.frame_time
        pass

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 64, 128, self.x, self.y)
        draw_rectangle(*(self.get_bb()))

    def get_bb(self):
        return self.x, self.y, self.x + 64, self.y + 128
