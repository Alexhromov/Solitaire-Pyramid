import random
import sys
from collections import deque

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import MainBoard  # импорт нашего сгенерированного файла


class Board(QtWidgets.QMainWindow):

    def __init__(self):
        super(Board, self).__init__()

        self.ui = MainBoard.Ui_MainWindow()
        self.ui.setupUi(self)

        self.deck = deque()
        self.cards_dict = {}

        self.sum = 0
        self.card_memory = 0

        self.setup_board_element()

        self.new_pasians()

    def setup_board_element(self):
        """Customizing the features and design of the board elements: buttons, label. """

        self.ui.pushButton.setStyleSheet("font: 25pt Comic Sans MS")
        self.ui.pushButton.setText("►")
        self.ui.pushButton.clicked.connect(self.dobor)

        self.ui.label.setText("Победа")
        self.ui.label.hide()
        self.ui.label.setStyleSheet("font: 100pt Comic Sans MS")

        self.ui.pushButton_2.setStyleSheet("font: 25pt Comic Sans MS")
        self.ui.pushButton_2.clicked.connect(lambda: self.gameplay(self.ui.pushButton_2))
        self.ui.pushButton_2.isDeleted = False

    def new_pasians(self):

        self.deck = Deck().deck

        pos_x = 550
        pos_y = 40
        for row in range(1, 8):

            for col in range(1, row+1):

                value = self.deck.popleft()
                self.cards_dict[row, col] = Card(QtWidgets.QPushButton(self.ui.centralwidget),  value, (pos_x, pos_y),
                                                 self.gameplay, card_style=self.card_color(value[0])).new_card()

                pos_x += 100

            pos_y += 80
            pos_x -= row * 100 + 50

        for col in range(1, 8):
            self.cards_dict[7, col].setDisabled(False)
            self.cards_dict[7, col].isReady = True

        self.ui.pushButton.setToolTip(str(len(self.deck)))
        self.dobor()

    def card_value(self, val):
        try:
            return {"J": 11, "Q": 12, "K": 13, "T": 1}[val]
        except KeyError:
            return int(val)

    def score(self):

        self.ui.lcdNumber.display(self.ui.lcdNumber.value()+1)

        self.ui.lcdNumber.update()

    def card_color(self, value):

        if value in "♦♥":
            return "font: 25pt Comic Sans MS; color: rgb(255, 1, 1)"

        return "font: 25pt Comic Sans MS"

    def dobor(self):
        """For using upper-left button, choice other card from deck """

        self.score()

        if self.ui.pushButton_2.isChecked():
            self.ui.pushButton_2.click()

        new_card = self.deck.popleft()
        self.ui.pushButton_2.setText(new_card)

        self.ui.pushButton_2.setStyleSheet(self.card_color(self.ui.pushButton_2.text()[0]))

        if self.ui.pushButton_2.isDeleted:

            self.ui.pushButton_2.show()
            self.ui.pushButton_2.isDeleted = False

        self.deck.append(new_card)

    def gameplay(self, btn):
        """Check if choices card right (them sum = 13) and remove them if yes"""

        def action_with_button(btn):

            if btn == self.ui.pushButton_2:
                self.deck.pop()
                self.ui.pushButton_2.setChecked(False)
                self.ui.pushButton_2.hide()

            else:
                btn.deleteLater()

        if btn == self.card_memory:
            """Button clicked twice time (user unclick card)"""

            self.sum = 0
            self.card_memory = 0

        else:
            self.sum += self.card_value(btn.text()[1:])

            if self.sum == 13:

                btn.isDeleted = True
                action_with_button(btn)

                self.sum = 0

                if self.card_memory:
                    self.card_memory.isDeleted = True

                    action_with_button(self.card_memory)

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
        """When card deleted check if new cards can be usable"""

        self.score()

        if len(self.deck) == 0:
            self.ui.pushButton.setDisabled(True)

        if self.cards_dict[1, 1].isDeleted:
            self.ui.label.show()

        self.ui.pushButton.setToolTip(str(len(self.deck)))

        for row in range(1, 7):

            for col in range(1, row+1):
                if self.cards_dict[row+1, col].isDeleted and self.cards_dict[row+1, col+1].isDeleted:
                    if not self.cards_dict[row, col].isDeleted:
                        self.cards_dict[row, col].setDisabled(False)


class Card:

    def __init__(self, button, value, posxy, function: "arg = button", card_size=(80, 130),
                 card_style="font: 25pt Comic Sans MS"):
        super().__init__()

        self.b = button
        self.value = value
        self.pos_xy = posxy
        self.card_size = card_size
        self.card_style = card_style
        self.function = function

    def new_card(self):

        self.b.setGeometry(QtCore.QRect(self.pos_xy[0], self.pos_xy[1], self.card_size[0], self.card_size[1]))
        self.b.setText(self.value)
        self.b.setStyleSheet(self.card_style)

        self.b.setDisabled(True)
        self.b.setCheckable(True)
        self.b.isDeleted = False

        self.b.setObjectName("pushButton")

        self.b.clicked.connect(lambda: self.function(self.b))

        return self.b


class Deck:
    """Contruct new deck of 52 card

        :return nothing
    """

    def __init__(self):

        self.deck = deque()

        self.construct_deck()

    def construct_deck(self):
        self.deck += [mast + value for mast in "♥♦♣♠" for value in ([str(i) for i in range(2, 11)] + ['J', "Q",
                                                                                                           "K", "T"])]
        random.shuffle(self.deck)

app = QtWidgets.QApplication([])
application = Board()
application.show()

sys.exit(app.exec())


