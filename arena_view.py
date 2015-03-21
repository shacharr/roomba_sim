import time
import pygame
import math

from helper_functions import *

class ScreenView(object):
    WHITE = (255,255,255)
    BLACK = (  0,  0,  0)
    BLUE  = (  0,  0,255)
    GREEN = (  0,255,  0)
    RED   = (255,  0,  0)

    ARROW_RELATIVE_COORDS = ((0,0.8),(0.4,0.5),(0.2,0.5),(0.2,-0.6),
                             (-0.2,-0.6),(-0.2,0.5),(-0.4,0.5),(0,0.8))


    def __init__(self, roomba_size, screen_size):
        self.screen = pygame.display.set_mode(screen_size)
        self.roomba_size = roomba_size
        self.arrow_scaled_coords = tuple((tuple((y*roomba_size for y in x))
                                          for x in self.ARROW_RELATIVE_COORDS))

    def clear_screen(self,room_surface):
        pygame.display.flip()
        self.screen.fill(self.WHITE)
        self.screen.blit(room_surface,(0,0))

    def draw_roomba(self,mid_point, direction):
        pygame.draw.circle(self.screen, self.RED,
                           mid_point, self.roomba_size)

        rotated_arrow = tuple(rotate(coords, direction)
                              for coords in self.arrow_scaled_coords)
        transposed_arrow = tuple((tuple((y1+y2 for (y1,y2) in zip(x,mid_point)))
                                  for x in rotated_arrow))
        pygame.draw.polygon(self.screen, self.BLACK,
                            transposed_arrow)

def testView():
    pygame.init()
    clock = pygame.time.Clock()
    view = ScreenView(50)
    done = False
    for i in range(0,360*10):
        clock.tick(30)
     
        for event in pygame.event.get(): # User did something
            #print "Got event",event,"type:",event.type
            if event.type == pygame.QUIT: # If user clicked close
                done=True
        if done:
            break
        view.draw_roomba((100,100),i * math.pi / 180. )
        view.clear_screen()

#time.sleep(10)

if __name__ == "__main__":
    testView()
