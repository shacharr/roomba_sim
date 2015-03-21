import math

class RoombaModel(object):
    def __init__(self, location, direction, speed):
        self.loc = location
        self.direction = direction
        self.speed = speed

    def step(self):
        x,y = self.loc
        step_x = -self.speed * math.sin(self.direction)
        step_y = self.speed * math.cos(self.direction)
        self.loc = (x+step_x, y+step_y)
        return ([int(x) for x in self.loc],self.direction)

    def turn(self, relative_direction):
        self.direction += relative_direction
