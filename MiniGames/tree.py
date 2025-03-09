import asyncio
import time
import threading
from HeraEngine import *


class Tree():
    def __init__(self,core: Core):
        self._core = core
        self.in_transition = True
        self.loaded = False

    def setup(self):
        self.setup_transition()
        self._core.update = self.update

    def _setup_clouds(self):
        textures = [
            ("background", "1.raw"),("behind_clouds_copy", "2.raw"), ("behind_clouds", "2.raw"),
            ("front_clouds", "3.raw"), ("front_clouds_copy", "3.raw")
            
        ]
        positions = [Vec2(0, 0)] * 3 + [Vec2(1920, 0)] * 2
        
        for i, (name, tex) in enumerate(textures):
            self.map.Entity(
                name, layer=layers.background,
                size=Vec2(1920, 1080), position=positions[i],
                texture=f"Assets/Textures/Clouds/1/{tex}")

    def _setup_floor(self):
        for i in range(3):
            self.map.Entity(
                f"floor_{i+1}", layer=layers.background,
                size=Vec2(640, 640), position=Vec2(640*i - 190,440),
                texture=f"Assets/Textures/Minigames/Tree/floor_{i+1}.raw")
            
    def _setup_tree(self):
        self.map.Entity(
                "tree_roots", layer=layers.background,
                size=Vec2(520*2, 100*2), position=Vec2(470,818),
                texture=f"Assets/Textures/Minigames/Tree/tree_roots.raw")
        textures = [
            ("tree_bottom", "tree_bottom.raw"),("tree_1", "tree_1.raw"), ("tree_2", "tree_2.raw"),("tree_3", "tree_3.raw"),("tree_top", "tree_top.raw")
        ]
        
        for i, (name, tex) in enumerate(textures):
            self.map.Entity(
                name, layer=layers.background,
                size=Vec2(768, 768), position=Vec2(576,162 - 768*i),
                texture=f"Assets/Textures/Minigames/Tree/{tex}")

    def _update_cloud_positions(self):
        count = self._core.tick_count % 1920
        count_dup = (self._core.tick_count / 2) % 1920
        
        self.map.behind_clouds.position = Vec2(0 - count_dup, self.map.behind_clouds.position.y)
        self.map.front_clouds.position = Vec2(0 - count, self.map.front_clouds.position.y)
        self.map.behind_clouds_copy.position = Vec2(1920 - count_dup, self.map.behind_clouds_copy.position.y)
        self.map.front_clouds_copy.position = Vec2(1920 - count, self.map.front_clouds_copy.position.y)

    def setup_map(self):
        self.map = Collection(self._core)
        self._setup_clouds()
        self._setup_floor()
        self._setup_tree()

    def update(self,_):
        if self.in_transition:
            self.update_transition()
            return
        
        if not self.loaded:
            self.setup_map()
            self.loaded = True

        self._update_cloud_positions()
        
       
    

    def setup_transition(self):
        self.start_count = self._core.tick_count
        self._chaged_start = False
        self.transition_collection = Collection(self._core)
        self.transition_collection.Entity("d",layer=layers.background,position = Vec2(825,-490),size=Vec2(30,52),texture="Assets/Textures/Transition/Dream1/D.raw")
        self.transition_collection.Entity("r",layer=layers.background,position = Vec2(857,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/Dream1/r.raw")
        self.transition_collection.Entity("e",layer=layers.background,position = Vec2(890,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/Dream1/e.raw")
        self.transition_collection.Entity("a",layer=layers.background,position = Vec2(925,-505),size=Vec2(30,38),texture="Assets/Textures/Transition/Dream1/a.raw")
        self.transition_collection.Entity("m",layer=layers.background,position = Vec2(957,-505),size=Vec2(39,38),texture="Assets/Textures/Transition/Dream1/m.raw")
        self.transition_collection.Entity("slash",layer=layers.background,position = Vec2(1020,-490),size=Vec2(34,52),texture="Assets/Textures/Transition/Dream1/#.raw")
        self.transition_collection.Entity("one",layer=layers.background,position = Vec2(1060,-490),size=Vec2(30,52),texture="Assets/Textures/Transition/Dream1/1.raw")

    def update_transition(self):
        elapsed_ticks = self._core.tick_count - self.start_count
        
        if elapsed_ticks <= 200:
            return
        
        transition_elements = [
            ("d", -490, 490),
            ("r", -490, 505),
            ("e", -490, 505),
            ("a", -490, 505),
            ("m", -490, 505),
            ("slash", -490, 490),
            ("one", -490, 490)
        ]
        
        if elapsed_ticks <= 700:
            for i, (key, start, end) in enumerate(transition_elements):
                t = (self._core.tick_count - (self.start_count + 200 + 10 * i)) / 100
                getattr(self.transition_collection,key).position = Vec2(
                    getattr(self.transition_collection,key).position.x,
                    elastic_interpolation(start, end, t)
                )
        
        elif elapsed_ticks <= 1200:
            if not self._chaged_start:
                self._chaged_start = True
                self.second_start_count = self._core.tick_count
            
            for i, (key, end, start) in enumerate(transition_elements):
                t = (self._core.tick_count - (self.second_start_count + 10 * i)) / 100
                getattr(self.transition_collection,key).position = Vec2(
                    getattr(self.transition_collection,key).position.x,
                    reverse_elastic_interpolation(start , end+ 1980, t) 
                )
        else:
            self.in_transition = False
            self.transition_collection.quit()
