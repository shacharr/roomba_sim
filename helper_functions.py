import math

class Point(object):
    def __init__(self,coords):
        self.x = coords[0]
        self.y = coords[1]

    def delta(self,other):
        return Point([self.x-other.x,self.y-other.y])

    def dot(self,other):
        return self.x*other.x + self.y*other.y

def rotate(coords, direction):
    # from https://www.siggraph.org/education/materials/HyperGraph/modeling/mod_tran/2drota.htm
    x,y = coords
    cos_d = math.cos(direction)
    sin_d = math.sin(direction)
    return (x*cos_d - y*sin_d,
            y*cos_d + x*sin_d)


def line_circle_intersect(line_details, circle_details):
    # Based upon http://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm
    E = line_details[0]
    L = line_details[1]
    C = circle_details[0]
    r = circle_details[1]
    d = L.delta(E)
    f = E.delta(C)
    a = d.dot(d)
    b = 2*f.dot(d)
    c = f.dot(f) - r*r
    discriminant = b*b-4*a*c
    if discriminant < 0:
        return False
    discriminant = math.sqrt(discriminant)
    t1 = (-b - discriminant)/(2*a)
    t2 = (-b + discriminant)/(2*a)
    t1_good = t1 >= 0 and t1 <= 1
    t2_good = t2 >= 0 and t2 <= 1
    return t1_good or t2_good

def rotate_polygon(poly,direction):
    return [rotate(p,direction) for p in poly]


def transpose_polygon(poly,delta_coords):
    return [[x+y for x,y in zip(p,delta_coords)] for p in poly]

def polygon_bbox(poly):
    return [min(x[0] for x in poly),
            min(x[1] for x in poly),
            max(x[0] for x in poly),
            max(x[1] for x in poly)]
