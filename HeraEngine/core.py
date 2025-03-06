import threading
import traceback
import time
import os

from HeraEngine.logger import Logger
from HeraEngine.childs.Entity import Entity
from HeraEngine.render.pipeline import PipeLine

from HeraEngine.types.Vec2 import Vec2

class Core():
    def __init__(self,start,update):

        self.os = os.name
        self.is_windows = self.os == "nt"
        self.log = Logger()
        self.running = False
        self.EntityList = {1:[],2:[],3:[],4:[]}
        self.size = Vec2(100,100)
        self.Pipeline = PipeLine(self.size)
        self.tick_count = 0

        if self.is_windows:
            self.log.DEBUG(f"Detected platform: Windows, importing window")
            from HeraEngine.window import Window
            self.window = Window(self)
            self.window.SetWindowSize(self.size)
            self.log.DEBUG(f"Loaded Window Size: {self.window.Size}")

        else:
            self.log.DEBUG(f"Detected platform: Unix (Max/Linux), importing pygame_adapter")
            from HeraEngine.pygame_adapter import Window
            self.window = Window(self)
            self.window.SetWindowSize(self.size)
            self.log.DEBUG(f"Loaded Window (PyGame Adapter) Size: {self.window.Size}")

        self.start = start
        self.update = update

    def add_entity(self,target):
        if isinstance(target,Entity):
            self.EntityList[target.layer].append(target)
        else:
            raise TypeError("Target is not an Entity.")

    def run(self):
        try:
            self.running = True
            self.log.DEBUG("Launching Start function")
            self.start(self)
            update_thread = threading.Thread(target=self.run_updates)
            update_thread.daemon = True
            update_thread.start()
            self.log.DEBUG("Launched Update thread.")
            self.window.MainWin()
            self.log.INFO("Launched Start Function, Update thread and Launched main window.")
                    
        except Exception as e:
            traceback.print_exc()
            self.log.ERROR(f"Failed to start: {e}")

    def run_updates(self):
        while self.running:
            self.tick_count += 1
            try:
                start_time = time.time()
                self.update(self)
                self.Pipeline.update(EntityList=self.EntityList)
                self.Pipeline.render()

                for y in range(self.size.y):
                    for x in range(self.size.x):
                        self.window.SetPixelColor(x,y,self.Pipeline.BackgroundBuffer[y*self.size.y+x])

                self.window.update()
                self.Pipeline.clear_buffer()
                end_time = time.time()

                execution_time = end_time - start_time
                execution_time += 0.00000001 #Prevent Divisions by 0 in fps calculation
                self.log.DEBUG(f"FPS: {1/execution_time}")
            except Exception as e: 
                traceback.print_exc()
                self.log.ERROR(f"Failed to run update : {e}")