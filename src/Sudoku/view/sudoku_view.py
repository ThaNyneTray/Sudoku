from PyQt5.QtCore import Qt, QModelIndex, QVariant
from PyQt5.QtGui import QFont, QPalette, QBrush, QColor
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
        self.clear_btn = QPushButton('Clear')
        self.clear_btn.setToolTip("clear the board and reset the puzzle")

        # create solve button
        self.solve_btn = QPushButton('Solve')
        self.solve_btn.setToolTip("solve the puzzle for me")

        # create how am I doing? button
        self.progress_btn = QPushButton('How Am I Doing')
        self.progress_btn.setToolTip("highlight mistakes")
        self.progress_highlight = False

        # create new board button
        self.get_new_board_btn = QPushButton('Get New Board')
        self.get_new_board_btn.setToolTip("gets you a new board")

        # create how am I doing? button
        # hide_progress_btn = QPushButton('Clear Highlights')
        # hide_progress_btn.setToolTip("clear highlighted mistakes")

        # connect buttons to slots
        self.clear_btn.clicked.connect(self.clear_board)
        self.solve_btn.clicked.connect(self.solve_board)
        self.progress_btn.clicked.connect(self.show_progress)
        self.get_new_board_btn.clicked.connect(self.get_new_board)

        # create layout for buttons, and add them
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.progress_btn)
        self.hbox.addWidget(self.clear_btn)
        self.hbox.addWidget(self.solve_btn)
        self.hbox.addWidget(self.get_new_board_btn)
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

    def show_progress(self):
        index = self.sudoku_view.currentIndex()
        if self.progress_highlight == True:
            self.progress_highlight = False
            self.progress_btn.setText("How Am I Doing")
            self.progress_btn.setToolTip("highlight mistakes")
        else:
            self.progress_highlight = True
            self.progress_btn.setText("Hide Highlights")
            self.progress_btn.setToolTip("hide highlighted mistakes")
        self.model.set_highlight_mistakes()
        self.model.setData(index, value=QVariant(), role=Qt.BackgroundRole)
        self.update()

    def clear_board(self):
        index = self.sudoku_view.currentIndex()
        self.model.setData(index, value=QVariant, role=Qt.UserRole)

    def solve_board(self):
        index = self.sudoku_view.currentIndex()
        self.model.setData(index, value=QVariant(), role=Qt.UserRole+1)

    def get_new_board(self):
        index = self.sudoku_view.currentIndex()
        self.model.setData(index, value=QVariant(), role=Qt.UserRole+2)