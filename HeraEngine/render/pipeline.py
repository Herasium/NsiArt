
from HeraEngine.types.Vec2 import Vec2

from HeraEngine.render.flat import FlatRenderer

class PipeLine():
    def __init__(self,size):

        self.size = size

        if not isinstance(self.size,Vec2):
            return TypeError("Size should be a Vec2.")
        
        self.size = size
        self.EntityList = {1:[],2:[],3:[],4:[]}
        self.ZMAP = [0] * self.size.x * self.size.y
        self.BackgroundBuffer = [0] * self.size.x * self.size.y

        self.FlatRenderer = FlatRenderer()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def clear_buffer(self): 
        self.BackgroundBuffer = [0] * self.size.x * self.size.y

    def render(self):
        self.BackgroundBuffer, self.ZMAP = self.FlatRenderer.render(self.size,self.BackgroundBuffer,self.ZMAP,self.EntityList[4],-999)
