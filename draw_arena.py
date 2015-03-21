import time
import pygame
import math

def rotate(coords, direction):
    # from https://www.siggraph.org/education/materials/HyperGraph/modeling/mod_tran/2drota.htm
    x,y = coords
    cos_d = math.cos(direction)
    sin_d = math.sin(direction)
    return (x*cos_d - y*sin_d,
            y*cos_d + x*sin_d)

class ScreenView(object):
    WHITE = (255,255,255)
    BLACK = (  0,  0,  0)
    BLUE  = (  0,  0,255)
    GREEN = (  0,255,  0)
    RED   = (255,  0,  0)

    SIZE  = (640, 480)

    ARROW_RELATIVE_COORDS = ((0,0.8),(0.4,0.5),(0.2,0.5),(0.2,-0.6),
                             (-0.2,-0.6),(-0.2,0.5),(-0.4,0.5),(0,0.8))


    def __init__(self, roomba_size):
        self.screen = pygame.display.set_mode(self.SIZE)
        self.roomba_size = roomba_size
        self.arrow_scaled_coords = tuple((tuple((y*roomba_size for y in x))
                                          for x in self.ARROW_RELATIVE_COORDS))

    def clear_screen(self):
        pygame.display.flip()
        self.screen.fill(self.WHITE)

    def draw_roomba(self,mid_point, direction):
        pygame.draw.circle(self.screen, self.RED,
                           mid_point, self.roomba_size)

        rotated_arrow = tuple(rotate(coords, direction * math.pi / 180.)
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
        view.draw_roomba((100,100),i/4.)
        view.clear_screen()

#time.sleep(10)

if __name__ == "__main__":
    testView()
