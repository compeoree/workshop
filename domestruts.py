# Python 3.4
# domestruts.py 
# Caculate strut types and bend angles of each strut type 

from domemath import *
from domefile import *
from domeutil import get_title

# Need to change these for mm unit 
margin = 0.75/12.0
bl = 0.75/12.0
at = 2.0
lt = 0.001
scale = 1.0

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

# Bending the ends of the pipe will shorten it slightly.
# returns the pre-bend length of the strut.
def bend_allowances(strut, bl):
        x1 = m.radians(strut.a0)
        x2 = m.radians(strut.a1)
        d = 1.0 - m.cos(x1)
        d += 1.0 - m.cos(x2) 
        return bl * d


def bend_angle(a, b):
        """
        Form two vectors: a to origin, a to b.
              + b | 
               \  | 
                \ |
                 \| 
        O+--------+ a

        Op0 = Op1 = radius 
        Return angle (90.0 - Op0p1) is ##.##  

        """
        v0, v1 = Point(-a.x, -a.y, -a.z), Point()
        len0 = vlen(v0)
        if len0 == 0.0:
                return 0.0

        len0 = 1.0 / len0      
        v0.x *= len0
        v0.y *= len0
        v0.z *= len0

        v1.x = b.x - a.x
        v1.y = b.y - a.y 
        v1.z = b.z - a.z
        len1 = vlen(v1)
        if len1 == 0.0:
                return 0.0

        len1 = 1.0 / len1
        v1.x *= len1
        v1.y *= len1
        v1.z *= len1

        x_ = dotprod(v0, v1)
        rad = m.acos(x_)
        theta = 90.0 - m.degrees(rad)

        return fn6(theta, 2)     


def match_strut(a, b, at, lt):
        """
        Return true if the two struts match within a small margin of error.
        """
        l0 = 1.0 - lt
        l1 = 1.0 + lt

        if b.length > a.length*l1 or b.length < a.length*l0:
                return False

        if (b.a0 >= a.a0-at) and (b.a0 <= a.a0+at) and \
                    (b.a1 >= a.a1-at) and (b.a1 <= a.a1+at):
                return True

        if (b.a0 >= a.a1-at) and (b.a0 <= a.a1+at) and \
                    (b.a1 >= a.a0-at) and (b.a1 <= a.a0+at):
                return False

        return False 

# tmp = compute_strut(vertices, edge)
# tmp.count = 1
def compute_strut(vsrc, edge):
        a = vsrc[edge.v0]
        b = vsrc[edge.v1]
        length = edge.length
        a0 = bend_angle(a, b)
        a1 = bend_angle(b, a)

        return Strut('', edge.length, a0, a1, 1) 

# https://docs.python.org/3.3/howto/sorting.html
def cmp_to_key(mycmp):
        'Convert a cmp= function into a key= function'
        class K:
                def __init__(self, obj, *args):
                         self.obj = obj
                def __gt__(self, other):
                        return mycmp(self.obj, other.obj) > 0
                def __ne__(self, other):
                        return mycmp(self.obj, other.obj) != 0
        return K


def strutcmp(a, b):
        # By frequency 
        n = b.count - a.count
        if n != 0:
                return n

        # By length 
        if b.length > a.length:
                return 1
        else:
                return -1


# Label all the struts by length and bend angles.
# Struts whose length are within .1% and angles within 2 degrees are identical.
def assign_labels(dome, at, lt):
        buf = list()
        
        for i in range(dome.nedge):
                edge = dome.edge(i)
                tmp = compute_strut(dome.V, edge)
                size, j = len(buf), 0
                while (j < size) and (not match_strut(buf[j], tmp, at, lt)):
                                j += 1
                if j >= size:
                        buf.append(tmp)
                else:
                        buf[j].count += 1

        S = sorted(buf, key=cmp_to_key(strutcmp))
        size = len(S)
        for i in S:
                print(i)

        for i in range(size):
                S[i].name = 'T{}'.format(str(i))
       
        for i in range(dome.nedge):
                edge = dome.edge(i)
                tmp = compute_strut(dome.V, edge)
                j = 0
                while j < size and (not match_strut(S[j], tmp, at, lt)):
                        j += 1
                edge.name = S[j].name

        return S 


def process_struts():
        import argparse as ap

        parser = ap.ArgumentParser(prog="domestruts", epilog="See instructions for more details.")
        parser.add_argument("dome_file", help="dome data file in OpenSCAD code")
        parser.add_argument("output_file", help="store strut data")
        parser.add_argument("-margin", default=1.60, type=float,
                        help="specify margin beyond the bolt hole (1.60)")
        parser.add_argument("-bl", default=1.60, type=float,
                        help="specify length of bend (1.60)")
        parser.add_argument("-at", default=2.0, type=float, 
                        help="angle tolerance in degrees (2.0)")
        parser.add_argument("-lt", default=0.1, type=float, 
                        help="length tolerance in percent (0.1)")
        parser.add_argument("-scale", default=1.0, type=float,
                        help="specify scale factor (1.0)")
        parser.add_argument("-cm", action="store_true", help="convert mm to cm unit")
        args = parser.parse_args()
                
        ifilename = args.dome_file
        ofilename = args.output_file
        margin = args.margin
        scale = args.scale
        cm_unit = args.cm

        adome = read_dome(ifilename)
        print(adome)

        strut_types = assign_labels(adome, args.at, args.lt)
        stype_num = len(strut_types)
        total_strut_num = 0 
        for i in range(stype_num):
                total_strut_num += strut_types[i].count

        strut_info = []
        s = "\n{0} struts total, {1} different lengths\n".format(
                        total_strut_num, stype_num)
        strut_info.append(s)

        s = "strut  count   length  a0  a1  length2  cut length\n"
        strut_info.append(s)

        SPACE = ' '
        for i in range(stype_num):
                st = strut_types[i] 
                l2 = st.length + bend_allowances(st, args.bl)
                _n = '{}{}'.format(2*SPACE, st.name)
                _c = '{}{:5d}'.format(1*SPACE, st.count)
                _l = '{}{:7.2f}'.format(1*SPACE, st.length*scale)
                _a0 = '{}{:3.0f}'.format(1*SPACE, st.a0)
                _a1 = '{:3.0f}'.format(st.a1)
                _l2 = '{:7.2f}'.format(l2*scale)
                _cut_len = '{:7.3f}'.format((l2 + 2*margin)*scale)
                s = '{} {} {} {} {} {} {}\n'.format(_n, _c, _l,
                                _a0, _a1, _l2, _cut_len)
                strut_info.append(s)

        notes = """
Notes:

length:      distance from vertex to vertex
a0, a1:      bend angles at the two ends
length2:     distance between bolt holes (accounts for bends)
cut length:  total strut length, including margins
Don't forget to make a few extras.
                """
        strut_info.append(notes)
        
        of = open(ofilename, 'w')
        stamp = get_title("domestruts", "alpha")
        of.write(stamp)
        for it in strut_info:
                of.write(it)
        of.close()

if __name__ == '__main__':
        process_struts()

