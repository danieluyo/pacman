# Thanks to Bart Grantham for all the fruit path details.

import sys
import json

path_chars = ['^','>','<','v']

exit_start = {'x':16, 'y':20}

pen_start = {'x':15, 'y':20}
pen_path = "fa ff 55 55 01 80 aa 02"
pen_count = "1d"

map_paths = [
    {
        "entrances": [
            {"start": "94 0c", "count": "13", "path": "80 aa aa bf aa"},
            {"start": "94 f4", "count": "22", "path": "80 0a 54 55 55 55 ff 5f 55"},
            {"start": "4c f4", "count": "27", "path": "ea ff 57 55 f5 57 ff 15 40 55"},
            {"start": "4c 0c", "count": "1c", "path": "ea af 02 ea ff ff aa"},
        ],
        "exits": [
            {"count": "14", "path": "55 40 55 55 bf"},
            {"count": "17", "path": "aa 80 aa aa bf aa"},
            {"count": "1a", "path": "aa 80 aa 02 80 aa aa"},
            {"count": "1d", "path": "55 00 00 00 55 55 fd aa"},
        ],
    },
    {
        "entrances": [
            {"start": "c4 0c", "count": "13", "path": "02 aa aa 80 2a"},
            {"start": "c4 f4", "count": "1e", "path": "02 40 55 7f 55 15 50 05"},
            {"start": "14 f4", "count": "26", "path": "ea ff 57 55 f5 ff 57 7f 55 05"},
            {"start": "14 0c", "count": "1d", "path": "ea ff ff ff ea af aa 02"},
        ],
        "exits": [
            {"count": "12", "path": "55 7f 55 d5 ff"},
            {"count": "1d", "path": "aa bf aa 2a a0 ea ff ff"},
            {"count": "21", "path": "aa 2a a0 02 00 00 a0 aa 02"},
            {"count": "2c", "path": "55 15 a0 2a 00 54 05 00 00 55 fd"},
        ],
    },
    {
        "entrances": [
            {"start": "54 0c", "count": "15", "path": "ea ff ab fa aa aa"},
            {"start": "54 f4", "count": "1e", "path": "ea ff 57 55 55 d5 57 55"},
            {"start": "54 f4", "count": "1e", "path": "ea ff 57 55 55 d5 57 55"},
            {"start": "54 0c", "count": "15", "path": "aa aa bf fa bf aa"},
        ],
        "exits": [
            {"count": "22", "path": "05 00 00 54 05 54 7f f5 0b"},
            {"count": "25", "path": "0a 00 00 a8 0a a8 bf fa ab aa aa 82 aa 00 a0 aa"},
            {"count": "25", "path": "0a 00 00 a8 0a a8 bf fa ab aa aa 82 aa 00 a0 aa"},
            {"count": "28", "path": "55 41 55 00 a0 02 40 f5 57 bf"},
        ],
    },
    {
        "entrances": [
            {"start": "8c 0c", "count": "14", "path": "80 aa be fa aa"},
            {"start": "8c f4", "count": "1d", "path": "00 50 fd 55 f5 d5 57 55"},
            {"start": "74 f4", "count": "2a", "path": "ea ff 57 d5 5f fd 15 50 01 50 55"},
            {"start": "74 0c", "count": "15", "path": "ea af fe 2a a8 aa"},
        ],
        "exits": [
            {"count": "15", "path": "55 50 41 55 fd aa"},
            {"count": "18", "path": "aa a0 82 aa fe aa"},
            {"count": "19", "path": "aa af 02 2a a0 aa aa"},
            {"count": "1c", "path": "55 5f 01 00 50 55 bf"},
        ],
    },
]

def getPixel(p):
    x = p['x']
    y = p['y']
    return {'x':30*8-x, 'y':y+2*8}

def getTile(p):
    p = getPixel(p)
    return {'x':p['x']/8, 'y':p['y']/8}

def decode_start(start):
    bytes = [int(token,16) for token in start.split()]
    return {"x": bytes[1], "y": bytes[0]}

def decode_path(path,count):
    bytes = [int(token,16) for token in reversed(path.split())]
    result = ""
    for b in bytes:
        for i in reversed(range(4)):
            result += path_chars[(b >> (i*2)) & 0x03]
    return result[-int(count,16):]

def main():
    def print_map(start,path,map):
        present = {}
        x = start['x']
        y = start['y']
        print
        for c in path:
            present[(x,y)] = c
            if c == '>':
                x += 1
            elif c == '<':
                x -= 1
            elif c == '^':
                y -= 1
            elif c == 'v':
                y += 1
        for y in range(36):
            sys.stdout.write("    ")
            for x in range(-1,29):
                c = " "
                if x >= 0 and x < 28:
                    c = map[x+y*28]
                if (x,y) in present:
                    if c == '|':
                        raise Error("Path travels over a wall")
                    c = present[(x,y)]
                sys.stdout.write(c)
            print
        print

    i = 0
    js_maplist = []
    for m,map in zip(map_paths,maps):
        js_map = {'entrances':[], 'exits':[]}
        js_maplist.append(js_map)
        for j,e in enumerate(m['entrances']):
            start = decode_start(e['start'])
            pixel = getPixel(start)
            tile = getTile(start)
            path = decode_path(e['path'], e['count'])
            #print_map(tile,path,map)

            js_map['entrances'].append({'start':pixel, 'path':path})

        for j,e in enumerate(m['exits']):
            path = decode_path(e['path'], e['count'])
            #print_map(exit_start,path,map)

            js_map['exits'].append({'path':path})
        i += 1

    print "// Generated JSON Map Paths"
    for line in json.dumps(js_maplist,indent=4).splitlines():
        print ' '*4,line
    print

    print "// Generated JSON Ghost Pen Path"
    path = decode_path(pen_path, pen_count)
    for line in json.dumps(path,indent=4).splitlines():
        print ' '*4,line

maps = [
    (
    "____________________________" +
    "____________________________" +
    "____________________________" +
    "||||||||||||||||||||||||||||" +
    "|......||..........||......|" +
    "|o||||.||.||||||||.||.||||o|" +
    "|.||||.||.||||||||.||.||||.|" +
    "|..........................|" +
    "|||.||.|||||.||.|||||.||.|||" +
    "__|.||.|||||.||.|||||.||.|__" +
    "|||.||.|||||.||.|||||.||.|||" +
    "   .||.......||.......||.   " +
    "|||.||||| |||||||| |||||.|||" +
    "__|.||||| |||||||| |||||.|__" +
    "__|.                    .|__" +
    "__|.||||| |||--||| |||||.|__" +
    "__|.||||| |______| |||||.|__" +
    "__|.||    |______|    ||.|__" +
    "__|.|| || |______| || ||.|__" +
    "|||.|| || |||||||| || ||.|||" +
    "   .   ||          ||   .   " +
    "|||.|||||||| || ||||||||.|||" +
    "__|.|||||||| || ||||||||.|__" +
    "__|.......   ||   .......|__" +
    "__|.|||||.||||||||.|||||.|__" +
    "|||.|||||.||||||||.|||||.|||" +
    "|............  ............|" +
    "|.||||.|||||.||.|||||.||||.|" +
    "|.||||.|||||.||.|||||.||||.|" +
    "|.||||.||....||....||.||||.|" +
    "|o||||.||.||||||||.||.||||o|" +
    "|.||||.||.||||||||.||.||||.|" +
    "|..........................|" +
    "||||||||||||||||||||||||||||" +
    "____________________________" +
    "____________________________"
    ),
    (
    "____________________________" +
    "____________________________" +
    "____________________________" +
    "||||||||||||||||||||||||||||" +
    "       ||..........||       " +
    "|||||| ||.||||||||.|| ||||||" +
    "|||||| ||.||||||||.|| ||||||" +
    "|o...........||...........o|" +
    "|.|||||||.||.||.||.|||||||.|" +
    "|.|||||||.||.||.||.|||||||.|" +
    "|.||......||.||.||......||.|" +
    "|.||.|||| ||....|| ||||.||.|" +
    "|.||.|||| |||||||| ||||.||.|" +
    "|......|| |||||||| ||......|" +
    "||||||.||          ||.||||||" +
    "||||||.|| |||--||| ||.||||||" +
    "|......|| |______| ||......|" +
    "|.||||.|| |______| ||.||||.|" +
    "|.||||.   |______|   .||||.|" +
    "|...||.|| |||||||| ||.||...|" +
    "|||.||.||          ||.||.|||" +
    "__|.||.|||| |||| ||||.||.|__" +
    "__|.||.|||| |||| ||||.||.|__" +
    "__|.........||||.........|__" +
    "__|.|||||||.||||.|||||||.|__" +
    "|||.|||||||.||||.|||||||.|||" +
    "   ....||...    ...||....   " +
    "|||.||.||.||||||||.||.||.|||" +
    "|||.||.||.||||||||.||.||.|||" +
    "|o..||.......||.......||..o|" +
    "|.||||.|||||.||.|||||.||||.|" +
    "|.||||.|||||.||.|||||.||||.|" +
    "|..........................|" +
    "||||||||||||||||||||||||||||" +
    "____________________________" +
    "____________________________"
    ),
    (
    "____________________________" +
    "____________________________" +
    "____________________________" +
    "||||||||||||||||||||||||||||" +
    "|.........||....||.........|" +
    "|o|||||||.||.||.||.|||||||o|" +
    "|.|||||||.||.||.||.|||||||.|" +
    "|.||.........||.........||.|" +
    "|.||.||.||||.||.||||.||.||.|" +
    "|....||.||||.||.||||.||....|" +
    "||||.||.||||.||.||||.||.||||" +
    "||||.||..............||.||||" +
    " ....|||| |||||||| ||||.... " +
    "|.|| |||| |||||||| |||| ||.|" +
    "|.||                    ||.|" +
    "|.|||| || |||--||| || ||||.|" +
    "|.|||| || |______| || ||||.|" +
    "|.     || |______| ||     .|" +
    "|.|| |||| |______| |||| ||.|" +
    "|.|| |||| |||||||| |||| ||.|" +
    "|.||                    ||.|" +
    "|.|||| ||||| || ||||| ||||.|" +
    "|.|||| ||||| || ||||| ||||.|" +
    "|......||....||....||......|" +
    "|||.||.||.||||||||.||.||.|||" +
    "|||.||.||.||||||||.||.||.|||" +
    "|o..||.......  .......||..o|" +
    "|.||||.|||||.||.|||||.||||.|" +
    "|.||||.|||||.||.|||||.||||.|" +
    "|......||....||....||......|" +
    "|.||||.||.||||||||.||.||||.|" +
    "|.||||.||.||||||||.||.||||.|" +
    "|......||..........||......|" +
    "||||||||||||||||||||||||||||" +
    "____________________________" +
    "____________________________"
    ),
    (
    "____________________________" +
    "____________________________" +
    "____________________________" +
    "||||||||||||||||||||||||||||" +
    "|..........................|" +
    "|.||.||||.||||||||.||||.||.|" +
    "|o||.||||.||||||||.||||.||o|" +
    "|.||.||||.||....||.||||.||.|" +
    "|.||......||.||.||......||.|" +
    "|.||||.||.||.||.||.||.||||.|" +
    "|.||||.||.||.||.||.||.||||.|" +
    "|......||....||....||......|" +
    "|||.|||||||| || ||||||||.|||" +
    "__|.|||||||| || ||||||||.|__" +
    "__|....||          ||....|__" +
    "||| ||.|| |||--||| ||.|| |||" +
    "    ||.|| |______| ||.||    " +
    "||||||.   |______|   .||||||" +
    "||||||.|| |______| ||.||||||" +
    "    ||.|| |||||||| ||.||    " +
    "||| ||.||          ||.|| |||" +
    "__|....||||| || |||||....|__" +
    "__|.||.||||| || |||||.||.|__" +
    "__|.||....   ||   ....||.|__" +
    "__|.|||||.|| || ||.|||||.|__" +
    "|||.|||||.|| || ||.|||||.|||" +
    "|.........||    ||.........|" +
    "|.||||.||.||||||||.||.||||.|" +
    "|.||||.||.||||||||.||.||||.|" +
    "|.||...||..........||...||.|" +
    "|o||.|||||||.||.|||||||.||o|" +
    "|.||.|||||||.||.|||||||.||.|" +
    "|............||............|" +
    "||||||||||||||||||||||||||||" +
    "____________________________" +
    "____________________________"
    )
]

main()
