class Inventory():
    def __init__(self):
        self.list_objects = list()
        self.amount_gold = 0
        self.slot_armor = dict()
        self.slot_armor = {1:"head", 2:"chest", 3:"pants", 4:"arms", 5:"legs"}
        self.slot_jewels = list()
        self.slot_weapon = list()

    def get_gold(self):
        return self.amount_gold

    def add_gold(self, quantity):
        self.amount_gold += quantity

    def spend_gold(self, quantity):
        self.amount_gold -= quantity

    def equip_armor(self, type, armor):
        self.list_objects.append(self.slot_armor.get(type))
        self.slot_armor[type] = armor