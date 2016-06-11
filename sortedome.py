# Python 3.4
# sortedome.py 
#
# Create a sorted dome 
# 
#               +                    - 1th level (1 vertex)
#       +               +            - 2th level 
#  
#   +                        +       - 3th level
#                                         ...
#                                       
#    +                      +        - Nth level (bottom) 
#
# A level is ordered set of vertices on xy plane by z coordinate  
#

from domemath import *
from domeutil import *
from copy import deepcopy

SDEBUG = False

# Unit circle
pp = [(1.0, 0.0),       # 0
        (0.87, 0.5),    # 30
        (0.5, 0.87),    # 60
        (0.0, 1.0),     # 90
        (-0.5, 0.87),   # 120 
        (-0.87, 0.5),   # 150
        (-1.0, 0.0),    # 180
        (-0.87, -0.5),  # 210
        (-0.5, -0.87),  # 240
        (-0.0, -1.0),   # 270
        (0.5, -0.87),   # 300
        (0.87, -0.5)    # 330
        ]


class Vertex:
        def __init__(self, x=0.0, y=0.0, z=0.0):
                self.level, self.pos = None, None
                self.p = Point(x, y, z, prec=3)
                self.zkey = round(z, 3)

                a = calculate_angle(self.p.x, self.p.y, 1.0, 0.0)
                self.angle = round(a, 2) 

        def find_angle(self, x=1.0, y=0.0):
                a = calculate_angle(self.p.x, self.p.y, x, y)
                self.angle = round(a, 2) 

        def set_zkey(self):
                self.zkey = round(self.p.z, 4)

        def set_level(self, l1):
                self.level = int(l1)

        def set_pos(self, pos1):
                self.pos = int(pos1)

        def point(self):
                return self.p 

        def xyz(self):
                return self.p.x, self.p.y, self.p.z 

        def __str__(self):
                return "Vertex<{0}-{1}, {2}, {3}>".format(self.level, self.pos,
                                self.p, self.angle)

# List of edges,[[0, 1, 6.56, "-"], [0, 2, #.##, "-"], ... ]
class EdgeTypes:
        def __init__(self, edges):
                self.typecount = 0
                self.edgetypes = list()
                self.t = deepcopy(edges) 

                # Sort by length        
                self.t2 = sorted(self.t, key=lambda e: e[2], reverse=False)

        def _color_code(self, n):
                import math

                i = n-1 
                if i == 0:
                        return [1, 0, 0]
                elif i == 1:
                        return [0, 1, 0]
                elif i == 2:
                        return [0, 0, 1]
                elif i > 2:
                        x = math.radians(5*i)
                        r = 0.5 + math.sin(x)/2
                        g = 0.5 + math.cos(x)/2
                        b = 0.5 + (r + g)/4
                        return [round(r, 2), round(g, 2), round(b, 2)]


        def process(self):
                dt = {}
                for e in self.t2:
                        v0, v1, key = e[0], e[1], e[2]
                        dt.setdefault(key, []).append((v0, v1))

                # Let's number to string conversion later    
                # i, base = 0, ord('A')
                # n = base + i 
                # chr(n) 
                tag = 1
                for key in dt.keys():
                        tag_num = len(dt[key])
                        r, g, b = self._color_code(tag)
                        self.edgetypes.append([key, tag, r, g, b, tag_num])
                        tag += 1
                dt.clear()


        def value(self):
                return self.edgetypes 


def create_vertex_dict(src):
        """ Create a vertex dictionary """
        d = dict()
        size = len(src)

        item = src[0]
        if type(item) == type(list()):
                for i in range(size):
                        v = src[i] 
                        key = "{0:6.3f}{1:6.3f}{2:6.3f}".format(v[0], v[1], v[2])
                        d[key] = i
        else:
                for i in range(size):
                        v = src[i]
                        x, y, z = v.xyz()
                        key = "{0:6.3f}{1:6.3f}{2:6.3f}".format(x, y, z)
                        d[key] = i
        return d


# list of vertex lists 
def create_vertex_levels(src):
        tt, t, i = list(), list(), 0 
        level_count = 0
        oldz = src[0].zkey 
        for i in range(len(src)):
                _curr = src[i] 
                currz = _curr.zkey
                v = Vertex(_curr.p.x, _curr.p.y, _curr.p.z)
                if oldz != currz: 
                        level_count += 1
                        tt.append(t[:])
                        del t[:]
                v.set_level(level_count)
                t.append(v)
                oldz = currz
        tt.append(t[:])      # last element
        return tt

# Sort each vertex level by angle 
def sort_angle(src):
        for i in range(len(src)):
                if len(src[i]) > 1:
                        tmp = sorted(src[i], key=lambda p: p.angle)
                        src[i] = tmp
                        for j in range(len(src[i])):
                                v = src[i][j]
                                v.set_pos(j)
                else:
                        v = src[i][0]
                        v.set_pos(0)

        return deepcopy(src)


# Convert the levels to one dimensional array 
def get_1d_array(src):
        tt = list()
        for i in range(len(src)):
                ECHO("\tLevel - {}".format(i), SDEBUG)
                sz = len(src[i])
                if sz > 1:
                        ECHO("\t {} vertices".format(sz), SDEBUG)
                        for v in src[i]:
                                tt.append(v)
                else:
                        ECHO(src[i][0], SDEBUG)
                        tt.append(src[i][0])
        return tt


# src is a list of Point objects
def sort_vertices(src):
        tmp = list()
        for p in src:
                v = Vertex(p.x, p.y, p.z)
                tmp.append(v)

        # Sort by z coordinate       
        tmp2 = sorted(tmp, key=lambda v: v.zkey, reverse=True)
        del tmp[:]
       
        levels1 = create_vertex_levels(tmp2)
        levels2 = sort_angle(levels1)
        ov = get_1d_array(levels2)

        return ov 

# A table that maps original vertices to sorted ones 
def get_v2ov_map(vsrc, ovsrc):
        # original verticies  
        vd = create_vertex_dict(vsrc)
        ovd = create_vertex_dict(ovsrc)

        v2ov = dict()
        for key in ovd:
                i = vd[key]
                v2ov[i] = ovd[key]

        return v2ov 

def _sort_edges_debug(src1, src2, debug=False):
        if debug is False:
                return

        print("_sort_edges_debug():")
        for i in range(len(src2)):
                v0, v1, d, bar = src2[i] 
                w1, w2, w3, w4 = src1[i].value()
                print("{}: ({}, {}, {})  {}, {}".format(i, v0, v1, d, w1, w2))

# Edge: v0, v1, length, name 
def sort_edges(src, vmap):
        # Create new edges 
        # [ 0,  1,  6.558388, "-"], ... 
        tt = list()
        for edge in src:
                v0, v1, d, bar = edge.value()
                v = vmap[v0]
                w = vmap[v1]
                tt.append([v, w, d, bar])
        
        _sort_edges_debug(src, tt, SDEBUG)
        return tt


# Create new faces 
# [0, 1, 2], ... 
def sort_faces(src, vmap):
        tt = list()
        for face in src:
                _a, _b, _c = face.value()
                a = vmap[_a] 
                b = vmap[_b]
                c = vmap[_c] 
                tt.append([a, b, c])

        return tt 


# Save data of sorted dome in OpenSCAD code 
# vsrc: list of Vertex 
# esrc: list of [0, 1, fn, "type"] 
# fsrc: list of [0, 1, 2] 
# etsrc: list of [key, tag, r, g, b, tag_num] 
def write_scad(vsrc, esrc, fsrc, etsrc, radius, frq, filename):
        stamp = get_title("Sorted dome", "test")

        array_head = ["V = [\n", "E = [\n", "F = [\n", "ET = [\n"]
        array_tail = "];\n\n"

        of = open(filename, 'w')
        of.write("// {}".format(stamp))
        of.write("// Frequency: {}\n".format(frq))
        of.write("// Radius: {}\n".format(radius))

        size = len(vsrc)
        of.write("//Vertices: {}\n".format(size))
        of.write(array_head[0])
        for i in range(size):
                v = vsrc[i]
                if i == size-1:
                        of.write("\t[{0:8.3f}, {1:8.3f}, {2:8.3f}]  //{3:3d} {4}-{5}\n".format(v.p.x, v.p.y, v.p.z, i, v.level, v.pos))
                else:
                        of.write("\t[{0:8.3f}, {1:8.3f}, {2:8.3f}], //{3:3d} {4}-{5}\n".format(v.p.x, v.p.y, v.p.z, i, v.level, v.pos))
        of.write(array_tail)

        size = len(esrc)
        of.write("// Edges: {}\n".format(size))
        of.write(array_head[1])
        for i in range(len(esrc)):
                e = esrc[i]
                name = esrc[3]
                etype = name if name != None else "-"
                if i == size-1:
                        of.write("\t[{0:2d}, {1:2d}, {2:8.3f}, \"{3}\"]  // {4:3d}\n".format(
                                                e[0], e[1], e[2], e[3], i))
                else:
                        of.write("\t[{0:2d}, {1:2d}, {2:8.3f}, \"{3}\"], // {4:3d}\n".format(
                                                e[0], e[1], e[2], e[3], i))
        of.write(array_tail)

        size = len(fsrc)
        of.write("// Faces: {}\n".format(size))
        of.write(array_head[2])
        for i in range(size):
                f = fsrc[i]
                if i == size-1:
                        of.write("\t[{0:2d}, {1:2d}, {2:2d}]  //{3:3d} \n".format(
                                                f[0], f[1], f[2], i))
                else:
                        of.write("\t[{0:2d}, {1:2d}, {2:2d}], //{3:3d} \n".format(
                                                f[0], f[1], f[2], i))
        of.write(array_tail)

        size = len(etsrc)
        of.write("// Edge types: {}\n".format(size))
        of.write(array_head[3])
        for i in range(size):
                key, tag, r, g, b, tag_num = etsrc[i]
                if i == size-1:
                        of.write("\t[{}, {}, {}, {}, {}, {}] //{} \n".format(
                                                key, tag, r, g, b, tag_num, i))
                else:
                        of.write("\t[{}, {}, {}, {}, {}, {}], //{} \n".format(
                                                key, tag, r, g, b, tag_num, i))
        of.write(array_tail)

        of.close()


def process_sorted_dome(vertices, edges, faces):
        print("wip")


#
# Create hub datatype to model 3D parts in OpenSCAD.  
#
# Outer vertices and one center vertex forms one hub
# Each spoke, i.e 0-1, has bend angle. 
#
#            2 
#                  
#                  
#     3             1  
#            0     
# 
#      
#       4         5 
#
#
class Hub:
        """  index: center vertex 
          vertices: list of outer vertices 
          index = 0 
          Spoke = [1, 2, 3, 4, 5]
          It forms len(vertices), i.e. 5 spokes. 

        """
        def __init__(self, index, vertices):
                self.index = index
                self.Spoke = vertices
                self.Angle = dict()
                self.radius = None
                self.angle_info = ''
                self.lable = ''

        # key = other vertex 
        def compute_bend_angle(self):
                x, y, z = V[self.index]
                a = Point(x, y, z)
                for i in self.Spoke:
                        key = i 
                        x, y, z = V[i]
                        b = Point(x, y, z)
                        self.Angle[key] = bend_angle(a, b) 

        def set_angle_info(self, types):
                info = ''
                for k, a in self.Angle.items():
                        t = types[a]   
                        info += '-{}'.format(t)
                self.angle_info = info[1:]

        # (angle_info, lable, count)
        # ('A0-A0-A0-A0', 'L0', 5)
        def get_lable(self, types):
                for key, lable, n in types:
                        if key == self.angle_info:
                                return lable
                print("get_lable(): {} is failed.".format(key))
                return ''
## Hub 

class HubLable:
        """ Store hub lables """
        def __init__(self, vsrc, fsrc):
                self.Hub = self.generate_hubs(vsrc, fsrc)
                self.Angle_type = self.get_angle_types()
                self.Lable_type = self.get_lable_types()

        # Prepare basic hubs using faces 
        def create_hub(self, x, faces):
                flist = list()
                for f in faces:
                        a, b, c = f
                        if x == a or x == b or x == c:
                                flist.append(f)
                t = set()
                for f in flist:
                        t |= set(f)   # union operator 
                        h = list(t)
                        h.sort()

                return list(h), flist  

        
        def generate_hubs(self, vsrc, fsrc):
                # buf for debugging 
                _hub, buf = list(), list()
                vertex = [x for x in range(len(vsrc))]
                for v in vertex:
                        h, b = self.create_hub(v, fsrc)
                        _hub.append(h)
                        buf.append(b)

                _hub2 = dict()
                for i in range(len(_hub)):
                        key = i
                        val = _hub[key] # remove the key in the spokes
                        val.remove(key)
                        _hub2[key] = val
              
                hbag = list()
                for key, val in _hub2.items():
                        h = Hub(key, val)
                        h.compute_bend_angle()
                        hbag.append(h)

                del _hub[:], buf[:]
                _hub2.clear() 

                return hbag 

        # Use set to remove duplicate angles 
        def get_angle_set(self, src, i):
                h = src[i]
                t = list()
                for k, a in h.Angle.items():
                        t.append(a)

                return set(t)

        # key: angle in number 
        # value: 'A[N]'
        # {15.86: 'A0', 18.0: 'A1'}
        def get_angle_types(self):
                buf = set()
                for i in range(len(self.Hub)):
                        t = self.get_angle_set(self.Hub, i)
                        buf |= t

                buf2 = list(buf)
                buf2.sort()
                d = dict()
                for i in range(len(buf2)):
                        key = buf2[i]
                        d[key] = 'A{}'.format(i)

                buf.clear()
                del buf2[:]
                return d


        # Create unique lables using angle_info 
        def get_lable_types(self):
                t = list()
                for i in range(len(self.Hub)):
                        h = self.Hub[i]
                        h.set_angle_info(self.Angle_type)
                        t.append(h.angle_info)

                lables = sorted(t)
                del t[:]

                count, end = 1, len(lables)
                lt, old = list(), lables[0]
                lt.append([old, count])
                for i in range(1, end):
                        cur = lables[i]
                        if old == cur:
                                count += 1
                        else:
                                it = lt[-1]     # last element  
                                it[1] = count 
                                count = 1
                                lt.append([cur, 1])
                        old = cur 
                lt[-1][1] = count

                lt2 = list()
                for i in range(len(lt)):
                        l, n = lt[i]
                        lable = 'L{}'.format(i)
                        lt2.append((l, lable, n))
                del lt[:]

                return lt2

        def set_lables(self):
                for i in range(len(self.Hub)):
                        h = self.Hub[i]
                        h.lable = h.get_lable(self.Lable_type)
## HubLable 

