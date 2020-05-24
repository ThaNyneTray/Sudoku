import sys
from PyQt5.QtWidgets import QApplication
from src.Sudoku.view.sudoku_view import SudokuMainWindow
from src.Sudoku.model.sudoku_model import SudokuModel
from src.Sudoku.model.sudoku_core import Sudoku


def main():
    app = QApplication(sys.argv)
    sudoku = Sudoku()
    board = sudoku.generate_puzzle()
    sudoku_model = SudokuModel(board)
    sudoku_main = SudokuMainWindow(sudoku_model)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()