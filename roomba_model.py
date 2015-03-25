import math
import random

from cleaning_robot_model import CleaningRobotModel

from helper_functions import *

MODE_TIME_LIMIT = [500,2000]

class RoombaModel(CleaningRobotModel):
    TURN_SIZE_ON_WALL_FOLLOW = math.pi/180.
    MAX_TURN_STEPS = 360
    def __init__(self, *args, **kwargs):
        super(RoombaModel,self).__init__(*args, **kwargs)
        self.in_random_direction_mode = False
        self.looking_for_wall = False
        self.time_in_mode = 0


    def step(self):
        if not self.in_random_direction_mode and not self.looking_for_wall:
            found_wall = False
            for i in range(self.MAX_TURN_STEPS):
                self.turn(-self.TURN_SIZE_ON_WALL_FOLLOW)
                if self.check_move():
                    found_wall = True
                    break
            if not found_wall:
                self.looking_for_wall = True
            self.turn(self.TURN_SIZE_ON_WALL_FOLLOW)
        collided = self.move()
        self.time_in_mode += 1
        if collided:
            self.looking_for_wall = False
            if self.in_random_direction_mode:
                self.turn(random.randint(0,360)*math.pi/180.)
            else:
                while self.check_move():
                    self.turn(self.TURN_SIZE_ON_WALL_FOLLOW)
            if self.time_in_mode > MODE_TIME_LIMIT[self.in_random_direction_mode]:
                self.in_random_direction_mode = not self.in_random_direction_mode
                self.time_in_mode = 0
                print "Switched to mode",self.in_random_direction_mode


    def get_draw_info(self):
        return ([int(x) for x in self.loc],self.direction)
