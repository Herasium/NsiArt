from HeraEngine import *
import math
import random

def start(app: Core):
    app.window.Title = "My Super Game"
    
    app.test = Entity(layer=layers.background,size=Vec2(15,15),position=Vec2(50,50))
    app.add_entity(app.test)
def update(app: Core):
    app.test.position = Vec2(int(50+math.sin(app.tick_count/200)*20),int(50+math.sin(app.tick_count/200*1.5)*20))
    app.test.color.update(r=random.randint(0,255),g=random.randint(0,255),b=random.randint(0,255))


app = Core(start=start,update=update)
app.run()