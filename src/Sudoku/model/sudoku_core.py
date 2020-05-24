import copy
import json
from pip._vendor import requests


class Sudoku:

    def __init__(self):
        self._original_board = None
        self._board = None
        self._level = "medium"
        self._solver = None

    def generate_puzzle(self):
        response = requests.get("https://sugoku.herokuapp.com/board", params={"difficulty": self._level})
        response_dict = json.loads(response.text)
        self._original_board = response_dict['board']
        self._board = copy.deepcopy(self._original_board)
        self._solver = SudokuSolver(self._board)
        return self._board

    # currently only checks if the row, col, and box placement is valid. No look ahead offered
    #   for when a valid placement will led to a non-solution down the line
    def add_value(self, pos, value, board):
        # board[pos[0]][pos[1]] = value
        solver = SudokuSolver(self._board)
        valid = solver.is_valid_spot(pos[0], pos[1], value)
        if valid:
            return True
        else:
            self._board[pos[0]][pos[1]] = 0
            return False


class SudokuSolver:

    def __init__(self, board):
        self._board = copy.deepcopy(board)
        self._solvable = True
        # self.solve()
        # self._row =

    # set of functions to solve the board.
    def solve(self):

        row, col = self.find_next_empty()
        if row == col == 8:
            return True

        for num in range(1, 10):
            if self.is_valid_spot(row, col, num):
                self._board[row][col] = num
                solved = self.solve()
                if solved:
                    self._solvable = True
                    return True
                else:
                    self._board[row][col] = 0

        self._solvable = False
        return False

    def find_next_empty(self):
        for row in range(0, 9):
            for col in range(0, 9):
                if self._board [row][col] == 0:
                    return row, col

        return 8, 8

    def is_valid_spot(self, row, col, num):

        for i in range(9):
            if self._board [i][col] == num:
                return False

        for j in range(9):
            # print(row, j)
            if self._board [row][j] == num:
                return False

        srow, scol, erow, ecol = self.get_limits(row, col)
        for i in range(srow, erow):
            for j in range(scol, ecol):
                if self._board [i][j] == num:
                    return False

        return True

    def get_limits(self, row, col):
        BOX_SIZE = 3

        srow = row // BOX_SIZE * BOX_SIZE
        scol = col // BOX_SIZE * BOX_SIZE
        erow = srow + 2
        ecol = scol + 2

        return srow, scol, erow, ecol

    # set of functions to check if the whole board setup is valid
    # do we even need this
    def is_valid_sudoku(self):
        return self.rows_valid() and self.cols_valid() and self.boxes_valid()

    def line_valid(self, line):
        line = [x for x in line if x != 0]
        print("this is the damn line", line)
        if len(line) != len(set(line)):
            return False
        return True

    def rows_valid(self, board_flipped):
        for row in board_flipped :
            if self.line_valid(row) is False:
                return False

        return True

    def cols_valid(self):
        return self.rows_valid(zip(*self._board ))

    def boxes_valid(self):
        for i in range(3):
            for j in range(3):
                s_row, s_col = i * 3, j * 3
                e_row, e_col = s_row + 2, s_col + 2
                box = []
                for row in range(s_row, e_row + 1):
                    for col in range(s_col, e_col + 1):
                        box.append(self._board [row][col])
                print("box is ", box)
                if self.line_valid(box) is False:
                    return False
        return True
