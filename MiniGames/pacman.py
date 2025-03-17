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
                    self.debug_map.Entity(f"debug-{y}-{x}",size=self._tile_size,position = Vec2(x*self._tile_size.x + 600,y*self._tile_size.y),color = Color(x*y+50,x*y+50,x*y+50),layer=layers.background)
    
    def _get_tile(self,position):
        rows, cols = self._collision_map_texture.data.shape

        if  0 <= position.x < cols and 0 <= position.y < rows: 
            return self._collision_map_texture.data[position.y,position.x] == 0
        return False
    
    def _setup_map(self):
        self.map = Collection(self._core)
        self.map.Entity(name="bg_0",size = Vec2(1920,1080),position=Vec2(0,0),color=Color(0,0,0),layer=layers.background)
        self.map.Entity("map_bg",size=Vec2(720,1080),position = Vec2(600,0),texture="Assets/Textures/Minigames/PacMan/map_big.raw", layer=layers.background)

    def _setup_player(self):
        self.map.Entity("player",size=Vec2(30,30),position =Vec2(610,10),color=Color(255,0,0),layer=layers.background )
        self.player_position = Vec2(0,0)
        self.player_screen_position = Vec2(610,10)
        self.player_target = Vec2(610,10)
        self.player_rotation = 1
        self.player_delay = 4

    def _position_player(self):
        self.map.player.position = self.player_screen_position
        self.player_screen_position += (self.player_target - self.player_screen_position)/self.player_delay

    def _move_player(self):
        if self.player_rotation == 1:
            if self._get_tile(self.player_position + Vec2(1,0)):
                self.player_position += Vec2(1,0)
                self.player_target = self.player_position * self._tile_size + Vec2(600,0) 
                
        if self.player_rotation == 2:
            if self._get_tile(self.player_position + Vec2(0,1)):
                self.player_position += Vec2(0,1)
                self.player_target = self.player_position * self._tile_size + Vec2(600,0) 
                
        if self.player_rotation == 3:
            if self._get_tile(self.player_position + Vec2(-1,0)):
                self.player_position += Vec2(-1,0)
                self.player_target = self.player_position * self._tile_size + Vec2(600,0) 
                
        if self.player_rotation == 4:
            if self._get_tile(self.player_position + Vec2(0,-1)):
                self.player_position += Vec2(0,-1)
                self.player_target = self.player_position * self._tile_size + Vec2(600,0) 
                

    def _handle_player_inputs(self):
        for key in self._core.keyboard.last_pressed:
            if self._core.keyboard.get_key(key) == "right_arrow":
                self.player_rotation = 1

            if self._core.keyboard.get_key(key) == "left_arrow":
                self.player_rotation = 3
                
            if self._core.keyboard.get_key(key) == "up_arrow":
                self.player_rotation = 4

            if self._core.keyboard.get_key(key) == "down_arrow":
                self.player_rotation = 2

    def setup(self):
        self._debug_collisions()
        self._setup_map()
        self._setup_player()
        self.map.Text("debug_text",position=Vec2(0,0),size=Vec2(100,100),font=self._core.monogram,text="Hello World",layer=layers.background)
        self._core.update = self.update
        self._core.Pipeline.clear_buffer()

    def update(self,_):
        self._position_player()
        if self._core.tick_count % 7 == 0:
            self._move_player()
        self._handle_player_inputs()
        self.map.debug_text.text = f"FPS: {int(self._core.fps)};{int(self._core.average_fps)} ECOUNT {self._core.entity_count} POSITION {self.player_position}"