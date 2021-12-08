from pico2d import *

import collision
import game_framework
import SMB_state
import mario
import world_start_state


class Stage_1_1:
    image = None

    def __init__(self):
        if Stage_1_1.image == None:
            Stage_1_1.image = load_image('bg_1_1.png')
        self.height = 50
        self.x = 0

    def update(self):
        if SMB_state.map_move is True and self.x < 6784 - 512:
            self.x += SMB_state.map_x_velocity * game_framework.frame_time
        if self.x > 6784 - 512:
            SMB_state.map_state = 2
            game_framework.change_state(world_start_state)

        pass

    def draw(self):
        self.image.clip_draw(int(self.x), 472, 512, 480, 256, 240)
        SMB_state.font.draw(0, 470, 'MARIO   COIN     WORLD     TIME', (255, 255, 255))
        SMB_state.font.draw(0, 450,
                            str(SMB_state.mario_score) + '         x' + str(SMB_state.mario_coin) + '      1-' + str(
                                SMB_state.map_state), (255, 255, 255))
        # draw_rectangle(*self.get_bb())

    # def get_bb(self):
    #     return 0, 0, 512 - 1, 50


class Stage_1_2:
    image = None

    def __init__(self):
        if Stage_1_2.image == None:
            Stage_1_2.image = load_image('stage_1_2_resample.png')
        self.height = 50
        self.x = 0
        self.stage_clear = 6408

    def update(self):
        if SMB_state.map_move is True and self.x < 6784 - 512:
            self.x += SMB_state.map_x_velocity * game_framework.frame_time
        if self.x > 6784 - 512:
            game_framework.change_state(world_start_state)
            SMB_state.map_state += 1
        pass

    def draw(self):
        self.image.clip_draw(int(self.x) + 522, 458, 512, 480, 256, 240)
        SMB_state.font.draw(0, 470, 'MARIO    COIN     WORLD     TIME', (255, 255, 255))
        SMB_state.font.draw(0, 450,
                            str(SMB_state.mario_score) + '         x' + str(SMB_state.mario_coin) + '      1-' + str(
                                SMB_state.map_state), (255, 255, 255))
        # draw_rectangle(*self.get_bb())

    # def get_bb(self):
    #     return 0, 0, 512 - 1, 50


class Floor:

    def __init__(self, x=10, width=100):
        self.height = 50
        self.width = width
        self.x = x
        pass

    def update(self):
        if SMB_state.map_move is True and self.x < 6784 - 512:
            self.x -= SMB_state.map_x_velocity * game_framework.frame_time

        # if collision.collide(self, SMB_state.mario):
        #     SMB_state.mario.y = clamp(82, SMB_state.mario.y, 480)
        #     # SMB_state.mario.x = clamp(0, SMB_state.mario.x, self.x - SMB_state.mario.front_width)

        # if collision.collide(self, SMB_state.bottom_mario) and SMB_state.mario.cur_state is not mario.JumpState:
        #     SMB_state.mario.collide_object = 'floor'
        #     SMB_state.mario.y = 82
        # elif collision.collide(self, SMB_state.bottom_mario) is False and SMB_state.mario.cur_state is not mario.JumpState:
        #     SMB_state.mario.y += SMB_state.mario.gravity_speed // -1 * game_framework.frame_time
        #     SMB_state.mario.collide_object = None
        #
        # if SMB_state.mario.cur_state is mario.JumpState and collision.collide(self, SMB_state.bottom_mario) is False:
        #     SMB_state.mario.collide_object = None
        # elif SMB_state.mario.cur_state is mario.JumpState and collision.collide(self, SMB_state.bottom_mario):
        #     SMB_state.mario.collide_object = 'floor'
        #     SMB_state.mario.y = clamp(82, SMB_state.mario.y, 480)
        if SMB_state.mario.cur_state != mario.JumpState:
            if collision.collide(SMB_state.mario, self):
                SMB_state.mario.y = clamp(self.height + SMB_state.mario.height // 2, SMB_state.mario.y, 480)
                SMB_state.mario.collide_object = 'floor'
            if collision.collide(SMB_state.mario, self) == False and SMB_state.mario.collide_object == None:
                SMB_state.mario.y += SMB_state.mario.gravity_speed // -1 * game_framework.frame_time
                print('falling')
            if SMB_state.mario.y < 32:
                SMB_state.mario.add_event(mario.GO_TO_GAMEOVER)
                SMB_state.mario.y = 96

    def draw(self):
        # debug_print('x :' + str(Game_over_zone.x) + '  gap:' + str(Game_over_zone.gap))
        # if self.x >= 0 and self.x <= 512 :
        # draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return int(self.x), 0, int(self.x + self.width), int(self.height)


class Floor_draw:
    image_1_1 = None

    def __init__(self):
        if Floor_draw.image_1_1 is None:
            Floor_draw.image_1_1 = load_image('floor_1_1.png')
        self.x = 0

    def update(self):
        if SMB_state.map_move == True and self.x < 6784 - 512:
            self.x += SMB_state.map_x_velocity * game_framework.frame_time

    def draw(self):
        self.image_1_1.clip_draw(int(self.x), 472, 512, 480, 256, 240)
