import pygame_adapter
from threading import Thread
import obj_parser
import time
from tqdm import tqdm
import random
import math
import pygame
from line_profiler import profile

window = pygame_adapter.Window("")
window.Size = (1000,1000)

texture = pygame.image.load("modules/render/uv-grid.png")  
texture = pygame.transform.flip(texture, False, True)
texture_width, texture_height = texture.get_size()
texture_data = pygame.PixelArray(texture)

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

@profile
def triangle(pts,uvs, zbuffer):
    t0, t1, t2 = pts
    uv0, uv1, uv2 = uvs

    if t0.y > t1.y:
        t0, t1 = t1, t0
        uv0, uv1 = uv1, uv0

    if t0.y > t2.y:
        t0, t2 = t2, t0
        uv0, uv2 = uv2, uv0

    if t1.y > t2.y:
        t1, t2 = t2, t1
        uv1, uv2 = uv2, uv1



    total_height = t2.y - t0.y

    @profile
    def draw_scanline(y, A, B, uvA, uvB):
        if A.x > B.x:
            A, B = B, A
            uvA,uvB = uvB, uvA
        for j in range(int(A.x), int(B.x + 1)):
            t = (j - A.x) / (B.x - A.x) if B.x != A.x else 0
            z = A.z + t * (B.z - A.z)
            uv_interp = Vec2(
                uvA.x + t * (uvB.x - uvA.x),
                uvA.y + t * (uvB.y - uvA.y)
            )
            if 0 <= (0-j) < window.Size[0] and 0 <= (0-y) < window.Size[1]:
            
                if zbuffer[j][y] < z:
                    zbuffer[j][y] = z

                    tex_x = int(uv_interp.x * texture_width)
                    tex_y = int(uv_interp.y * texture_height)
                    tex_x = max(0, min(tex_x, texture_width - 1))
                    tex_y = max(0, min(tex_y, texture_height - 1))
                    color = texture_data[tex_x, tex_y]
                    window.SetPixelColor(0 - j, 0 - y, color)

    for y in range(int(t0.y), int(t1.y + 1)):
        segment_height = t1.y - t0.y + 1
        alpha = (y - t0.y) / total_height
        beta = (y - t0.y) / segment_height if segment_height != 0 else 0

        A = Vec3(
            t0.x + (t2.x - t0.x) * alpha,
            t0.y + (t2.y - t0.y) * alpha,
            t0.z + (t2.z - t0.z) * alpha
        )
        B = Vec3(
            t0.x + (t1.x - t0.x) * beta,
            t0.y + (t1.y - t0.y) * beta,
            t0.z + (t1.z - t0.z) * beta
        )

        uvA = uv0 + alpha * (uv2 - uv0)
        uvB = uv0 + beta * (uv1 - uv0)

        draw_scanline(y, A, B, uvA, uvB)

    for y in range(int(t1.y), int(t2.y + 1)):
        segment_height = t2.y - t1.y + 1
        alpha = (y - t0.y) / total_height
        beta = (y - t1.y) / segment_height if segment_height != 0 else 0

        A = Vec3(
            t0.x + (t2.x - t0.x) * alpha,
            t0.y + (t2.y - t0.y) * alpha,
            t0.z + (t2.z - t0.z) * alpha
        )
        B = Vec3(
            t1.x + (t2.x - t1.x) * beta,
            t1.y + (t2.y - t1.y) * beta,
            t1.z + (t2.z - t1.z) * beta
        )

        uvA = uv0 + alpha * (uv2 - uv0)
        uvB = uv1 + beta * (uv2 - uv1)

        draw_scanline(y, A, B, uvA, uvB)

@profile
def start():
    while not window.ready:
        pass

    start_time = time.time()
    zbuffer = [[-float('inf') for _ in range(window.Size[1])] for _ in range(window.Size[0])]
    faces = obj_parser.parse_obj("modules/render/example.obj")
    light_dir = Vec3(0, 0, -1)

    
    for a in faces["faces"]:
                v0 = Vec3(*faces["vertices"][a[0][0] - 1]) * (window.Size[0] / 4.0) + Vec3(-500,-500,-500)
                v1 = Vec3(*faces["vertices"][a[1][0] - 1]) * (window.Size[0] / 4.0) + Vec3(-500,-500,-500)
                v2 = Vec3(*faces["vertices"][a[2][0] - 1]) * (window.Size[0] / 4.0) + Vec3(-500,-500,-500)
  
                u0 = faces["textures"][a[0][1] - 1]
                u1 = faces["textures"][a[1][1] - 1]
                u2 = faces["textures"][a[2][1] - 1]
    
                n = (v2 - v0).cross(v1 - v0)
                n = n.normalize()
                intensity = n.dot(light_dir)
                if intensity > 0:
                    triangle([v0, v1, v2],[Vec2(u0[0],u0[1]), Vec2(u1[0],u1[1]), Vec2(u2[0],u2[1])], zbuffer)

    window.update()
    window.clear_buffer()

    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")

main_thread = Thread(target=start)
main_thread.daemon = True
main_thread.start()

window.MainWin()



