from copy import deepcopy
from random import shuffle

from solving.utils.framework import Puzzle

SIZE = 9
BOX_SIZE = 3

numberCheck = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0 , 7:0, 8:0, 9:0}


BOARD = [ # ZERO represents empty tile
    [5,0,0,0,1,0,0,0,4],
    [2,7,4,0,0,0,6,0,0],
    [0,8,0,9,0,4,0,0,0],
    [8,1,0,4,6,0,3,0,2],
    [0,0,2,0,3,0,1,0,0],
    [7,0,6,0,9,1,0,5,8],
    [0,0,0,5,0,3,0,1,0],
    [0,0,5,0,0,0,9,2,7],
    [1,0,0,0,2,0,0,0,3]
]

# FILLS A BOX OF TILES WITH NUMBERS FROM 1-9
def fill_box(board, start_x, start_y):
    numbers_to_append = [1,2,3,4,5,6,7,8,9]
    shuffle(numbers_to_append)

    # check if there is any numbers in the block
    # if so, we remove it from numbers we want to append


    for x in range(start_x, start_x + 3):
        for y in range(start_y, start_y + 3):
            tile = board[x][y]
            if tile != 0:
                numbers_to_append.remove(tile)


    for x in range(start_x, start_x + 3):
        for y in range(start_y, start_y + 3):
            tile = board[x][y]
            if tile == 0:
                board[x][y] = numbers_to_append.pop(0)
            else:
                continue


# FILLS ALL BOXES OF TILES WITH NUMBERS FROM 1-9
def fill_all_boxes(board):
    for start_x in range(0, 7, 3):
        for start_y in range(0, 7, 3):
            fill_box(board, start_x, start_y)


# POPULATE INITIAL TILES LIST
def make_fixed():
    for startX in range(SIZE):
        for startY in range(SIZE):
            if BOARD[startX][startY] != 0:
                initial_tile = startX, startY
                initial_tiles.append(initial_tile)

# CREATE AN INITIAL TILES LIST TO SAVE STARTING POSITIONS
initial_tiles = list()
make_fixed()
fill_all_boxes(BOARD)


# Superclass for puzzles
class Sudoku(Puzzle):

    def __init__(self, board = BOARD):
        self.board = board

    # Return whether this puzzle is equivalent to the other
    def __eq__(self, other):
        return self.board == other.board

    # Return a hash code for this puzzle
    def __hash__(self):
        return hash(str(self.board))

    # Return whether this puzzle comes before the other in a sort
    def __lt__(self, other):
        return self.board < other.board

    # Return whether this puzzle is solved
    def solved(self):
        return self.heuristic() == 0

    # Return an estimate of how far this puzzle is from being solved
    def heuristic(self):
        return check_rows(self.board) + check_columns(self.board) + check_all_boxes(self.board)



    # Return a list of legal moves
    def moves(self):
        total_moves_lists = list()
        moves = list()

        for start_x in range(0, 7, 3):
            for start_y in range(0, 7, 3):
                total_moves_lists.append(check_moves(start_x, start_y))


        for a_list in total_moves_lists:
            for move in a_list:
                moves.append(move)

        return moves

    # Return a new puzzle created by a move
    def neighbor(self, move):

        copyBoard = deepcopy(self.board)
        tile_1 , tile_2 = move

        row_1, col_1 = tile_1
        row_2, col_2 = tile_2

        copyBoard[row_1][col_1], copyBoard[row_2][col_2] = copyBoard[row_2][col_2], copyBoard[row_1][col_1]

        return Sudoku(copyBoard)


    # Print this puzzle to the console
    def display(self):
        for row in range(SIZE):
            for col in range(SIZE):
                print(self.board[row][col], end=' ')
            print()
        print()





#  H E L P E R    F U N C T I O N S

# CHECKING POSSIBLE MOVES FOR EVERY ONE BOX

def check_moves(start_x, start_y):
    moves = list()

    for r1 in range(start_x, start_x + 3):
        for c1 in range(start_y, start_y + 3):
            for r2 in range(start_x, start_x + 3):
                for c2 in range(start_y, start_y + 3):
                    tile_1 = r1, c1
                    tile_2 = r2, c2

                    if (r1, c1) not in initial_tiles and (r2, c2) not in initial_tiles:
                        moves.append((tile_1, tile_2))

    return moves

# CHECKING UNIQUE NUMBERS IN EACH ROW
def check_rows(board):

    conflicts = 0
    for row in range(SIZE):
        # reset tempNumberCheck to zeroes
        tempNumberCheck = deepcopy(numberCheck)

        for index in range(SIZE):

            # increase the count of specific number
            tile = board[row][index]
            tempNumberCheck[tile] += 1

            if tempNumberCheck[tile] >= 2:
                conflicts += 1

    return conflicts


# CHECKING UNIQUE NUMBERS IN EACH COLUMN
def check_columns(board):
    conflicts = 0
    columnCount = 0
    columns_list = list()

    while columnCount < SIZE:
        column = list()
        for row in range(SIZE):
            column.append(board[row][columnCount])

            # reset tempNumberCheck to zeroes
            tempNumberCheck = deepcopy(numberCheck)

            for number in column:
                tempNumberCheck[number] += 1

                if tempNumberCheck[number] >= 2:
                    conflicts += 1

        columns_list.append(column)
        columnCount += 1

    return conflicts


# CHECKING ALL BOXES AND COUNTING CONFLICTS
def check_all_boxes(board):

    total_conflicts = 0

    for start_x in range(0,7, 3):
        for start_y in range(0,7,3):
            total_conflicts += check_box(board, start_x, start_y)


    return total_conflicts

# CHECKING UNIQUE NUMBERS IN EACH BOX
def check_box(board, start_x, start_y):

    block = list()
    conflicts = 0
    for x in range(start_x, start_x + 3):
        for y in range(start_y, start_y + 3):

            block.append(board[x][y])

            tempNumberCheck = deepcopy(numberCheck)

            for number in block:
                tempNumberCheck[number] += 1

                if tempNumberCheck[number] >= 2:
                    conflicts += 1

    return conflicts
