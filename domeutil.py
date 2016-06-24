# Python 3.4
# domeutil.py 

# Generate timestamp 
# pydome 0.1 2016/05/22 23:49:00
def get_title(head="pydome", version="alpha"):
        import time 

        now = time.strftime("%Y/%m/%d %H:%M:%S")
        name = head + ' ' + version
        return '{} {}\n\n'.format(name, now) 


def ECHO(message, is_debug=False):
        if is_debug:
                print(message)

def ECHOS(is_debug=False, **args):
        if not is_debug:
                return
        for key, val in args.items():
                print('{}:{}'.format(key, str(val)))


class Color:
        def __init__(self, r=128, g=128, b=128, name="grey"):
                self.r = round(r/256, 3)
                self.g = round(g/256, 3)
                self.b = round(b/256, 3)
                self.name = name
        
        def rgb(self):
                return self.r, self.g, self.b 

        def __str__(self):
                return 'Color<{}, {}, {}, {}>'.format(self.r, self.g, self.b,
                                self.name)

# default 9 colors  
colors = [
        Color(256, 0, 0, "red"),
        Color(0, 256, 0, "green"),
        Color(0, 0, 256, "blue"),
        Color(205, 205, 0, "yellow"),
        Color(256, 0, 256, "magennta"),
        Color(0, 256, 256, "cyan"),
        Color(256, 128, 0, "orange"),
        Color(0, 0, 0, "black"),
        Color(166, 42, 42, "brown")
        ]

ncolors = len(colors) 

# return a Color object 
def get_color(c):
        i = c % ncolors
        return colors[i]

