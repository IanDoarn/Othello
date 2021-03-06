from gameboard import GameBoard, BLACK_PIECE, WHITE_PIECE
from os import system
from colorama import init, Fore


if __name__ == '__main__':
    game = GameBoard()
    game.setup()

    init(autoreset=True)

    print(Fore.LIGHTWHITE_EX + str(game))

    current_piece = BLACK_PIECE

    while game.is_setup:
        print(Fore.LIGHTGREEN_EX + "Black({}) : {}\tWhite({}) : {}".format(
            BLACK_PIECE,
            str(game.count_black_tiles),
            WHITE_PIECE,
            str(game.count_white_tiles)
        ))
        coordinates = input("Enter coordinates for {} piece: ".format(current_piece))
        coord = coordinates.split(' ')
        x, y = int(coord[0]), int(coord[1])
        if game.add_tile(x, y, current_piece):
            system('cls')
            print(Fore.LIGHTWHITE_EX + str(game))
            current_piece = game.opposite(current_piece)
            if game.game_state(current_piece):
                continue
            else:
                if game.is_setup:
                    print("{} Has no possible moves!".format(current_piece))
                current_piece = game.opposite(current_piece)
        else:
            print("Invalid move: x:{} y:{}".format(str(x), str(y)))
