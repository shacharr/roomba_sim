import math
import random

from cleaning_robot_model import CleaningRobotModel

from helper_functions import *


class RoombaModel(CleaningRobotModel):
    MODE_TIME_LIMIT = [500,2000]
    TURN_SIZE_ON_WALL_FOLLOW = math.pi/180.
    MAX_TURN_STEPS = 360
    SPIRAL_ANGLE_INIT = math.pi/18.
    SPIRAL_ANGLE_RATIO = 0.995
    def __init__(self, *args, **kwargs):
        super(RoombaModel,self).__init__(*args, **kwargs)
        self.in_random_direction_mode = False
        self.looking_for_wall = False
        self.spiral_mode = True
        self.spiral_angle = self.SPIRAL_ANGLE_INIT
        self.time_in_mode = 0
        if "MODE_TIME_LIMIT" in kwargs:
            self.MODE_TIME_LIMIT = kwargs["MODE_TIME_LIMIT"]
        if "TURN_SIZE_ON_WALL_FOLLOW" in kwargs:
            self.TURN_SIZE_ON_WALL_FOLLOW = kwargs["TURN_SIZE_ON_WALL_FOLLOW"]
            self.MAX_TURN_STEPS = (2*math.pi)/self.TURN_SIZE_ON_WALL_FOLLOW

    def left_hand_tracking(self):
        found_wall = False
        for i in range(self.MAX_TURN_STEPS):
            self.turn(-self.TURN_SIZE_ON_WALL_FOLLOW)
            if self.check_move():
                found_wall = True
                break
        if not found_wall:
            self.looking_for_wall = True
        self.turn(self.TURN_SIZE_ON_WALL_FOLLOW)


    def spiral_step(self):
        self.turn(self.spiral_angle)
        self.spiral_angle = self.spiral_angle * self.SPIRAL_ANGLE_RATIO

    def step(self):
        if not self.in_random_direction_mode and not self.looking_for_wall:
            self.left_hand_tracking()
        if self.spiral_mode:
            self.spiral_step()
        collided = self.move()
        self.time_in_mode += 1
        if collided:
            self.looking_for_wall = False
            self.spiral_mode = False
            if self.in_random_direction_mode:
                self.turn(random.randint(0,360)*math.pi/180.)
            else:
                while self.check_move():
                    self.turn(self.TURN_SIZE_ON_WALL_FOLLOW)
        if not self.spiral_mode and self.time_in_mode > self.MODE_TIME_LIMIT[self.in_random_direction_mode]:
            self.in_random_direction_mode = not self.in_random_direction_mode
            self.time_in_mode = 0
            print "Switched to mode",self.in_random_direction_mode

