# Python 3.4 
# domemath.py 

import math as m        # math functions 

# mm to inch 
unit_mm = 0.0393700787402 

# Point
#
# Angle calculation on the xy plane 
#      + (x, y)
#     /
#    / o
#   +-----+ (1.0, 0.0)
#
# o is the angle between the unit point on x axis and a point (x, y)
#
class Point:
        def __init__(self, x=0, y=0, z=0):
                self.x = fn6(x)
                self.y = fn6(y)
                self.z = fn6(z)
                self.ix = int(x)
                self.iy = int(y)
                self.iz = int(z)
                self.angle = None

        def find_angle(self, x=1.0, y=0.0):
                a = calculate_angle(self.x, self.y, x, y)
                self.angle = round(a, 2)

        def xyz(self):
                return self.x, self.y, self.z 

        def __str__(self):
                return 'Point<{0:9.6f}, {1:9.6f}, {2:9.6f}>'.format(
                                                self.x, self.y, self.z)


def fn6(n, prec=6):
        """ Round off floating point number to prec """
        return round(float(n), prec)


# Return the distance between two Points 
def ptDist(a, b):
        dx = a.x - b.x
        dy = a.y - b.y
        dz = a.z - b.z
        d = m.sqrt(dx*dx + dy*dy + dz*dz)
        return fn6(d)


# Add two Points 
def ptAdd(a, b):
        x = fn6(a.x + b.x)
        y = fn6(a.y + b.y)
        z = fn6(a.z + b.z)
        return Point(x, y, z)


# Subtract two Points 
def ptSub(a, b):
        x = fn6(a.x - b.x)
        y = fn6(a.y - b.y)
        z = fn6(a.z - b.z)
        return Point(x, y, z)


# Multiply Mx to a Point 
def ptMul(a, Mx):
        x = fn6(Mx*a.x)
        y = fn6(Mx*a.y)
        z = fn6(Mx*a.z)
        return Point(x, y, z)


# Dot product of two vectors
def dotprod(a, b):
        v = a.x*b.x + a.y*b.y + a.z*b.z
        return fn6(v)


# Cross product of two vectors
def crossprod(a, b):
        x = a.y*b.z - a.z*b.y
        y = a.z*b.x - a.x*b.z
        z = a.x*b.y - a.y*b.x
        return Point(fn6(x), fn6(y), fn6(z))


def calculate_angle(x1, y1, x=1.0, y=0.0):
        """
          a dot b = |a||b|cos(theta)
                           a dot b
          theta = arccos( ---------- )
                            |a||b|
          
          On Cartesian XY plane there are four quadrants: I, II, III, IV.
                I:       0 < theta <= 90
                II:     90 < theta <= 180
                III:   180 < theta <= 270
                IV:    270 < theta <= 360
                    y
                    ^
                    |   
                 II | I
               -----+-----> x    
                III | IV
                    |

        """
        if x1 == 0.0 and y1 == 0.0:
                return 0.0

        adotb = x1*x + y1*y
        ma = m.sqrt(x1*x1 + y1*y1)
        mb = 1.0
        v = adotb / (ma*mb)
        rad = m.acos(v)
        _ang = m.degrees(rad)
        if x1 >= 0.0 and y1 >= 0.0:     # I 
                return _ang
        elif x1 < 0.0 and y1 >= 0.0:    # II
                return _ang
        elif x1 < 0.0 and y1 < 0.0:     # III
                return 360.0 - _ang
        elif x1 >= 0.0 and y1 < 0.0:    # IV
                return 360.0 - _ang


def vlen(v):
        """ 
        Return the length of a vector created by a point and the origin.t 
        Point v: 
        """
        d = m.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)
        return fn6(d)



def vnormalize(v):
        """
        Normalize a vector (x, y, z) to unit vector (u)
               v
        u  = ----- 
              |v| 
        |v| = sqrt(x^2 + y^2 + z^2)
        Point v:
        """
        _d = m.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)
        d = fn6(_d)
        if d == 0.0:
                print("normalize(): zero length vector")
                return

        x = fn6(v.x / d)
        y = fn6(v.y / d)
        z = fn6(v.z / d)
        return Point(x, y, z)


# http:#http.developer.nvidia.com/Cg/acos.html
def acos2(x):
        negate = float(x<0)
        x=abs(x)
        ret = -0.0187293
        ret = ret * x
        ret = ret + 0.0742610
        ret = ret * x
        ret = ret - 0.2121144
        ret = ret * x
        ret = ret + 1.5707288
        ret = ret * m.sqrt(1.0-x)
        ret = ret - 2 * negate * ret
        return negate * 3.14159265358979 + ret

