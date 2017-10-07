BLANK_PIECE = ' '
BLACK_PIECE = 'X'
WHITE_PIECE = 'O'
INTERSECTION = '+'
GRID = INTERSECTION + '-' * 3
PADDING = 1


class GameBoard(object):
    def __init__(self, dimensions: int = 8):

        if dimensions % 2 != 0:
            raise ValueError('dimensions must be even.')

        if dimensions == 2:
            raise ValueError('dimensions must be >= 4.')

        self.MAX_X = dimensions
        self.MAX_Y = dimensions

        self.board_tiles = []

        self.is_setup = False

        self.count_blank_tiles = 0
        self.count_black_tiles = 2
        self.count_white_tiles = 2

        self.blank_pieces = []

    def setup(self):
        for x in range(self.MAX_X):
            row = [Tile([x, y]) for y in range(self.MAX_Y)]
            self.board_tiles.append(row)

        self.board_tiles[int(self.MAX_X / 2) - 1][int(self.MAX_Y / 2) - 1] = Tile(
            position=[int(self.MAX_X / 2) - 1, int(self.MAX_Y / 2) - 1], tile=WHITE_PIECE)

        self.board_tiles[int(self.MAX_X / 2)][int(self.MAX_Y / 2)] = Tile(
            position=[int(self.MAX_X / 2), int(self.MAX_Y / 2)], tile=WHITE_PIECE)

        self.board_tiles[int(self.MAX_X / 2) - 1][int(self.MAX_Y / 2)] = Tile(
            position=[int(self.MAX_X / 2) - 1, int(self.MAX_Y / 2)], tile=BLACK_PIECE)

        self.board_tiles[int(self.MAX_X / 2)][int(self.MAX_Y / 2) - 1] = Tile(
            position=[int(self.MAX_X / 2), int(self.MAX_Y / 2) - 1], tile=BLACK_PIECE)

        self.is_setup = True

    def reset_game(self):
        self.board_tiles = []

        self.count_blank_tiles = 0
        self.count_black_tiles = 2
        self.count_white_tiles = 2

        self.blank_pieces = []

        self.is_setup = False

    def __count_tiles(self):
        self.count_black_tiles = 0
        self.count_white_tiles = 0
        self.count_blank_tiles = 0
        for row in self.board_tiles:
            for tile in row:
                if str(tile) == BLANK_PIECE:
                    self.count_blank_tiles += 1
                elif str(tile) == BLACK_PIECE:
                    self.count_black_tiles += 1
                elif str(tile) == WHITE_PIECE:
                    self.count_white_tiles += 1

    def __find_blank_tiles(self):
        for row in self.board_tiles:
            for tile in row:
                if str(tile) == BLANK_PIECE:
                    self.blank_pieces.append([tile.x, tile.y])

    def __check_if_has_moves(self, piece):
        self.__find_blank_tiles()
        temp = []
        for tile in self.blank_pieces:
            x, y = tile[0], tile[1]
            temp.append(self.verify_placement(Tile(position=[x, y], tile=piece)))
        return any(temp)

    def game_state(self, current_piece):
        self.__find_blank_tiles()
        self.__count_tiles()
        winner = None

        if self.count_blank_tiles == 0:
            if self.count_black_tiles > self.count_white_tiles:
                winner = BLACK_PIECE
            elif self.count_black_tiles < self.count_white_tiles:
                winner = WHITE_PIECE

            print("Winner: {}\n {} = {} : {} = {}".format(
                winner, BLACK_PIECE,
                str(self.count_black_tiles),
                WHITE_PIECE, str(self.count_white_tiles)
            ))
            self.reset_game()

        else:
            return self.__check_if_has_moves(current_piece)
        return self.__check_if_has_moves(current_piece)

    def add_tile(self, y, x, piece, flip=True):
        if str(self.board_tiles[x][y]) == BLANK_PIECE:
            tile = Tile(position=[x, y], tile=piece)
            while self.verify_placement(tile, flip=flip):
                self.board_tiles[x][y] = tile
            if self.board_tiles[x][y] == tile:
                return True
            else:
                return False
        else:
            return False

    def verify_placement(self, tile, flip=False):

        if self.__verify_upper_bounds(tile, flip=flip):
            return True

        elif self.__verify_upper_diagonal_bounds(tile, flip=flip):
            return True

        elif self.__verify_lower_bounds(tile, flip=flip):
            return True

        elif self.__verify_lower_diagonal_bounds(tile, flip=flip):
            return True

        elif self.__verify_left_bound(tile, flip=flip):
            return True

        elif self.__verify_right_bound(tile, flip=flip):
            return True

        return False

    def __verify_upper_bounds(self, tile, flip=False):
        if self.__upper_tile(tile.x, tile.y) is not None and self.__upper_tile(tile.x, tile.y).state not in [
            BLANK_PIECE, tile.state
        ]:
            return self.__scan_tiles(tile.x, tile.y, tile.state, self.__upper_tile, flip=flip)

        return False

    def __verify_lower_bounds(self, tile, flip=False):
        if self.__bottom_tile(tile.x, tile.y) is not None and self.__bottom_tile(tile.x, tile.y).state not in [
            BLANK_PIECE, tile.state
        ]:
            return self.__scan_tiles(tile.x, tile.y, tile.state, self.__bottom_tile, flip=flip)

        return False

    def __verify_left_bound(self, tile, flip=False):
        if self.__left_tile(tile.x, tile.y) is not None and self.__left_tile(tile.x, tile.y).state not in [
            BLANK_PIECE, tile.state
        ]:
            return self.__scan_tiles(tile.x, tile.y, tile.state, self.__left_tile, flip=flip)

        return False

    def __verify_right_bound(self, tile, flip=False):
        if self.__right_tile(tile.x, tile.y) is not None and self.__right_tile(tile.x, tile.y).state not in [
            BLANK_PIECE, tile.state
        ]:
            return self.__scan_tiles(tile.x, tile.y, tile.state, self.__right_tile, flip=flip)

        return False

    def __verify_upper_diagonal_bounds(self, tile, flip=False):
        if self.__upper_left_tile(tile.x, tile.y) is not None and self.__upper_left_tile(tile.x, tile.y).state not in [
            BLANK_PIECE, tile.state
        ]:
            return self.__scan_tiles(tile.x, tile.y, tile.state, self.__upper_left_tile, flip=flip)

        if self.__upper_right_tile(tile.x, tile.y) is not None and self.__upper_right_tile(tile.x, tile.y).state not in [
            BLANK_PIECE, tile.state
        ]:
            return self.__scan_tiles(tile.x, tile.y, tile.state, self.__upper_right_tile, flip=flip)

        return False

    def __verify_lower_diagonal_bounds(self, tile, flip=False):
        if self.__bottom_left_tile(tile.x, tile.y) is not None and self.__bottom_left_tile(tile.x, tile.y).state not in [
            BLANK_PIECE, tile.state
        ]:
            return self.__scan_tiles(tile.x, tile.y, tile.state, self.__bottom_left_tile, flip=flip)

        if self.__bottom_right_tile(tile.x, tile.y) is not None and self.__bottom_right_tile(tile.x, tile.y).state not in [
            BLANK_PIECE, tile.state
        ]:
            return self.__scan_tiles(tile.x, tile.y, tile.state, self.__bottom_right_tile, flip=flip)

        return False

    def __scan_tiles(self, x: int, y: int, piece: str, direction, flip: bool = False):
        tile = direction(x, y)
        tile_list = [Tile(position=[x, y], tile=piece)]
        while tile is not None:
            if tile.state == BLANK_PIECE:
                break
            elif tile.state == piece:
                tile_list.append(tile)
                break
            else:
                tile_list.append(tile)
                tile = direction(tile.x, tile.y)
        if len(tile_list) >= 3:
            if tile_list[0].state == piece and tile_list[len(tile_list) - 1].state == piece:
                for t in tile_list:
                    if self.opposite(t.state) == piece:
                        if flip:
                            t.flip()
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def opposite(piece):
        return BLACK_PIECE if piece == WHITE_PIECE else WHITE_PIECE

    def __right_tile(self, x, y):
        if not y + 1 > self.MAX_Y - 1:
            return self.board_tiles[x][y + 1]
        return None

    def __left_tile(self, x, y):
        if not y - 1 < 0:
            return self.board_tiles[x][y - 1]
        return None

    def __bottom_tile(self, x, y):
        if not x + 1 > self.MAX_X - 1:
            return self.board_tiles[x + 1][y]
        return None

    def __upper_tile(self, x, y):
        if not x - 1 < 0:
            return self.board_tiles[x - 1][y]
        return None

    def __upper_left_tile(self, x, y):
        if not x - 1 < 0 and not y - 1 < 0:
            return self.board_tiles[x - 1][y - 1]
        return None

    def __upper_right_tile(self, x, y):
        if not x - 1 < 0 and not y + 1 > self.MAX_Y - 1:
            return self.board_tiles[x - 1][y + 1]
        return None

    def __bottom_left_tile(self, x, y):
        if not x + 1 > self.MAX_X - 1 and not y - 1 < 0:
            return self.board_tiles[x + 1][y - 1]
        return None

    def __bottom_right_tile(self, x, y):
        if not x + 1 > self.MAX_X - 1 and not y + 1 > self.MAX_Y - 1:
            return self.board_tiles[x + 1][y + 1]
        return None

    def __str__(self):
        white_space = ' ' * 3
        board = '    ' + white_space.join([str(x) for x in range(self.MAX_X)]) + '\n'
        board += '  ' + GRID * len(self.board_tiles[0]) + INTERSECTION + '\n'
        for i, row in enumerate(self.board_tiles):
            board += str(i) + ' |'
            for tile in row:
                board += ' ' * PADDING + "{0!s:2}|".format(tile)
            board += '\n' + '  ' + GRID * len(row) + INTERSECTION + '\n'
        return board

    def __repr__(self):
        return str(self.board_tiles)


class Tile(GameBoard):
    def __init__(self, position: list = None, tile: chr = BLANK_PIECE):
        super(Tile, self).__init__()
        self.position = position
        self.state = tile
        self.x = position[0]
        self.y = position[1]

    def flip(self):
        self.state = BLACK_PIECE if self.state == WHITE_PIECE else WHITE_PIECE
        return self.state

    def __str__(self):
        return self.state

    def __repr__(self):
        return self.state
