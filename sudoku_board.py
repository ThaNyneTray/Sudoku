import sys

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QTableView


class QString(object):
    pass


class SudokuModel(QAbstractTableModel):

    def __init__(self, board):
        super().__init__()
        self._board = board

    def rowCount(self, parent=QModelIndex()):
        return len(self._board)

    def columnCount(self, parent=QModelIndex()):
        return len(self._board[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._board[index.row()][index.column()])
        return QVariant()


class SudokuView(QTableView):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
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
        model = SudokuModel(board)
        self.setModel(model)
        self.setFont(QFont("Sanserif", 20))

        for col in range(9):
            self.setColumnWidth(col, 90)

        for row in range(9):
            self.setRowHeight(row, 90)

        self.setGeometry(100, 100, 900, 900)
        self.setWindowTitle("Sudoku")
        self.show()


def main():
    app = QApplication(sys.argv)
    view = SudokuView()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
