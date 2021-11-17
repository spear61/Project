from pico2d import *
import game_framework
import SMB_state
import world_start_state

class Stage_1_1:

    image = None

    def __init__(self):
        if Stage_1_1.image == None:
            Stage_1_1.image = load_image('stage_1_1_resample.png')
        self.height = 50
        self.x = 0
        self.stage_clear = 6408

    def update(self):
        if SMB_state.map_move is True and self.x < 6920 - 512:
            self.x += SMB_state.map_x_velocity * game_framework.frame_time
        if self.x > 6920 - 512:
            game_framework.change_state(world_start_state)
            SMB_state.map_state += 1
        pass

    def draw(self):
        self.image.clip_draw(int(self.x), 0, 512, 480, 256, 240)
        debug_print('map_x :' + str(self.x))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 0, 512 - 1, 50

class Stage_1_2:

    image = None

    def __init__(self):
        if Stage_1_2.image == None:
            Stage_1_2.image = load_image('stage_1_2_resample.png')
        self.height = 50
        self.x = 0
        self.stage_clear = 6408

    def update(self):
        if SMB_state.map_move is True and self.x < 5666 - 522:
            self.x += SMB_state.map_x_velocity * game_framework.frame_time
        if self.x > 5666 - 522:
            game_framework.change_state(world_start_state)
            SMB_state.map_state += 1
        pass

    def draw(self):
        self.image.clip_draw(int(self.x)+522, 458, 512, 480, 256, 240)
        debug_print('map_x :' + str(self.x))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 0, 512 - 1, 50

class Game_over_zone:

    def __init__(self):
        self.x = -10
        self.gap = 0
        pass

    def update(self):
        if SMB_state.map_move == True :
            self.x -= SMB_state.map_x_velocity * game_framework.frame_time
        pass

    def draw(self):
        # debug_print('x :' + str(Game_over_zone.x) + '  gap:' + str(Game_over_zone.gap))
        # if self.x >= 0 and self.x <= 512 :
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x, 0, self.x + self.gap, 50 + 20


