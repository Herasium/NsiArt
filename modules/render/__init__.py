import pygame_adapter
from threading import Thread
import obj_parser
import time
from tqdm import tqdm
import random
window = pygame_adapter.Window("")
window.Size = (1000,1000)

def line(x0, y0, x1, y1, color):
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        window.SetPixelColor(x0 + x*xx + y*yx -1 ,y0 + x*xy + y*yy -1,color)
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy


def start():
    while window.ready == False: pass

    faces = obj_parser.parse_obj("modules/render/example.obj")
    while True:
        for a in faces["faces"]:
            for j in range(3):
                v0 = a[j]
                v1 = a[(j + 1) % 3]
                x0 = 500-int((faces["vertices"][v0[0]-1][0] + 1.0) * window.Size[0] / 4.0)
                y0 = 500-int((faces["vertices"][v0[0]-1][1] + 1.0) * window.Size[1] / 4.0)
                x1 = 500-int((faces["vertices"][v1[0]-1][0] + 1.0) * window.Size[0] / 4.0)
                y1 = 500-int((faces["vertices"][v1[0]-1][1] + 1.0) * window.Size[1] / 4.0)
                line(x0, y0, x1, y1,0xFFFFFF)
            window.update()
        


main_thread = Thread(target=start)
main_thread.daemon = True
main_thread.start()

window.MainWin()



