# Python 3.4
# domestruts.py 

from domemath import *

# Need to change these for mm unit 
margin = 0.75/12.0
bl = 0.75/12.0
at = 2.0
lt = 0.001
scale = 1.0

class StrutInfo:
        """ Represent one group of identical struts  """
        def __init__(self, name='', length=0.0, a0=0.0, a1=0.0, count=0):
                self.name = name
                self.length = length
                self.a0 = fn6(a0, 2)
                self.a1 = fn6(a1, 2)
                self.count = count 

# Bending the ends of the pipe will shorten it slightly.
# returns the pre-bend length of the strut.
def bend_allowances(strut):
        x1 = m.radians(strut.a0)
        x2 = m.radians(strut.a1)
        d = 1.0 - m.cos(x1)
        d += 1.0 - m.cos(x2) 
        return bl * d


def bend_angle(p0, p1):
        """
                Form two vectors: p0 to origin, p0 to p1.
                      + p1 
                       \  
                        \
                         \ 
              O +--------+ p0
        """
        v0, v1 = Point(), Point()

        v0.x, v0.y, v0.z = -p0.x, -p0.y, -p0.z
        l = vlen(v0)
        if l == 0.0:
                return 0.0

        l = 1.0 / l 
        v0.x *= l
        v0.y *= l
        v0.z *= l

        v1.x = p1.x - p0.x
        v1.y = p1.y - p0.y 
        v1.z = p1.z - p0.z
        l2 = vlen(v1)
        if l2 == 0.0:
                return 0.0

        l2 = 1.0 / l2
        v1.x *= l2
        v1.y *= l2
        v1.z *= l2

        x_ = dotprod(v0, v1)
        rad = m.acos(x_)
        theta = 90.0 - m.degrees(rad)
        return theta 


def match_strut(a, b, at, lt):
        """
        Return true if the two struts match within a small margin of error.
        """
        l0 = 1.0 - lt
        l1 = 1.0 + lt

        if b.length > a.length*l1 or b.length < a.length*l0:
                return 0

        if (b.a0 >= a.a0-at) and (b.a0 <= a.a0+at) and
           (b.a1 >= a.a1-at) and (b.a1 <= a.a1+at):
                return 1

        if (b.a0 >= a.a1-at) and (b.a0 <= a.a1+at) and
           (b.a1 >= a.a0-at) and (b.a1 <= a.a0+at):
                return 0

        return 0

# tmp = compute_strut(vertices, edge)
# tmp.count = 1
def compute_strut(vsrc, edge):
        p0 = vsrc[edge.v0]
        p1 = vsrc[edge.v1]

        t = StrutInfo()
        t.length = edge.length
        t.a0 = bend_angle(p0, p1)
        t.a1 = bend_angle(p1, p0)

        return t 


                
