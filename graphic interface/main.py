import random
import sys
from collections import deque

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import MainBoard  # импорт нашего сгенерированного файла


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
                                                   
        self.ui = MainBoard.Ui_MainWindow()

        self.ui.setupUi(self)
        self.cards_dict = {}

        self.all_card = deque()  # Черга
        self.sum = 0
        self.card_memory = 0

        self.ui.pushButton.setStyleSheet("font: 25pt Comic Sans MS")
        self.ui.pushButton.setText("►")
        self.ui.pushButton.clicked.connect(self.dobor)

        self.ui.label.setText("Победа")
        self.ui.label.hide()
        self.ui.label.setStyleSheet("font: 100pt Comic Sans MS")

        self.ui.pushButton_2.setStyleSheet("font: 25pt Comic Sans MS")
        self.ui.pushButton_2.clicked.connect(lambda: self.check_card_sum(self.ui.pushButton_2))
        self.ui.pushButton_2.isDeleted = False
        self.new_pasians()

    def construct_deck(self):
        self.all_card += [mast + value for mast in "♥♦♣♠" for value in ([str(i) for i in range(2, 11)] + ['J', "Q",
                                                                                                           "K", "T"])]
        random.shuffle(self.all_card)

    def new_card(self, pos_x, pos_y):
        b = QtWidgets.QPushButton(self.ui.centralwidget)
        b.setGeometry(QtCore.QRect(pos_x, pos_y, 80, 130))
        b.setDisabled(True)
        b.setCheckable(True)

        b.setObjectName("pushButton")
        b.setText(self.all_card.popleft())

        b.setStyleSheet("font: 25pt Comic Sans MS")

        if b.text()[0] in "♦♥":
            b.setStyleSheet("font: 25pt Comic Sans MS; color: rgb(255, 1, 1)")

        b.isDeleted = False

        b.clicked.connect(lambda: self.check_card_sum(b))

        return b

    def new_pasians(self):
        self.construct_deck()
        pos_x = 550
        pos_y = 40
        for row in range(1, 8):

            for col in range(1, row+1):
                self.cards_dict[row, col] = self.new_card(pos_x, pos_y)

                pos_x += 100

            pos_y += 80
            pos_x -= row * 100 + 50

        for col in range(1, 8):
            self.cards_dict[7, col].setDisabled(False)
            self.cards_dict[7, col].isReady = True

        self.ui.pushButton.setToolTip(str(len(self.all_card)))
        self.dobor()

    def dobor(self):

        self.score()

        if self.ui.pushButton_2.isChecked():
            self.ui.pushButton_2.click()

        new_card = self.all_card.popleft()
        self.ui.pushButton_2.setText(new_card)

        if self.ui.pushButton_2.text()[0] in "♦♥":
            self.ui.pushButton_2.setStyleSheet("font: 25pt Comic Sans MS; color: rgb(255, 1, 1)")

        else:
            self.ui.pushButton_2.setStyleSheet("font: 25pt Comic Sans MS")

        if self.ui.pushButton_2.isDeleted:

            self.ui.pushButton_2.show()
            self.ui.pushButton_2.isDeleted = False

        self.all_card.append(new_card)

    def card_value(self, val):
        try:
            return {"J": 11, "Q": 12, "K": 13, "T": 1}[val]
        except KeyError:
            return int(val)

    def score(self):

        self.ui.lcdNumber.display(self.ui.lcdNumber.value()+1)

        self.ui.lcdNumber.update()

    def check_card_sum(self, btn):

        if btn == self.card_memory:

            self.sum = 0
            self.card_memory = 0

        else:
            self.sum += self.card_value(btn.text()[1:])
            if self.sum == 13:

                btn.isDeleted = True
                self.score()
                if btn == self.ui.pushButton_2:
                    self.all_card.pop()
                    self.ui.pushButton_2.setChecked(False)
                    self.ui.pushButton_2.hide()

                else:
                    btn.deleteLater()
                self.sum = 0

                if self.card_memory:
                    self.card_memory.isDeleted = True

                    self.score()
                    if self.card_memory == self.ui.pushButton_2:
                        self.all_card.pop()
                        self.ui.pushButton_2.setChecked(False)
                        self.ui.pushButton_2.hide()

                    else:
                        self.card_memory.deleteLater()

                    self.card_memory = 0

            elif self.card_memory != 0:

                self.card_memory.click()
                btn.click()
                self.sum = 0
                self.card_memory = 0
            else:

                self.card_memory = btn

        self.check_pasians_card()

    def check_pasians_card(self):

        self.score()

        if len(self.all_card) == 0:
            self.ui.pushButton.setDisabled(True)

        if self.cards_dict[1, 1].isDeleted:
            self.ui.label.show()

        self.ui.pushButton.setToolTip(str(len(self.all_card)))

        for row in range(1, 7):

            for col in range(1, row+1):
                if self.cards_dict[row+1, col].isDeleted and self.cards_dict[row+1, col+1].isDeleted:
                    if not self.cards_dict[row, col].isDeleted:
                        self.cards_dict[row, col].setDisabled(False)


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(app.exec())