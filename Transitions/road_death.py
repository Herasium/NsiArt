from HeraEngine import *

class RoadDeathTransition:
    
    def __init__(self,map,core: Core):
        self._core = core
        self._map = map
        self._core.update = self.update
        self._core.log.INFO("Launched ROAD Death transition. Took over the update event.")
        self.tick = 0
        self.speed = 17


    def update(self,_):
        self.tick += 1
        if self.speed > 0:
            self._map.player.position -= Vec2(0,self.speed)
            self._map.player.rotation += self.speed
            self.speed -= 0.3