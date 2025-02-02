import threading
import traceback
import time
from modules.render import RenderEngine
from modules.logger import Logger
import os

class Core():
    def __init__(self,start,update):

        self.os = os.name
        self.is_windows = self.os == "nt"
        self.log = Logger()

        if self.is_windows:
            from modules.window import Window
            self.window = Window(self)

        else:
            from modules.pygame_adapter import Window
            self.window = Window(self)

        self.render = RenderEngine(self)
        self.start = start
        self.update = update

    def run(self):
        try:
            self.start(self)
            update_thread = threading.Thread(target=self.run_updates)
            update_thread.daemon = True
            update_thread.start()
            self.window.MainWin()
                    
        except Exception as e:
            traceback.print_exc()
            self.log.ERROR(f"Code crashed: {e}")

    def run_updates(self):
        while True:
            try:
                start_time = time.time()
                self.update(self)
                end_time = time.time()

                execution_time = end_time - start_time
                execution_time += 0.00000001
                
            except Exception as e: 
                traceback.print_exc()
                self.log.ERROR(f"Failed to run update : {e}")