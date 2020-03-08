import random
from collections import deque


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class Board:

    def __init__(self):
        super(Board, self).__init__()
        self.deck = deque()
        self.cards_dict = {}
        self.sum = 0
        self.card_memory = 0

        self.game()

    def new_pasians(self):

        self.deck = Deck().deck

        self.cards_dict[0, 0] = Card(" ►", len(self.deck), "      ")
        self.cards_dict[0, 1] = Card('  ', 0, (0, 1))

        self.cards_dict[0, 0].isReady = True
        self.cards_dict[0, 1].isReady = True

        for row in range(1, 8):

            for col in range(1, row+1):

                value = self.deck.popleft()
                self.cards_dict[row, col] = Card(value, self.card_value(value[1:]), (row, col))

        for col in range(1, 8):
            self.cards_dict[7, col].isReady = True

        self.dobor()

    def dobor(self):
        """For using upper-left button, choice other card from deck """

        new_card = self.deck.popleft()
        self.cards_dict[0, 1].value_show = new_card
        self.cards_dict[0, 1].value = self.card_value(new_card[1:])
        self.deck.append(new_card)

    def gameplay(self, index: str):
        """Check if choices card right (them sum = 13) and remove them if yes"""

        l = []
        for i in index.split():
            l.append((int(i.split(",")[0]), int(i.split(",")[1])))
        index = l
        print(index)
        print(self.cards_dict[index[0]].value)
        if self.cards_dict[index[0]].value == 13:
            self.cards_dict[index[0]].isDeleted = True
            print("1")
        if len(index) > 1:

            if self.cards_dict[index[0]].value + self.cards_dict[index[1]].value == 13:
                print("2")
                self.cards_dict[index[0]].isDeleted = True
                self.cards_dict[index[1]].isDeleted = True

            elif self.cards_dict[index[1]].value == 13:
                self.cards_dict[index[1]].isDeleted = True

        self.check_pasians_card()

    def card_value(self, val):
        try:
            return {"J": 11, "Q": 12, "K": 13, "T": 1, "": -1}[val]
        except KeyError:
            return int(val)

    def show(self):
        # 7 - size window * 7 max last row, 2 - whitespace + size dobor + 2 whitespace * 3 Colors = 7 letters
        size_window = 7 * 7 + 7 * 2 + 7 * 2 + 4

        for index in range(4):

            b = [self.cards_dict[0, col].show()[index] for col in range(0, 2)]
            print(f'{"  ".join(b)}', end=" ")
            print(f'{"".join(self.cards_dict[1, 1].show()[index]):^{size_window-7*4-8}}')

        for row in range(2, 8):
            for index in range(4):
                b = [self.cards_dict[row, col].show()[index] for col in range(1, row + 1)]
                print(f'{"  ".join(b):^{size_window}}')

    def check_pasians_card(self):
        """When card deleted check if new cards can be usable"""

        if self.cards_dict[1, 1].isDeleted:
            print("U win this f*ck game. GJ")
            pass

        for row in range(1, 7):

            for col in range(1, row+1):

                if self.cards_dict[row+1, col].isDeleted and self.cards_dict[row+1, col+1].isDeleted:
                    if not self.cards_dict[row, col].isDeleted:
                        self.cards_dict[row, col].isReady = True
        self.show()

    def game(self):
        print("Game start")
        self.new_pasians()
        self.show()
        while True:

            if self.cards_dict[1, 1].isDeleted:
                break

            answer = str(input())

            if answer == "":
                self.dobor()
                self.show()
                continue

            print("Answer")
            self.gameplay(answer)


class Card:

    def __init__(self, value_show: str, value,  index: tuple):
        super().__init__()

        self.isReady = False
        self.value_show = value_show
        self.value = value
        self.index = index
        self.isDeleted = False

    def show(self):

        if self.isReady and not self.isDeleted:
            return ["┌─────┐",
                    f"|{self.value_show:^5}|",
                    "└─────┘",
                    f" {self.index}"]
        elif not self.isReady:
            return ["┌─────┐",
                    f"|{'???':^5}|",
                    "└─────┘",
                    "       "]

        return ["       ",
                "       ",
                "       ",
                "       "]


class Deck:
    """Contruct new deck of 52 card

        :return dict of cards
    """

    def __init__(self):

        self.deck = deque()

        self.construct_deck()

    def construct_deck(self):
        self.deck += [mast + value for mast in "♥♦♣♠" for value in ([str(i) for i in range(2, 11)] + ['J', "Q",
                                                                                                      "K", "T"])]
        random.shuffle(self.deck)


if __name__ == "__main__":
    application = Board()

