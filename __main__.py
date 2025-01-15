from modules.core import Core
import random
import time
from line_profiler import profile

rainbow_colors = [
    0xFF0000, 0xFF3300, 0xFF6600, 0xFF9900, 0xFFCC00, 0xFFFF00, 0xB2FF00, 0x80FF00,
    0x4DFF00, 0x1AFF00, 0x00FF00, 0x00FF33, 0x00FF66, 0x00FF99, 0x00FFCC, 0x00FFFF,
    0x00B2FF, 0x0099FF, 0x007FFF, 0x0066FF, 0x004DFF, 0x0033FF, 0x001AFF, 0x0000FF,
    0x3200FF, 0x4D00FF, 0x6600FF, 0x7F00FF, 0x9900FF, 0xB200FF, 0xCC00FF, 0xE600FF,
    0xFF00FF, 0xFF00CC, 0xFF0099, 0xFF0066, 0xFF0033, 0xFF0000, 0xFF3300, 0xFF6600,
    0xFF9900, 0xFFCC00, 0xFFFF00, 0xFFFF33, 0xFFFF66, 0xFFFF99, 0xFFFFCC, 0xFFFFFF,
    0xCCFFCC, 0x99FF99, 0x66FF66, 0x33FF33, 0x00FF00
]

def start(core):
    core.window.SetWindowSize(600,500)
    core.window.Title = "My Super Game"
    core.data = {"x":0}

@profile
def update(core):
    core.data["x"] += 1
    core.render.draw_cube(0xFFFFFF,core.render.cube)
    core.render.rotate_object(core.render.cube, 0.1, (0,1,0))
    core.render.rotate_object(core.render.cube, 0.01, (0,0,1))
    core.render.rotate_object(core.render.cube, 0.01, (1,0,0))
    core.window.update()
    core.window.clear_buffer()




core = Core(start=start,update=update)
core.run()