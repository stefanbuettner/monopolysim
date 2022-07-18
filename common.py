import random as rng
from enum import IntEnum

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

class PlayerBase:

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
        return self.pos
    
    def move(self):
        steps = self.throw_dice()

        if FieldPos.JAIL == self.pos:
            self.tries_for_doubles += 1
            if not self.buy_free and self.tries_for_doubles < 3 and self.num_doubles <= 0:
                return self.pos
        else:
            if self.num_doubles >= 3:
                return self.go_to_jail()

        return self.move_steps(steps)

    def move_steps(self, steps):
        
        self.pos = (self.pos + steps) % self.num_fields

        if FieldPos.GO_TO_JAIL == self.pos:
            return self.go_to_jail()
        
        return self.pos

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