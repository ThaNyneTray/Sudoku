from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QColor, QFont, QBrush
from PyQt5.QtWidgets import QStyledItemDelegate


class SudokuItemDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        # print(Qt.UserRole, index.data())
        # print(option.displayAlignment)
        # if index.data() == Qt.UserRole:
        #     print("here")
        #     painter.setPen(QColor.red)
        #     painter.drawRect(option.rect)
        # else:
        #     super().paint(painter, option, index)
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        return super().sizeHint(option, index)


class SudokuModel(QAbstractTableModel):

    def __init__(self, sudoku):
        super().__init__()

        self._sudoku = sudoku
        self._board = self._sudoku.get_board()
        row_len, col_len = len(self._board), len(self._board[0])
        self._fixed = [(row, column)
                       for row in range(row_len)
                       for column in range(col_len)
                       if self._board[row][column] != 0]

    def rowCount(self, parent=QModelIndex()):
        return len(self._board)

    def columnCount(self, parent=QModelIndex()):
        return len(self._board[0])

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            if self._board[row][column] == 0:
                return ""
            return str(self._board[row][column])

        # handle other roles
        elif role == Qt.EditRole:
            return str(self._board[row][column])

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        elif role == Qt.TextColorRole:
            # we make it blue for cells that
            if (row, column) not in self._fixed:
                return QColor("blue")

        elif role == Qt.FontRole:
            return QFont("Times", 20)

        # allows cells to be editable - must be reimplemented for edit functionality

    def setData(self, index, value, role=Qt.EditRole):
        row, column = index.row(), index.column()
        # self._valid = self._sudoku.add_value((row, column), int(value), self._board)
        # valid = self._valid
        if role == Qt.EditRole:
            if (row, column) in self._fixed:
                return False
        self._board[row][column] = int(value)
        return True

    def flags(self, index):
        if (index.row(), index.column()) in self._fixed:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable


