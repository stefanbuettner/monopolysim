import random as rng
from matplotlib import pyplot as plt
from matplotlib import colors
from enum import IntEnum
from argparse import ArgumentParser
import numpy as np

class FieldPos(IntEnum):
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
        if player.pos <= FieldPos.STATION_1:
            player.pos = FieldPos.STATION_1
        elif player.pos <= FieldPos.STATION_2:
            player.pos = FieldPos.STATION_2
        elif player.pos <= FieldPos.STATION_3:
            player.pos = FieldPos.STATION_3
        elif player.pos <= FieldPos.STATION_4:
            player.pos = FieldPos.STATION_4
        else:
            player.pos = FieldPos.STATION_1
    
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
        if player.pos <= FieldPos.ELECTRIC_COMPANY:
            player.pos = FieldPos.ELECTRIC_COMPANY
        elif player.pos <= FieldPos.WATER_WORKS:
            player.pos = FieldPos.WATER_WORKS
        else:
            player.pos = FieldPos.ELECTRIC_COMPANY
    
    def __repr__(self):
        return "ToNextSupplier"

class Player:

    def __init__(self, num_fields, buy_free=False):
        self.num_fields = num_fields
        self.pos = 0
        self.num_doubles = 0
        self.tries_for_doubles = 0
        self.buy_free = buy_free
        self.threw = 0

    def throw_dice(self):
        d1 = rng.randint(1,6)
        d2 = rng.randint(1,6)

        if d1 == d2:
            self.num_doubles += 1
        else:
            self.num_doubles = 0

        self.threw = d1 + d2
        return self.threw

    def go_to_jail(self):
        self.pos = FieldPos.JAIL
        self.num_doubles = 0
        self.tries_for_doubles = 0
    
    def move(self):
        steps = self.throw_dice()

        if FieldPos.JAIL == self.pos:
            self.tries_for_doubles += 1
            if not self.buy_free and self.tries_for_doubles < 3 and self.num_doubles <= 0:
                return self.pos
        else:
            if self.num_doubles >= 3:
                self.go_to_jail()

        return self.move_steps(steps)

    def move_steps(self, steps):
        
        self.pos = (self.pos + steps) % self.num_fields

        if FieldPos.GO_TO_JAIL == self.pos:
            self.go_to_jail()
        
        return self.pos


def init_chance_cards():
    # print("Initializing chance cards")
    chance_cards = [
        GoToJailCard(),
        ToNextStationCard(),
        ToNextStationCard(),
        ToNextSupplierCard(),
        ToFieldCard(FieldPos.START),
        ToFieldCard(FieldPos.STATION_1),
        ToFieldCard(FieldPos.PACIFIC_AVENUE),
        ToFieldCard(FieldPos.NEW_YORK_AVENUE),
        ToFieldCard(FieldPos.BOARDWALK),
        MoveBackwardCard(3),
    ]
    chance_cards = chance_cards + [NoopCard()] * (16 - len(chance_cards))
    rng.shuffle(chance_cards)
    return chance_cards

def init_community_cards():
    # print("Initializing community cards")
    community_cards = [
        GoToJailCard(),
        ToFieldCard(FieldPos.START)
    ]
    community_cards = community_cards + [NoopCard()] * (16 - len(community_cards))
    rng.shuffle(community_cards)
    return community_cards

class Field:
    def __init__(self, name, color, rent_0=0, rent_all=0, rent_1=0, rent_2=0, rent_3=0, rent_4=0, rent_hotel=0):
        self.name = name
        self.color = color
        self.rent_0 = rent_0
        self.rent_all = rent_all
        self.rent_1 = rent_1
        self.rent_2 = rent_2
        self.rent_3 = rent_3
        self.rent_4 = rent_4
        self.rent_hotel = rent_hotel
    
    def get_rent_0(self, dice):
        return self.rent_0
    
    def get_rent_all(self, dice):
        return self.rent_all
    
    def get_rent_1(self, dice):
        return self.rent_1
    
    def get_rent_2(self, dice):
        return self.rent_2
    
    def get_rent_3(self, dice):
        return self.rent_3
    
    def get_rent_4(self, dice):
        return self.rent_4
    
    def get_rent_hotel(self, dice):
        return self.rent_hotel

class SupplierField(Field):
    def __init__(self, name, color):
        super(SupplierField, self).__init__(name, color, 0)
    
    def get_rent_0(self, dice):
        return 4 * dice
    
    def get_rent_all(self, dice):
        return 10 * dice
    
    def get_rent_1(self, dice):
        return self.get_rent_all(dice)
    
    def get_rent_2(self, dice):
        return self.get_rent_1(dice)
    
    def get_rent_3(self, dice):
        return self.get_rent_3(dice)

    def get_rent_hotel(self, dice):
        return self.get_rent_4(dice)

class Station(Field):
    def __init__(self, name, color):
        super(Station, self).__init__(name, color)
    
    def get_rent_0(self, dice):
        return 25
    
    def get_rent_all(self, dice):
        return self.get_rent_0(dice)
    
    def get_rent_1(self, dice):
        return 50
    
    def get_rent_2(self, dice):
        return 100
    
    def get_rent_3(self, dice):
        return 200

    def get_rent_4(self, dice):
        return self.get_rent_3(dice)
    
    def get_rent_hotel(self, dice):
        return self.get_rent_4(dice)

if __name__  == "__main__":

    parser = ArgumentParser(description="Simulates the player movement of the board game monopoly and shows the approximated propability density of the player's position.")
    parser.add_argument("-n", "--games", dest="num_games", default=1000, type=int, help="Number of games to simulate.")
    parser.add_argument("-k", "--moves", dest="num_moves", default=300, type=int, help ="Number of moves per game.")
    parser.add_argument("--buy-free", dest="buy_free", action='store_true', help="The player always buys himself/herself out of jail.")
    args = parser.parse_args()

    num_games = args.num_games
    num_moves = args.num_moves

    print("Simulating %d games with %d moves each." % (num_games, num_moves))
    
    num_fields = 40
    board = np.zeros(num_fields)
    profit_0 = np.zeros(num_fields)
    chance_fields = [FieldPos.CHANCE_1, FieldPos.CHANCE_2, FieldPos.CHANCE_3]
    community_fields = [FieldPos.COMMUNITY_1, FieldPos.COMMUNITY_2, FieldPos.COMMUNITY_3]

    color = colors.get_named_colors_mapping()
    # Rents from 
    # http://www.math.yorku.ca/~zabrocki/math2042/Monopoly/prices.html
    board_fields = [
        Field("Start", color['springgreen']),
        Field("Mediterranean Avenue", color['sienna'], 2),
        Field("Community Chest", color['gray']),
        Field("Baltic Avenue", color['sienna'], 4),
        Field("Income Tax", color['gray']),
        Station("Reading Railroad", color['black']),
        Field("Oriental Avenue", color['skyblue'], 6),
        Field("Chance", color['gray']),
        Field("Vermont Avenue", color['skyblue'], 6),
        Field("Conneticut Avenue", color['skyblue'], 8),
        Field("Jail", color['springgreen']),
        Field("St. Charles Place", color['violet'], 10),
        SupplierField("Electric Company", color['gray']),
        Field("States Avenue", color['violet'], 10),
        Field("Virginia Avenue", color['violet'], 12),
        Station("Pennsylvania Railroad", color['black']),
        Field("St. James Place", color['darkorange'], 14),
        Field("Community Chest", color['gray']),
        Field("Tennessee Avenue", color['darkorange'], 14),
        Field("New York Avenue", color['darkorange'], 16),
        Field("Free Parking", color['springgreen']),
        Field("Kentucky Avenue", color['red'], 18),
        Field("Chance", color['gray']),
        Field("Indiana Avenue", color['red'], 18),
        Field("Illinois Avenue", color['red'], 20),
        Station("B. & O. Railroad", color['black']),
        Field("Atlantic Avenue", color['gold'], 22),
        Field("Ventnor Avenue", color['gold'], 22),
        SupplierField("Water Works", color['gray']),
        Field("Marvin Gardens", color['gold'], 24),
        Field("Go to Jail", color['springgreen']),
        Field("Pacific Avenue", color['green'], 26),
        Field("North Carolina Avenue", color['green'], 26),
        Field("Community Chest", color['gray']),
        Field("Pennsylvania Avenue", color['green'], 28),
        Station("Short Line", color['black']),
        Field("Chance", color['gray']),
        Field("Park Place", color['mediumblue'], 35),
        Field("Luxury Tax", color['gray']),
        Field("Broadwalk", color['mediumblue'], 50),
    ]

    i = 0
    for game in range(num_games):

        chance_cards = init_chance_cards()
        community_cards = init_community_cards()

        player = Player(num_fields, args.buy_free)

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
            profit_0[player.pos] += board_fields[player.pos].get_rent_0(player.threw)
            i += 1

    board = board / i
    profit_0 = profit_0 / i

    board_colors = [f.color for f in board_fields]
    field_names = [f.name for f in board_fields]
    rents_0 = np.array([f.rent_0 for f in board_fields]) * board

    x = np.arange(num_fields)

    scale = 5
    plt.xkcd()
    fig, ax = plt.subplots(figsize=(2 * scale, 1 * scale))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # prop = ax.bar(x, board, color=board_colors)
    # ax.set_title("Monopoly probability density distribution")
    # ax.set_ylabel("Probability")
    # ax.set_xlabel("FieldPos index")

    profit = ax.bar(x, profit_0, color=board_colors)
    ax.set_title("Monopoly's expected return per throw")
    ax.set_ylabel("Expected return")
    ax.set_xlabel("FieldPos index")

    plt.tight_layout()
    plt.show()
