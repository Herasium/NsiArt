from HeraEngine import *
import math
import random


def start(app: Core):
    app.window.Title = "My Super Game"
    app.clear = False
    app.fullscreen = True

    app.game_ver = "0.0.2"

    app.monogram = Font("Monogram")


    #Background
    app.background = Entity(layer=layers.background,size=Vec2(1920,1080),position=Vec2(0,0),texture="Assets/Textures/Clouds/1.raw")
    app.stars = Entity(layer=layers.background,size=Vec2(1920,1080),position=Vec2(0,0),texture="Assets/Textures/Clouds/2.raw")
    app.behind_clouds = Entity(layer=layers.background,size=Vec2(1920,1080),position=Vec2(0,0),texture="Assets/Textures/Clouds/3.raw")
    app.front_clouds = Entity(layer=layers.background,size=Vec2(1920,1080),position=Vec2(0,0),texture="Assets/Textures/Clouds/4.raw")
    app.behind_clouds_copy = Entity(layer=layers.background,size=Vec2(1920,1080),position=Vec2(1920,0),texture="Assets/Textures/Clouds/3.raw")
    app.front_clouds_copy = Entity(layer=layers.background,size=Vec2(1920,1080),position=Vec2(1920,0),texture="Assets/Textures/Clouds/4.raw")

    #Main Menu
    app.main_menu_title = Entity(layer=layers.background,size=Vec2(630,81),position=Vec2(40,285),texture="Assets/Textures/Menus/Main/title.raw")
    app.main_menu_play = Entity(layer=layers.background,size=Vec2(200,63),position=Vec2(40,600),texture="Assets/Textures/Menus/Main/play.raw")
    app.main_menu_quit = Entity(layer=layers.background,size=Vec2(266,80),position=Vec2(40,685),texture="Assets/Textures/Menus/Main/quit.raw")


    #Technical
    app.fps_counter = Text(layer=layers.background,size=Vec2(100,28),position=Vec2(0,0),text="Hello World!",font=app.monogram)
    app.version_display = Text(layer=layers.background,size=Vec2(100,28),position=Vec2(0,20),text=f"Once Upon a Dream {app.game_ver} ; HeraEngine {app.ver}",font=app.monogram)
    app.cursor_tracker = Entity(layer=layers.background,size=Vec2(0,0),position=Vec2(0,0))
    app.cursor_tracker.hitbox.size = Vec2(1,1)


    #Background
    app.add_entity(app.background)
    app.add_entity(app.stars)
    #Clouds + Paralax + Infinite scrolling effect
    app.add_entity(app.behind_clouds)
    app.add_entity(app.behind_clouds_copy)
    app.add_entity(app.front_clouds)    
    app.add_entity(app.front_clouds_copy)
    #Main Menu
    app.add_entity(app.main_menu_title)
    app.add_entity(app.main_menu_play)
    app.add_entity(app.main_menu_quit)
    #Technical stuff
    app.add_entity(app.fps_counter)
    app.add_entity(app.cursor_tracker)
    app.add_entity(app.version_display)

    def on_click(cursor):
        if app.cursor_tracker.collide(app.main_menu_quit):
            app.quit()

    app.Cursor.on_right_click.append(on_click)

def update(app: Core):
    count = app.tick_count % (1920)
    count_dup = (app.tick_count/2) % (1920)
    
    app.behind_clouds.position = Vec2(0-count_dup,0)
    app.front_clouds.position = Vec2(0-count,0)
    app.behind_clouds_copy.position = Vec2(1920-count_dup,0)
    app.front_clouds_copy.position = Vec2(1920-count,0)

    app.cursor_tracker.position = app.Cursor.position

    app.main_menu_title.position = Vec2(40+math.sin(app.tick_count/50)*2,285+math.sin(app.tick_count/30)*10)

    if app.tick_count % 10 == 0:
        app.fps_counter.text = f"{int(app.fps)} FPS"

app = Core(start=start,update=update)

app.run()
