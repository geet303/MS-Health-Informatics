'''
   CS 5001
   Spring 2020
   Project Connect_four
   Geetanjali Gupta
'''

from game import Game


def main():

    rows = int(input('Enter number of rows you want in your game: '))
    cols = int(input('Enter number of columns you want in your game: '))
    choice = input('Do you want to play against computer?(y/n): ')
    if (choice == 'y' or choice == 'Y'):
        play_AI = 1
    else:
        play_AI = 0

    # creating game object for class Game to play the main game in driver.
    game = Game(cols, rows, 500, 700, play_AI)
    game.play_game()


main()