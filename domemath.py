# Python 3.4 
# domemath.py 

import math as m        # math functions 

# mm to inch 
unit_mm = 0.0393700787402 

# Icosahedron
# Sorted by quadrant order of Cartesian coordinate system 
icos_vert = [
        [ 0.000000,  0.000000,  1.000000],  # 0

        [ 0.894427,  0.000000 , 0.447214],  # 1
        [ 0.276393,  0.850651,  0.447214],  # 2
        [-0.723607,  0.525731,  0.447214],  # 3
        [-0.723607, -0.525731,  0.447214],  # 4
        [ 0.276393, -0.850651,  0.447214],  # 5

        [ 0.723607,  0.525731, -0.447214],  # 6
        [-0.276393,  0.850651, -0.447214],  # 7
        [-0.894427,  0.000000, -0.447214],  # 8 
        [-0.276393, -0.850651, -0.447214],  # 9
        [ 0.723607, -0.525731, -0.447214],  # 10 

        [ 0.000000,  0.000000, -1.000000]   # 11
        ]

# 30 edges 
icos_edge = [
        [0, 1, 0., None],   [0, 2, 0., None],   [0, 3, 0., None],
        [0, 4, 0., None],   [0, 5, 0., None],   [1, 2, 0., None],
        [2, 3, 0., None],   [3, 4, 0., None],   [4, 5, 0., None],
        [5, 1, 0., None],   [1, 10, 0., None],   [1, 6, 0., None],
        [2, 6, 0., None],  [2, 7, 0., None],  [3, 7, 0., None],
        [3, 8, 0., None],   [4, 8, 0., None],   [4, 9, 0., None],
        [5, 9, 0., None],   [5, 10, 0., None],   [10, 6, 0., None],
        [6, 7, 0., None],   [7, 8, 0., None],   [8, 9, 0., None],
        [9, 10, 0., None],  [11, 6, 0., None],  [11, 7, 0., None],
        [11, 8, 0., None],  [11, 9, 0., None], [11, 10, 0., None]
        ]

# 20 faces 
icos_face = [
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 5],
        [0, 5, 1],
        [1, 2, 6],
        [2, 6, 7],
        [2, 3, 7],
        [3, 7, 8],
        [3, 4, 8],
        [4, 8, 9],
        [4, 5, 9],
        [5, 9, 10],
        [5, 1, 10],
        [1, 6, 10],
        [11, 6, 7],
        [11, 7, 8],
        [11, 8, 9],
        [11, 9, 10],
        [11, 10, 6]
        ]


def fn6(n, prec=6):
        """ Round off floating point number to prec """
        return round(float(n), prec)

def MIN(a, b):
        return a if a < b else b

def MAX(a, b):
        return a if a > b else b


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
                self.ix = int(self.x)
                self.iy = int(self.y)
                self.iz = int(self.z)
                self.angle = None

        def find_angle(self, x=1.0, y=0.0):
                a = calculate_angle(self.x, self.y, x, y)
                self.angle = round(a, 2)

        def xyz(self):
                return self.x, self.y, self.z 

        def __str__(self):
                return 'Point<{0:9.6f}, {1:9.6f}, {2:9.6f}>'.format(
                                                self.x, self.y, self.z)

class Edge:
        """ 
        Edge has two vertices, length, name.
                Default length unit is mm, decimal point to two.
        """
        def __init__(self, v0=0, v1=0, length=0, name='-'):
                self.v0 = int(v0)
                self.v1 = int(v1)
                self.length = fn6(length) 
                self.name = name

        def set_length(self, val, metric):
                self.length = fn6(val, 2) if metric is True else fn6(val, 4)

        def set_name(self, edgetype):
                self.name = edgetype

        def value(self):
                return self.v0, self.v1, self.length, self.name

        def __str__(self):
                if self.length is None:
                        return 'Edge<{0}, {1}>'.format(self.v0, self.v1)
                else:
                        return 'Edge<{0}, {1}, {2:9.6f}, {3}>'.format(self.v0, self.v1,
                                                    self.length, self.name)

class Face:
        """ Face has three vertices: A, B, C """

        def __init__(self, a=0, b=0, c=0):
                self.A = int(a)
                self.B = int(b)
                self.C = int(c)

        def set_(self, a, b, c):
                self.A = int(a)
                self.B = int(b)
                self.C = int(c)

        def value(self):
                return self.A, self.B, self.C

        def __str__(self):
                return 'Face<{}, {}, {}>'.format(self.A, self.B, self.C)


class Strut:
        """ Represent one group of identical struts  """
        def __init__(self, name='', length=0.0, a0=0.0, a1=0.0, count=0):
                self.name = name
                self.length = length
                self.a0 = fn6(a0, 2)
                self.a1 = fn6(a1, 2)
                self.count = count

        def __str__(self):
                return 'Strut<{}, {}, {}, {}, {}>'.format(self.name,
                                self.length, self.a0, self.a1, self.count)

# Create a vector from a to b
# vector = b - a
# Return Point object 
def pt_vector(a, b):
        x = b.x - a.x 
        y = b.y - a.y
        z = b.z - a.z 

        return Point(x, y, z)

        

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

# Geodome version
# vsrc is array of Point objects 
def find_vertex0(target, vsrc,  prec=6):
        Mx = 10 ** prec
        epsilon = 0.1 * Mx

        size = len(vsrc)
        for i in range(size):
                v = vsrc[i]
                distance = int(Mx * ptDist(v, target))
                if distance < epsilon:
                        return i
        return -1

# New version 
def find_vertex1(target, vsrc, prec=5):
        Mx = 10 ** prec
        x = int(Mx * target.x) 
        y = int(Mx * target.y)
        z = int(Mx * target.z)
        
        size = len(vsrc)
        for i in range(size):
                v = vsrc[i]
                x_ = int(Mx * v.x) 
                y_ = int(Mx * v.y)
                z_ = int(Mx * v.z)
                if x == x_ and y == y_ and z == z_:
                        return i
        return -1

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
        Point v: 
        Return the length between v and the origin. 
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


def normalize_vertex(vtx, r, frac):
        """
        Normalize a vertex so it has a specified radius from the center.
        Point vtx: a vertex 
        float r: radius of the sphere 
        float frac
        """
        frac1 = 1.0 - frac
        l = vlen(vtx)
        if l > 0.0 and frac > 0.0:
                l = frac/l + frac1
                l *= r
                x = vtx.x * l
                y = vtx.y * l
                z = vtx.z * l
                return Point(x, y, z)


#  Take a point, and project it to the "flattened" xy plane. 
def project_point(p, radius):
        zero = Point(0.0, 0.0, 0.0)

        """
        How do we flatten this?  Find the circumfrential distance
        from the top of the dome to the vertex, project the
        vertex that far from the center.

        Find the angle described by this point.  Since we're taking
        the angle relative to a vertical vector (0,0,1), this is
        trivially computed from the z component of the normalized
        vector.
        """
        _p0 = Point(p.x, p.y, p.z)
        p0 = normalize_vertex(_p0, 1.0, 1.0)
        print('p0:', p0)
        a = m.acos(p0.z)
        dist = a * radius
        p1 = Point(p.x, p.y, 0.0)
        print('p1:', p1)

        pp = project_point_on_line(zero, p1, zero, dist)
        if pp != None:
                pp.z = 0.0
                return pp 
        else:
                print("project_point(): failed to create the projected point")
                return None


#
# Find the projection of a point on a line, with optional offset.
#
# l0            first end point of line
# l1            second end point of line
# pt            point to project onto line
# offset        optional offset; returned point will be this much
#               further away from l0.
# return 
#       Point   new point on the line 
#       None    failure  
#
def project_point_on_line(l0, l1, pt, offset):  
        # Construct l0 to l1 vector, normalize it 
        # Use vnormalize(v)?
        # pt_vector(a, b):
        v1 = pt_vector(l0, l1)
        print(v1)
        len_ = vlen(v1) 
        if len_ == 0.0:
                return Point() 

        len_ = 1.0 / len_
        v1.x *= len_
        v1.y *= len_
        v1.z *= len_

        # Construct l0 to pt vector 
        v2 = pt_vector(l0, pt)

        # Use dot-product to project this vector on vetor v1.
        # It gives a distance, to which we add the offset.
        dist = dotprod(v1, v2) + offset

        # Compute the projected point - rval
        x = l0.x + dist*v1.x
        y = l0.y + dist*v1.y
        z = l0.z + dist*v1.z
        
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

