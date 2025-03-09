import threading
import traceback
import time
from line_profiler import profile
import os
import ctypes

from HeraEngine.logger import Logger
from HeraEngine.childs.Entity import Entity
from HeraEngine.render.pipeline import PipeLine
from HeraEngine.cursor import Cursor

from HeraEngine.types.Vec2 import Vec2

class Core():
    def __init__(self,start,update):

        self.ascii_art = """
Powered by
╦ ╦┌─┐┬─┐┌─┐╔═╗┌┐┌┌─┐┬┌┐┌┌─┐
╠═╣├┤ ├┬┘├─┤║╣ ││││ ┬││││├┤ 
╩ ╩└─┘┴└─┴ ┴╚═╝┘└┘└─┘┴┘└┘└─┘"""

        self.os = os.name
        self.is_windows = self.os == "nt"
        self.running = False
        self.EntityList = {1:[],2:[],3:[],4:[]}
        self._fullscreen = False
        self._size = Vec2(500,500)

        self.ver = "1.0.3"

        self.log = Logger()
        self.Pipeline = PipeLine(self.size)
        self.cursor = Cursor()
        self.clear = False

        self.tick_count = 0
        self.fps = 0

        self.log.INFO(self.ascii_art)

        if self.is_windows:
            self.log.DEBUG(f"Detected platform: Windows, importing window")
            from HeraEngine.window import Window
            self.window = Window(self,self.size,self.cursor)
            self.log.DEBUG(f"Loaded Window Size: {self.window.Size}")

        else:
            self.log.DEBUG(f"Detected platform: Unix (Max/Linux), importing pygame_adapter")
            from HeraEngine.pygame_adapter import Window
            self.window = Window(self,self.size,self.cursor)
            self.log.DEBUG(f"Loaded Window (PyGame Adapter) Size: {self.window.Size}")

        self.start = start
        self.update = update


    @property
    def fullscreen(self):
        return self._fullscreen
    
    @fullscreen.setter
    def fullscreen(self,value):
        self._fullscreen = value
        self.window.fullscreen = value
        fullsize = self.window.GetFullscreenSize()
        self.size = Vec2(fullsize[0],fullsize[1])

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self,value):
        if not isinstance(value, Vec2):
            raise TypeError(f"Size should be a Vec2, not {value.__class__.__name__}")
        self._size = value
        self.Pipeline.update(size=self._size) 
        self.Pipeline.clear_buffer()

    def add_entity(self,target):
        if isinstance(target,Entity):
            self.EntityList[target.layer].append(target)
        else:
            raise TypeError("Target is not an Entity.")
        
    def remove_entity(self,target):
        if target in self.EntityList[1]:
            self.EntityList[1].remove(target)
        if target in self.EntityList[2]:
            self.EntityList[2].remove(target)
        if target in self.EntityList[3]:
            self.EntityList[3].remove(target)
        if target in self.EntityList[4]:
            self.EntityList[4].remove(target)

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
            self.log.INFO("Code Ended. Goodbye ;)")

        except SystemExit:
                raise
        except Exception as e:
            traceback.print_exc()
            self.log.ERROR(f"Failed to start: {e}")

    @profile
    def run_updates(self):
        while self.running:
            self.tick_count += 1
            try:

                #Actual code that does everything, break this and everything explode.
                start_time = time.time()
                self.cursor.update()
                self.update(self) #Run the update function
                self.Pipeline.update(EntityList=self.EntityList) #Updates the pipeline with the existing entites, including positions and stuff because it might have changed 
                self.Pipeline.render() #Drawing the screen
                self.window.buffer = self.Pipeline.BackgroundBuffer #Updating the window data
                self.window.update() #Drawing the window
                if self.clear:
                    self.Pipeline.clear_buffer()
                end_time = time.time()


                execution_time = end_time - start_time
                execution_time += 0.00000001 #Prevent Divisions by 0 in fps calculation
                self.fps = 1/execution_time
            except SystemExit:
                raise
            except Exception as e: 
                traceback.print_exc()
                self.log.ERROR(f"Failed to run update : {e}")
                raise Exception("Crashed")
            
    def quit(self):
        self.window.kill = True
        quit(0)