import time
import pygame
import math
import random

import arena_model
import arena_view


MODE_TIME_LIMIT = [1000,5000]

def main():
    pygame.init()
    clock = pygame.time.Clock()
    roomba_size = 50
    view = arena_view.ScreenView(roomba_size)
    room_model = arena_model.RoomModel([(0,0),(640,0),(640,480),(0,480)])
    roomba_model = arena_model.RoombaModel((300,300), roomba_size, 1.9, 0, 3, room_model)
    done = False
    in_random_direction_mode = False
    time_in_mode = 0
    while True:
        view.clear_screen(room_model.state)
        clock.tick(30)
     
        for event in pygame.event.get(): # User did something
            #print "Got event",event,"type:",event.type
            if event.type == pygame.QUIT: # If user clicked close
                done=True
        if done:
            break
        collided = roomba_model.step()
        view.draw_roomba(*roomba_model.get_draw_info())
        time_in_mode += 1
        if collided:
            if in_random_direction_mode:
                roomba_model.turn(random.randint(0,360)*math.pi/180.)
            else:
                roomba_model.turn(math.pi/180.)
            if time_in_mode > MODE_TIME_LIMIT[in_random_direction_mode]:
                in_random_direction_mode = not in_random_direction_mode
                time_in_mode = 0
                print "Switched to mode",in_random_direction_mode
    
if __name__ == "__main__":
    main()
