import random
import sys
from collections import deque

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QFrame

import MainBoardv2 as MainBoard


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

        self.ui.cardDobor = Card(self.ui.centralwidget,  "", (140, 40), self.gameplay)

        self.ui.cardDobor.setStyleSheet("font: 25pt Comic Sans MS")

        self.ui.cardDobor.isDeleted = False
        self.ui.cardDobor.setDisabled(False)

    def card_value(self, val):
        try:
            return {"J": 11, "Q": 12, "K": 13, "T": 1, "": -1}[val[1:]]
        except KeyError:
            return int(val[1:])

    def dobor(self):
        """For using upper-left button, choice other card from deck """

        new_card = self.deck.popleft()
        self.ui.cardDobor.setText(new_card)
        self.ui.cardDobor.value = new_card

        self.ui.cardDobor.setStyleSheet(self.card_color(self.ui.cardDobor.text()[0]))

        if self.ui.cardDobor.isDeleted:

            self.ui.cardDobor.show()
            self.ui.cardDobor.isDeleted = False

        self.deck.append(new_card)

        self.check_pasians_card()

    def new_pasians(self):

        self.deck = Deck().deck

        pos_x = 550
        pos_y = 40
        for row in range(1, 8):

            for col in range(1, row+1):

                value = self.deck.popleft()
                self.cards_dict[row, col] = Card(self.ui.centralwidget,  value, (pos_x, pos_y),
                                                 self.gameplay, card_style=self.card_color(value[0]))

                pos_x += 100

            pos_y += 80
            pos_x -= row * 100 + 50

        for col in range(1, 8):
            self.cards_dict[7, col].setDisabled(False)

        self.deck.append("☻")

    def gameplay(self, card1, card2=None):

        def action_with_button(btn):

            if btn == self.ui.cardDobor:
                self.deck.pop()
                self.ui.cardDobor.hide()

            else:
                btn.deleteLater()

        if card2 is None:
            if self.card_value(card1.value) == 13:
                card1.isDeleted = True
                action_with_button(card1)
        else:
            if self.card_value(card1.value) + self.card_value(card2.value) == 13:
                card1.isDeleted = True
                action_with_button(card1)
                card2.isDeleted = True
                action_with_button(card2)
        self.check_pasians_card()

    def card_color(self, value):

        if value in "♦♥":
            return "font: 25pt Comic Sans MS; color: rgb(255, 1, 1)"

        return "font: 25pt Comic Sans MS"

    def check_pasians_card(self):
        """When card deleted check if new cards can be usable"""

        if len(self.deck) == 0:
            self.ui.pushButton.setDisabled(True)

        if self.cards_dict[1, 1].isDeleted:
            self.ui.pushButton.setDisabled(True)
            self.ui.label.show()

        self.ui.pushButton.setToolTip(str(len(self.deck)-1))

        for row in range(1, 7):

            for col in range(1, row+1):

                if self.cards_dict[row+1, col].isDeleted and self.cards_dict[row+1, col+1].isDeleted:
                    if not self.cards_dict[row, col].isDeleted:
                        self.cards_dict[row, col].setDisabled(False)


class Card(QtWidgets.QLabel):

    def __init__(self, parent, value, posxy, function, card_size=(80, 130),
                 card_style="font: 25pt Comic Sans MS"):
        super().__init__(parent)

        self.value = value
        self.pos_xy = posxy
        self.card_size = card_size
        self.card_style = card_style
        self.function = function

        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Panel)

        self.setGeometry(QtCore.QRect(self.pos_xy[0], self.pos_xy[1], self.card_size[0], self.card_size[1]))
        self.setText(self.value)
        self.setStyleSheet(self.card_style)

        self.setDisabled(True)
        self.isDeleted = False

        self.setObjectName("pushButton")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.function(self)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setParent(self)
        drag.setMimeData(mimedata)

        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        card1 = e.mimeData().parent()
        self.function(self, card1)

        e.acceptProposedAction()
        e.accept()


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


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    application = Board()
    application.show()

    sys.exit(app.exec())
