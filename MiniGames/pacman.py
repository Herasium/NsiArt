from HeraEngine import *

class PacMan():

    def __init__(self,core:Core):
        self._core = core
        self._tile_size = Vec2(20,20)
        self._collision_map_texture = Texture("Assets/Textures/Minigames/PacMan/collision_map.raw",self._core)

    def _debug_collisions(self):
        self.debug_map = Collection(self._core)

        for y in range(self._collision_map_texture.size.y):
            for x in range(self._collision_map_texture.size.x):
                value = self._collision_map_texture.data[y,x] == 0
                if value:
                    self.debug_map.Entity(f"debug-{y}-{x}",size=self._tile_size,position = Vec2(x*self._tile_size.x + 720,y*self._tile_size.y),color = Color(255,255,255),layer=layers.background)
    
    def _setup_map(self):
        self.map = Collection(self._core)
        self.map.Entity("map_bg",size=Vec2(720,1080),position = Vec2(720,0),texture="Assets/Textures/Minigames/PacMan/map_big.raw", layer=layers.background)

    def setup(self):
        self._debug_collisions()
        self._setup_map()
        self._core.update = self.update
        self._core.Pipeline.clear_buffer()

    def update(self,_):
        pass