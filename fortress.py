#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
# Make sure 'dejavu10x10_gs_tc.png' is in the same directory as this script.
import tcod

WIDTH, HEIGHT = 16, 16  # Console width and height in tiles.

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
            console.print(x=0, y=0, string="""╔╦╦╦╦╦╦╦╦╦╦╦╦╦╦╗\n╠              ╣\n╠   FORTRESS   ╣\n╠              ╣\n╠   ╔╦╦╦╦╦╦╗   ╣\n╠   ╠┌────┐╣   ╣\n╠   ╠│PLAY│╣   ╣\n╠   ╠└────┘╣   ╣\n╠   ╠      ╣   ╣\n╠   ╠CREDIT╣   ╣\n╠   ╠      ╣   ╣\n╠   ╚╩╩╩╩╩╩╝   ╣\n╠              ╣\n╠              ╣\n╠              ╣\n╚╩╩╩╩╩╩╩╩╩╩╩╩╩╩╝""")
            context.present(console, keep_aspect=True, clear_color=(255,0,0))  # Show the console.

            for event in tcod.event.wait():
                context.convert_event(event)  # Sets tile coordinates for mouse events.
                print(event)  # Print event information to stdout.
                if event.type == "QUIT":
                    raise SystemExit()
        # The window will be closed after the above with-block exits.


if __name__ == "__main__":
    main()