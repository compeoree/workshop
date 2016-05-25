# Python 3.4
# domeutil.py 

# Generate timestamp 
# pydome 0.1 2016/05/22 23:49:00
def get_title(head="pydome", version="alpha"):
        import time 

        now = time.strftime("%Y/%m/%d %H:%M:%S")
        name = head + ' ' + version
        return '{} {}\n\n'.format(name, now) 

