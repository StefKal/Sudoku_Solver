from copy import deepcopy
from time import time




# check possible numbers for a tile based on
# elimination on rows, columns and box
def check_possible_numbers(board, row_num, col_num):
    possible_numbers = [1,2,3,4,5,6,7,8,9]
    current_row = board[row_num]
    current_col = [current_row[col_num] for current_row in board]

    for number in current_row:
        if number != 0:
            try:
                possible_numbers.remove(number)
            except ValueError:
                pass
    for number in current_col:
        if number != 0:
            try:
                possible_numbers.remove(number)
            except ValueError:
                pass
    # Calculate what box the number is in based on row and col number
    box_row = row_num // 3  # --> 0, 1, 2
    box_col = col_num // 3  # --> 0, 1, 2

    start_row_index = box_row * 3  # --> 0, 3, 6
    start_col_index = box_col * 3  # --> 0, 3, 6
    for box_x in range(start_row_index, start_row_index + 3):
        for box_y in range(start_col_index, start_col_index + 3):
            if board[box_x][box_y] != 0:
                try:
                    possible_numbers.remove(board[box_x][box_y])
                except ValueError:
                    pass
    return possible_numbers

# checks if there are any empty tiles in puzzle
def count_till_solve(board):
    count = 0
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                count += 1
    return count

# Can solve a simple sudoku as long as there tiles with only 1 option
def solve(board):
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == 0:
                possible_nums = check_possible_numbers(board, x, y)

                if len(possible_nums) == 1:
                    board[x][y] = possible_nums[0]

    if count_till_solve(board) > 0:
        print("Simple solver could not solve sudoku")
    display(board)
# finds all the tiles that are empty and returns
# a dictionary with {coordinate_tuple : possible value}
#UNFIXED_SPOT_DICT = {}
def find_unfixed(board):
    unfixed_spot_dict = {}
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == 0:
                possible_nums = check_possible_numbers(board, x, y)
                unfixed_spot_dict[(x,y)] = possible_nums
    return unfixed_spot_dict

# finds the list with least elements in our dictionary
def find_min(dict_of_lists):
    minimum = len(dict_of_lists[next(iter(dict_of_lists))])
    least_key = next(iter(dict_of_lists))
    for key, val in dict_of_lists.items():
        if len(val) < minimum:
            minimum = len(val)
            least_key = key

    return least_key

# backtracking algorithm
def solve_backtrack(board):
    if count_till_solve(board) == 0:
        display(board)
        return
    unfixed_spot_dict = find_unfixed(board)
    minimum_key = find_min(unfixed_spot_dict)

    if len(unfixed_spot_dict[minimum_key]) == 0:
        return
    for number in unfixed_spot_dict[minimum_key]:
        x,y = minimum_key
        copyBoard = deepcopy(board)
        copyBoard[x][y] = number
        solve_backtrack(copyBoard)


def display(board):
    for x in range(len(board)):
        for y in range(len(board)):
            print(board[x][y], end=' ')
        print()
    print('\n')


if __name__ == '__main__':
    BOARD_LEVEL_EXPERT = [  # ZERO represents empty tile
        [0, 0, 6, 0, 0, 0, 0, 0, 0],
        [9, 0, 0, 2, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 4, 0, 3, 7],
        [0, 0, 5, 0, 4, 0, 0, 0, 3],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 7, 6],
        [4, 5, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 6, 8, 0, 0, 0],
        [0, 0, 9, 5, 0, 0, 0, 2, 4]
    ]


    BOARD_LEVEL_EASY = [  # ZERO represents empty tile
        [0,0,6,0,0,5,7,4,2],
        [0,0,8,3,2,4,0,9,1],
        [2,0,0,0,0,0,0,0,0],
        [0,7,0,0,0,9,0,0,5],
        [0,0,9,0,3,0,2,7,0],
        [0,0,1,0,7,0,8,3,0],
        [6,9,7,0,4,0,3,0,8],
        [0,0,0,9,0,0,0,0,0],
        [0,4,0,0,5,0,9,1,6]
    ]
  
    start = time()
    solve_backtrack(BOARD_LEVEL_EASY)
    seconds = time() - start
    print("Backtracking solved easy level after", seconds, "seconds")

    start = time()
    solve_backtrack(BOARD_LEVEL_EXPERT)
    seconds = time() - start
    print("Backtracking solved expert level after", seconds, "seconds")

    start = time()
    solve(BOARD_LEVEL_EASY)
    seconds = time() - start
    print("Simple solver solved easy after", seconds, "seconds")

    start = time()
    solve(BOARD_LEVEL_EXPERT)
    seconds = time() - start
    print("After", seconds, "seconds:")