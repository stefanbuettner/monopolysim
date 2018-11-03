import random as rng
from matplotlib import pyplot as plt
from enum import IntEnum

class Field(IntEnum):
    START = 0
    JAIL = 10
    GO_TO_JAIL = 30

class Player:

    def __init__(self, num_fields):
        self.num_fields = num_fields
        self.pos = 0
        self.num_doubles = 0
        self.tries_for_doubles = 0

    def throw_dice(self):
        d1 = rng.randint(1,6)
        d2 = rng.randint(1,6)

        if d1 == d2:
            self.num_doubles += 1
        else:
            self.num_doubles = 0

        return d1 + d2

    def go_to_jail(self):
        self.pos = Field.JAIL
        self.num_doubles = 0
        self.tries_for_doubles = 0
    
    def move(self):
        step = self.throw_dice()

        if Field.JAIL == self.pos:
            self.tries_for_doubles += 1
            if self.tries_for_doubles < 3 and self.num_doubles <= 0:
                return self.pos
        else:
            if self.num_doubles >= 3:
                self.go_to_jail()

        self.pos = (self.pos + step) % self.num_fields

        if Field.GO_TO_JAIL == self.pos:
            self.go_to_jail()
        
        return self.pos

if __name__  == "__main__":

    num_fields = 40
    board = [0 for x in range(num_fields)]
    num_games = 1000
    num_moves = 300
    i = 0
    for game in range(num_games):

        player = Player(num_fields)

        for move in range(num_moves):

            pos = player.move()
            board[pos] += 1
            i += 1

    board = [x / i for x in board]
    print(board)
    plt.bar(range(num_fields), board)
    plt.show()
