from gameboard import GameBoard, BLACK_PIECE
from os import system
from colorama import init, Fore

if __name__ == '__main__':
    game = GameBoard()
    game.setup()

    init(autoreset=True)

    print(Fore.LIGHTCYAN_EX + str(game))

    current_piece = BLACK_PIECE

    while game.is_setup:
        print(Fore.LIGHTGREEN_EX + "Black : {}\tWhite : {}".format(
            str(game.count_black_tiles),
            str(game.count_white_tiles)
        ))
        coordinates = input("Enter coordinates for {} piece: ".format(current_piece))
        coord = coordinates.split(' ')
        x, y = int(coord[0]), int(coord[1])
        if game.add_tile(x, y, current_piece):
            system('cls')
            print(Fore.LIGHTCYAN_EX + str(game))
            game.game_state()
            current_piece = game.opposite(current_piece)
        else:
            print("Invalid move: x:{} y:{}".format(str(x), str(y)))
