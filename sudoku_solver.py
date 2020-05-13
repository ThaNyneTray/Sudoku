import pprint
import copy
import json

from pip._vendor import requests


def get_limits(row, col):
    BOX_SIZE = 3

    srow = row // BOX_SIZE * BOX_SIZE
    scol = col // BOX_SIZE * BOX_SIZE
    erow = srow + 2
    ecol = scol + 2

    return srow, scol, erow, ecol


def is_valid(board, row, col, num):
    for i in range(9):
        if board[i][col] == num:
            return False

    for j in range(9):
        if board[row][j] == num:
            return False

    srow, scol, erow, ecol = get_limits(row, col)
    for i in range(srow, erow):
        for j in range(scol, ecol):
            if board[i][j] == num:
                return False

    return True


# def find_next_idx(board, srow, scol):
#
#     for row in (srow, 9):
#         for col in ()


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
        if is_valid(board, row, col, num):
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
    print("\n", solved, "\n")
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
    assert (is_valid(board, 0, 2, 3) is True)
    assert (is_valid(board, 0, 2, 2) is False)
    assert (is_valid(board, 1, 1, 2) is False)
    assert (is_valid(board, 1, 1, 1) is True)
    print("All tests passed!")


def test_get_limits():
    print("testing...\n")

    assert(get_limits(0, 0) == (0, 0, 2, 2))
    assert(get_limits(3, 0) == (3, 0, 5, 2))
    assert(get_limits(3, 5) == (3, 3, 5, 5))
    assert(get_limits(4, 7) == (3, 6, 5, 8))

    print("All tests passed!")


# test_find_next_empty()
# test_is_valid()
# test_get_limits()
main()
# get_new_puzzle("easy")
