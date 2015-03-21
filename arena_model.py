import math
import pygame

from helper_functions import *

class Point(object):
    def __init__(self,coords):
        self.x = coords[0]
        self.y = coords[1]

    def delta(self,other):
        return Point([self.x-other.x,self.y-other.y])

    def dot(self,other):
        return self.x*other.x + self.y*other.y

class RoombaModel(object):
    def __init__(self, location, size, direction, speed, room):
        self.loc = location
        self.direction = direction
        self.speed = speed
        self.size = size
        self.room = room

    def step(self):
        x,y = self.loc
        step_x = -self.speed * math.sin(self.direction)
        step_y = self.speed * math.cos(self.direction)
        new_loc = (x+step_x, y+step_y)
        # Assumes speed is slow enough to prevent quantom tunneling of the roomba...
        if not self.is_coliding(new_loc):
            mid_point = [(x+y)/2. for x,y in zip(new_loc,self.loc)]
            self.room.clean_box(self.size*1.9, self.speed,
                                self.direction, mid_point)
            self.loc = new_loc
            return False
        return True

    def turn(self, relative_direction):
        self.direction += relative_direction

    def get_draw_info(self):
        return ([int(x) for x in self.loc],self.direction)

    def is_coliding(self, loc):
        room_polygon = self.room.polygon
        for line in zip(room_polygon,room_polygon[1:]+[room_polygon[0]]):
            if line_circle_intersect([Point(line[0]),Point(line[1])],
                                     [Point(loc), self.size]):
                return True
        return False

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
        coords = [rotate(p,direction) for p in coords]

        #Move
        coords = [[x+y for x,y in zip(p,mid_point)] for p in coords]
        pygame.draw.polygon(self.state,(0,0,255),coords)

