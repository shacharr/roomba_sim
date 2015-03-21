import time
import pygame
import math
import random

import arena_model
import arena_view


def main():
    pygame.init()
    clock = pygame.time.Clock()
    view = arena_view.ScreenView(50)
    roomba_model = arena_model.RoombaModel((300,300),0,3)
    done = False
    while True:
        clock.tick(30)
     
        for event in pygame.event.get(): # User did something
            #print "Got event",event,"type:",event.type
            if event.type == pygame.QUIT: # If user clicked close
                done=True
        if done:
            break
        view.draw_roomba(*roomba_model.step())
        view.clear_screen()
        if random.randint(0,1000) > 300:
            roomba_model.turn(random.randint(0,10)*math.pi/100.)
    
if __name__ == "__main__":
    main()
