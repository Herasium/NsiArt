from modules.window import Window
import threading
import time

class Core():
    def __init__(self,start,update):
        self.window = Window()
        self.start = start
        self.update = update

    def run(self):
        self.start(self)
        update_thread = threading.Thread(target=self.run_updates)
        update_thread.daemon = True
        update_thread.start()
        self.window.MainWin()

    def run_updates(self):
        while True:
            start_time = time.time()
            self.update(self)
            end_time = time.time()

            execution_time = end_time - start_time
            execution_time += 0.00000001
            print(f"FPS: {1/execution_time}")