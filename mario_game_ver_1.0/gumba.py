import random
import math

import collision
import game_framework
import game_world
import mario
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import ball

import SMB_state

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2


class Gumba:
    image = None

    def load_image(self):
        if Gumba.image == None:
            Gumba.image = load_image('gumba.png')

    def __init__(self, x=256, y=66, dir=1):
        self.x, self.y = x, y
        self.load_image()
        self.dir = dir
        self.speed = 0
        self.timer = 0
        self.wait_timer = 0
        self.frame = 0
        self.build_behavior_tree()
        self.life = 1
        self.life_timer = 2
        self.dead_cod = 0

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.5
            if self.dir == 1:
                self.dir = -1
            elif self.dir == -1:
                self.dir = 1
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def wait(self):
        self.speed = 0
        self.wait_timer -= game_framework.frame_time
        if self.wait_timer <= 0:
            self.wait_timer = 0.1
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        wait_node = LeafNode('Wait', self.wait)
        wander_wait_node = SequenceNode('WanderWait')
        wander_wait_node.add_children(wander_node, wait_node)

        self.bt = BehaviorTree(wander_wait_node)

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def update(self):
        self.bt.run()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * self.dir * game_framework.frame_time
        if SMB_state.map_move is True:
            self.x -= SMB_state.map_x_velocity * game_framework.frame_time

        # if collision.collide(self, SMB_state.bottom_mario):
        #     if self.life == 1:
        #         self.life_timer = 2
        #         self.life = 0
        #     if self.life_timer < 0:
        #         game_world.remove_object(self)
        if self.life == 0:
            self.life_timer -= game_framework.frame_time
            if self.dead_cod == 0:
                self.dead_cod = self.x
            if self.dead_cod != 0 and SMB_state.map_move == True:
                self.dead_cod -= SMB_state.map_x_velocity * game_framework.frame_time
            if self.life_timer < 0:
                game_world.remove_object(self)
        if self.life == 1 and collision.collide(SMB_state.bottom_mario, self):
            self.life = 0
            SMB_state.mario_score += 100
        if self.life == 1 and collision.collide(SMB_state.mario, self):
            mario.y = self.y + 32
            SMB_state.mario.add_event(mario.GO_TO_GAMEOVER)



    def draw(self):
        # draw_rectangle(*self.get_bb())
        if self.life == 0:
            self.image.clip_draw(0,0,32,32,self.dead_cod, self.y)
        elif self.dir > 0:
            if self.speed == 0:
                self.image.clip_draw(32, 0, 32, 32, self.x, self.y)
            else:
                self.image.clip_draw(32 + int(self.frame) * 32, 0, 32, 32, self.x, self.y)
        else:
            if self.speed == 0:
                self.image.clip_draw(32, 0, 32, 32, self.x, self.y)
            else:
                self.image.clip_draw(32 + int(self.frame) * 32, 0, 32, 32, self.x, self.y)



    def handle_event(self, event):
        pass
