import math

from helper_functions import *


class CleaningRobotModel(object):
    TURN_STEP_FOR_DRAWING = math.pi/18.
    def __init__(self, location, size, cleaning_head_size, direction, speed, room):
        self.loc = location
        self.direction = direction
        self.speed = speed
        self.size = size
        self.room = room
        self.cleaning_head_size = cleaning_head_size
        self.trace = [location]

    def calc_move_next_loc(self):
        x,y = self.loc
        step_x = -self.speed * math.sin(self.direction)
        step_y = self.speed * math.cos(self.direction)
        return (x+step_x, y+step_y)

    def check_move(self):
        new_loc = self.calc_move_next_loc()
        return self.room.is_coliding(new_loc,self.size)

    def move(self):
        new_loc = self.calc_move_next_loc()
        # Assumes speed is slow enough to prevent quantom tunneling of the roomba...
        if not self.room.is_coliding(new_loc,self.size):
            mid_point = [(x+y)/2. for x,y in zip(new_loc,self.loc)]
            self.room.clean_box(self.size*1.9, self.speed,
                                self.direction, mid_point)
            self.loc = new_loc
            self.trace.append(new_loc)
            return False
        return True

    def clean_step(self,initial_step,step_size):
        delta_x = self.size * self.cleaning_head_size / 2.
        cleaned_triangle_1 = [(0,0), (delta_x,0), rotate((delta_x,0), step_size)]
        cleaned_triangle_2 = [(0,0), (-delta_x,0), rotate((-delta_x,0), step_size)]

        cleaned_triangle_1 = rotate_polygon(cleaned_triangle_1,
                                            self.direction+initial_step)
        cleaned_triangle_2 = rotate_polygon(cleaned_triangle_2,
                                            self.direction+initial_step)

        cleaned_triangle_1 = transpose_polygon(cleaned_triangle_1,self.loc)
        cleaned_triangle_2 = transpose_polygon(cleaned_triangle_2,self.loc)
        self.room.clean_polygon(cleaned_triangle_1)
        self.room.clean_polygon(cleaned_triangle_2)

    def turn(self, relative_direction):
        step = 1
        if relative_direction < 0:
            step = -1
        target_step = abs(int(relative_direction/self.TURN_STEP_FOR_DRAWING))
        for turn_step in range(0,target_step+1):
            self.clean_step(step*turn_step*self.TURN_STEP_FOR_DRAWING,
                            step*self.TURN_STEP_FOR_DRAWING)

        self.clean_step(step*target_step*self.TURN_STEP_FOR_DRAWING,
                        relative_direction - step*target_step*self.TURN_STEP_FOR_DRAWING)
        self.direction += relative_direction

    def step(self):
        raise Exception("Pure virtual function called")

    def get_draw_info(self):
        return ([int(x) for x in self.loc],self.direction,self.trace)
