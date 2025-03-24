
from HeraEngine import *

def Scene0():
    def __init__(self,core:Core):
        self.core = core
        self.core.update = core

    def update(self,_):
        pass
        
    def _setup_scene(self):
        self.scene = Collection(self.core)

        self.scene.Entity("bg",size=Vec2(1920,1080),position = Vec2(0,0),color = Color(255,0,0),layer=layers.background)
        self.scene.Entity(layer=layers.background,name="text_bg",size=Vec2(1260,252),position = Vec2(330,-250),texture ="Assets/Textures/Fonts/Background/back_1.raw")
        self.scene.Text(layer=layers.background,name="textline",font=self._core.monogram_big,position = Vec2(360,295),size = Vec2(50,500),text="")

    def setup(self):
        self._setup_scene()