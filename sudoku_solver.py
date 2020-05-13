import pprint
import copy
import json
from pip._vendor import requests
import os
import csv

def get_limits(row, col):
    BOX_SIZE = 3

    srow = row // BOX_SIZE * BOX_SIZE
    scol = col // BOX_SIZE * BOX_SIZE
    erow = srow + 2
    ecol = scol + 2

    return srow, scol, erow, ecol


def is_valid_spot(board, row, col, num):

    for i in range(9):
        if board[i][col] == num:
            return False

    for j in range(9):
        # print(row, j)
        if board[row][j] == num:
            return False

    srow, scol, erow, ecol = get_limits(row, col)
    for i in range(srow, erow):
        for j in range(scol, ecol):
            if board[i][j] == num:
                return False

    return True


def find_next_empty(board):
    for row in range(0, 9):
        for col in range(0, 9):
            if board[row][col] == 0:
                return row, col

    return 8, 8


def solve(board):

    row, col = find_next_empty(board)
    if row == col == 8:
        return True

    for num in range(1, 10):
        if is_valid_spot(board, row, col, num):
            board[row][col] = num
            solved = solve(board)
            if solved:
                return True
            else:
                board[row][col] = 0

    return False


def get_new_puzzle(level):
    response = requests.get("https://sugoku.herokuapp.com/board?difficulty={}".format(level))
    print(response.text)
    response_dict = json.loads(response.text)
    return response_dict['board']


def is_valid_sudoku(board):
    return rows_valid(board) and cols_valid(board) and boxes_valid(board)


def line_valid(line):
    line = [x for x in line if x != 0]
    print("this is the damn line", line)
    if len(line) != len(set(line)):
        return False
    return True


def rows_valid(board):
    for row in board:
        if line_valid(row) is False:
            return False

    return True


def cols_valid(board):
    return rows_valid(zip(*board))


def boxes_valid(board):
    for i in range(3):
        for j in range(3):
            s_row, s_col = i * 3, j * 3
            e_row, e_col = s_row + 2,  s_col + 2
            box = []
            for row in range(s_row, e_row + 1):
                for col in range(s_col, e_col + 1):
                    box.append(board[row][col])
            print("box is ", box)
            if line_valid(box) is False:
                return False

    return True


def test_validator():
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    assert(rows_valid(board) is True)
    assert(cols_valid(board) is True)
    assert(boxes_valid(board) is True)

    board[0][2] = 7

    assert (rows_valid(board) is False)
    assert (cols_valid(board) is False)
    assert (boxes_valid(board) is False)


test_validator()


def main():
    board = get_new_puzzle("hard")

    # board = [
    #     [7, 8, 0, 4, 0, 0, 1, 2, 0],
    #     [6, 0, 0, 0, 7, 5, 0, 0, 9],
    #     [0, 0, 0, 6, 0, 1, 0, 7, 8],
    #     [0, 0, 7, 0, 4, 0, 2, 6, 0],
    #     [0, 0, 1, 0, 5, 0, 9, 3, 0],
    #     [9, 0, 4, 0, 6, 0, 0, 0, 5],
    #     [0, 7, 0, 3, 0, 0, 0, 1, 2],
    #     [1, 2, 0, 0, 0, 7, 4, 0, 0],
    #     [0, 4, 9, 2, 0, 6, 0, 0, 7]
    # ]

    original = copy.deepcopy(board)
    pprint.pprint(board)
    solved = solve(board)
    print("\ncheck valid")
    pprint.pprint(is_valid_sudoku(board))
    # print("\n", solved, "\n")
    pprint.pprint(board)
    print("\n", original == board)


def test_find_next_empty():
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    assert(find_next_empty(board) == (0, 2))

    board[0][2] = 4
    assert(find_next_empty(board) == (0, 4))

    board[0] = [7, 8, 2, 4, 6, 9, 1, 3, 5]
    assert(find_next_empty(board) == (1, 1))


def test_is_valid():
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    print("testing...\n")
    assert (is_valid_spot(board, 0, 2, 3) is True)
    assert (is_valid_spot(board, 0, 2, 2) is False)
    assert (is_valid_spot(board, 1, 1, 2) is False)
    assert (is_valid_spot(board, 1, 1, 1) is True)
    print("All tests passed!")


def test_get_limits():
    print("testing...\n")

    assert(get_limits(0, 0) == (0, 0, 2, 2))
    assert(get_limits(3, 0) == (3, 0, 5, 2))
    assert(get_limits(3, 5) == (3, 3, 5, 5))
    assert(get_limits(4, 7) == (3, 6, 5, 8))

    print("All tests passed!")


def read_sudoku_tests():
    fname = os.getcwd() + "\\data\\sudoku.csv"
    boards = []
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            boards.append(row)
            line_count += 1

            if line_count == 21:
                break
    # pprint.pprint(boards)
    return boards


def format_board(board):
    result = []
    for i in range(9):
        start_i = i * 9
        row = [int(x) for x in board[start_i:start_i+9]]
        result.append(row)
    # sanity checks
    return result


def test_solver():
    boards = read_sudoku_tests()

    # pprint.pprint(boards)
    # print(len(boards[0][0]))
    for i in range(len(boards)):
        boards[i][0] = format_board(boards[i][0])
        boards[i][1] = format_board(boards[i][1])
        # # sanity checks
        # print(i, "\n")
        # print(boards[i][0][0])
        # print(len(boards[i][0]))
        # for row in boards[i][0]:
        #     print(len(row))

        # return

    # pprint.pprint(boards[0])

    counter = 0
    for board in boards[:1]:
        print("solving puzzle {} \n".format(counter))
        solved = solve(board[0])
        pprint.pprint(board[0])
        pprint.pprint(board[1])
        assert (is_valid_sudoku(board[0]) is True)
        assert (is_valid_sudoku(board[1]) is True)
        # assert (board[0] == board[1])


# test_find_next_empty()
# test_is_valid()
# test_get_limits()
# main()
# get_new_puzzle("easy")
test_solver()
