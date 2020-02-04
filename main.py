import random
import sys
import time
from collections import deque

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import MainBoard  # импорт нашего сгенерированного файла


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = MainBoard.Ui_MainWindow()
        self.ui.setupUi(self)
        self.cards_dict = {}
        self.card_value = {"B": 11, "D": 12, "K": 13, "T": 1}
        self.all_card = deque()  # Черга
        self.sum = 0
        self.card_memory = 0

        self.btn_grp = QtWidgets.QButtonGroup()

        self.ui.pushButton.setStyleSheet("font: 25pt Comic Sans MS")
        self.ui.pushButton.setText("►")
        self.ui.pushButton.clicked.connect(self.dobor)
        self.ui.pushButton_2.setStyleSheet("font: 25pt Comic Sans MS")


        self.new_pasians()

    def construct_deck(self):
        self.all_card += [mast + value for mast in "♥♦♣♠" for value in ([str(i) for i in range(2, 11)] + ['B', "D",
                                                                                                           "K", "T"])]
        random.shuffle(self.all_card)

    def new_card(self, pos_x, pos_y):
        b = QtWidgets.QPushButton(self.ui.centralwidget)
        b.setGeometry(QtCore.QRect(pos_x, pos_y, 80, 130))
        b.setDisabled(True)
        b.setCheckable(True)

        b.setObjectName("pushButton")
        b.setText(self.all_card.popleft())

        b.isDeleted = False
        b.isReady = False

        self.btn_grp.addButton(b)
        #print(self.btn_grp.button(5))
        b.setStyleSheet("font: 25pt Comic Sans MS")
        return b

    def new_pasians(self):
        self.construct_deck()
        pos_x = 550
        pos_y = 40
        for row in range(1, 8):

            for col in range(1, row+1):
                self.cards_dict[row, col] = self.new_card(pos_x, pos_y)
                self.cards_dict[row, col].clicked.connect(lambda: self.check_card_sum((row, col)))

                pos_x += 100

            pos_y += 80
            pos_x -= row * 100 + 50

        for col in range(1, 8):
            self.cards_dict[7, col].setDisabled(False)
            self.cards_dict[7, col].isReady = True


        #self.cards_dict[7, 3].click()
        #print(self.cards_dict[7, 4].isChecked())
        print(self.cards_dict)
        self.dobor()

    def dobor(self):
        new_card = self.all_card.popleft()
        self.ui.pushButton_2.setText(new_card)

        self.all_card.append(new_card)

    def check_card_sum(self, row_col):

        if row_col == self.card_memory:
            self.sum = 0
            self.card_memory = 0

        else:
            self.sum += self.card_value[row_col]
            if self.sum == 13:
                self.cards_dict[row_col].isDeleted = True
                self.cards_dict[row_col].deleteLater()

                if self.card_memory:
                    self.cards_dict[self.card_memory].deleteLater()

            elif self.card_memory:
                self.cards_dict[self.card_memory].click()
                self.cards_dict[row_col].click()
                self.sum = 0
                self.card_memory = 0
            else:
                self.card_memory = row_col



    def check_pasians_card(self):

        for row in range(1, 7):

            for col in range(1, row+1):
                if self.cards_dict[row+1, col].isDeleted and self.cards_dict[row+1, col+1].isDeleted:
                    self.cards_dict[row, col].setDisabled(False)
                    self.cards_dict[row, col].isReady = True

app = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(app.exec())