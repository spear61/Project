from pico2d import *
import game_framework
import SMB_state
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
            game_framework.change_state(world_start_state)
            SMB_state.map_state += 1
        pass

    def draw(self):
        # self.image.clip_draw(int(self.x), 472, 512, 480, 256, 240)
        SMB_state.font.draw(0, 470, 'MARIO            WORLD     TIME', (255, 255, 255))
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
        SMB_state.font.draw(0, 470, 'MARIO            WORLD     TIME', (255, 255, 255))
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
        if SMB_state.map_move == True and self.x < 6784 - 512:
            self.x -= SMB_state.map_x_velocity * game_framework.frame_time
        pass

    def draw(self):
        # debug_print('x :' + str(Game_over_zone.x) + '  gap:' + str(Game_over_zone.gap))
        # if self.x >= 0 and self.x <= 512 :
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x, 0, self.x + self.width, self.height


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


