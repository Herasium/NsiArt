
from HeraEngine.types.Vec2 import Vec2

from HeraEngine.render.flat import FlatRenderer

import ctypes
from line_profiler import profile

class PipeLine():
    def __init__(self,core):

        self.core = core
        self.size = self.core.size
        self.target_size = self.core.size

        if not isinstance(self.size,Vec2):
            return TypeError("Size should be a Vec2.")
        
        self.EntityList = {1:[],2:[],3:[],4:[]}
        self.ZMAP = (ctypes.c_int32 * (self.size.x * self.size.y))()
        self.BackgroundBuffer = (ctypes.c_uint32 * (self.size.y*self.size.x))()

        self.FlatRenderer = FlatRenderer(self.core)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @profile
    def clear_buffer(self): 
        self.BackgroundBuffer = (ctypes.c_uint32 * (self.size.y*self.size.x))()
        self.ZMAP = (ctypes.c_int32 * (self.size.x * self.size.y))()

    def render(self):
        self.BackgroundBuffer, self.ZMAP = self.FlatRenderer.render(self.size,self.target_size,self.BackgroundBuffer,self.ZMAP,self.EntityList[4],-999)
