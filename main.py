import sys
from time import sleep
import ctypes
import os
import random
from math import copysign
import math
from collections import defaultdict
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QPushButton, \
    QLineEdit, QLabel, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5 import QtGui
from PyQt5 import QtCore
from sudoku import SudokuSolver


buttonslist = [QtCore.Qt.Key_1, QtCore.Qt.Key_2, QtCore.Qt.Key_3, QtCore.Qt.Key_4, QtCore.Qt.Key_5, QtCore.Qt.Key_6,
               QtCore.Qt.Key_7, QtCore.Qt.Key_8, QtCore.Qt.Key_9]


class Window(QWidget):
    def __init__(self):
        super().__init__()
        global w, h
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('Sudoku Solver')
        self.setStyleSheet('background-color: white')
        self.setMouseTracking(True)
        self.selected = [0, 0]
        self.buttons = [[Cell(self, j, i) for i in range(9)] for j in range(9)]
        self.solvestarting = SolveStarting(self)
        self.show()

    def mouseMoveEvent(self, ev):
        self.mouseMoveCatcher(ev.x(), ev.y())

    def mouseMoveCatcher(self, x, y):
        x, y = x // 50, y // 50
        if x < 9 and y < 9:
            self.selected = [x, y]

    def keyPressEvent(self, e):  # should be placed here!
        if e.key() in buttonslist:
            self.buttons[self.selected[0]][self.selected[1]].setText(str(buttonslist.index(e.key()) + 1))
            self.buttons[self.selected[0]][self.selected[1]].text = str(buttonslist.index(e.key()) + 1)


class Cell(QPushButton):
    def __init__(self, window, x, y, text=' '):
        super().__init__(text, window)
        self.cs = [x, y]
        self.text = '0'
        self.move(x * 50, y * 50)
        self.resize(50, 50)
        self.setStyleSheet('{font: 30pt Helvetica MS;}')
        self.clicked.connect(self.action)
        self.setMouseTracking(True)
        self.show()

    def action(self):
        print('ok')

    def mouseMoveEvent(self, ev):  # pyqt's "feature"
        print((ev.x() + self.cs[0]*50, ev.y() + self.cs[1]*50))
        window.mouseMoveCatcher(ev.x() + self.cs[0]*50, ev.y() + self.cs[1]*50)

    def get_text(self):
        return self.text


class SolveStarting(QPushButton):
    def __init__(self, window):
        super().__init__('Решить судоку!', window)
        self.resize(200, 40)
        self.move(500, 20)
        self.clicked.connect(self.action)
        self.show()

    def action(self):
        board = [[int(window.buttons[j][i].get_text()) for i in range(9)] for j in range(9)]
        print(board)
        s = SudokuSolver(board)
        res = s.solve()
        if res:
            for i in range(9):
                for j in range(9):
                    window.buttons[i][j].setText(str(res[i][j]))
        else:
            print("No solutions.")



def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    # sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys._excepthook = sys.excepthook
sys.excepthook = my_exception_hook
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())