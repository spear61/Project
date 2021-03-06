import math
import game_framework
import game_world
import SMB_state
from pico2d import *

import main_state
import world_start_state
from ball import Ball
from collision import collide

history = []

# mario Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Mario Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, DASH_TIMER, DEBUG_KEY, JUMP, TO_IDLE, TO_RUN, TO_DASH, SPACE, GO_TO_GAMEOVER = range(
    14)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SHIFT_DOWN', 'SHIFT_UP', 'DASH_TIMER',
              'DEBUG_KEY', 'JUMP', 'TO_IDLE', 'TO_RUN', 'TO_DASH', 'SPACE', 'GO_TO_GAMEOVER']

key_event_table = {
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP,

    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,

    (SDL_KEYDOWN, SDLK_UP): JUMP,

    (SDL_KEYDOWN, SDLK_v): DEBUG_KEY,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE

}


# Boy States

class IdleState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

        mario.last_state = 'Idle'

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()
        pass

    def do(mario):
        SMB_state.map_move = False
        # if mario.collide_object == 'floor':
        #     SMB_state.mario.y = 50 + SMB_state.mario.height // 2
        mario.y = clamp(32, mario.y, 480)

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(0, 0, 40, 64, mario.x, mario.y)
        else:
            mario.image.clip_draw(0, 64, 40, 64, mario.x, mario.y)


class RunState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        if event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        if event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        if event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

        mario.dir = clamp(-1, mario.velocity, 1)
        mario.last_state = 'Run'
        mario.timer = 0
        # fill here
        pass

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        mario.x += mario.velocity * game_framework.frame_time

        # if mario.collide_object == 'floor':
        #     SMB_state.mario.y = 50 + SMB_state.mario.height // 2

        if mario.x >= 255:
            SMB_state.map_x_velocity = RUN_SPEED_PPS
            SMB_state.map_move = True
        else:
            SMB_state.map_x_velocity = 0
            SMB_state.map_move = False

        mario.x = clamp(16, mario.x, 256)
        mario.y = clamp(32, mario.y, 480)

    @staticmethod
    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame + 1) * 40, 0, 40, 64, mario.x, mario.y)
        else:
            mario.image.clip_draw(int(mario.frame + 1) * 40, 64, 40, 64, mario.x, mario.y)


class DashState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        if event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        if event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        if event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS
        mario.last_state = 'Dash'
        # fill here
        pass

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * 2 * ACTION_PER_TIME * game_framework.frame_time) % 4
        mario.x += mario.velocity * game_framework.frame_time * 3
        # if mario.collide_object == 'floor':
        #     SMB_state.mario.y = 50 + SMB_state.mario.height // 2
        if mario.x >= 255:
            SMB_state.map_x_velocity = RUN_SPEED_PPS * 3
            SMB_state.map_move = True
        else:
            SMB_state.map_x_velocity = 0
            SMB_state.map_move = False
        mario.x = clamp(16, mario.x, 256)
        mario.y = clamp(32, mario.y, 480)

    @staticmethod
    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame + 1) * 40, 0, 40, 64, mario.x, mario.y)
        else:
            mario.image.clip_draw(int(mario.frame + 1) * 40, 64, 40, 64, mario.x, mario.y)


class JumpState:

    def enter(mario, event):

        if event == RIGHT_DOWN:
            if mario.last_state == 'Dash':
                pass
            else:
                mario.last_state = 'Run'
        if event == LEFT_DOWN:
            if mario.last_state == 'Dash':
                pass
            else:
                mario.last_state = 'Run'
        if event == RIGHT_UP:
            if mario.last_state == 'Dash':
                mario.last_state = 'IdleDash'
            else:
                mario.last_state = 'Idle'
        if event == LEFT_UP:
            if mario.last_state == 'Dash':
                mario.last_state = 'IdleDash'
            else:
                mario.last_state = 'Idle'
        if event == SHIFT_UP:
            if mario.last_state == 'Dash':
                mario.last_state = 'RunDash'
            else:
                pass

        pass

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()
        pass

    def do(mario):
        mario.jump_sound.play()
        if mario.jump_enable == False:
            mario.timer = 0
            mario.collide_object = None
        mario.jump_enable = True

        mario.timer += game_framework.frame_time
        # mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if mario.last_state == 'Dash' or mario.last_state == 'IdleDash' or mario.last_state == 'RunDash':
            mario.x += mario.velocity * game_framework.frame_time * 3
            if mario.x >= 255:
                SMB_state.map_x_velocity = RUN_SPEED_PPS * 3
                SMB_state.map_move = True
            else:
                SMB_state.map_x_velocity = 0
                SMB_state.map_move = False
        else:
            mario.x += mario.velocity * game_framework.frame_time
            if mario.x >= 255:
                SMB_state.map_x_velocity = RUN_SPEED_PPS
                SMB_state.map_move = True
            else:
                SMB_state.map_x_velocity = 0
                SMB_state.map_move = False
        # mario.gravity_speed += math.sin(mario.gravity_speed) * game_framework.frame_time
        # mario.y += mario.gravity_speed // -2 * (mario.timer ** 2) + 60 * mario.timer
        mario.y += mario.gravity_speed // -0.6 * (mario.timer ** 2) + 50 * mario.timer

        if mario.y < 82:
            if mario.collide_object == 'floor':
                mario.y = 82
            mario.jump_enable = False
            if mario.last_state == 'Run' or mario.last_state == 'RunDash':
                mario.add_event(TO_RUN)
            elif mario.last_state == 'Dash':
                mario.add_event(TO_DASH)
            elif mario.last_state == 'Idle' or mario.last_state == 'IdleDash':
                mario.add_event(TO_IDLE)
                mario.velocity = 0




        mario.x = clamp(16, mario.x, 256)
        mario.y = clamp(32, mario.y, 480)

    @staticmethod
    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(200, 0, 40, 64, mario.x, mario.y)
        else:
            mario.image.clip_draw(200, 64, 40, 64, mario.x, mario.y)


class GameOverState:

    def enter(mario, event):
        SMB_state.map_move = 0
        if mario.game_over == 0:
            mario.game_over_timer = 0
            # mario.y = 96
        mario.game_over = 1
        mario.velociy = 0
        mario.dead_cod_x = 0
        mario.dead_cod_y = 0
        pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.game_over_timer += game_framework.frame_time
        mario.mario_die_sound.play()
        if mario.dead_cod_x == 0:
            mario.dead_cod_x = mario.x
            mario.dead_cod_y = mario.y
        # if mario.game_over_timer > 1.5:
        #     mario.y += mario.gravity_speed // -0.6 * (mario.game_over_timer ** 2) + 50 * mario.game_over_timer
        if mario.game_over_timer > 2:
            SMB_state.mario_life -= 1
            game_framework.change_state(world_start_state)
            mario.game_over = 0
        pass

    @staticmethod
    def draw(mario):
        mario.image.clip_draw(0, 128, 32, 32, mario.dead_cod_x, mario.dead_cod_y)
        pass


next_state_table = {
    DashState: {SHIFT_UP: RunState, SHIFT_DOWN: RunState, RIGHT_DOWN: IdleState,
                LEFT_DOWN: IdleState, RIGHT_UP: IdleState, LEFT_UP: IdleState,
                SPACE: DashState, JUMP: JumpState, GO_TO_GAMEOVER: GameOverState,TO_DASH: DashState,
                TO_RUN:DashState,TO_IDLE: DashState},
    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SHIFT_DOWN: IdleState, SHIFT_UP: IdleState, SPACE: IdleState,
                JUMP: JumpState, GO_TO_GAMEOVER: GameOverState, TO_IDLE: IdleState, TO_RUN:IdleState, TO_DASH: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState, SPACE: RunState, JUMP: JumpState, GO_TO_GAMEOVER: GameOverState,
               TO_RUN: RunState, TO_IDLE: RunState, TO_DASH: RunState},
    JumpState: {SHIFT_DOWN: JumpState, RIGHT_DOWN: JumpState, RIGHT_UP: JumpState, LEFT_DOWN: JumpState,
                LEFT_UP: JumpState, SHIFT_UP: JumpState, SPACE: JumpState, TO_RUN: RunState,
                TO_IDLE: IdleState, TO_DASH: DashState, JUMP: JumpState, GO_TO_GAMEOVER: GameOverState},
    GameOverState: {SHIFT_DOWN: GameOverState, SHIFT_UP: GameOverState, RIGHT_DOWN: GameOverState,
                    RIGHT_UP: GameOverState, LEFT_DOWN: GameOverState, LEFT_UP: GameOverState,
                    SPACE: GameOverState, JUMP: GameOverState, GO_TO_GAMEOVER: GameOverState,
                    TO_RUN: GameOverState, TO_IDLE: GameOverState, TO_DASH: GameOverState}
}


class Mario:

    def __init__(self):
        self.x, self.y = 512//8, 100
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('mario.png')
        # fill here
        self.font = load_font('mario_text.TTF', 16)
        self.jump_sound = load_wav('smb_jump-super.wav')
        self.jump_sound.set_volume(10)
        self.mario_die_sound = load_wav('smb_mariodie.wav')
        self.mario_die_sound.set_volume(10)
        self.gravity_speed = RUN_SPEED_PPS // 2
        self.last_state = 'Idle'
        self.jump_enable = False
        self.collide_object = None
        self.game_over = 0
        self.timer = 0
        self.dir = 1
        self.velocity = 0
        self.height = 64
        self.front_width = 12
        self.back_width = 20
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.ball = None

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir * 3)
        game_world.add_object(ball, 1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_bb(self):
        return int(self.x - 20), int(self.y - 32), int(self.x + 12), int(self.y + 32)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                history.append((self.cur_state.__name__, event_name[event]))
                self.cur_state = next_state_table[self.cur_state][event]
            except:
                print('State:', self.cur_state.__name__, 'Event:', event_name[event])
                exit(-1)
            self.cur_state.enter(self, event)
        # if self.cur_state == IdleState or self.cur_state == RunState or self.cur_state == DashState:
        #     for _ in SMB_state.floors:
        #         if collide(SMB_state.bottom_mario, _) == False:
        #             self.y -= self.gravity_speed // 1.9 * game_framework.frame_time
        print(self.collide_object)
        print(self.x, self.y)

    def draw(self):
        self.cur_state.draw(self)
        # debug_print('Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir))
        # fill here
        # self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f' %get_time(), (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if DEBUG_KEY == key_event:
                print(history[-10:])
            else:
                self.add_event(key_event)


# class Top_mario:
#
#     def __init__(self):
#         self.x, self.y = 0, 0
#         pass
#
#     def update(self):
#         self.x = SMB_state.mario.x
#         self.y = SMB_state.mario.y
#         pass
#
#     def draw(self):
#         # debug_print('x :' + str(Game_over_zone.x) + '  gap:' + str(Game_over_zone.gap))
#         # if self.x >= 0 and self.x <= 512 :
#         draw_rectangle(*self.get_bb())
#         pass
#
#     def get_bb(self):
#         return self.x - 18, self.y, self.x + 10, self.y + 35
#
#
class Bottom_mario:

    def __init__(self):
        self.x, self.y = 0, 0
        pass

    def update(self):
        self.x = SMB_state.mario.x
        self.y = SMB_state.mario.y
        pass

    def draw(self):
        # debug_print('x :' + str(Game_over_zone.x) + '  gap:' + str(Game_over_zone.gap))
        # if self.x >= 0 and self.x <= 512 :
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 18, self.y - 32, self.x + 10, self.y - 35
