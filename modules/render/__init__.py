import modules.pygame_adapter as pygame_adapter
from threading import Thread
import modules.render.obj_parser
import time
from tqdm import tqdm
import random
from line_profiler import profile


window = pygame_adapter.Window("")
window.Size = (500,500)

@profile
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

@profile
def start():
    while window.ready == False: pass

    faces = obj_parser.parse_obj("modules/render/example.obj")
    offset = 1
    canvas_size = 500
    while True:
        for a in faces["faces"]:
            for j in range(3):
                v0 = a[j]
                v1 = a[(j + 1) % 3]
                x0 = canvas_size-int((faces["vertices"][v0[0]-1][0] + 1.0) * canvas_size / 2.0)
                y0 = canvas_size-int((faces["vertices"][v0[0]-1][1] + 1.0) * canvas_size / 2.0)
                z0 = int((faces["vertices"][v0[0]-1][2] + 1.0) * 50)
                x1 = canvas_size-int((faces["vertices"][v1[0]-1][0] + 1.0) * canvas_size / 2.0)
                y1 = canvas_size-int((faces["vertices"][v1[0]-1][1] + 1.0) * canvas_size / 2.0)
            
                line(x0, y0, x1, y1,0xFFFFFF)

        offset += 1
        if offset > 90:
            offset = 1

        window.update()
        window.clear_buffer()
        


main_thread = Thread(target=start)
main_thread.daemon = True
main_thread.start()

window.MainWin()



