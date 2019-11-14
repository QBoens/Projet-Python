from random import randint
import json
class Item():
    def __init__(self, nom, gold_price):
        self.name = nom
        self.gold_price = gold_price

    def get_name(self):
        return self.name

    def save(self):
        data = {}
        for attr in self.__dict__.keys():
            if(attr != 'name'):
                data[attr] = self.__getattribute__(attr)
        data["Classe"] = type(self).__name__
        return data

    def load(self,nom,data):
        self.name = nom
        for attr in self.__dict__.keys():
            if attr != 'name':
                self.__setattr__(attr,data[attr])

class Equipments(Item):
    def __init__(self, nom, gold_price, min_lvl):
        super().__init__( nom, gold_price)
        self.lvl = min_lvl

    def get_level(self):
        return self.lvl


class Weapon(Equipments):
    def __init__(self):
        DATA_PATH = "Item/"
        file = open(DATA_PATH + "Data_weapon.json")
        data = json.load(file)

        list_weapons = list()
        for weapon in data:
            list_weapons.append(weapon)

        weapon_choice = randint(0, len(list_weapons) - 1)
        nom = list_weapons[weapon_choice]
        gold_price = data[list_weapons[weapon_choice]]["gold_price"]
        min_lvl = data[list_weapons[weapon_choice]]["min_lvl"]
        super().__init__(nom,gold_price,min_lvl)

        self.dg_bonus = data[list_weapons[weapon_choice]]["damage"]


    def set_level(self, lvl_joueur):
        self.lvl = lvl_joueur + 2
        for i in range(0, lvl_joueur):
            self.dg_bonus = int(self.dg_bonus * 1.5)

    def __str__(self):
        texte = "Nom :\t" + self.name + "\nlevel :\t" + str(self.lvl)
        texte += "\nDégats:\t" + str(self.dg_bonus) #+ "\nCarac bonus :\t" + str(self.car_bonus)
        texte += "\nPrix :\t" + str(self.gold_price)
        return texte


class Armor(Equipments):
    def __init__(self):
        DATA_PATH = "Item/"
        file = open(DATA_PATH + "Data_armor.json")
        data = json.load(file)

        list_armors = list()
        for armor in data:
            list_armors.append(armor)

        armor_choice = randint(0, len(list_armors) - 1)
        nom = list_armors[armor_choice]
        gold_price = data[list_armors[armor_choice]]["gold_price"]
        min_lvl = data[list_armors[armor_choice]]["min_lvl"]
        super().__init__(nom,gold_price,min_lvl)

        self.df_bonus = data[list_armors[armor_choice]]["df_bonus"]
        self.type = data[list_armors[armor_choice]]["type"]

    def __str__(self):
        texte = "Name :\t\t" + self.name + "\nlevel :\t\t" + str(self.lvl)
        texte += "\nDefence:\t" + str(self.df_bonus)
        texte += "\nPrice :\t\t" + str(self.gold_price)
        return texte

    def set_level(self, lvl_joueur):
        self.lvl = lvl_joueur + 2
        for i in range(0, lvl_joueur):
            self.df_bonus = int(self.df_bonus * 1.4)


class Jewels(Equipments):
    def __init__(self, nom, gold_price, min_lvl, new_power, carac_bonus):
        super().__init__(nom,gold_price,min_lvl)
        self.power_bonus = new_power
        self.car_bonus = carac_bonus




class Consumables(Item):
    def __init__(self, nom, gold_price):
        super().__init__(nom, gold_price)

    def __str__(self):
        return self.name

class Potion(Consumables):
    def __init__(self,  nom, gold_price, joueur):
        super().__init__(nom,gold_price)
        list_of_stat = ["HP","MP","dodge","parry"]
        stat_index = randint(0, len(list_of_stat) - 1)
        self.stat = list_of_stat[stat_index]
        self.name = "Potion for " + list_of_stat[stat_index]
        if(1 < stat_index):
            self.value = 5
        else:
            self.value = 30

        if(stat_index <= 1):
            for i in range(0, joueur.stat.level):
                self.value = int(self.value * 1.6)



    