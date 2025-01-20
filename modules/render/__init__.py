import pygame_adapter
from threading import Thread
import obj_parser
import time
from tqdm import tqdm
import random
import math
window = pygame_adapter.Window("")
window.Size = (1000,1000)

class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)): 
            return Vec3(self.x * other, self.y * other, self.z * other)
        if isinstance(other, Vec3): 
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        return NotImplemented

    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self):
        magnitude = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        if magnitude == 0:
            return self
        return Vec3(self.x / magnitude, self.y / magnitude, self.z / magnitude)


    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"
    
class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)): 
            return Vec2(self.x * other, self.y * other)
        if isinstance(other, Vec2): 
            return Vec2(self.x * other.x, self.y * other.y)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

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

def triangle(t0, t1, t2, color):
    # Sort the vertices by y-coordinate, t0, t1, t2 lower-to-upper
    if t0.y > t1.y:
        t0, t1 = t1, t0
    if t0.y > t2.y:
        t0, t2 = t2, t0
    if t1.y > t2.y:
        t1, t2 = t2, t1

    total_height = t2.y - t0.y

    for y in range(int(t0.y), int(t1.y + 1)):
        segment_height = t1.y - t0.y + 1
        alpha = (y - t0.y) / total_height
        beta = (y - t0.y) / segment_height if segment_height != 0 else 0

        A = Vec2(
            t0.x + (t2.x - t0.x) * alpha,
            t0.y + (t2.y - t0.y) * alpha
        )
        B = Vec2(
            t0.x + (t1.x - t0.x) * beta,
            t0.y + (t1.y - t0.y) * beta
        )

        if A.x > B.x:
            A, B = B, A

        for j in range(int(A.x), int(B.x + 1)):
            window.SetPixelColor(0-j, 0-y, color)

    for y in range(int(t1.y), int(t2.y + 1)):
        segment_height = t2.y - t1.y + 1
        alpha = (y - t0.y) / total_height
        beta = (y - t1.y) / segment_height if segment_height != 0 else 0

        A = Vec2(
            t0.x + (t2.x - t0.x) * alpha,
            t0.y + (t2.y - t0.y) * alpha
        )
        B = Vec2(
            t1.x + (t2.x - t1.x) * beta,
            t1.y + (t2.y - t1.y) * beta
        )

        if A.x > B.x:
            A, B = B, A

        for j in range(int(A.x), int(B.x + 1)):
            window.SetPixelColor(0-j, 0-y, color)

def start():
    while window.ready == False: pass

    faces = obj_parser.parse_obj("modules/render/example.obj")
    light_dir = Vec3(0, 0, -1)

    while True:
        for a in faces["faces"]:
            v0 = Vec3(*faces["vertices"][a[0][0]-1]) *( window.Size[0] / 4.0) + Vec3(-500,-500,-500)
            v1 = Vec3(*faces["vertices"][a[1][0]-1]) *( window.Size[0] / 4.0) + Vec3(-500,-500,-500)
            v2 = Vec3(*faces["vertices"][a[2][0]-1]) *( window.Size[0] / 4.0) + Vec3(-500,-500,-500)

            n = (v2 - v0).cross(v1 - v0)  
            n.normalize()                
            intensity = n.dot(light_dir)
            if intensity > 0:  
  
                color = int(intensity * 255)
                shaded_color = (color << 16) | (color << 8) | color  

                triangle(v0,v1,v2,shaded_color)


        window.update()
        window.clear_buffer()
    


main_thread = Thread(target=start)
main_thread.daemon = True
main_thread.start()

window.MainWin()



