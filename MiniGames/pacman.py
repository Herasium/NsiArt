from HeraEngine import *
import numpy as np

class PacMan():

    def __init__(self,core:Core):
        self._core = core
        self._tile_size = Vec2(20,20)
        self._collision_map_texture = Texture("Assets/Textures/Minigames/PacMan/collision_map.raw",self._core)

    def _debug_collisions(self):
        self.debug_map = Collection(self._core)

        for y in range(self._path_grid_x.shape[1]):
            for x in range(self._path_grid_x.shape[0]):
                value = self._get_path_tile(Vec2(x,y))
                if value != False:
                    self.debug_map.Entity(f"debug-{y}-{x}",size=Vec2(10,10),position =value * 10 + Vec2(600,0),color = Color(100,100),layer=layers.background)
    
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
        self.map.Entity("player",size=Vec2(20,20),position =Vec2(610,10),color=Color(255,0,0),layer=layers.background )
        self.player_position = Vec2(1,1)
        self.player_screen_position = Vec2(610,10)
        self.player_target = Vec2(610,10)
        self.player_rotation = 1
        self.player_delay = 15
        self.target_rotation = 1

    def _position_player(self):
        self.map.player.position = self.player_screen_position
        self.player_screen_position += (self.player_target - self.player_screen_position)/self.player_delay

    def _can_go(self):
        if self.target_rotation == 1:
            next_tile = self._get_path_tile(self.player_position + Vec2(1,0))
            if next_tile.x != -1 and next_tile.y != -1:
                return True
            return False

        if self.target_rotation == 2:
            vector = Vec2(0,1)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                return True
            return False

        if self.target_rotation == 3:
            vector = Vec2(-1,0)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                return True
            return False

        if self.target_rotation == 4:
            vector = Vec2(0,-1)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                return True
            return False

    def _move_player(self):
        if self.player_rotation == 1:
            next_tile = self._get_path_tile(self.player_position + Vec2(1,0))
            if next_tile.x != -1 and next_tile.y != -1:
                self.player_target = self._get_path_tile(self.player_position + Vec2(1,0)) * 10 + Vec2(600,0)
                self.player_position += Vec2(1,0)
        if self.player_rotation == 2:
            vector = Vec2(0,1)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                self.player_target = self._get_path_tile(self.player_position + vector) * 10 + Vec2(600,0)
                self.player_position += vector

        if self.player_rotation == 3:
            vector = Vec2(-1,0)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                self.player_target = self._get_path_tile(self.player_position + vector) * 10 + Vec2(600,0)
                self.player_position += vector

        if self.player_rotation == 4:
            vector = Vec2(0,-1)
            next_tile = self._get_path_tile(self.player_position + vector)
            if next_tile.x != -1 and next_tile.y != -1:
                self.player_target = self._get_path_tile(self.player_position + vector) * 10 + Vec2(600,0)
                self.player_position += vector

    def _handle_player_inputs(self):
        for key in self._core.keyboard.last_pressed:
            if self._core.keyboard.get_key(key) == "right_arrow":
                self.target_rotation = 1

            if self._core.keyboard.get_key(key) == "left_arrow":
                self.target_rotation = 3
                
            if self._core.keyboard.get_key(key) == "up_arrow":
                self.target_rotation = 4

            if self._core.keyboard.get_key(key) == "down_arrow":
                self.target_rotation = 2

        if self._can_go():
            self.player_rotation = self.target_rotation

    def _setup_path_grid(self):
        self._path_grid_x,self._path_grid_y = np.array(CSV().read("Assets/Textures/Minigames/Pacman/collisions.txt"))
        self._path_grid_x = self._path_grid_x.reshape(108,72)
        self._path_grid_y = self._path_grid_y.reshape(108,72)
        print(self._path_grid_x,self._path_grid_y)

    def _get_path_tile(self, position):
        if 0 <= position.x < self._path_grid_x.shape[1] and 0 <= position.y < self._path_grid_y.shape[0]:
            return Vec2(self._path_grid_x[position.y, position.x], self._path_grid_y[position.y, position.x])
        return Vec2(-1, -1)

    def setup(self):
        self._setup_map()
        self._setup_player()
        self._setup_path_grid()
        self._debug_collisions()
        self.map.Text("debug_text",position=Vec2(0,0),size=Vec2(100,100),font=self._core.monogram,text="Hello World",layer=layers.background)
        self.map.Entity("debug_cursor",position = Vec2(0,0),size=Vec2(10,10),layer=layers.background,color=Color(255,0,255))
        self._core.update = self.update
        self._core.Pipeline.clear_buffer()

    def update(self,_):
        self._position_player()
        if self._core.tick_count % 7 == 0:
            self._move_player()
        self._handle_player_inputs()
        self.map.debug_cursor.position = Vec2(round(self._core.cursor.x/10)*10,round(self._core.cursor.y/10)*10)
        self.map.debug_text.text = f"FPS: {int(self._core.fps)};{int(self._core.average_fps)} ECOUNT {self._core.entity_count} POSITION {self.player_position} CURSOR {self.map.debug_cursor.position}"