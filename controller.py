import time
import pygame
import math
import random

import arena_model
import arena_view


MODE_TIME_LIMIT = [1000,5000]

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
    in_random_direction_mode = False
    time_in_mode = 0
    while True:
        view.clear_screen(room_model.state)
        clock.tick(60)
     
        for event in pygame.event.get(): # User did something
            #print "Got event",event,"type:",event.type
            if event.type == pygame.QUIT: # If user clicked close
                done=True
        if done:
            break
        if not in_random_direction_mode:
            for i in range(MAX_TURN_STEPS):
                roomba_model.turn(-TURN_SIZE_ON_WALL_FOLLOW)
                if roomba_model.check_step():
                    break
            roomba_model.turn(TURN_SIZE_ON_WALL_FOLLOW)
        collided = roomba_model.step()
        view.draw_roomba(*roomba_model.get_draw_info())
        time_in_mode += 1
        if collided:
            if in_random_direction_mode:
                roomba_model.turn(random.randint(0,360)*math.pi/180.)
            else:
                while roomba_model.check_step():
                    roomba_model.turn(TURN_SIZE_ON_WALL_FOLLOW)
            if time_in_mode > MODE_TIME_LIMIT[in_random_direction_mode]:
                in_random_direction_mode = not in_random_direction_mode
                time_in_mode = 0
                print "Switched to mode",in_random_direction_mode
    
if __name__ == "__main__":
    main()
