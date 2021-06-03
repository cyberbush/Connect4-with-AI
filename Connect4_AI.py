# This is a simple Connect 4 Program using an AI
# David Bush, CS 470 Soule, 6/1/2021

import math

COLLUMN_SIZE = 7
ROW_SIZE = 6
SECTION_SIZE = 4

MAXDEPTH = 5

EMPTY = 0
PLAYER = 1
AI = 2

WIN = 1000000000000
LOSS = -1000000000000
DRAW = 0

# class containing each square object for the connect4 board 
class square:
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner # who own's the square?


def playerInput():
    move = input("Enter a move 1-7: ")
    return move

def printBoard(b:list):
    for r in b:
        for c in r:
            print(c.owner, end = " ")
        print()
    print()

def copyBoard(b1:list):
    b2 = []
    for r in b1:
        row = []
        for c in r:
            x  = c.x
            y = c.y
            o = c.owner
            sq = square(x, y, o)
            row.append(sq)
        b2.append(row)
    return b2

def check_valid_move(b:list, m):
    if(b[0][m-1].owner == EMPTY):
        return True
    return False

def check_invalid_move(b:list, m):
    if(b[0][m-1].owner == EMPTY):
        return False
    return True

def get_available_moves(b:list):
    a_moves = []
    for c in range(1, COLLUMN_SIZE+1, 1):
        if check_valid_move(b, c):
            a_moves.append(c)
    return a_moves

def get_open_row(b:list, c):
    for r in range(ROW_SIZE-1, -1, -1):
        if b[r][c-1].owner == EMPTY:
            return r
    return -1

def applyMove(b:list, r, c, o):
    new_b = copyBoard(b)
    new_b[r][c-1].owner = o
    return new_b

#check for win, returns owner ID if winner, otherwise returns 0
def check_Win_Loss(b:list):
    #check for horizontal win
    for c in range(COLLUMN_SIZE-3):
        for r in range(ROW_SIZE):
            owner = b[r][c].owner
            if(owner != EMPTY):
                if(b[r][c].owner == owner and b[r][c+1].owner == owner and b[r][c+2].owner == owner and b[r][c+3].owner == owner):
                    return owner
    #check for vertical win
    for c in range(COLLUMN_SIZE):
        for r in range(ROW_SIZE-3):
            owner = int(b[r][c].owner)
            if(owner != EMPTY):
                if(b[r][c].owner == owner and b[r+1][c].owner == owner and b[r+2][c].owner == owner and b[r+3][c].owner == owner):
                    return owner
    #check positive slope for win
    for c in range(COLLUMN_SIZE-3):
        for r in range(ROW_SIZE-3):
            owner = int(b[r][c].owner)
            if(owner != EMPTY):
                if(b[r][c].owner == owner and b[r+1][c+1].owner == owner and b[r+2][c+2].owner == owner and b[r+3][c+3].owner == owner):
                    return owner
    #check negative slope for win
    for c in range(COLLUMN_SIZE-3):
        for r in range(ROW_SIZE):
            owner = int(b[r][c].owner)
            if(owner != EMPTY):
                if(b[r][c].owner == owner and b[r-1][c+1].owner == owner and b[r-2][c+2].owner == owner and b[r-3][c+3].owner == owner):
                    return owner
    #No win
    return EMPTY

def is_game_over(u):
    return (u == WIN or u == LOSS or u == DRAW)

def section_score(s:list, o):
    score = 0
    other = PLAYER
    if(o == PLAYER):
        other = AI
    
    if(s.count(o) == 4): 
        score += 500
    elif(s.count(o) == 3 and s.count(EMPTY) == 1):
        score += 25
    elif(s.count(o) == 2 and s.count(EMPTY) == 2):
        score += 10
    
    if(s.count(other) == 3 and s.count(EMPTY) == 1):
        score -= 4

    return score

def evaluate(b:list, o):
    score = 0
    x = check_Win_Loss(b)
    if(x == PLAYER): #Player win
        score = LOSS
        return score
    elif(x == AI): #AI win
        score = WIN
        return score
    elif(len(get_available_moves(b)) == 0): #draw
        score = DRAW
        return score

    else:
        # Score pieces in center
        center_sect = []
        for y in range(ROW_SIZE):
            center_sect.append(b[y][COLLUMN_SIZE//2].owner)
        c_count = center_sect.count(o)
        score += c_count * 10
	    
        # Score pieces in horizontal lines
        for y in range(ROW_SIZE):
            row_sect = []
            for x in range(COLLUMN_SIZE):
                row_sect.append(b[y][x].owner)
            for c in range(COLLUMN_SIZE-3):
                section = row_sect[c:c+SECTION_SIZE]
                score += section_score(section, o)

	    # Score pieces in vertical lines
        for x in range(COLLUMN_SIZE):
            col_sect = []
            for y in range(ROW_SIZE):
                col_sect.append(b[y][x].owner)
            for r in range(ROW_SIZE-3):
                section = col_sect[r:r+SECTION_SIZE]
                score += section_score(section, o)

	    # Score pieces in positive diagonal lines
        for r in range(ROW_SIZE-3):
            for c in range(COLLUMN_SIZE-3):
                section = [b[r+i][c+i].owner for i in range(SECTION_SIZE)]
                score += section_score(section, o)


	    # Score pieces in negative diagonal lines
        for r in range(ROW_SIZE-3):
            for c in range(COLLUMN_SIZE-3):
                section = [b[r+3-i][c+i].owner for i in range(SECTION_SIZE)]
                score += section_score(section, o)
    return score



def max_val(b:list, m, d, o):
    row = get_open_row(b, m)
    new_b = applyMove(b, row, m, o)
    u = evaluate(new_b, AI)
    if(is_game_over(u) or d == MAXDEPTH):
        return u
    u = -math.inf
    a_moves = get_available_moves(b)
    for new_m in a_moves:
        tmp = min_val(new_b, new_m, d+1, AI)
        if tmp > u:
            u = tmp
    return u

def min_val(b:list, m, d, o):
    row = get_open_row(b, m)
    new_b = applyMove(b, row, m, o)
    u = evaluate(new_b, AI)
    if(is_game_over(u) or d == MAXDEPTH):
        return u
    u = math.inf
    a_moves = get_available_moves(b)
    for new_m in a_moves:
        tmp = max_val(new_b, new_m, d+1, PLAYER)
        if tmp < u:
            u = tmp
    return u

def minmax(b:list):
    utility = -math.inf
    a_moves = get_available_moves(b)
    for m in a_moves:
        tmp = min_val(b, m, 0, AI)
        if tmp > utility:
            utility = tmp
            best_move = m
    return best_move

#set up
count = 0
board = []      #game board
state = 0
for y in range(ROW_SIZE):
    r = []
    for x in range(COLLUMN_SIZE):
        sq = square(x, y, EMPTY)
        r.append(sq)
    board.append(r)
#ask user who starts
inp = input("""Enter '1' to start first or '2' for AI start first: """)
turn = int(inp)
printBoard(board) # print start
count = turn

# game loop
while True:
    available_moves = get_available_moves(board)
    if(len(available_moves) != 0): # make sure theres still available moves left
        if(turn == AI): # AI's turn
            move = minmax(board)
            #move = randint(1,7)
            print("AI's move: ", move)
        else: # Player's turn
            move = playerInput()
            while(not(int(move) in available_moves)):
                print("Invalid move, Try again please.")
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
