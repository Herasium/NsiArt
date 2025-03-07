from HeraEngine import *
import math
import random

def get_rainbow_color(t):
    r = int(math.sin(0.3 * t) * 127 + 128)
    g = int(math.sin(0.3 * t + 2 * math.pi / 3) * 127 + 128)
    b = int(math.sin(0.3 * t + 4 * math.pi / 3) * 127 + 128)
    return r, g, b

def start(app: Core):
    app.window.Title = "My Super Game"
    app.fullscreen = True
    app.test = Entity(layer=layers.background,size=Vec2(10,10),position=Vec2(0,0))
    app.add_entity(app.test)

def update(app: Core):

    app.test.position = Vec2(int(random.randint(1,48))*10, int(random.randint(1,48))*10)
    r, g, b = get_rainbow_color(app.tick_count / 60)
    app.test.color.update(r=r, g=g, b=b)


app = Core(start=start,update=update)
app.run()
