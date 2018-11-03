import random as rng
from matplotlib import pyplot as plt
from enum import IntEnum
from argparse import ArgumentParser

class Field(IntEnum):
    START = 0
    JAIL = 10
    GO_TO_JAIL = 30
    CHANCE_1 = 2
    CHANCE_2 = 17
    CHANCE_3 = 33
    COMMUNITY_1 = 7
    COMMUNITY_2 = 22
    COMMUNITY_3 = 36
    STATION_1 = 5
    STATION_2 = 15
    STATION_3 = 25
    STATION_4 = 35
    NEW_YORK_AVENUE = 19
    PACIFIC_AVENUE = 11
    ELECTRIC_COMPANY = 12
    WATER_WORKS = 28
    BOARDWALK = 39

class ActionCard:
    def execute(self, player):
        raise NotImplementedError

class NoopCard(ActionCard):
    def execute(self, player):
        pass
    
    def __repr__(self):
        return "NoopCard"

class GoToJailCard(ActionCard):
    def execute(self, player):
        player.go_to_jail()
    
    def __repr__(self):
        return "GoToJail"

class ToFieldCard(ActionCard):
    def __init__(self, field):
        self.field = field

    def execute(self, player):
        player.pos = self.field
    
    def __repr__(self):
        return "To" + str(self.field)

class ToNextStationCard(ActionCard):
    def execute(self, player):
        if player.pos <= Field.STATION_1:
            player.pos = Field.STATION_1
        elif player.pos <= Field.STATION_2:
            player.pos = Field.STATION_2
        elif player.pos <= Field.STATION_3:
            player.pos = Field.STATION_3
        elif player.pos <= Field.STATION_4:
            player.pos = Field.STATION_4
        else:
            player.pos = Field.STATION_1
    
    def __repr__(self):
        return "ToNextStation"

class MoveBackwardCard(ActionCard):
    def __init__(self, steps):
        self.steps = steps
    
    def execute(self, player):
        player.move_steps(-self.steps)
    
    def __repr__(self):
        return "Move"+ str(self.steps) + "Backward"

class ToNextSupplierCard(ActionCard):
    def execute(self, player):
        if player.pos <= Field.ELECTRIC_COMPANY:
            player.pos = Field.ELECTRIC_COMPANY
        elif player.pos <= Field.WATER_WORKS:
            player.pos = Field.WATER_WORKS
        else:
            player.pos = Field.ELECTRIC_COMPANY
    
    def __repr__(self):
        return "ToNextSupplier"

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
        steps = self.throw_dice()
        return self.move_steps(steps)

    def move_steps(self, steps):
        if Field.JAIL == self.pos:
            self.tries_for_doubles += 1
            if self.tries_for_doubles < 3 and self.num_doubles <= 0:
                return self.pos
        else:
            if self.num_doubles >= 3:
                self.go_to_jail()

        self.pos = (self.pos + steps) % self.num_fields

        if Field.GO_TO_JAIL == self.pos:
            self.go_to_jail()
        
        return self.pos


def init_chance_cards():
    # print("Initializing chance cards")
    chance_cards = [
        GoToJailCard(),
        ToNextStationCard(),
        ToNextStationCard(),
        ToNextSupplierCard(),
        ToFieldCard(Field.START),
        ToFieldCard(Field.STATION_1),
        ToFieldCard(Field.PACIFIC_AVENUE),
        ToFieldCard(Field.NEW_YORK_AVENUE),
        ToFieldCard(Field.BOARDWALK),
        MoveBackwardCard(3),
    ]
    chance_cards = chance_cards + [NoopCard()] * (16 - len(chance_cards))
    rng.shuffle(chance_cards)
    return chance_cards

def init_community_cards():
    # print("Initializing community cards")
    community_cards = [
        GoToJailCard(),
        ToFieldCard(Field.START)
    ]
    community_cards = community_cards + [NoopCard()] * (16 - len(community_cards))
    rng.shuffle(community_cards)
    return community_cards

if __name__  == "__main__":

    parser = ArgumentParser(description="Simulates the player movement of the board game monopoly and shows the approximated propability density of the player's position.")
    parser.add_argument("-n", "--games", dest="num_games", default=1000)
    parser.add_argument("-k", "--moves", dest="num_moves", default=300)
    args = parser.parse_args()

    num_games = args.num_games
    num_moves = args.num_moves

    print("Simulating %d games with %d moves each." % (num_games, num_moves))
    
    num_fields = 40
    board = [0 for x in range(num_fields)]
    chance_fields = [Field.CHANCE_1, Field.CHANCE_2, Field.CHANCE_3]
    community_fields = [Field.COMMUNITY_1, Field.COMMUNITY_2, Field.COMMUNITY_3]

    i = 0
    for game in range(num_games):

        chance_cards = init_chance_cards()
        community_cards = init_community_cards()

        player = Player(num_fields)

        for move in range(num_moves):

            player.move()

            if player.pos in chance_fields:
                card = chance_cards.pop()
                card.execute(player)
                if len(chance_cards) <= 0:
                    chance_cards = init_chance_cards()

            if player.pos in community_fields:
                card = community_cards.pop()
                card.execute(player)
                if len(community_cards) <= 0:
                    community_cards = init_community_cards()

            board[player.pos] += 1
            i += 1

    board = [x / i for x in board]
    print(board)
    plt.bar(range(num_fields), board)
    plt.show()
