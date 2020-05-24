from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant


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
            row = index.row()
            column = index.column()
            return str(self._board[row][column])

        return QVariant()
