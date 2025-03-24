import numpy as np
import random
from HeraEngine import *

class Puzzle():
    
    def __init__(self,core: Core):
        self.core = core
        self.core.update = self.update
        self.tile_size = Vec2(360,360)
        
    def _generate_matrix(self):
        matrix = np.arange(1, 10).reshape(3, 3) 
        matrix = np.random.permutation(matrix.flatten()).reshape(3, 3)  
        matrix[2, 1] = 0
        self.matrix = matrix

        
    def _setup_map(self):
        
        self._generate_matrix()
        
        self.map = Collection(self.core)
        self.map.Entity(f"back",size=Vec2(1920,1080),position=Vec2(0,0),color=Color(0,0,0),layer=layers.background)
        self.map.Entity(f"cursor",size=Vec2(0,0),position=Vec2(0,0),color=Color(0,0,0),layer=layers.background)
        self.map.cursor.hitbox.size = Vec2(1, 1)
        self.blank = Vec2(1,2)
        
        self.texture_list = []
        

        for x in range(3):
            for y in range(3):
                self.map.Entity(f"tile_{x}_{y}",size=self.tile_size,position=Vec2(self.tile_size.x*x,self.tile_size.y*y),color=Color(255,255,255),layer=layers.background)
                self.texture_list.append(Texture(f"Assets/Textures/Minigames/Puzzle/sunny/{y}_{x}.raw",self.core))
                getattr(self.map,f"tile_{x}_{y}").index = Vec2(x,y)
                    
                    
    def _has_neighbor(self,pos):
        rows, cols = len(self.matrix), len(self.matrix[0]) 
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        
        for dy, dx in directions:
            ny, nx = pos.y + dy,  pos.x + dx
            if 0 <= ny < rows and 0 <= nx < cols and self.matrix[ny][nx] == 0:
                return True
        
        return False
    
    def _switch(self,pos):
        value = self.matrix[pos.y,pos.x]
        position = tuple(np.argwhere(self.matrix == 0)[0])
   
        self.matrix[position[0],position[1]] = value
        self.matrix[pos.y,pos.x] = 0

                    
    def _update_textures(self):
        for x in range(3):
            for y in range(3): 
                if self.matrix[y,x] != 0:
                    texture = self.texture_list[self.matrix[y,x]-1] 
                    getattr(self.map,f"tile_{x}_{y}").texture = texture
                else:
                    getattr(self.map,f"tile_{x}_{y}").textured = False
                    
    
    def setup(self):
        self._setup_map()
        self.core.cursor.on_left_click.append(self._check_collisions)
        self.core.cursor.on_right_click.append(self._check_collisions)
        
    def _check_collisions(self,*args):
        for i in self.map.entity_list:
            entity = self.map.entity_list[i]
            
            if getattr(entity,"index",None) != None:  
                if self.map.cursor.collide(entity):
                    if self._has_neighbor(entity.index):
                        self._switch(entity.index)
        
    def update(self,_):
        self._update_textures()
        self.map.cursor.position = self.core.cursor.position
