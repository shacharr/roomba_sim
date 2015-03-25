import pygame

from helper_functions import *


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
