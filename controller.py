import time
import pygame
import math
import random

import arena_model
import arena_view



#ROOM_POLYGON = [(0,0),(640,0),(640,480),(0,480)]
ROOM_POLYGON = [(0,0),(640,0),(640,480),(320,480),(320,240),(0,240)]

ROOMBA_SIZE = 20

TURN_SIZE_ON_WALL_FOLLOW = math.pi/180.
MAX_TURN_STEPS = 360

def main():
    pygame.init()
    clock = pygame.time.Clock()

    view = arena_view.ScreenView(ROOMBA_SIZE, [max(x[0] for x in ROOM_POLYGON),max(x[1] for x in ROOM_POLYGON)])
    room_model = arena_model.RoomModel(ROOM_POLYGON)
    roomba_model = arena_model.RoombaModel((100,100), ROOMBA_SIZE, 1.9, 0, 3, room_model)
    done = False
    while True:
        view.clear_screen(room_model.state)
        clock.tick(60)
     
        for event in pygame.event.get(): # User did something
            #print "Got event",event,"type:",event.type
            if event.type == pygame.QUIT: # If user clicked close
                done=True
        if done:
            break
        roomba_model.step()
        view.draw_roomba(*roomba_model.get_draw_info())
    
if __name__ == "__main__":
    main()
