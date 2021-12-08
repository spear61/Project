import random
import math
import game_framework
from collision import collide
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *

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


class Piranha_plant:
    image = None

    def load_image(self):
        if Piranha_plant.image == None:
            Piranha_plant.image = load_image('piranha_plant.png')

    def __init__(self, x = 256, y = 73):
        self.x, self.y = x, y
        self.load_image()
        self.speed = 0
        self.timer = 0
        self.wait_timer = 0
        self.frame = 0
        self.build_behavior_tree()

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def wait(self):
        self.speed = 0
        self.wait_timer -= game_framework.frame_time
        if self.wait_timer <= 0:
            self.wait_timer = 1.5
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        wait_node = LeafNode('Wait', self.wait)
        wander_wait_node = SequenceNode('WanderWait')
        wander_wait_node.add_children(wander_node, wait_node)

        self.bt = BehaviorTree(wander_wait_node)

    def get_bb(self):
        return self.x - 16, self.y - 23, self.x + 16, self.y + 23

    def update(self):
        self.bt.run()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.y += self.speed * game_framework.frame_time
        if SMB_state.map_move is True:
            self.x -= SMB_state.map_x_velocity * game_framework.frame_time

    def draw(self):
        draw_rectangle(*self.get_bb())

        if self.speed == 0:
            self.image.clip_draw(int(self.frame) * 32, 0, 32, 46, self.x, self.y)
        else:
            self.image.clip_draw(int(self.frame) * 32, 0, 32, 46, self.x, self.y)

    def handle_event(self, event):
        pass
