import asyncio
import time
import threading
import random
from HeraEngine import *


class Tree():
    def __init__(self,core: Core):
        self._core = core
        self.in_transition = True
        self.loaded = False
        self.offset_y = 0 
        self.target_offset_y = 0
        self.player_in_transition = False
        self.player_position = Vec2(1980/2,1080-200)
        self.player_branch = -1
        self.player_side= False #left: False, right: True because if I'm right, my thoughts are TRUE lol
        self.player_dead = False
        self.last_status = True
        self.finished_intro = False
        self.intro_locations = {}

    def setup(self):
        self.setup_transition()
        self._core.update = self.update
        self._branch_list = [random.randint(0, 1) == 1 for _ in range(10)]
        self._offset = [[
            Vec2(304, 131 + 0),
            Vec2(256, 26 + (-170)),
            Vec2(256, 2 + (-450)),
            Vec2(208, 228 + (-950)),
            Vec2(208, 76 + (-1220)),
            Vec2(256, 60 + (-1510)),
            Vec2(256, 72 + (-1800)),
            Vec2(208, 102 + (-2230)),
            Vec2(160, 29 + (-2540)),
        ],[
            Vec2(1248, 96 + 0),
            Vec2(1152, 10 + (-170)),
            Vec2(1152, 3 + (-450)),
            Vec2(1176, 84 + (-820)),
            Vec2(1152, 84 + (-1180)),
            Vec2(1200, 20 + (-1460)),
            Vec2(1104, 42 + (-1770)),
            Vec2(1152, 43 + (-2180)),
            Vec2(1124, 52 + (-2540)),
        ]]
        self._player_offset = [Vec2(250,140),Vec2(192,140),Vec2(304,140),Vec2(144,140)] #rotten left, rotten right, good left, good right
        self._core.log.DEBUG(str(self._branch_list))

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
                size=Vec2(1280, 1280), position=Vec2(-1150 +1280*i,-200),
                texture=f"Assets/Textures/Minigames/Tree/floor_{i+1}.raw")
            
    def _setup_tree(self):
        self.map.Entity(
                "tree_bottom", layer=layers.background,
                size=Vec2(768*2, 768*2), position=Vec2(576-336,0),
                texture=f"Assets/Textures/Minigames/Tree/tree_bottom.raw")
        textures = [
            ("tree_1", "tree_1.raw"), ("tree_2", "tree_2.raw"),("tree_3", "tree_3.raw"),("tree_top", "tree_top.raw")
        ]
        
        for i, (name, tex) in enumerate(textures):
            self.map.Entity(
                name, layer=layers.background,
                size=Vec2(768, 768), position=Vec2(576,0 - 768*(i+1)),
                texture=f"Assets/Textures/Minigames/Tree/{tex}")

    def _update_tree_positions(self):
        textures = [
            ("tree_1", "tree_1.raw"), ("tree_2", "tree_2.raw"),("tree_3", "tree_3.raw"),("tree_top", "tree_top.raw")
        ]
        for i, (name, tex) in enumerate(textures):
            getattr(self.map,name).position = Vec2(576,0 - 768*(i+1) - self.offset_y)

        self.map.tree_bottom.position=Vec2(576-336,0 - self.offset_y)

    def _update_branch_positions(self):
        for i in range(len(self._branch_list)-1):
            value = self._branch_list[i]
            if value:
                getattr(self.map,"branch_good_"+str(i)).position = self._offset[0][i] - Vec2(0,self.offset_y)
                getattr(self.map,"branch_bad_"+str(i)).position = self._offset[1][i] - Vec2(0,self.offset_y)

            else:
                getattr(self.map,"branch_good_"+str(i)).position = self._offset[1][i] - Vec2(0,self.offset_y)
                getattr(self.map,"branch_bad_"+str(i)).position = self._offset[0][i] - Vec2(0,self.offset_y)



    def _update_cloud_positions(self):
        count = self._core.tick_count % 1920
        count_dup = (self._core.tick_count / 2) % 1920
        
        self.map.behind_clouds.position = Vec2(0 - count_dup, self.map.behind_clouds.position.y)
        self.map.front_clouds.position = Vec2(0 - count, self.map.front_clouds.position.y)
        self.map.behind_clouds_copy.position = Vec2(1920 - count_dup, self.map.behind_clouds_copy.position.y)
        self.map.front_clouds_copy.position = Vec2(1920 - count, self.map.front_clouds_copy.position.y)

    def _setup_branch(self):
        self.branch_collection = Collection(self._core)
        self.branch_collection.Text("position_debug",layer=layers.background,font=self._core.monogram,size=Vec2(100, 28), position=Vec2(0, 0),text="Hello Wotld")
        for i in range(len(self._branch_list)-1):
            value = self._branch_list[i]
            if value:
                self.map.Entity(
                "branch_good_"+str(i), layer=layers.background,
                size=Vec2(512, 512), position=self._offset[0][i],
                texture=f"Assets/Textures/Minigames/Tree/branch_left.raw")
                

                self.map.Entity(
                "branch_bad_"+str(i), layer=layers.background,
                size=Vec2(512, 512), position=self._offset[1][i],
                texture=f"Assets/Textures/Minigames/Tree/rotten_right.raw")

            else:
                self.map.Entity(
                "branch_good_"+str(i), layer=layers.background,
                size=Vec2(512, 512), position=self._offset[1][i],
                texture=f"Assets/Textures/Minigames/Tree/branch_right.raw")

                self.map.Entity(
                "branch_bad_"+str(i), layer=layers.background,
                size=Vec2(512, 512), position=self._offset[0][i],
                texture=f"Assets/Textures/Minigames/Tree/rotten_left.raw")

    def _setup_player(self):
        self.player = Entity(layer=layers.background,size=Vec2(50,100),position=self.player_position,color=Color(255,0,0))
        self._core.add_entity(self.player)

    def setup_map(self):
        self.map = Collection(self._core)
        self._setup_clouds()
        self._setup_floor()
        self._setup_tree()
        self._setup_branch()
        self._setup_player()


    def _update_floor(self):
        for i in range(3):
            getattr(self.map,f"floor_{i+1}").position = Vec2(-1150 +1280*i,-200) - Vec2(0,self.offset_y)
            
    def _update_intro(self):
        if (self._core.tick_count-(self.start_intro_time+10*len(self.map.entity_list))) < 100:
            count = 0
            for i in self.map.entity_list:
                entity = self.map.entity_list[i]
                target = self.intro_locations[entity] if entity in self.intro_locations else Vec2(0,0)
                entity.position = elastic_interpolation(Vec2(target.x,1080),target,(self._core.tick_count-(self.start_intro_time+10*count))/100)
                count += 1
        else:
            self.finished_intro = True

    def update(self,_):
        if self.in_transition:
            self.update_transition()
            return
         
        if not self.loaded:
            self.setup_map()
            self.start_player_count = self._core.tick_count
            self.start_intro_time = self._core.tick_count
            self.loaded = True
            for i in self.map.entity_list:
                entity = self.map.entity_list[i]
                self.intro_locations[entity] = entity.position
                entity.position = Vec2(entity.position.x,1080)
        if not self.finished_intro:
            self._update_intro()
            return

        if self.player_in_transition:
            self._update_player_transition()
        else:
            for key in self._core.keyboard.last_pressed:
                if not self.player_in_transition and not self.player_dead:
                    if self._core.keyboard.key_codes[key] == "right_arrow":
                        self.player_branch += 1
                        self.player_side = True
                        self.target_offset_y = self.offset_y - 340
                        self._update_player_transition(self.player_position,self._offset[1][self.player_branch] + self._player_offset[3 if not self._branch_list[self.player_branch] else 1])

                    if self._core.keyboard.key_codes[key] == "left_arrow":
                        self.player_branch += 1
                        self.player_side = False
                        self.target_offset_y = self.offset_y - 340
                        self._update_player_transition(self.player_position,self._offset[0][self.player_branch] + self._player_offset[2 if self._branch_list[self.player_branch] else 0])

                
        self._update_cloud_positions()
        self._update_tree_positions()
        if not self.player_dead:
            self._update_branch_positions()
        self._update_floor()
        if self.player_dead:
            self._update_game_over()
        else:
            self.offset_y += (self.target_offset_y - self.offset_y)/10
        self.player.position = self.player_position - Vec2(0,self.offset_y)
        self.branch_collection.position_debug.text="Mouse position: " + str(self._core.cursor.position) + " Offset: " + str(self.offset_y) + " Fps: "+str(int(self._core.fps)) + " Delta: " +str(getattr(self,"d",None)) + str(self.player_position)
       
    def _update_game_over(self):
        self.d = self._core.tick_count - self.player_kill_tick
        branch_id = f"branch_{'good' if self._branch_list[self.player_branch] != self.player_side else 'bad'}_{self.player_branch}"
        branch = getattr(self.map,branch_id,None)
        branch_exist = branch != None
        
        show = self._offset[1 if self.player_side else 0][self.player_branch]
        hide = Vec2(-1000,-1000) 
        
        if self.d < 90 and branch_exist:
            if self.last_status != False:
                self.last_status = False
                branch.position = hide
                print("hide",self.d)
        elif self.d < 120 and branch_exist :
            if self.last_status != True:
                self.last_status = True
                branch.position = show - Vec2(0,self.offset_y)
                print("show",self.d)
        elif self.d < 150 and branch_exist :
            if self.last_status != False:
                self.last_status = False
                branch.position = hide
                print("hide",self.d)
        elif self.d < 180 and branch_exist :
            if self.last_status != True:
                self.last_status = True
                branch.position = show - Vec2(0,self.offset_y)
                print("show",self.d)
        elif self.d < 210 and branch_exist :
            if self.last_status != False:
                self.last_status = False
                branch.position = hide
                print("hide",self.d)
                
        elif self.d < 310:
            self.player_position = reverse_elastic_interpolation(self.player_transition_end,self.player_transition_end + Vec2(0,1080),(self._core.tick_count - (self.player_kill_tick+210))/100)

       
    def _update_player_transition(self,start = None,end = None):
        if not self.player_in_transition:
            self.start_player_count = self._core.tick_count
            self.player_in_transition = True
            self.player_transition_start= start
            self.player_transition_end= end

        else:
            
            if (self._core.tick_count - self.start_player_count) <= 30:
                self.player_position = ease_in_out_quadratic_bezier(self.player_transition_start,Vec2(self.player_transition_start.x,self.player_transition_end.y),self.player_transition_end,(self._core.tick_count - self.start_player_count)/30) 
            else:
                self.player_position = self.player_transition_end
                self.player_in_transition = False
                if self._branch_list[self.player_branch] == self.player_side:
                    self.player_dead = True
                    self.player_kill_tick = self._core.tick_count
                    self.offset_y = self.target_offset_y-1
                    self._update_branch_positions()
    

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
