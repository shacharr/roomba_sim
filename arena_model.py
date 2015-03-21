import math
import pygame
import random

from helper_functions import *

MODE_TIME_LIMIT = [1000,5000]

class RoombaModel(object):
    TURN_SIZE_ON_WALL_FOLLOW = math.pi/180.
    MAX_TURN_STEPS = 360
    def __init__(self, location, size, cleaning_head_size, direction, speed, room):
        self.loc = location
        self.direction = direction
        self.speed = speed
        self.size = size
        self.room = room
        self.cleaning_head_size = cleaning_head_size
        self.in_random_direction_mode = False
        self.time_in_mode = 0

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
            return False
        return True

    def turn(self, relative_direction):
        delta_x = self.size * self.cleaning_head_size / 2.
        cleaned_triangle_1 = [(0,0), (delta_x,0), rotate((delta_x,0), relative_direction)]
        cleaned_triangle_2 = [(0,0), (-delta_x,0), rotate((-delta_x,0), relative_direction)]

        cleaned_triangle_1 = rotate_polygon(cleaned_triangle_1,
                                            self.direction)
        cleaned_triangle_2 = rotate_polygon(cleaned_triangle_2,
                                            self.direction)

        cleaned_triangle_1 = transpose_polygon(cleaned_triangle_1,self.loc)
        cleaned_triangle_2 = transpose_polygon(cleaned_triangle_2,self.loc)
        self.room.clean_triangle(cleaned_triangle_1)
        self.room.clean_triangle(cleaned_triangle_2)

        self.direction += relative_direction

    def step(self):
        if not self.in_random_direction_mode:
            for i in range(self.MAX_TURN_STEPS):
                self.turn(-self.TURN_SIZE_ON_WALL_FOLLOW)
                if self.check_move():
                    break
            self.turn(self.TURN_SIZE_ON_WALL_FOLLOW)
        collided = self.move()
        self.time_in_mode += 1
        if collided:
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


class RoomModel(object):
    def __init__(self, polygon):
        self.polygon = polygon
        max_x = max([x[0] for x in polygon])
        max_y = max([x[1] for x in polygon])
        self.state = pygame.Surface((max_x,max_y))
        self.state.fill((255,255,255))
        pygame.draw.polygon(self.state,(0,255,0),polygon)

    def clean_box(self, len_x, len_y, direction, mid_point):
        # Start at zero-coords
        coords = [(-len_x/2,-len_y/2),( len_x/2,-len_y/2),
                  ( len_x/2, len_y/2),(-len_x/2, len_y/2)]

        #Rotate
        coords = rotate_polygon(coords,direction)

        #Move
        coords = transpose_polygon(coords,mid_point)
        pygame.draw.polygon(self.state,(0,0,255),coords)

    def clean_triangle(self, corners):
        pygame.draw.polygon(self.state,(0,0,255),corners)

    def is_coliding(self, loc, size):
        room_polygon = self.polygon
        for line in zip(room_polygon,room_polygon[1:]+[room_polygon[0]]):
            if line_circle_intersect([Point(line[0]),Point(line[1])],
                                     [Point(loc), size]):
                return True
        return False

