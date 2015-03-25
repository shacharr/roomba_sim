import time
import pygame
import math
import matplotlib.pyplot

import arena_model
import arena_view
import roomba_model

from helper_functions import *

#ROOM_POLYGON = [(0,0),(640,0),(640,480),(0,480)]
#ROOM_POLYGON = [(0,0),(640,0),(640,480),(320,480),(320,240),(0,240)]
ROOM_POLYGON = [(0,0),(640,0),(640,480),(320,480),(250,240),(0,240)]

SMALL_SQUARE = [(0,0),(10,0),(10,10),(0,10)]

OBSTECLES = [transpose_polygon(SMALL_SQUARE,(200,45)),
             transpose_polygon(SMALL_SQUARE,(270,45)),
             transpose_polygon(SMALL_SQUARE,(200,125)),
             transpose_polygon(SMALL_SQUARE,(270,125)),]

ROOMBA_SIZE = 20

MIN_COVERAGE_TO_EXIT = 0.988
MAX_NO_GAIN_STEPS = 3000

def main():
    pygame.init()
    stats = [0]
    clock = pygame.time.Clock()

    view = arena_view.ScreenView(ROOMBA_SIZE, [max(x[0] for x in ROOM_POLYGON),max(x[1] for x in ROOM_POLYGON)])
    room_model = arena_model.RoomModel(ROOM_POLYGON,OBSTECLES)
    roomba = roomba_model.RoombaModel((100,100), ROOMBA_SIZE, 1.9, 0, 3, room_model)
    done = False
    last_coverage = 0
    steps_with_no_improvement = 0
    while True:
        coverage = float(room_model.clean_count)/(room_model.clean_count + room_model.dirty_count)
        stats.append(coverage)
        if coverage == last_coverage and coverage > MIN_COVERAGE_TO_EXIT:
            steps_with_no_improvement += 1
            if steps_with_no_improvement > MAX_NO_GAIN_STEPS:
                done = True
        last_coverage = coverage
        view.clear_screen(room_model.state)
     
        for event in pygame.event.get(): # User did something
            #print "Got event",event,"type:",event.type
            if event.type == pygame.QUIT: # If user clicked close
                done=True
        if done:
            break
        roomba.step()
        view.draw_roomba(*roomba.get_draw_info())

    matplotlib.pyplot.plot(stats)
    matplotlib.pyplot.show()

if __name__ == "__main__":
    main()
