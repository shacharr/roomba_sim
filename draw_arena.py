import time
import pygame
import math

class ScreenView(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((640,480))
        self.roomba = pygame.image.load("roomba.png")
        self.orig_clip = self.roomba.get_clip()

    def clear_screen(self):
        pygame.display.flip()
        self.screen.fill((255,255,255))

    def draw_roomba(self,start_point, direction):
        rotated = pygame.transform.rotate(self.roomba, direction)
        rotated_clip = rotated.get_clip()
        delta_x = ((rotated_clip.width-self.orig_clip.width)+1)/2
        delta_y = ((rotated_clip.height-self.orig_clip.height)+1)/2
        self.screen.blit(rotated,
                         (start_point[0]-self.orig_clip.width/2,
                          start_point[1]-self.orig_clip.height/2),
                         (delta_x,delta_y,
                          self.orig_clip.width+1,self.orig_clip.height+1) )
    
    
#screen.blit(roomba, (50, 100))
#pygame.display.flip()
#time.sleep(1)

def testView():
    pygame.init()
    clock = pygame.time.Clock()
    view = ScreenView()
    done = False
    for i in range(0,360*10):
        clock.tick(30)
     
        for event in pygame.event.get(): # User did something
            #print "Got event",event,"type:",event.type
            if event.type == pygame.QUIT: # If user clicked close
                done=True
        if done:
            break
        view.draw_roomba((100,100),i/4.)
        view.clear_screen()

#time.sleep(10)

if __name__ == "__main__":
    testView()
