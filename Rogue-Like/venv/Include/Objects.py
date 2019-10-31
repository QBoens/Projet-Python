from random import randint

class Item():
    def __init__(self, nom, gold_price):
        self.name = nom
        self.price = gold_price

    def get_name(self):
        return self.name

class Equipments(Item):
    def __init__(self, nom, gold_price, min_lvl):
        Item.__init__(self, nom, gold_price)
        self.lvl = min_lvl
        self.slot = -1

    def get_level(self):
        return self.lvl


class Weapon(Equipments):
    def __init__(self, nom, gold_price, min_lvl, damage, carac_bonus):
        Equipments.__init__(self,nom,gold_price,min_lvl)
        self.dg_bonus = damage
        self.car_bonus = carac_bonus

    def __str__(self):
        texte = "Nom :\t" + self.name + "\nlevel :\t" + str(self.lvl)
        texte += "\nDégats:\t" + str(self.dg_bonus) + "\nCarac bonus :\t" + str(self.car_bonus)
        texte += "\nPrix :\t" + str(self.price)
        return texte


class Armor(Equipments):
    def __init__(self, nom, gold_price, min_lvl, defence, carac_bonus, type):
        Equipments.__init__(self,nom,gold_price,min_lvl)
        self.df_bonus = defence
        self.car_bonus = carac_bonus
        self.type = type

    def __str__(self):
        texte = "Nom :\t" + self.name + "\nlevel :\t" + str(self.lvl)
        texte += "\nDégats:\t" + str(self.df_bonus) + "\nCarac bonus :\t" + str(self.car_bonus)
        texte += "\nPrix :\t" + str(self.price)
        return texte


class Jewels(Equipments):
    def __init__(self, nom, gold_price, min_lvl, new_power, carac_bonus):
        Equipments.__init__(self,nom,gold_price,min_lvl)
        self.power_bonus = new_power
        self.car_bonus = carac_bonus




class Consomables(Item):
    def __init__(self, nom, gold_price):
        Item.__init__(self, nom, gold_price)

    def __str__(self):
        return self.name

class Potion(Consomables):
    def __init__(self,  nom, gold_price, joueur):
        Consomables.__init__(self, nom, gold_price)

        list_of_stat = ["HP","MP","dodge","parry"]
        stat_index = randint(0, len(list_of_stat) - 1)
        self.stat = list_of_stat[stat_index]
        self.value = 30



    def set_value(self, joueur):
        return 0