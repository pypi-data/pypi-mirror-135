from tkinter import font
import pygame as pyg
from random import *
from py2048.measures import *
from copy import deepcopy
import jsonpickle
import os
import threading
from math import log10
import itertools as it
from py2048.Button import Button
from py2048.downloader import *

pyg.font.init()

def do_twice(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper

class Direction():
    UP    = pyg.Vector2( 0, -1) 
    DOWN  = pyg.Vector2( 0,  1) 
    LEFT  = pyg.Vector2(-1,  0) 
    RIGHT = pyg.Vector2( 1,  0) 
    NONE  = pyg.Vector2( 0,  0)
    LIST  = [] #Order : Up, down, left, right
    
    @classmethod
    def init(cls):
        cls.LIST = [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]

class Board():
    HIGHER_NUMBER_CHANCE = 0.10

    class Tile(pyg.sprite.Sprite):
        font_dict = {}
        SPEED = 10

        def __init__(self, location, number):
            pyg.sprite.Sprite.__init__(self)
            self.number = number
            self.grid_coords = location
            self.dir = Direction.NONE
            self.update_rectangle()
            self.update_text()
            self.set_color()
            self.merged = False #Flag to ensure that a tile does not merge twice during a single loop (unintended behavior)

        @classmethod
        def init(cls):
            if not cls.font_dict:
                cls.font_dict = {digit : pyg.font.Font(font_path, \
                    int(2 * DIMENSION / (digit + 1))) for digit in range(3, 7 + 1)}


        def update_rectangle(self):
            self.rect = PLACEHOLDER_ARRAY[int(self.grid_coords.x)][int(self.grid_coords.y)].copy()

        def update_text(self):
            self.text = Board.Tile.font_dict[max(int(log10(self.number)) + 1, 3)].render(str(self.number), True, (249, 246, 242) if self.number > NUMBER_LIST[1] else (119, 110, 101))

        def initiate_move(self, dir):
            self.dir = dir

        def update(self, tile_list):
            if self.rect.left not in POS_VALUES or self.rect.top not in POS_VALUES or self._can_move(tile_list):
                self.rect.move_ip(Board.Tile.SPEED*self.dir)
            else:
                self.dir = Direction.NONE

            self._update_grid_coords()

        def _update_grid_coords(self):
            if self.rect.left in POS_VALUES and self.rect.top in POS_VALUES:
                self.grid_coords = pyg.Vector2(POS_VALUES.index(self.rect.left), POS_VALUES.index(self.rect.top))

        def _can_move(self, tile_list):
            return self.can_move(self.dir, tile_list)

        def can_move(self, dir, tile_list):
            if dir != Direction.NONE and \
               0 <= self.grid_coords.x + dir.x <= BOARD_SIZE - 1 and 0 <= self.grid_coords.y + dir.y <= BOARD_SIZE - 1:
                next_coords = self.grid_coords + dir
                next = tile_list[int(next_coords.x)][int(next_coords.y)]
                if next == 0 or (next.number == self.number and not (self.merged or next.merged)) or next.can_move(dir, tile_list):
                    return True 
            return False

        def set_color(self):
            self.color = NUMBER_COLOR_DICT[self.number]

        def double(self):
            self.number = NUMBER_LIST[NUMBER_LIST.index(self.number) + 1]
            self.merge()
            self.set_color()
            self.update_text()

        def merge(self):
            self.merged = True
        
        def draw(self):
            screen = pyg.display.get_surface()
            text_rect = self.text.get_rect()
            text_rect.center = self.rect.center

            rect = pyg.draw.rect(screen, self.color, self.rect, border_radius = 1)
            screen.blit(self.text, text_rect)
            return rect

    def __init__(self):
        self.group = pyg.sprite.Group()
        self.array_moving = False
        self.try_read_file()

    @do_twice
    def start(self):
        board_list = self.generate_list()
        self.add_tile(board_list)

    def reset(self, wait = True):
        if wait:
            event = threading.Event()
            event.wait(timeout=2)
        self.group.empty()
        self.start()
    
    def add_tile(self, board_list):
        zeros = []
        for x, row in enumerate(board_list):
            for y, tile_space in enumerate(row):
                if tile_space == 0:
                    zeros.append(pyg.Vector2(x, y))
        if zeros:
            self.group.add(Board.Tile(choice(zeros), NUMBER_LIST[1] if random() <= Board.HIGHER_NUMBER_CHANCE else NUMBER_LIST[0]))

    def move_board(self, dir):
        for tile in self.group:
            tile.initiate_move(dir)

    def generate_list(self):
        a = [[0 for y in range(0, BOARD_SIZE)] for x in range(0, BOARD_SIZE)]
        for tile in self.group:
            a[int(tile.grid_coords.x)][int(tile.grid_coords.y)] = tile
        return a
        
    def draw(self):
        rect_list = []
        for tile in self.group:
            rect_list.append(tile.draw())
        pyg.display.update(rect_list)

    def update(self):
        board_list = self.generate_list()

        last_array_moving = deepcopy(self.array_moving)
        self.array_moving = False

        for tile in self.group:
            tile.update(board_list)
            if tile.dir != Direction.NONE:
                self.array_moving = True
        if last_array_moving:
            self.merge()
            if not self.array_moving:
                for tile in self.group:
                    tile.merged = False
                self.add_tile(board_list)
        if self.check_loss(board_list):
            self.reset()

    def on_keydown(self):
        if not self.array_moving:
            dir = Direction.NONE
            if pyg.key.get_pressed()[pyg.K_UP]:
                dir = Direction.UP
            elif pyg.key.get_pressed()[pyg.K_DOWN]:
                dir = Direction.DOWN
            elif pyg.key.get_pressed()[pyg.K_LEFT]:
                dir = Direction.LEFT
            elif pyg.key.get_pressed()[pyg.K_RIGHT]:
                dir = Direction.RIGHT
            if dir != Direction.NONE:
                self.move_board(dir)
    def merge(self):
        for a, b in it.combinations(self.group, 2):
            if a.rect.center == b.rect.center:
                    a.double()
                    b.kill()

    def check_loss(self, tile_list):
        if len(self.group) == BOARD_SIZE**2:
            for tile in self.group:
                if tile.can_move(Direction.UP, tile_list)   or tile.can_move(Direction.DOWN, tile_list) or \
                   tile.can_move(Direction.LEFT, tile_list) or tile.can_move(Direction.RIGHT, tile_list): 
                    #Determines if any box can move in any direction
                    return False
            return True

    def try_read_file(self):
        if os.path.isfile(save_path) and os.path.getsize(save_path) != 0: 
            with open(save_path, 'r') as f:
                tile_list = jsonpickle.decode(f.read())
                for tile in tile_list:
                    tile.add(self.group)
                    tile.update_text()
                    tile.update_rectangle()
                    tile.set_color()
                f.close()
        else:
            self.start()

    def write_file(self):
        with open(save_path, 'w') as f:
            tile_list = []
            for tile in self.group:
                tile.kill() #Makes sure that the group itself is not saved
                tile_list.append(tile)
            f.write(jsonpickle.encode(tile_list, indent=4))
            f.close()