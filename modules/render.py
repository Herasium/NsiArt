from math import sin, cos

ORIGINX = 0
ORIGINY = 0

class RenderEngine():
    def __init__(self,core):
        self.core = core
        self.window = core.window
        self.Size = self.window.Size
        

    def set_pixel(self, x, y, value):
        if 0 <= x < self.Size[0] and 0 <= y < self.Size[1]:
            self.window.Buffer[y * self.Size[1] + x] = value

    def draw_line(self, x1, y1, x2, y2, value=0, max_steps=None):

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        if max_steps is None:
            max_steps = self.Size[0] * self.Size[1]

        steps = 0
        while steps < max_steps:
            self.set_pixel(x1, y1, value)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
            steps += 1

        if steps == max_steps:
            raise RuntimeError("Line drawing exceeded maximum steps. Possible infinite loop.")