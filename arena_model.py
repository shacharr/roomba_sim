import math
import pygame
import random

from helper_functions import *

MODE_TIME_LIMIT = [500,2000]

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
        self.looking_for_wall = False
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
        self.room.clean_polygon(cleaned_triangle_1)
        self.room.clean_polygon(cleaned_triangle_2)

        self.direction += relative_direction

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


class RoomModel(object):
    DIRTY_COLOR = (0,255,0)
    CLEAN_COLOR = (0,0,255)
    def __init__(self, polygon):
        self.polygon = polygon
        max_x = max([x[0] for x in polygon])
        max_y = max([x[1] for x in polygon])
        self.state = pygame.Surface((max_x,max_y))
        self.state.fill((0,0,0))
        pygame.draw.polygon(self.state,self.DIRTY_COLOR,polygon)
        self.clean_count, self.dirty_count = self.count_clean_dirty(0,0,max_x,max_y)

    def clean_box(self, len_x, len_y, direction, mid_point):
        # Start at zero-coords
        coords = [(-len_x/2,-len_y/2),( len_x/2,-len_y/2),
                  ( len_x/2, len_y/2),(-len_x/2, len_y/2)]

        #Rotate
        coords = rotate_polygon(coords,direction)

        #Move
        coords = transpose_polygon(coords,mid_point)
        self.clean_polygon(coords)

    def clean_polygon(self, corners):
        bbox = polygon_bbox(corners)
        orig_clean,orig_dirty = self.count_clean_dirty(*bbox)
        pygame.draw.polygon(self.state,self.CLEAN_COLOR,corners)
        new_clean,new_dirty = self.count_clean_dirty(*bbox)
        self.clean_count += (new_clean - orig_clean)
        self.dirty_count += (new_dirty - orig_dirty)

    def is_coliding(self, loc, size):
        room_polygon = self.polygon
        for line in zip(room_polygon,room_polygon[1:]+[room_polygon[0]]):
            if line_circle_intersect([Point(line[0]),Point(line[1])],
                                     [Point(loc), size]):
                return True
        return False

    def count_clean_dirty(self,start_x,start_y,end_x,end_y):
        clean_count = 0
        dirty_count = 0
        start_x = int(max(start_x-1,0))
        max_x = self.state.get_clip().width
        delta_x = int(min(end_x+1,max_x)) - start_x
        start_y = int(max(start_y-1,0))
        max_y = self.state.get_clip().height
        delta_y = int(min(end_y+1,max_y)) - start_y
        if delta_x <= 0 or delta_y <= 0:
            return (0,0)
        rect = pygame.Rect(start_x,start_y, delta_x,delta_y)
        sub_surf = self.state.subsurface(rect)
        ar = pygame.PixelArray(sub_surf)
        for x in range(delta_x):
            for y in range(delta_y):
                if ar[x,y] == self.state.map_rgb(self.DIRTY_COLOR):
                    dirty_count += 1
                elif ar[x,y] == self.state.map_rgb(self.CLEAN_COLOR):
                    clean_count += 1
        del ar,sub_surf
        return (clean_count,dirty_count)
