#Test Python

import math
import random

COLLUMN_SIZE = 7
ROW_SIZE = 6

EMPTY = 0
PLAYER = 1
AI = 2

def check_valid_move(b:list, m):
    if(b[0][m-1] == EMPTY):
        return True
    return False

def get_available_moves(b:list):
    a_moves = []
    for c in range(1, COLLUMN_SIZE+1, 1):
        if check_valid_move(b, c):
            a_moves.append(c)
    return a_moves

def get_open_row(b:list, c):
    for r in range(ROW_SIZE-1, -1, -1):
        if b[r][c-1] == EMPTY:
            return r
    return -1

def playerInput():
    move = input("Enter a move 1-7: ")
    a_moves = get_available_moves
    while(not(int(move) in available_moves)):
        move = input("Invalid move, try again: ")
    return move

def createBoard():
    board = []
    for y in range(ROW_SIZE):
        row = []
        for x in range(COLLUMN_SIZE):
            row.append(EMPTY)
        board.append(row)
    return board

def printBoard(board):
    for r in range(ROW_SIZE):
        for c in range(COLLUMN_SIZE):
            print(board[r][c], end = " ")
        print()
    print()

def copyBoard(b1:list):
    b2 = []
    for r in b1:
        row = []
        for c in r:
            row.append(c)
        b2.append(row)
    return b2

#check for win, returns owner ID if winner, otherwise returns 0
def check_Win_Loss(b:list):
    #check for horizontal win
    for c in range(COLLUMN_SIZE-3):
        for r in range(ROW_SIZE):
            owner = b[r][c] 
            if(owner != EMPTY):
                if(b[r][c] == owner and b[r][c+1] == owner and b[r][c+2] == owner and b[r][c+3] == owner):
                    return owner
    #check for vertical win
    for c in range(COLLUMN_SIZE):
        for r in range(ROW_SIZE-3):
            owner = b[r][c]
            if(owner != EMPTY):
                if(b[r][c] == owner and b[r+1][c] == owner and b[r+2][c] == owner and b[r+3][c] == owner):
                    return owner
    #check positive slope for win
    for c in range(COLLUMN_SIZE-3):
        for r in range(ROW_SIZE-3):
            owner = b[r][c]
            if(owner != EMPTY):
                if(b[r][c] == owner and b[r+1][c+1] == owner and b[r+2][c+2] == owner and b[r+3][c+3] == owner):
                    return owner
    #check negative slope for win
    for c in range(COLLUMN_SIZE-3):
        for r in range(ROW_SIZE):
            owner = b[r][c]
            if(owner != EMPTY):
                if(b[r][c] == owner and b[r-1][c+1] == owner and b[r-2][c+2] == owner and b[r-3][c+3] == owner):
                    return owner
    #No win
    return EMPTY

def applyMove(b:list, r, c, o):
    new_b = copyBoard(b)
    new_b[r][c-1] = o
    return new_b



count = 0
state = 0
inp = input("""Enter '1' to start first or '2' for AI start first: """)
turn = int(inp)
board = createBoard()
printBoard(board)
count = turn

while True:
    available_moves = get_available_moves(board)
    if(len(available_moves) != 0):
        if(turn == AI): #AI turn
            move = random.choice(available_moves)
            print("AI's move: ", move)
        else: #Player turn
            move = playerInput()
            while(not(int(move) in available_moves)):
                print("Invalid move, Try again.")
                move = playerInput()
        row = get_open_row(board, int(move))
        board = applyMove(board, row, int(move), turn)
        state = check_Win_Loss(board)    
        printBoard(board)
        if (state == PLAYER):
            print("Player wins!")
            break #games over
        elif(state == AI):
            print("AI wins!")
            break
    else:
        print("Game is a draw!")
        break
    turn =(count%2)+1 #switches between players
    count += 1

