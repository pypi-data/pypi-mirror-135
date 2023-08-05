import sys

from py2048.downloader import download_assets
sys.path.append("../..")

import pygame as pyg
from pygame._sdl2.video import Window
import py2048.move_window as mw
from py2048.measures import *
from py2048.Board import *
from py2048.downloader import *
import itertools as it

def main():
    pyg.init()
    Direction.init()

    if not os.path.exists(font_path):
        download_assets()

    Board.Tile.init()

    monitor = pyg.Vector2(pyg.display.Info().current_w, pyg.display.Info().current_h)
    
    screen = pyg.display.set_mode(WINDOW_SIZE, pyg.NOFRAME)
    
    window = Window.from_display_module()
    window.position = ((monitor.x - WINDOW_SIZE[0]) / 2, (monitor.y - WINDOW_SIZE[1]) / 2)

    pyg.display.set_caption("2048")

    board_instance = Board()

    game_clock = pyg.time.Clock()

    pressed = False
    start_pos = (0, 0)
    while True:
        game_clock.tick(200)

        for event in pyg.event.get():
            mouse_pos = pyg.mouse.get_pos()
            if event.type == pyg.QUIT or (event.type == pyg.KEYDOWN and pyg.key.get_pressed()[pyg.K_ESCAPE]):
                running = False
                break
            elif event.type == pyg.KEYDOWN:
                if pyg.key.get_pressed()[pyg.K_r]:
                    board_instance.reset(wait = False)
                board_instance.on_keydown()
            mw.check_event(window, event)
            
        if pyg.key.get_pressed()[pyg.K_ESCAPE]:
            break
        
        screen.fill((187, 173, 160))
        
        for placeholder in it.chain.from_iterable(PLACEHOLDER_ARRAY):
            pyg.draw.rect(screen, (205, 193, 180), placeholder, border_radius = 1)
        board_instance.draw()
        
        board_instance.update()

        pyg.display.flip()
    
    board_instance.write_file()
    pyg.quit()

if __name__ == "__main__":
    main()