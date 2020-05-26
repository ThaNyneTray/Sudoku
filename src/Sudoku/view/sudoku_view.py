from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QFont, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QTableView, QVBoxLayout, QHBoxLayout, QPushButton, QWidget


class SudokuMainWindow(QWidget):

    def __init__(self, model):
        super().__init__()

        self.model = model
        self.init_ui()

    def init_ui(self):

        # create table view
        self.sudoku_view = QTableView(self)
        self.sudoku_view.setModel(self.model)
        self.sudoku_view.verticalHeader().hide()
        self.sudoku_view.horizontalHeader().hide()
        self.sudoku_view.setFont(QFont("Times", 20))
        # self.sudoku_view.setFocusPolicy(Qt.NoFocus)

        # change palette - to change highlighting color
        palette = self.sudoku_view.palette()
        palette.setBrush(QPalette.Highlight, QBrush(Qt.lightGray))
        self.sudoku_view.setPalette(palette)

        # resize the
        for col in range(9):
            self.sudoku_view.setColumnWidth(col, 90)

        for row in range(9):
            self.sudoku_view.setRowHeight(row, 90)

        # create clear button
        clear_btn = QPushButton('Clear')
        clear_btn.setToolTip("clear the board and reset the puzzle")

        # create solve button
        solve_btn = QPushButton('Solve')
        solve_btn.setToolTip("solve the puzzle for me")

        # create how am I doing? button
        progress_btn = QPushButton('How Am I Doing')
        progress_btn.setToolTip("highlight mistakes")

        # create layout for buttons, and add them
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(progress_btn)
        self.hbox.addWidget(clear_btn)
        self.hbox.addWidget(solve_btn)
        self.hbox.addStretch(1)

        # create layout to hold sudoku view, and
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.sudoku_view)
        self.vbox.addLayout(self.hbox)

        # set the layout, and set the window title, size, and trigger show()
        self.setLayout(self.vbox)
        self.setFixedSize(860, 915)
        self.setWindowTitle("Sudoku")
        self.show()

    # def keyPressEvent(self, event):
    #     print(self.sudoku_view.selectedIndexes()[0].row())
    #     if event.key() == Qt.Key_Left or event.key() == Qt.Key_Right:
    #         print("here")
    #         QTableView.keyPressEvent(self.sudoku_view, event)
    #
    #         row = self.sudoku_view.selectedIndexes()[0].row()
    #         if row != 0:
    #             self.sudoku_view.selectRow(row-1)
    #
    #     elif event.key() == Qt.RightArrow:
    #         print("here")
    #         pass
