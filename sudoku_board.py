import sys
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QMainWindow


class SudokuModel(QAbstractTableModel):

    def __init__(self, board):
        super().__init__()
        self._board = board

    # returns number of rows - must be reimplemented
    def rowCount(self, parent=QModelIndex()):
        return len(self._board)

    # returns number of columns - must be reimplemented
    def columnCount(self, parent=QModelIndex()):
        return len(self._board[0])

    # returns data at given index, in given role - must be reimplemented
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._board[index.row()][index.column()])
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return QVariant()

    # allows cells to be editable - must be reimplemented for edit functionality
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            if not self.check_index(index):
                return False
        self._board[index.row()][index.column()] = int(value)
        return False

    def check_index(self, index):
        row, col = index.row(), index.column()
        return self._board[row][col] == 0

    # set flags to allow editable - must be reimplemented for edit functionality
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled


class SudokuMainWindow(QMainWindow):

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

        self.view = QTableView()
        self.model = SudokuModel(board)

        self.view.setModel(self.model)
        self.view.verticalHeader().hide()
        self.view.horizontalHeader().hide()
        self.view.setFont(QFont("Sanserif", 20))

        for col in range(9):
            self.view.setColumnWidth(col, 90)

        for row in range(9):
            self.view.setRowHeight(row, 90)


        self.setCentralWidget(self.view)
        self.setGeometry(100, 100, 900, 900)
        self.setWindowTitle("Sudoku")
        self.show()


def main():
    app = QApplication(sys.argv)
    view = SudokuMainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
