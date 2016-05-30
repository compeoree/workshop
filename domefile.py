# Python 3
# domefile.py

import re
from domemath import fn6
from pydome import *

VERTEX, EDGE, FACE = 0, 1, 2

def re_search(src, i, pattern, is_single=True):
        s = src[i]
        if is_single:
                m = re.search(pattern, s)
                return m.group()
        else:
                m = re.findall(pattern, s)
                return m

def re_extract_list(start, size, pattern, list_type, is_float=True):
        tt = list()
        end = start + int(size)
        for i in range(start, end):
                x, y, z = re_search(lines, i, pattern, is_single=False)
                item = [fn6(x), fn6(y), fn6(z)]
                tt.append(item)
        print("size of V", len(V))


# Read OpenSCAD dome file 
def read_dome(filename):
        import re
        

        ifile = open(filename, 'r')

        lines = ifile.readlines()
        ifile.close()
        size = len(lines)
        for i in range(size):
                line0 = lines[i]
                line = line0.rstrip('\r\n')
                print(i, line)

        t = lines[0]
        dome_stamp = t[2:]
        
        frq = re_search(lines, 2, '\d+', is_single=True)
        radius = re_search(lines, 3, '\d+\.\d+', is_single=True)
        vnum = re_search(lines, 4, '\d+', is_single=True)

        print(dome_stamp, frq, radius, vnum)

        V = list()
        start = 6
        end = start + int(vnum)
        for i in range(start, end):
                x, y, z = re_search(lines, i, '[-]?\d+\.\d+', is_single=False)
                print(i, ": ", x, y, z)
                v = [fn6(x), fn6(y), fn6(z)]
                V.append(v)
        print("size of V", len(V))




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



# Obsolete 
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


