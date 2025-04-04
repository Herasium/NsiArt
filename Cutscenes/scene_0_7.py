from HeraEngine import *
import time
from Transitions.dream_2 import Dream2

class Scene07():
    
    def __init__(self, core: Core):
        self.core = core
        self.core.update = self.update
        self.cut_text = lambda s, x: s[:int(len(s) * x)]
        self.Text = [
    "Alors comme ca c'est toi la nouvelle ?",
    "...",
    "Tu peux me parler tu sais, je vais pas te bouffer..",
    "(pathetique)",
    "Tu sais quoi si tu es timide, viens demain sur le toit..",
    "Qu'on parle juste nous deux."
]


        self.current_text_index = 0
        self.display_progress = 0.0
        self.last_update_time = time.time()
        self.text_speed = 0.01  # Speed of text appearance (lower is faster)
        self.pause_time = 3     # Pause between sentences (in seconds)
        self.displaying_text = True
        self.old_text = ""
        self.cutscene_finished = False  # Flag to avoid printing multiple times

    def finish_cutscene(self):
       self.scene.quit()
       Dream2(self.core)

    def update(self, _):
        current_time = time.time()
        
        if self.current_text_index < len(self.Text):
            if self.displaying_text:
                elapsed = current_time - self.last_update_time
                self.display_progress += elapsed * self.text_speed
                
                if self.display_progress >= 1.0:
                    self.display_progress = 1.0
                    self.displaying_text = False
                    self.last_update_time = current_time  
                
                displayed_text = self.cut_text(self.Text[self.current_text_index], self.display_progress)
                self.scene.textline.text = displayed_text
                if displayed_text != self.old_text:
                    self.old_text = displayed_text
            else:
                if current_time - self.last_update_time > self.pause_time:
                    self.current_text_index += 1
                    self.display_progress = 0.0
                    self.displaying_text = True
                    self.last_update_time = current_time
        else:
            if not self.cutscene_finished:
                self.cutscene_finished = True
                self.finish_cutscene()

    def _setup_scene(self):
        self.scene = Collection(self.core)
        self.scene.Entity("bg", size=Vec2(1920, 1080), position=Vec2(0, 0), 
                          color=Color(255, 0, 0), layer=layers.background, 
                          texture="Assets/Textures/Cutscenes/0/3.raw")
        self.scene.Entity(layer=layers.background, name="text_bg", size=Vec2(1260, 252), 
                          position=Vec2(330, 800), texture="Assets/Textures/Fonts/Background/back_1.raw")
        self.scene.Text(layer=layers.background, name="textline", font=self.core.monogram_big, 
                        position=Vec2(360, 845), size=Vec2(50, 500), text="")

    def setup(self):
        self._setup_scene()
