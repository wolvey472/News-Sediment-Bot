import pygame 
import PySimpleGUI as sg
import random as rd

board = [0, 0, 0,
         0, 0, 0,
         0, 0, 0]

#----------------
# 0 - top left
# 1 - topm iddle
# 2 - top right
# 3 middle left
# 4 middle middle
# 5 middle righht
# 6 bottom left
# 7 bottom middle
# 8 bottom right
#----------------

# 0 | 1 | 2
# 3 | 4 | 5
# 6 | 7 | 8

# 0 = empty
# 1 = player
# -1 = opponent

player_win_status = 0
opponent_win_status = 0

top_row = (board[0:3:1])
middle_row = (board[3:6:1])
bottom_row = (board[6:9:1])

left_colum = board[0:7:3]
middle_colum = board[1:8:3]
right_colum = board[2:9:3]
print(top_row)
print(middle_row)
print(bottom_row)

def print_board(board):
    print(board[0:3])
    print(board[3:6])
    print(board[6:9])
    print()

def get_lines(board):
        
        return [
        board[0:3],      # top row
        board[3:6],      # middle row
        board[6:9],      # bottom row

        board[0:7:3],    # left column
        board[1:8:3],    # middle column
        board[2:9:3],    # right column

        board[0:9:4],    # diagonal top-left to bottom-right
        board[2:7:2]     # diagonal top-right to bottom-left
    ]

def winner(board): 
    #run every move to check if return none noone won
    for line in get_lines(board):
        if line == [1,1,1]:
            return 1 #player win
        if line == [-1,-1,-1]:
            return -1 #opponent win
        
def random_move(board):
    empty_spots = []

    for i in range(9):
        if board[i] == 0:
            empty_spots.append(i)
            # for the index that is 0 its valid
        
        if len(empty_spots) == 0:
            print("tie game")
            return
        


        move = rd.randint(0, 8)
    
        board[move] = -1 

        print("opponent moved", move)
        print_board(board=board)

        win = winner(board=board)

        if win == 1:
            print("player wins")
            return
        elif win == -1:
            print("opponent won")
            return
        else:
            player_move(board=board)





def player_move(board):
    valid_move = False
    while valid_move is False:
        move = int(input("Player move: "))

        if move < 0 or move > 8:
            print("move from 0 - 8")
            continue

        if board[move] == 0:
            valid_move = True
            board[move] = 1

            print("player moved:", move)
            print_board(board=board)

            win = winner(board=board)

            if win == 1:
                print("player wins")
                return
            elif win == -1:
                print("opponent won")
                return
            else:
                random_move(board=board)
        else:
            print("spot already taken")





print_board(board)
random_move(board)