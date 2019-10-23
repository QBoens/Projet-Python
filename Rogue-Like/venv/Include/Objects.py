
class Objects():
    def __init__(self, nom, gold_price):
        self.name = nom
        self.price = gold_price

class Equipments(Objects):
    def __init__(self, nom, gold_price, min_lvl):
        Objects.__init__(self, nom, gold_price)
        self.lvl = min_lvl
        self.slot = -1

    def __str__(self):
        return self.name + " level : " + str(self.lvl)

class Weapon(Equipments):
    def __init__(self, nom, gold_price, min_lvl, damage, carac_bonus):
        Equipments.__init__(self,nom,gold_price,min_lvl)
        self.dg_bonus = damage
        self.car_bonus = carac_bonus


class Armor(Equipments):
    def __init__(self, nom, gold_price, min_lvl, defence, carac_bonus):
        Equipments.__init__(self,nom,gold_price,min_lvl)
        self.df_bonus = defence
        self.car_bonus = carac_bonus

class Jevels(Equipments):
    def __init__(self, nom, gold_price, min_lvl, new_power, carac_bonus):
        Equipments.__init__(self,nom,gold_price,min_lvl)
        self.power_bonus = new_power
        self.car_bonus = carac_bonus
