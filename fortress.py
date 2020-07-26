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

    def drawWall(self, thick, x, y, w, h):
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
    
    def printStr(self, x, y, str, vert: bool=False):
        if (vert):
            for i in range(len(str)):
                self.setchar(ord(str[i]), x, y+i)
        else:
            for i in range(len(str)):
                self.setchar(ord(str[i]), x+i, y)

menuchar = ["╔╦╦╦╦╦╦╦╦╦╦╦╦╦╦╗",
            "╠              ╣",
            "╠   FORTRESS   ╣",
            "╠              ╣",
            "╠   ╔╦╦╦╦╦╦╗   ╣",
            "╠   ╠      ╣   ╣",
            "╠   ╠ PLAY ╣   ╣",
            "╠   ╠      ╣   ╣",
            "╠   ╠      ╣   ╣",
            "╠   ╠CREDIT╣   ╣",
            "╠   ╠      ╣   ╣",
            "╠   ╚╩╩╩╩╩╩╝   ╣",
            "╠              ╣",
            "╠              ╣",
            "╠              ╣",
            "╚╩╩╩╩╩╩╩╩╩╩╩╩╩╩╝"]

menufg = ["                ",
          "                ",
          "    rrrrrrrr    ",
          "                ",
          "                ",
          "                ",
          "      gggg      ",
          "                ",
          "                ",
          "     bbbbbb     ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                "]

menubg = ["                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                ",
          "                "]

menu = Map(16, 16)
menu.setfg((255,255,255,255),0,0)
menu.drawWall(True,0,0,16,16)
menu.drawWall(True,0,0,4,4)
menu.drawWall(True,12,0,4,4)
menu.drawWall(True,0,12,4,4)
menu.drawWall(True,12,12,4,4)
menu.drawWall(False,4,4,8,8)
menu.printStr(4,2,"FORTRESS")
menu.printStr(6,6,"PLAY")
menu.printStr(5,9,"CREDIT")

class Room:
    """A simple display class."""
    def __init__(self, name, map, p_loc, disp_player):
        self.name = name
        self.map = map
        self.p_loc = p_loc
        self.disp_player = disp_player

def draw(cnsl):
    for i in range(WIDTH):
        for j in range(HEIGHT):
            cnsl.tiles[i, j] = menu.buffer[i, j]

def main() -> None:
    """Script entry point."""
    # Load the font, a 10 by 10 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        "KennyCP437.png", 16, 16, tcod.tileset.CHARMAP_CP437,
    )
    # Create the main console.
    console = tcod.Console(WIDTH, HEIGHT)
    # Create a window based on this console and tileset.
    with tcod.context.new_terminal(
        console.width, console.height, tileset=tileset,
    ) as context:
        while True:  # Main loop, runs until SystemExit is raised.
            console.clear()
            draw(console)
            context.present(console, keep_aspect=True, clear_color=(0,0,0))  # Show the console.

            for event in tcod.event.wait():
                context.convert_event(event)  # Sets tile coordinates for mouse events.
                print(event)  # Print event information to stdout.
                if event.type == "QUIT":
                    raise SystemExit()
        # The window will be closed after the above with-block exits.


if __name__ == "__main__":
    main()