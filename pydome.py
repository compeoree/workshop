#
#    pydome - Geodesic dome construction program 
#    Copyright (C) 2016  Hughe <janpenguin@riseup.net>   
#
#    This file is part of pydome.
#
#    pydome is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#

# Python 3.4 
# pydome.py 

from domemath import *
from domeutil import * 
import sortedome as sd 
from copy import deepcopy    # deep copy a list object    


VERSION = "0.1"
PROGRAM = "pydome"
DEBUG = True 


# coordinates for icosahedron with edge length 1.05146 
# radius is 1.0
# Z is up 
# 12 vertices
_icos_vert0 = [
        [ 0.000000,  0.000000,  1.000000],  # 0 
        [ 0.894427,  0.000000 , 0.447214],  # 1
        [ 0.276393, -0.850651,  0.447214],  # 2
        [-0.723607, -0.525731,  0.447214],  # 3
        [-0.723607,  0.525731,  0.447214],  # 4
        [ 0.276393,  0.850651,  0.447214],  # 5
        [-0.894427,  0.000000, -0.447214],  # 6 
        [-0.276393,  0.850651, -0.447214],  # 7 
        [ 0.723607,  0.525731, -0.447214],  # 8 
        [ 0.723607, -0.525731, -0.447214],  # 9 
        [-0.276393, -0.850651, -0.447214],  # 10 
        [ 0.000000,  0.000000, -1.000000]   # 11
        ]

# Sorted by quadrant order of Cartesian coordinate system 
_icos_vert = [
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
_icos_edge0 = [
        [0, 1, 0., None],   [0, 2, 0., None],   [0, 3, 0., None],
        [0, 4, 0., None],   [0, 5, 0., None],   [1, 2, 0., None],
        [2, 3, 0., None],   [3, 4, 0., None],   [4, 5, 0., None],
        [5, 1, 0., None],   [1, 9, 0., None],   [9, 2, 0., None],
        [2, 10, 0., None],  [10, 3, 0., None],  [3,6,0., None],
        [6, 4, 0., None],   [4, 7, 0., None],   [7, 5, 0., None],
        [5, 8, 0., None],   [8, 1, 0., None],   [6, 7, 0., None],
        [7, 8, 0., None],   [8, 9, 0., None],   [9, 10, 0., None],
        [10, 6, 0., None],  [11, 7, 0., None],  [11, 8, 0., None],
        [11, 9, 0., None],  [11, 10, 0., None], [11, 6, 0., None]
        ]

_icos_edge = [
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
_icos_face0 = [
        [0, 2, 1],
        [0, 3, 2],
        [0, 4, 3],
        [0, 5, 4],
        [0, 1, 5],
        [1, 2, 9],
        [2, 10, 9],
        [2, 3,10],
        [3, 6, 10],
        [3, 4, 6],
        [4, 7, 6],
        [4, 5, 7],
        [5, 8, 7],
        [5, 1, 8],
        [1, 9, 8],
        [11, 6, 7],
        [11, 7, 8],
        [11, 8, 9],
        [11, 9, 10],
        [11, 10, 6]
        ]

# 20 faces 
_icos_face = [ 
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

global f0dome, tdome, Vv

# Number of objects to print in _print_object() 
global print_size 

print_size = 8

def _print_object(obj, size=0, header="_print_object()"):
        start, end = 0, len(obj)
        if end > 0: 
                if size == 0:
                        start = 0
                elif end > size:
                        start = end - size 
                print("{}: {} to {}".format((header), start, end))
                for i in range(start, end):
                        print(i, obj[i])
        else:
                print("{}: {}".format(header, "Empty container!!"))


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


class Edge:
        """ 
        Edge has two vertices, length, name.
                Default length unit is mm, decimal point to two.
        """
        def __init__(self, v0=0, v1=0):
                self.v0 = int(v0)
                self.v1 = int(v1)
                self.length = None
                self.name = '-' 

        def set_length(self, val, metric=True):
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


# Vertex
class Vertex0:
        SZ = 6  # size of integer array (list) 
        def __init__(self, v1, n1, edgelist1):
                self.vtx = v1
                self.nedge = n1
                self.edges = deepcopy(edgelist1)

        def __str__(self):
                s1 = 'Vertex <{0}, {1} '.format(self.vtx, self.nedge)
                s2 = str(self.edges)
                return s1+s2 


def _Dome_init_helper(lst):
        if lst is None:
                return list(), 0
        else:
                return deepcopy(lst), len(lst)


class Dome:

        def __init__(self, metric=True, r=10.0, nu=2, vertexlist=None, edgelist=None,
                        facelist=None):
                self.unit, self.radius, self.frq = metric, r, nu 
                self.V, self.nvert = _Dome_init_helper(vertexlist)
                self.E, self.nedge = _Dome_init_helper(edgelist)
                self.F, self.nface = _Dome_init_helper(facelist)
       
                # total number of verticies, edges, and faces 
                self.nV, self.nE, self.nF = 0, 0, 0 
                self.L, self.nL = None, 0

        def set_dimension(self, v, e, f):
                self.nV, self.nE, self.nF = v, e, f


        # Point object 
        def add_vertex(self, other):
                t = Point(other.x, other.y, other.z)
                self.V.append(t)
                self.nvert = len(self.V) 
                print("__ add_vertex(): {} {}, {}, {}".format(self.nvert-1, 
                                                            t.x, t.y, t.z))

        # Edge object 
        def add_edge(self, other):
                t = Edge(other.v0, other.v1) 
                self.E.append(other)
                self.nedge = len(self.E)
                print("__ add_edge(): {} {}-{}".format(self.nedge-1, 
                                                    t.v0, t.v1))

        # Face object
        def add_face0(self, other):
                t = Face(other.A, other.B, other.C)
                self.F.append(t)
                self.nface = len(self.F) 
                print("__ add_face(): {} <{}, {}, {}>".format(self.nface-1, 
                                                    t.A, t.B, t.C))

        # Return i-th Point in self.V 
        def vertex(self, i):
                return self.V[i] if i < len(self.V) else -1
    
        # Return i-th Edge in self.E
        def edge(self, i):
                return self.E[i] if i < len(self.E) else -1

        # Return i-th Face in self.F
        def face(self, i):
                return self.F[i] if i < len(self.F) else -1

        # Helper function
        def _edge_length(self, pos):
                e = self.E[pos]

                # Get two Points
                a, b = self.V[e.v0], self.V[e.v1]
                d = ptDist(a, b)
                self.E[pos].set_length(d, self.unit)     

        # Compute the length of one or all edges
        def compute_edge_length(self, pos=None):
                if pos is None:
                        for i in range(self.nedge):
                                self._edge_length(i)
                elif 0 <= pos < self.nedge:
                        self._edge_length(pos)
                else:
                        print(pos, ": out of range")

        # Print edge data 
        def report_edge(self, pos=None):
                if pos is None:
                        for i in range(self.nedge):
                                print(i, ": ",  self.E[i]) 
                elif 0 <= pos < self.nedge:
                        print(pos, ": ", self.E[pos])
                else:
                        print(pos, ": out of range")


        def normalize(self, frac=1.0):
                """
                Normalize all the vertices in a dome to the specified sphere. 
                    float r: the sphere radius 
                    float frac
                """
                for i in range(self.nvert):
                        _v = self.V[i]
                        self.V[i] = normalize_vertex(_v, self.radius, frac)

                self.compute_edge_length()


        # Scale the dome by factor
        # Usually factor is dome radius. 
        def scale(self, Mx):
                for i in range(self.nvert):
                        _v = self.V[i]
                        x = fn6(Mx * _v.x)
                        y = fn6(Mx * _v.y)
                        z = fn6(Mx * _v.z)
                        self.V[i] = Point(x, y, z)

                self.compute_edge_length()


        def find_edge(self, v0, v1):
                """
                Return the index of the edge that matches this one.
                    int  v0, v1  vertices to match
                    Dome dome    containing vertices and edges
                """
                size = len(self.E)
                for i in range(size):
                        e = self.edge(i)
                        if (v0 == e.v0 and v1 == e.v1) or (v0 == e.v1 and v1 == e.v0):
                                print("\tfind_edge(): {}: {}-{} vs {}".format(i, v0, v1, e))
                                return i
                return None


        def match_edge(self, v0, v1):
                """
                 Return the index of the edge that matches this one.  Insert if needed.
                    int v0, v1: vertices to form the edge  
                    Domex dome: the dome object containing vertices and edges
                """
                if self.nedge > self.nE:
                        print("match_edge(): out of edges")
                        return -1

                # Add new Edge object 
                pos = self.find_edge(v0, v1)
                if pos is None:
                        e = Edge(v0, v1)
                        self.add_edge(e)
                        print("match_edge(): NEW ", e)
                else:
                        print("match_edge(): {}-{} exists {}".format(v0, v1, self.edge(pos)))


        def vtx_find0(self, target):
                M = 1000000
                epsilon = 0.1 * M

                for i in range(len(self.V)):
                        v = self.vertex(i)
                        if int(M * ptDist(v, target)) < epsilon:
                                print("\t\t vtx_find0(): {} == {}".format(v, target))
                                return i
                return -1

   
        # integer number comparision
        def vtx_find1(self, target):
                M = 1000000
                ix = int(target.x * M) 
                iy = int(target.y * M)
                iz = int(target.z * M)
                        
                print("vtx_find1(): ({}, {}, {})->({},{},{})".format(target.x,
                                                target.y, target.z, ix, iy, iz))
                for i in range(len(self.V)):
                        v = self.vertex(i)
                        jx = int(v.x * M) 
                        jy = int(v.y * M)
                        jz = int(v.z * M)
                        if ix == jx and iy == jy and iz == jz:
                                print("\t\t vtx_find1({}): ({}, {}, {})".format(i, jx, jy, jz))
                                print("\t\t vtx_find1({}): {} == {}".format(i, v, target))
                                return i
                return -1

        def match_vtx(self, target):
                """
                Return the index of vertex that matches this one.
                Insert if needed.
                Point: vtx 
                Dome: dome
                """
                print("match_vtx(): Target = ", target)

                # Check the vertex in Dome's vertex array
                pos = self.vtx_find0(target)
                if pos != -1:
                        return pos

                if self.nvert > self.nV: # nvert
                        print("match_vtx(): out of vertices in tesselate")
                        return

                # Add new vertex - Point object 
                self.add_vertex(target)

                # [0 ... vertex_count-1] 
                return self.nvert-1

        def add_face(self, p0, p1, p2):
                """
                Append a face to the dome's face list. This may involve adding 
                vertices and edges too.
                    Point p0, p1, p2    3 vertices
                    Dome: dome
                    ptr_int nf, ne, nv: face, edge, and vertex count 
                """
                print("\nadd_face(): START")
                global print_size

                print("add_face(): p0 ", p0)
                print("add_face(): p1 ", p1)
                print("add_face(): p2 ", p2)
                _print_object(self.V, print_size, "add_face()")  
                print_size += 1

                if self.nface > self.nF:   # nFace
                        print("add_face(): Internal error: out of faces in tesselate.")
                        return

                # Find 3 vertices for the face
                v0 = self.match_vtx(p0)
                v1 = self.match_vtx(p1)
                v2 = self.match_vtx(p2)

                # Add new Face object 
                tFace = Face(v0, v1, v2)
                self.add_face0(tFace)

                # Add 3 Edge objects
                self.match_edge(v0, v1)
                self.match_edge(v1, v2)
                self.match_edge(v2, v0)
                print("add_face():  END\n")

        def tesselate1(self, din, face):
                """
                Tesselate one triangle
                    Dome din: input Dome 
                    Face face: face of input Dome  
                    int f: frequency number
                """
                f = self.frq        # frequency 
                frac = fn6(1.0 / f)

                p0, p1, p2 = din.vertex(face.A), din.vertex(face.B), din.vertex(face.C)
                v01, v02, v12 = ptSub(p1, p0), ptSub(p2, p0), ptSub(p2, p1)
                v01f, v02f, v12f = ptMul(v01, frac), ptMul(v02, frac), ptMul(v12, frac)

                if DEBUG:
                        print("  p0:", p0) 
                        print("  p1:", p1)
                        print("  p2:", p2)
                        print(" v01:", v01)
                        print(" v02:", v02)
                        print(" v12:", v12)
                        print("v01f:", v01f)
                        print("v02f:", v02f)
                        print("v12f:", v12f)
       
 
                for i in range(f):
                        j = 0
                        while j <= i: 
                
                                # Top of new triangle = p0 + v01f * i + v12f * j 
                                if i == 0 and j == 0:
                                        n0 = p0
                                else:
                                        _n0 = ptMul(v01, i*frac)
                                        _n1 = ptAdd(_n0, p0)
                                        n2 = ptMul(v12, j*frac)
                                        n0 = ptAdd(_n1, n2)

                                # 2nd point = top + v01f
                                if i == f-1 and j == 0:
                                        n1 = p1
                                else:
                                        n1 = ptAdd(n0, v01f)

                                # 3rd point = top + v02f
                                if i == f-1 and j == f-1:
                                        n2 = p2
                                else:
                                        n2 = ptAdd(n0, v02f)

                                print("\ntesselate1({}, {}): add_face(n0, n1, n2)".format(i, j))
                                print("tesselate1(): n0 ", n0)
                                print("tesselate1(): n1 ", n1)
                                print("tesselate1(): n2 ", n2)

                                self.add_face(n0, n1, n2)

                                if j < i:
                                        n1 = ptAdd(n0, v12f)
                                        print("\ntesselate1({}, {}): add_face(n0, n2, n1)".format(i, j))
                                        print("tesselate1(): n0 ", n0)
                                        print("tesselate1(): n2 ", n2)
                                        print("tesselate1(): n1 ", n1)
                                        self.add_face(n0, n2, n1)
                                j += 1 # end of inner loop

        def tesselate(self, inDome):
                """
                 Subdivide a dome.  Previous values in output dome are freed.

                    Dome: din, dout     input and result domes
                    self.frq            tesselation frequency, 2 or more.
                """
                # Set outDome's estimate dimension  
                nu = self.frq * self.frq

                # Number of faces 
                # F = face_number * nu  
                nf = inDome.nface * nu

                # Number of edges 
                ne = nf * 3

                # Number of vertices 
                nv = nf * 3

                self.set_dimension(nv, ne, nf)
                print("Py_tesselate(): V{}, E{}, F{}".format(self.nV,
                                                            self.nE, self.nF))
                for i in range(inDome.nface):
                        curFace = inDome.face(i)
                        if DEBUG:
                                print("Py_tesselate({}): {}".format(i, curFace))
                        self.tesselate1(inDome, curFace)

                if DEBUG:
                        print("Py_tesselate(): nface {}, nedge {}, nvert {}".format(
                                                self.nface, self.nedge, self.nvert))

        def _tesselate1_helper1(self, pos, lst):
                it = lst[pos]
                return Point(*it)

        def __str__(self):
                s0 = 'Dome:'
                s1 = 'radius: {}\n'.format(self.radius)
                s2 = 'vertices: {}\n'.format(self.nvert)
                s3 = 'edges: {}\n'.format(self.nedge)
                s4 = 'faces: {}\n'.format(self.nface)
                s5 = s0 + s1 + s2 +  s3 + s4
                return s5
        ## End of Dome 


def init_array(src_arr, obj_type, del_num):
        """ 
        Initialize array of given objects
        src_arr: default array data
        obj_type: Point | Edge | Face
        """
        buf = []
        size = len(src_arr) - del_num
        tPoint, tEdge, tFace = type(Point()), type(Edge()), type(Face())
        t = type(obj_type())

        for i in range(size):
                it = src_arr[i]
                if t == tPoint:
                        obj = Point(*it)
                elif t == tEdge:
                        it1 = it[:2]
                        obj = Edge(*it1)
                elif t == tFace:
                        obj = Face(*it)
                buf.append(obj)

        return deepcopy(buf)


# Create array of Point objects 
icos_vert = init_array(_icos_vert, Point, 1)

# Create array of Edge objects
icos_edge = init_array(_icos_edge, Edge, 5)

# Create array of Face objects
icos_face = init_array(_icos_face, Face, 5)

# Unit (Icosahedron) dome of radius 1.0 
f0dome = Dome(True, 1.0, 1, icos_vert, icos_edge, icos_face)

def normalize_cmd(dome, radius, f):
        """
        Normalize cdome to the desired radius.  Partial normalization is ok.
        Dome dome: Dome object
        float radius: radius of the dome
        float f: 
        """
        normalize_dome(dome, radius, f)


# Save dome data in OpenSCAD file
def write_dome2(dome, radius, filename):
        stamp = get_title(PROGRAM, VERSION)

        array_head = ["V = [\n", "E = [\n", "F = [\n"]
        array_tail = "];\n\n"

        of = open(filename, 'w')
        of.write("// {}".format(stamp))
        of.write("// Frequency: {}\n".format(dome.frq))
        of.write("// Radius: {}\n".format(radius))

        of.write("// Vertices: {}\n".format(dome.nvert))
        of.write(array_head[0])
        for i in range(dome.nvert):
                v = dome.V[i]
                if i == dome.nvert-1:
                        of.write("\t[{0:9.6f}, {1:9.6f}, {2:9.6f}]  //{3:3d}\n".format(v.x, v.y, v.z, i))
                else:
                        of.write("\t[{0:9.6f}, {1:9.6f}, {2:9.6f}], //{3:3d}\n".format(v.x, v.y, v.z, i))
        of.write(array_tail)

        of.write("// Edges: {}\n".format(dome.nedge))
        of.write(array_head[1])
        for i in range(dome.nedge):
                e = dome.E[i]
                etype = e.name if e.name != None else "-"
                if i == dome.nedge:
                        of.write("\t[{0:2d}, {1:2d}, {2:9.6f}, \"{3}\"]  // {4:3d}\n".format(e.v0, e.v1, 
                                                                                 e.length, etype, i))
                else:
                        of.write("\t[{0:2d}, {1:2d}, {2:9.6f}, \"{3}\"], // {4:3d}\n".format(e.v0, e.v1, 
                                                                                 e.length, etype, i))
        of.write(array_tail)

        of.write("// Faces: {}\n".format(dome.nface))
        of.write(array_head[2])
        for i in range(dome.nface):
                f = dome.F[i]
                if i == dome.nface-1:
                        of.write("\t[{0:2d}, {1:2d}, {2:2d}]  //{3:3d} \n".format(f.A, f.B, f.C, i))
                else:
                        of.write("\t[{0:2d}, {1:2d}, {2:2d}], //{3:3d} \n".format(f.A, f.B, f.C, i))
        of.write(array_tail)
        
        of.close()


def write_dome(dome, radius, filename):
        """ 
        Write out a dome file
        Dome dome: Dome object 
        string name: file name 
        """
        stamp = get_title() 

        of  = open(filename, 'w')
        of.write(stamp)
        of.write("Frequency: {}\n".format(dome.frq))
        of.write("Radius: {}\n".format(radius))

        of.write("Vertices: {}\n".format(dome.nvert))

        for i in range(dome.nvert):
                v = dome.V[i]
                of.write("{0:3d}: {1:9.6f}, {2:9.6f}, {3:9.6f}\n".format(i, v.x, v.y, v.z))
    
        of.write("\nEdges: {}\n\n".format(dome.nedge))
        for i in range(dome.nedge):
                e = dome.E[i]
                of.write("{0:3d}: {1:2d}, {2:2d}, {3:f} {4}\n".format( i, e.v0, e.v1, 
                                                e.length, e.name if e.name != None else '-')) 

        of.write("\nFaces: {}\n\n".format(dome.nface))
        for i in range(dome.nface):
                f = dome.F[i]
                of.write("{0:3d}: {1:2d}, {2:2d}, {3:2d}\n".format(i, f.A, f.B, f.C))
        of.close()


def tesselate_cmd(metric, radius, frq):
        """
        Initialize a tesselated dome.  Tesselate f0dome by the specified
        frequency and copy to cdome.
        int frq: freqency  
        float radius: radius of new dome
        """
        global f0dome

        adome = Dome(metric, radius, frq)
        adome.tesselate(f0dome)
        adome.scale(radius)
        adome.normalize()

        # Default file 
        fname  = "pydome.data"
        write_dome(adome, radius, fname)
        write_dome2(adome, radius, "pydome.scad")

        # Sort vertices, edges, faces  
        svertices = sd.sort_vertices(adome.V)
        vertex_map = sd.get_v2ov_map(adome.V, svertices)
        sedges = sd.sort_edges(adome.E, vertex_map)
        sfaces = sd.sort_faces(adome.F, vertex_map)

        et = sd.EdgeTypes(sedges)
        et.process() 
        edgetypes = et.value()
        for i in edgetypes:
                print(i)

        sd.write_sdome_scad(svertices, sedges, sfaces, radius, frq, "pydome_sorted.scad")


if __name__ == '__main__':

        # Radius 304.80 mm, frequency 3
        # tesselate_cmd(304.80, 3)
        
        # Radius 20 mm, frequency 2
        tesselate_cmd(True, 30.00, 4)


