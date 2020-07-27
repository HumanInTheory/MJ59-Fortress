#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
import tcod
import numpy as np

WIDTH, HEIGHT = 16, 16  # Console width and height in tiles.

class Map:
    """Contains all drawing info"""
    def __init__(self, w, h, fg: tuple=(255,255,255,255), bg: tuple=(0,0,0,255)):
        self.buffer = np.zeros(
                shape=(w, h),
                dtype=tcod.console.Console.DTYPE,
                order="F",
            )
        self.buffer["fg"][:,:] = fg
        self.buffer["bg"][:,:] = bg
    
    def setchar(self, char, x, y):
        self.buffer["ch"][y,x] = char

    def setfg(self, color, x, y):
        self.buffer["fg"][y,x] = color

    def setbg(self, color, x, y):
        self.buffer["bg"][y,x] = color

    def getbuffer(self):
        return self.buffer

    def getchar(self, x, y):
        return self.buffer["ch"][y,x]

    def fillchar(self, char):
        self.buffer["ch"][:,:] = char

    def fillfg(self, color):
        self.buffer["fg"][:,:] = color

    def fillbg(self, color):
        self.buffer["bg"][:,:] = color

    def draw_wall(self, thick, x, y, w, h):
        for i in range(x, x+w):
            for j in range(y, y+h):
                if (i==x):
                    if (j==y):
                        char = ('╔' if thick else'┌')
                    elif (j==y+h-1):
                        char = ('╚' if thick else '└')
                    else:
                        char = ('╠' if thick else '│')
                elif (i==x+w-1):
                    if (j==y):
                        char = ('╗' if thick else '┐')
                    elif (j==y+h-1):
                        char = ('╝' if thick else '┘')
                    else:
                        char = ('╣' if thick else '│')
                else:
                    if (j==y):
                        char = ('╦' if thick else '─')
                    elif (j==y+h-1):
                        char = ('╩' if thick else '─')
                    else:
                        char = ' '
                self.setchar(ord(char), i, j)
    
    def print_str(self, x, y, str, vert: bool=False):
        if (vert):
            for i in range(len(str)):
                self.setchar(ord(str[i]), x, y+i)
        else:
            for i in range(len(str)):
                self.setchar(ord(str[i]), x+i, y)

class Selector:
    def __init__(self, x, y, w, h):
        self.selected = False
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.map = Map(h, w)
        self.selfg = (0, 255, 0, 255)
        self.selbg = (64, 128, 64, 255)
        self.unselfg = (255, 255, 255, 255)
        self.unselbg = (0, 0, 0, 255)
    
    def setselected(self, set):
        if (set):
            self.map.fillfg(self.selfg)
            self.map.fillbg(self.selbg)
        else:
            self.map.fillfg(self.unselfg)
            self.map.fillbg(self.unselbg)

    def draw_sel(self, cnsl):
        for i in range(0,self.w):
            for j in range(0,self.h):
                cnsl.tiles[self.y+j,self.x+i] = self.map.buffer[j,i]

class UI:
    def __init__(self):
        self.cells = []
        self.currentcell = 0

    def addcell(self, cell):
        self.cells.append(cell)
        self.cells[0].setselected(True)

    def process_input(self, input):
        self.cells[self.currentcell].setselected(False)
        if (input):
            self.currentcell += 1
        else:
            self.currentcell -= 1
        self.currentcell = self.currentcell%len(self.cells)
        self.cells[self.currentcell].setselected(True)

    def draw_ui(self, cnsl):
        for i in range(len(self.cells)):
            self.cells[i].draw_sel(cnsl)

class Scene():
    def __init__(self):
        self.map = Map(WIDTH, HEIGHT)
        self.ui = UI()
        self.entities = []

    def process_input(self, event):
        return ""

    def draw(self, cnsl):
        for i in range(WIDTH):
            for j in range(HEIGHT):
                cnsl.tiles[i, j] = self.map.buffer[i, j]
                self.ui.draw_ui(cnsl)
                for k in range(len(self.entities)):
                    self.entities[k].draw(cnsl)

class GameState():
    def __init__(self, initialscene):
        self.currentscene = initialscene

    def set_scene(self, newscene):
        self.currentscene = newscene

class Sprite():
    def __init__(self, x, y, char, color: tuple=(255,255,255,255)):
        self.x = x
        self.y = y
        self.map = Map(1,1, fg=(color))
        self.map.setchar(ord(char),0,0)
        self.health = 4

    def setpos(self, x, y):
        self.x = x
        self.y = y

    def move(self, vel_x, vel_y):
        self.x += vel_x
        self.y += vel_y

    def takedamage(self):
        self.health -= 1

    def draw(self, cnsl):
        cnsl.tiles[self.y, self.x] = self.map.buffer[0,0]

# Main Menu State
# Make the map
menu = Map(16, 16)
menu.draw_wall(True,0,0,16,16)
menu.draw_wall(True,0,0,4,4)
menu.draw_wall(True,12,0,4,4)
menu.draw_wall(True,0,12,4,4)
menu.draw_wall(True,12,12,4,4)
menu.draw_wall(False,4,4,8,8)
menu.print_str(4,2,"FORTRESS")

# Make the ui
menu_ui = UI()
play = Selector(6,6,4,1)
play.map.print_str(0,0,"PLAY")
menu_ui.addcell(play)
credit = Selector(5,9,6,1)
credit.map.print_str(0,0,"CREDIT")
menu_ui.addcell(credit)

# Declare the state
class MainMenu(Scene):
    def __init__(self):
        self.map = menu
        self.ui = menu_ui
        self.entities = []

    def process_input(self, event):
        if event.type == "KEYDOWN":
            if event.scancode == tcod.event.SCANCODE_UP:
                menu_ui.process_input(True)
            elif event.scancode == tcod.event.SCANCODE_DOWN:
                menu_ui.process_input(False)
            elif event.scancode == tcod.event.SCANCODE_RETURN:
                if menu_ui.currentcell == 0:
                    return "play"
                else:
                    return "credits"
        return ""

# Make the credits state
# Make the map
credits = Map(16, 16)
credits.draw_wall(True,0,0,16,16)
credits.draw_wall(True,0,0,4,4)
credits.draw_wall(True,12,0,4,4)
credits.draw_wall(True,0,12,4,4)
credits.draw_wall(True,12,12,4,4)
credits.print_str(4,2,"FORTRESS")
credits.print_str(2,5,"HUMANINTHEORY")
credits.print_str(2,7,"ASSETS:KENNY")
credits.print_str(3,9,"MADE USING")
credits.print_str(4,10,"LIBTCOD")
credits.print_str(5,11,"NUMPY")
# No ui
empty_ui = UI()

class Credits(Scene):
    def __init__(self):
        self.map = credits
        self.ui = empty_ui
        self.entities = []
    
    def process_input(self, event):
        if event.type == "KEYDOWN":
            if event.scancode == tcod.event.SCANCODE_ESCAPE:
                return "main"
        return ""

# Setting up the arena
arena = Map(16,16)
arena.draw_wall(True,0,0,16,16)
arena.draw_wall(True,0,0,4,4)
arena.draw_wall(True,12,0,4,4)
arena.draw_wall(True,0,12,4,4)
arena.draw_wall(True,12,12,4,4)

player = Sprite(8,14,"Ç",(0,255,0,255))
skeleton = Sprite(7,1,"é")

class Arena(Scene):
    def __init__(self):
        self.map = arena
        self.ui = empty_ui
        self.entities = [skeleton, player]

    def reset(self):
        self.entities[0] = Sprite(7,1,"é")
        self.entities.append(Sprite(8,14,"Ç",(0,255,0,255)))
    
    def process_input(self, event):
        vel_x = 0
        vel_y = 0
        win = ""
        if event.type == "KEYDOWN":
            if event.scancode == tcod.event.SCANCODE_ESCAPE:
                return "main"
            elif event.scancode == tcod.event.SCANCODE_UP:
                vel_y = -1
            elif event.scancode == tcod.event.SCANCODE_DOWN:
                vel_y = 1
            elif event.scancode == tcod.event.SCANCODE_LEFT:
                vel_x = -1
            elif event.scancode == tcod.event.SCANCODE_RIGHT:
                vel_x = 1
            win = self.process_movement(vel_x, vel_y)
        return win

    def process_movement(self, vel_x, vel_y):
        for i in range(len(self.entities)):
            wall = False
            while not wall:
                if self.map.getchar(self.entities[i].x+vel_x,self.entities[i].y+vel_y) == ord(" "):
                    self.entities[i].move(vel_x, vel_y)
                else:
                    wall = True
            for j in range(len(self.entities)-1):
                if self.entities[i].x == self.entities[j].x and self.entities[i].y == self.entities[j].y and i != j:
                    self.entities.remove(self.entities[j])
        if len(self.entities) == 1:
            self.reset()
            return "win"
        return ""

# Make the win state
# Make the map
win = Map(16, 16)
win.draw_wall(True,0,0,16,16)
win.draw_wall(True,0,0,4,4)
win.draw_wall(True,12,0,4,4)
win.draw_wall(True,0,12,4,4)
win.draw_wall(True,12,12,4,4)
win.print_str(4,2,"FORTRESS")
win.print_str(5,5,"WINNER")
win.print_str(2,7,"ASSETS:KENNY")
win.print_str(3,9,"MADE USING")
win.print_str(4,10,"LIBTCOD")
win.print_str(5,11,"NUMPY")
# No ui

class Win(Scene):
    def __init__(self):
        self.map = win
        self.ui = empty_ui
        self.entities = []
    
    def process_input(self, event):
        if event.type == "KEYDOWN":
            if event.scancode == tcod.event.SCANCODE_ESCAPE:
                return "main"
        return ""

def main() -> None:
    """Script entry point."""
    # Load the font, a 10 by 10 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        "KennyCP437.png", 16, 16, tcod.tileset.CHARMAP_CP437,
    )
    # Create the main console.
    console = tcod.Console(WIDTH, HEIGHT)
    mainmenu_s = MainMenu()
    credits_s = Credits()
    arena_s = Arena()
    win_s = Win()
    statemachine = GameState(mainmenu_s)
    # Create a window based on this console and tileset.
    with tcod.context.new_terminal(
        console.width, console.height, tileset=tileset,
    ) as context:
        while True:  # Main loop, runs until SystemExit is raised.
            console.clear()
            statemachine.currentscene.draw(console)
            context.present(console, keep_aspect=True, clear_color=(0,0,0))  # Show the console.
            for event in tcod.event.wait():
                context.convert_event(event)  # Sets tile coordinates for mouse events.
                print(event)  # Print event information to stdout.
                newstate = statemachine.currentscene.process_input(event)
                if newstate == "main":
                    statemachine.set_scene(mainmenu_s)
                elif newstate == "credits":
                    statemachine.set_scene(credits_s)
                elif newstate == "play":
                    statemachine.set_scene(arena_s)
                elif newstate == "win":
                    statemachine.set_scene(win_s)
                if event.type == "QUIT":
                    raise SystemExit()
        # The window will be closed after the above with-block exits.


if __name__ == "__main__":
    main()