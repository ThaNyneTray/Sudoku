import sys
from PyQt5.QtWidgets import QApplication
from src.Sudoku.view.sudoku_view import SudokuMainWindow
from src.Sudoku.model.sudoku_model import SudokuModel
from src.Sudoku.model.sudoku_core import Sudoku


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


def main():
    app = QApplication(sys.argv)
    sudoku = Sudoku()
    sudoku_model = SudokuModel(sudoku)
    sudoku_main = SudokuMainWindow(sudoku_model)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
