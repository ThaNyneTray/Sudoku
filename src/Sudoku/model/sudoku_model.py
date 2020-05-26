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
        self.set_fixed_cells()

        # this will be used when showing the player where he has gone wrong.
        self._invalid = set()
        # this is a boolean highlighting how data() should color the background of the
        # cells
        self._highlight_invalid = False

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

        elif role == Qt.BackgroundRole:
            if self._highlight_invalid and (row, column) in self._invalid:
                return QBrush(QColor(255, 0, 0, 127))
            return QBrush(QColor(0, 0, 0, 0))

        # elif role == Qt.UserRole:

        # allows cells to be editable - must be reimplemented for edit functionality

    def setData(self, index, value, role=Qt.EditRole):
        row, column = index.row(), index.column()
        top_left = self.createIndex(0, 0)
        bottom_right = self.createIndex(len(self._board)-1, len(self._board[0])-1)

        if role == Qt.EditRole:
            self.check_placement(row, column, value)
            self._board[row][column] = int(value)

        # elif role == Qt.BackgroundRole:
        #     # self._highlight_invalid = True
        #     self.dataChanged.emit(top_left, bottom_right)

        elif role == Qt.UserRole:
            self._board = self._sudoku.get_original_board()

        elif role == Qt.UserRole + 1:
            solved_board = self._sudoku.solve()
            self._board = solved_board

        elif role == Qt.UserRole + 2:
            new_board = self._sudoku.generate_puzzle()
            self._board = new_board
            self.set_fixed_cells()

        self.dataChanged.emit(top_left, bottom_right)
        return True

    def flags(self, index):
        if (index.row(), index.column()) in self._fixed:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def set_fixed_cells(self):
        row_len, col_len = len(self._board), len(self._board[0])
        self._fixed = [(row, column)
                       for row in range(row_len)
                       for column in range(col_len)
                       if self._board[row][column] != 0]

    # function checks if a placement is valid
    def check_placement(self, row, column, value):
        is_valid = self._sudoku.add_value((row, column), int(value), self._board)

        if is_valid and (row, column) in self._invalid:
            self._invalid.remove((row, column))

        elif not is_valid:
            print("here")
            self._invalid.add((row, column))

    # this is a quick dirty fix to the problem of deciding when to highlight
    # TODO: fix this later
    def set_highlight_mistakes(self):
        self._highlight_invalid = not self._highlight_invalid
