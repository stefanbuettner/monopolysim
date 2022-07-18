from common import *
from matplotlib import colors


def init_chance_cards():
    # print("Initializing chance cards")
    chance_cards = [
        GoToJailCard(),
        ToFieldCard(FieldPos.START),
        ToFieldCard(FieldPos.PACIFIC_AVENUE), # Wandereiche
        ToFieldCard(FieldPos.BOARDWALK), # Enthüllung der Wahrheit
        ToFieldCard(26), # Der verzauberte Wald
        ToFieldCard(34), # Tue das Richtige
        ToFieldCard(24), # der Ruf
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


class Player(PlayerBase):
    def move_steps(self, steps):
        super(Player, self).move_steps(steps)
        if self.pos in [FieldPos.STATION_1, FieldPos.STATION_2, FieldPos.STATION_3, FieldPos.STATION_4]:
           ToNextStationCard().execute(self)
        return self.pos


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
