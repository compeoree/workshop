# Python 3.4
# domelayout.py 
#
# Generate postscript layout diagram 

from domemath import *
from domefile import *
from domeutil import * 
from domestruts import *

# TODO: Handle paper size in name or metric unit 
# letter 8.5x11         216x279
# A4     8.268x11.693   210x297

# Use Paper object instead global variables 
class Paper:
        def __init__(self):
                # letter size, 8.5x11.0 inches 
                self.width = 8.5
                self.height = 11.0 
                
                # margins 
                self.lm, self.rm, self.tm, self.bm = 1.0, 0.5, 0.5, 0.5

                # postscript transform 
                self.sx, self.sy = 0.0, 0.0
                self.tx, self.ty = 0.0, 0.0

                # 1st color 
                self.c0 = 'T0'

                # text height
                self.text_height = 10.0

                # page number 
                self.sheets = 1

# Manage the global variables 
global g

g = Paper()

# Adjust the two end points so that they are the specified distance apart
def adjust_edge(p0, p1, len_):
        d = ptDist(p0, p1)
        d = (d - len_)/2        # adjustment factor
        
        p0_ = project_point_on_line(p0, p1, p0, d)
        p1_ = project_point_on_line(p1, p0, p1, d)

        return p0_, p1_


def draw_edge(ofile, dome, edge, is_explode, is_color):
        global g
        sx, sy = g.sx, g.sy
        tx, ty = g.tx, g.ty

        _p0 = dome.vertex(edge.v0)
        _p1 = dome.vertex(edge.v1)
        p0 = project_point(_p0, dome.radius)
        p1 = project_point(_p1, dome.radius)

        # We've transformed the end points, but this will cause increasing
        # distortion as we move away from the center, so now we shorten
        # the edge back to its original length.  This will cause all the
        # endpoints to break away from each other, but this is a desirable
        # side-effect, since we're going for an exploded view.
        if is_explode:
                p0, p1 = adjust_edge(p0, p1, edge.length) # WIP

        # Convert to postscript coordinates 
        p0.x = fn6(p0.x*sx + tx, 2)
        p0.y = fn6(p0.y*sy + ty, 2)
        p1.x = fn6(p1.x*sx + tx, 2) 
        p1.y = fn6(p1.y*sy + ty, 2)

        ofile.write("%% strut {}\n".format(edge.name))
        # Select one out of 9 colors
        if is_color:
                c = int(edge.name[1:]) - int(g.c0[1:])     
                clr = get_color(c)
                red, green, blue = clr.rgb()
                ofile.write("{} {} {} setrgbcolor\n".format(red, green, blue))
        ofile.write("newpath {:.2f} {:.2f} moveto {:.2f} {:.2f} lineto stroke\n".format(p0.x, p0.y, p1.x, p1.y))
        if is_color:
                ofile.write("0 setgray\n")

        lx = fn6((p0.x + p1.x)/2, 2)
        ly = fn6((p0.y + p1.y)/2, 2)
        ofile.write("{} {} moveto ({}) ctrTxt\n\n".format(lx, ly, edge.name))



def write_prolog(ofile):
        _dimension = "%%%%BoundingBox: {} {} {} {}\n".format(
                        0.0, 0.0, g.width*72.0, g.height*72.0)
        _page = "%%%%Pages: %d\n".format(g.sheets)
        script_body = [
                "%%!PS-Adobe-3.0\n",
                _dimension,
                _page,
                "%%%%Creator: pydome\n",
                "%%%%DocumentFonts: (atend)\n",
                "%%%%DocumentNeedsFonts: (atend)\n",
                "%%%%EndComments:\n\n",
                "%%%%BeginProlog\n\n",
                "/stringbounds           %% (string) => wid hgt\n",
                "{\n",
                "  gsave 0 0 moveto true charpath flattenpath pathbbox grestore\n",
                "  3 1 roll sub 3 2 roll exch sub exch\n",
                "} bind def\n\n",
                "/rect                %% wid hgt =>\n",
                "{\n",
                "  currentpoint newpath moveto\n",
                "  1 index 0 rlineto 0 exch rlineto neg 0 rlineto closepath fill\n",
                "} bind def\n\n",
                "/ctrTxt              %% (string) =>\n",
                "{\n",
                "  dup stringbounds 2 copy 2 div neg exch 2 div neg exch rmoveto\n",
                "  1 setgray gsave rect grestore 0 setgray\n",
                "  show\n",
                "} bind def\n\n",
                "%%%%EndProlog\n\n"
                ]
        for line in script_body:
                ofile.write(line)


def start_page(ofile, pagenum, height):
        script_body = [
                "%%%%Page: \"{}\" {}\n\n".format(pagenum, pagenum),
                "0 setlinejoin\n0 setlinecap\n[] 0 setdash\n",
                "1 setlinewidth\n",
                "/Times-Roman findfont {} scalefont setfont\n\n".format(height)
                ]
        for line in script_body:
                ofile.write(line)


def end_page(ofile, pagenum):
        script_body = [
                "showpage \n\n",
                "%%%%EndPage: \"{}\" {}\n\n".format(pagenum, pagenum)
                ]
        for line in script_body:
                ofile.write(line)


def write_trailer(ofile):
        ofile.write("%%%%Trailer\n")
        ofile.write("%%%%EOF\n")

# callback of -paper option 
def paper_size(string):
        if string == 'letter':
                return 8.5, 11.0
        if (string == 'a4') or (string == 'A4'):
                return 8.3, 11.7

def generate_layout():
        import argparse as ap

        text1 = "In practice, letter or A4 size should be sufficient.\n See instructions for more details."
        parser = ap.ArgumentParser(prog="domelayout", epilog=text1)
        parser.add_argument("dome_file", help="dome file in OpenSCAD code")
        parser.add_argument("postscript_file",
                        help="layout file in postscript format")
        parser.add_argument("-at", default=2.0, type=float,
                        help="angle tolerance in degrees (2.0)")
        parser.add_argument("-lt", default=0.001, type=float,
                        help="length tolerance in percent (0.1)")
        parser.add_argument("-paper", default='letter', type=paper_size,
                        help="letter (216x279)")
        parser.add_argument("-margins", nargs=4,
                                metavar=('LEFT', 'RIGHT', 'TOP', 'BOTTOM'),
                                default=[1.0, 0.5, 0.5, 0.5], type=float,
                                help="margins (1.0 0.5 0.5 0.5)")
        parser.add_argument("-text_height", default=10.0, type=float,
                        help="set text height, points (10)")
        parser.add_argument("-explode", action="store_true",
                        help="exploded diagram")
        parser.add_argument("-color", action="store_true",
                        help="generate color-coded struts")
        args = parser.parse_args()


        ifilename = args.dome_file
        ofilename = args.postscript_file 
        g.width, g.height = args.paper
        g.lm, g.rm, g.tm, g.bm = args.margins 
        g.text_height = args.text_height 

        adome = read_dome(ifilename)
        ofile = open(ofilename, 'w')

        strut_types = assign_labels(adome, args.at, args.lt)
        c0 = strut_types[0].name 

        # Find the bounding box of the projected vertices 
        xmin, xmax = 0.0, 0.0
        ymin, ymax = 0.0, 0.0
        for i in range(adome.nvert):
                _pt = adome.vertex(i)
                pt = project_point(_pt, adome.radius)
                xmin = MIN(xmin, pt.x)
                xmax = MAX(xmax, pt.x)
                ymin = MIN(ymin, pt.y)
                ymax = MAX(ymax, pt.y)

        if (xmax > xmin) and (ymax > ymin):
                # Canvas dimension in ps points 
                w = (g.width - g.lm - g.rm) * 72.0    
                h = (g.height - g.tm - g.bm) * 72.0
                sx = w / (xmax-xmin)
                sy = h / (ymax-ymin)
                g.sx = MIN(sx, sy)        # why?
                g.sy = MIN(sx, sy)
                g.tx = g.lm*72.0 + w/2.0
                g.ty = g.bm*72.0 + h/2.0

        write_prolog(ofile)
        start_page(ofile, 1, g.text_height)

        for i in range(adome.nedge):
                _edge = adome.edge(i)
                draw_edge(ofile, adome, _edge, args.explode, args.color)

        end_page(ofile, 1)
        write_trailer(ofile)
        ofile.close()

if __name__ == '__main__':
        generate_layout()

