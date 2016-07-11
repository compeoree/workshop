# Python 3.4
from domemath import *

import math as m

# Frequency: 2
# Radius: 30.0
#Vertices: 36 [x, y, z] 
V = [
        [   0.000,    0.000,   30.000], #  0 0-0
        [  15.772,    0.000,   25.520], #  1 1-0
        [   4.874,   15.000,   25.520], #  2 1-1
        [ -12.760,    9.270,   25.520], #  3 1-2
        [ -12.760,   -9.270,   25.520], #  4 1-3
        [   4.874,  -15.000,   25.520], #  5 1-4
        [  20.646,   15.000,   15.772], #  6 2-0
        [  -7.886,   24.270,   15.772], #  7 2-1
        [ -25.520,    0.000,   15.772], #  8 2-2
        [  -7.886,  -24.270,   15.772], #  9 2-3
        [  20.646,  -15.000,   15.772], # 10 2-4
        [  26.833,    0.000,   13.416], # 11 3-0
        [   8.292,   25.520,   13.416], # 12 3-1
        [ -21.708,   15.772,   13.416], # 13 3-2
        [ -21.708,  -15.772,   13.416], # 14 3-3
        [   8.292,  -25.520,   13.416], # 15 3-4
        [  28.532,    9.270,    0.000], # 16 4-0
        [  17.634,   24.271,    0.000], # 17 4-1
        [   0.000,   30.000,    0.000], # 18 4-2
        [ -17.634,   24.271,    0.000], # 19 4-3
        [ -28.532,    9.271,    0.000], # 20 4-4
        [ -28.532,   -9.270,    0.000], # 21 4-5
        [ -17.634,  -24.271,    0.000], # 22 4-6
        [   0.000,  -30.000,    0.000], # 23 4-7
        [  17.634,  -24.271,    0.000], # 24 4-8
        [  28.532,   -9.270,    0.000], # 25 4-9
        [  21.708,   15.772,  -13.416], # 26 5-0
        [  -8.292,   25.520,  -13.416], # 27 5-1
        [ -26.833,    0.000,  -13.416], # 28 5-2
        [  -8.292,  -25.520,  -13.416], # 29 5-3
        [  21.708,  -15.772,  -13.416], # 30 5-4
        [  25.520,    0.000,  -15.772], # 31 6-0
        [   7.886,   24.271,  -15.772], # 32 6-1
        [ -20.646,   15.000,  -15.772], # 33 6-2
        [ -20.646,  -15.000,  -15.772], # 34 6-3
        [   7.886,  -24.271,  -15.772]  # 35 6-4
        ]

# test function 
def load_vertex(src):
        t = list()
        for i in range(len(src)):
                x, y, z = src[i]
                t.append(Point(x, y, z, prec=3))

        return t



# Axis angles of a vector P(x, y, z)
# alpha - x axis 
# beta - y axis         // Do not need. 
# gamma - z axis 
#
#      P (x, y, 0)
#     /|
#    / |  
#   /  |
#  +---+----> X
#    x            
#                 x
#  alpha = acos(----)
#                |P|
#

# Two axis angles are sufficent to represent the vector?
def get_axis_angle(vec):
        x, y, z = vec.x, vec.y, vec.z 

        d = m.sqrt(x*x + y*y + z*z)
        _a = m.acos(x/d)
        _g = m.acos(z/d)
        alpha = m.degrees(_a) if y >= 0.0 else 360.0 - m.degrees(_a)
        gamma = m.degrees(_g)
       
        return fn6(alpha, 2), fn6(gamma, 2) 

# 
# Spherical coordinate 
#
# P(x, y, z) = S(r, theta, phi)
# r is length of P from origin, 
# theta is x axis angle to r_pro on xy plane,
# phi is z axis angle to vector P. 
# 
# r_pro = r*sin(theta)
# x = r_pro * cos(phi) = r * cos(phi) * sin(theta)
# y = r_pro * sin(phi) = r * sin(phi) * sin(theta)
# z = r * cos(theta)
# r = sqrt(x^2 + y^2 + z^2)
#               
# theta = arccos(z/r)
#
#     y                          x
# ---------- = sin(theta) = -----------
# r*sin(phi)                 r*cos(phi)
# 
# phi = arctan(y/x)
# 
def get_sph_coordinate(vec):
        x, y, z = vec.x, vec.y, vec.z 

        r = m.sqrt(x*x + y*y + z*z)
        _th = m.acos(z/r)
        
        # y/0 = oo, ZeroDivisionError 
        # 90.0 = pi/2 
        _ph = m.pi/2 if x == 0.0 else m.atan(y/x)  
        theta = m.degrees(_th)
        print(m.degrees(_ph))
        if x >= 0.0 and y >= 0.0: 
                phi = m.degrees(_ph) 
        elif x < 0.0 and y >= 0.0:
                phi = 180 + m.degrees(_ph)
        elif x <= 0.0 and y < 0.0:
                phi = 180 + m.degrees(_ph)
        elif x > 0.0 and y < 0.0:
                phi = 360 + m.degrees(_ph)

        return fn6(r, 3), fn6(theta, 2), fn6(phi, 2) 

# Apply Rz ang Ry matrices to a vector.
def do_Rz_Ry(phi, theta, vec):
        v2 = Rz(-phi, vec)
        v3 = Ry(-theta, v2)

        return v3


def test_func(vec):
        r, theta, phi = get_sph_coordinate(vec)
        vec2 = do_Rz_Ry(phi, theta, vec)
        print('Input vector =', vec)
        print('r = {}, phi = {}, theta = {}'.format(r, phi, theta))
        print('Output vector =', vec2)


# return cos(x), sin(x) 
def get_cos_sin(x):
        rad = m.radians(x)
        c = m.cos(rad)
        s = m.sin(rad)

        return c, s


# Rotation matrices in right-hand coordinate system
#       c = cos(o), s = sin(o)
#
#         1  0  0
# Rx(o) = 0  c -s
#         0  s  c 
#
# Input vector = [x, y, z]
# Output vector = [x, c*y - s*z, c*z + s*y]
# 
def Rx(angle, vec):
        x, y, z = vec.x, vec.y, vec.z 
        c, s = get_cos_sin(angle)      
 
        x2 = x
        y2 = c*y - s*z
        z2 = c*z + s*y

        return Point(x2, y2, z2)


#
#          c  0  s
# Ry(o) =  0  1  0
#         -s  0  c 
#
# Input vector = [x, y, z]
# Output vector = [c*x + s*z, y, c*z - s*x]
#
def Ry(angle, vec):
        x, y, z = vec.x, vec.y, vec.z
        c, s = get_cos_sin(angle)

        x2 = c*x + s*z 
        y2 = y
        z2 = c*z - s*x 

        return Point(x2, y2, z2)

#
#         c  -s  0
# Rz(o) = s   c  0
#         0   0  1 
# 
# Input vector = [x, y, z]
# Output vector = [c*x - s*y, c*y + s*x, z]
#
def Rz(angle, vec):
        x, y, z = vec.x, vec.y, vec.z 
        c, s = get_cos_sin(angle)

        x2 = c*x - s*y
        y2 = c*y + s*x
        z2 = z 

        return Point(x2, y2, z2)

VV = load_vertex(V)

