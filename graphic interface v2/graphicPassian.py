import random
import sys
import time
from collections import deque

import MainBoardv2 as MainBoard
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QIcon, QMovie
from PyQt5.QtWidgets import QApplication


class Board(QtWidgets.QMainWindow):

    def __init__(self):
        super(Board, self).__init__()
        self.ui = MainBoard.Ui_MainWindow()
        self.ui.setupUi(self)
        self.deck = deque()
        self.cards_dict = {}

        self.setup_board_element()
        self.new_pasians()

    def setup_board_element(self):
        """Customizing the features and design of the board elements: buttons, label. """
        self.ui.label.setPixmap(QPixmap("background.jpg").scaled(self.width(), self.height()))
        self.ui.pushButton.setIcon(QIcon('default/purple_back.png'))
        self.ui.pushButton.setIconSize(QtCore.QSize(self.ui.pushButton.height(), self.ui.pushButton.height()))
        self.ui.pushButton.clicked.connect(self.dobor)
        self.ui.cardDobor = Card(self.ui.centralwidget,  "", (140, 40), self.gameplay)
        self.ui.restart.triggered.connect(self.restart_game)
        self.ui.restart.setShortcut("Ctrl+R")
        self.ui.score.setPixmap(QPixmap("score.PNG").scaled(self.ui.score.width(), self.ui.score.height()))
        self.ui.score.hide()
        self.ui.back.triggered.connect(self.last_dobor)
        self.ui.back.setShortcut("Ctrl+Z")
        self.ui.showscore.triggered.connect(lambda: self.ui.score.show() if self.ui.score.isHidden()
                                                    else self.ui.score.hide())

    def restart_game(self):
        self.start_time = time.time()
        self.ui.lcdNumber.display(0)
        self.ui.lcdNumber.update()
        self.ui.lcdNumber.show()
        self.ui.pushButton.setToolTip(str(len(self.deck)-1))
        self.deck = Deck().deck
        self.ui.cardDobor.set_image("background.jpg")
        self.ui.label.setPixmap(QPixmap("background.jpg").scaled(self.width(), self.height()))
        self.ui.cardDobor.value = ""
        self.ui.cardDobor.show()
        self.ui.pushButton.show()

        self.ui.cardDobor.isDeleted = False
        self.ui.cardDobor.setDisabled(False)
        for row in range(1, 8):

            for col in range(1, row+1):
                value = self.deck.popleft()

                self.cards_dict[row, col].setDisabled(True)
                self.cards_dict[row, col].isDeleted = False
                self.cards_dict[row, col].isActive = False
                self.cards_dict[row, col].value = value
                self.cards_dict[row, col].set_image()
                self.cards_dict[row, col].show()

        for col in range(1, 8):
            self.cards_dict[7, col].setDisabled(False)
            self.cards_dict[7, col].set_active()

        self.deck.append("back_cards-07")

    def new_pasians(self):
        self.start_time = time.time()
        self.ui.cardDobor.set_image("background.jpg")

        self.ui.cardDobor.isDeleted = False
        self.ui.cardDobor.setDisabled(False)

        self.deck = Deck().deck

        pos_x = 550
        pos_y = 40
        for row in range(1, 8):

            for col in range(1, row+1):

                value = self.deck.popleft()
                self.cards_dict[row, col] = Card(self.ui.centralwidget,  value, (pos_x, pos_y), self.gameplay)

                pos_x += 100

            pos_y += 80
            pos_x -= row * 100 + 50

        for col in range(1, 8):
            self.cards_dict[7, col].setDisabled(False)
            self.cards_dict[7, col].set_active()

        self.deck.append("back_cards-07")
        self.ui.check_turn.setShortcut("Ctrl+P")
        self.ui.check_turn.triggered.connect(self.prompt_turn)

    def card_value(self, val):
        try:
            try:
                return {"J": 11, "Q": 12, "K": 13, "A": 1, "": -1}[val[:-1]]
            except KeyError:
                return int(val[:-1])
        except ValueError:
            return -1

    def dobor(self):
        """For using upper-left button, choice other card from deck """

        self.update_score()
        new_card = self.deck.popleft()
        self.ui.cardDobor.value = new_card
        self.ui.cardDobor.set_active()

        if self.ui.cardDobor.isDeleted:
            self.ui.cardDobor.show()
            self.ui.cardDobor.isDeleted = False

        self.deck.append(new_card)

        self.check_pasians_card()

    def gameplay(self, card1, card2=None):

        def action_with_button(btn):

            if btn == self.ui.cardDobor:
                self.deck.pop()
                self.ui.cardDobor.hide()

            else:
                btn.hide()

        if card2 is None:
            if self.card_value(card1.value) == 13:
                card1.isDeleted = True
                action_with_button(card1)

                self.update_score()

        else:
            if self.card_value(card1.value) + self.card_value(card2.value) == 13:
                card1.isDeleted = True
                action_with_button(card1)
                card2.isDeleted = True
                action_with_button(card2)

                self.update_score()

        self.check_pasians_card()

    def game_win(self):
        self.ui.score.hide()
        self.ui.pushButton.hide()
        self.ui.cardDobor.hide()
        self.ui.lcdNumber.hide()
        movie = QMovie("firework.gif")
        movie.setScaledSize(QtCore.QSize(self.width(), self.height()))
        self.ui.label.setMovie(movie)
        movie.start()
        self.show_popup("Win")

    def show_popup(self, game="Win"):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(game)
        msg.setText("You " + game.lower() + " this game")
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Retry)

        utime = int(time.time() - self.start_time)
        utime = f"{utime // 60}m. {utime % 60}s."
        text = f"You time is {utime} and you score is {self.ui.lcdNumber.intValue()}\n\n" \
               f"Programmer, that wrote this game, won this game by 1m. 17s. and his score was 61"
        msg.setDetailedText(text)
        msg.buttonClicked.connect(self.popup_button)

        x = msg.exec_()

    def popup_button(self, i):
        if i.text() == "Retry":
            self.restart_game()

    def update_score(self):

        self.ui.lcdNumber.display(self.ui.lcdNumber.value()+1)
        self.ui.lcdNumber.update()

    def check_pasians_card(self):
        """When card deleted check if new cards can be usable"""

        if len(self.deck) == 0:
            self.ui.pushButton.setDisabled(True)

        if self.cards_dict[1, 1].isDeleted:
            self.game_win()

        self.ui.pushButton.setToolTip(str(len(self.deck)-1))

        for row in range(1, 7):

            for col in range(1, row+1):

                if self.cards_dict[row+1, col].isDeleted and self.cards_dict[row+1, col+1].isDeleted:
                    if not self.cards_dict[row, col].isDeleted:
                        self.cards_dict[row, col].setDisabled(False)
                        self.cards_dict[row, col].set_active()

    def last_dobor(self):
        last = self.deck.pop()
        self.deck.appendleft(last)

        last = self.deck.pop()
        self.deck.append(last)

        self.ui.cardDobor.value = last
        self.ui.cardDobor.set_active()

    def prompt_turn(self):
        for row in range(1, 8):
            for col in range(1, row+1):
                if self.cards_dict[row, col].isActive and not self.cards_dict[row, col].isDeleted:

                    if self.card_value(self.cards_dict[row, col].value) == 13:
                        self.cards_dict[row, col].setStyleSheet("border: 10px solid red;")
                        return

                    for row2 in range(1, 8):
                        for col2 in range(1, row2 + 1):
                            if self.cards_dict[row2, col2].isActive and not self.cards_dict[row2, col2].isDeleted:

                                if self.card_value(self.cards_dict[row, col].value) + self.card_value(
                                        self.cards_dict[row2, col2].value) == 13:
                                    self.cards_dict[row, col].setStyleSheet("border: 10px solid red;")
                                    self.cards_dict[row2, col2].setStyleSheet("border: 10px solid red;")
                                    return
        for card in self.deck:
            if self.card_value(card) == 13:
                if card == self.ui.cardDobor.value:
                    self.ui.cardDobor.setStyleSheet("border: 10px solid red;")
                else:
                    self.ui.pushButton.setStyleSheet("border: 10px solid red;")
                return

            for row in range(1, 8):
                for col in range(1, row + 1):
                    if self.cards_dict[row, col].isActive and not self.cards_dict[row, col].isDeleted:

                        if self.card_value(self.cards_dict[row, col].value) + self.card_value(card) == 13:

                            if card == self.ui.cardDobor.value:
                                self.ui.cardDobor.setStyleSheet("border: 10px solid red;")
                            else:
                                self.ui.pushButton.setStyleSheet("border: 10px solid red;")
                            self.cards_dict[row, col].setStyleSheet("border: 10px solid red;")
                            return

        self.show_popup("Lose")


class Card(QtWidgets.QLabel):

    def __init__(self, parent, value, posxy, function, card_size=(80, 130)):
        super().__init__(parent)

        self.value = value
        self.pos_xy = posxy
        self.card_size = card_size
        self.function = function

        self.setAcceptDrops(True)
        self.setGeometry(QtCore.QRect(self.pos_xy[0], self.pos_xy[1], self.card_size[0], self.card_size[1]))
        self.set_image()
        self.setDisabled(True)
        self.isDeleted = False
        self.isActive = False
        self.setObjectName("pushButton")

    def set_image(self, value="default/purple_back.png", card_size=(80, 130)):
        """Paste image in card.
        value: has type example 10C, KH"""
        pixmap = QPixmap(value)
        pixmap = pixmap.scaled(card_size[0], card_size[1])
        self.setStyleSheet("")
        self.setPixmap(pixmap)

    def set_active(self, card_size=(80, 130)):
        self.isActive = True
        pixmap = QPixmap("default/" + self.value + '.png')
        pixmap = pixmap.scaled(card_size[0], card_size[1])
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.function(self)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        self.hide()
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
        drag.exec_(Qt.MoveAction | Qt.CopyAction)
        if not self.isDeleted:
            self.show()

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
        self.deck += [value + mast for mast in "CDHS" for value in ([str(i) for i in range(2, 11)] + ['J', "Q",
                                                                                                           "K", "A"])]
        random.shuffle(self.deck)


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    application = Board()
    application.show()

    sys.exit(app.exec())
