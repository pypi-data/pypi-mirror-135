import unittest
from py2048.Board import *
from copy import deepcopy
import itertools as it
from measures import *

class TestBoard(unittest.TestCase):
    def general_test(self, tile_init_args : list, assertion_list : list, dir : Direction) -> None:
        """Tuple format : grid position (tuple), number
        tile_init_args should be a list of places where you want to put tiles. \n
        Each element of assertion list will be used to check the number at a specific grid position."""
        boards = [Board() for x in range(0, 3)]

        tile_adders = []
        for tup in tile_init_args:
            tile_adders.append(lambda x : x.group.add(Board.Tile(pyg.Vector2(tup[0]), tup[1])))

        tile_arg_perms = list(it.permutations(tile_init_args))

        for board, perm in zip(boards, tile_arg_perms): # Add the tiles in different orders
            board.group.empty()
            for arg in perm:
                board.group.add(Board.Tile(pyg.Vector2(arg[0]), arg[1]))
            board.move_board(dir)

        #Wait until the board has finished moving
        arrays_moving = True
        while arrays_moving:
            arrays_moving = False
            for board in boards:
                board.update()
                if board.array_moving:
                    arrays_moving = True
        
        for board in boards:
            board_list = board.generate_list()
            
            #Test if there board is in the expected configuration
            for a_grid, a_num in assertion_list:
                assert(board_list[a_grid[0]][a_grid[1]].number == a_num)
            
            #Test if there are tiles which occupy the same grid position
            tiles_in_list = 0
            for row in board_list:
                for tile in row:
                    if tile != 0:
                        tiles_in_list += 1

            assert(tiles_in_list == len(board.group))

    def test_vertical_upper(self):
        self.general_test([((0, 0), NUMBER_LIST[0]), ((0, 1), NUMBER_LIST[0]), ((0, 2), NUMBER_LIST[1])], \
            [((0, 0), NUMBER_LIST[1]), ((0, 1), NUMBER_LIST[1])], Direction.UP)
        print("Testing two 2 tiles in the first vertical column followed by a 4 below them, then moving up")

    def test_vertical_lower(self):
        self.general_test([((0, 0), NUMBER_LIST[0]), ((0, 1), NUMBER_LIST[0]), ((0, 2), NUMBER_LIST[1])], \
            [((0, BOARD_SIZE - 2), NUMBER_LIST[1]), ((0, BOARD_SIZE - 1), NUMBER_LIST[1])], Direction.DOWN)
        print("Testing two 2 tiles in the first vertical column followed by a 4 below them, then moving down")

    def test_horizontal_upper(self):
        self.general_test([((0, 0), NUMBER_LIST[0]), ((1, 0), NUMBER_LIST[0]), ((2, 0), NUMBER_LIST[1])], \
            [((0, 0), NUMBER_LIST[1]), ((1, 0), NUMBER_LIST[1])], Direction.LEFT)
        print("Testing two 2 tiles in the first row followed by a 4 in front of them, then moving left")

    def test_horizontal_lower(self):
        self.general_test([((0, 0), NUMBER_LIST[0]), ((1, 0), NUMBER_LIST[0]), ((2, 0), NUMBER_LIST[1])], \
            [((BOARD_SIZE - 2, 0), NUMBER_LIST[1]), ((BOARD_SIZE - 1, 0), NUMBER_LIST[1])], Direction.RIGHT)
        print("Testing two 2 tiles in the first row followed by a 4 in front of them, then moving right")

if __name__ == "__main__":
    unittest.main()