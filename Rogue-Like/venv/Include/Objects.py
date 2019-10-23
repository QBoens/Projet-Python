
class Objects():
    def __init__(self, nom, gold_price):
        self.name = nom
        self.price = gold_price

    def get_name(self):
        return self.name

class Equipments(Objects):
    def __init__(self, nom, gold_price, min_lvl):
        Objects.__init__(self, nom, gold_price)
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



class Jevels(Equipments):
    def __init__(self, nom, gold_price, min_lvl, new_power, carac_bonus):
        Equipments.__init__(self,nom,gold_price,min_lvl)
        self.power_bonus = new_power
        self.car_bonus = carac_bonus
