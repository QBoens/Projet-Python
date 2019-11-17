from random import randint
import json

class Item():
    """
    Classe correspondant à tous les objets pouvant être utilisées en jeu
    """
    def __init__(self, nom, gold_price):
        self.name = nom
        self.gold_price = gold_price

    def get_name(self):
        """Renvoie le nom de l'objet"""
        return self.name

    def save(self):
        """Sauvegarde toutes les informations de l'objet"""
        data = {}
        for attr in self.__dict__.keys():
            if(attr != 'name'):
                data[attr] = self.__getattribute__(attr)
        data["Classe"] = type(self).__name__
        return data

    def load(self,nom,data):
        """Charge les données d'un objet appellé nom"""
        self.name = nom
        for attr in self.__dict__.keys():
            if attr != 'name':
                self.__setattr__(attr,data[attr])

class Equipments(Item):
    """
    Classe mêre des armes et des armures
    """
    def __init__(self, nom, gold_price, min_lvl):
        super().__init__( nom, gold_price)
        self.lvl = min_lvl

    def get_level(self):
        """Renvoie le niveau min pour s'équiper un équipement"""
        return self.lvl


class Weapon(Equipments):
    """
    Arme que peut utiliser le joueur
    Peut être récupéré sur les monstres
    """
    def __init__(self):
        """
        Lorsque la classe est appellée l'arme est crée de façon aléatoire
        """
        DATA_PATH = "Item/"
        file = open(DATA_PATH + "Data_weapon.json")
        data = json.load(file)

        list_weapons = list()
        for weapon in data:
            list_weapons.append(weapon)

        """On charge les données d'une arme aléatoire"""
        weapon_choice = randint(0, len(list_weapons) - 1)
        nom = list_weapons[weapon_choice]
        gold_price = data[list_weapons[weapon_choice]]["gold_price"]
        min_lvl = data[list_weapons[weapon_choice]]["min_lvl"]
        super().__init__(nom,gold_price,min_lvl)

        self.dg_bonus = data[list_weapons[weapon_choice]]["damage"]


    def set_level(self, lvl_joueur):
        """Adapte les statistiques de l'arme au niveau du joueur"""
        self.lvl = lvl_joueur
        for i in range(0, lvl_joueur):
            self.dg_bonus = int(self.dg_bonus * 1.5)

    def __str__(self):
        """Ce qui doit être affiché"""
        texte = "Nom :\t" + self.name + "\nlevel :\t" + str(self.lvl)
        texte += "\nDégats:\t" + str(self.dg_bonus) #+ "\nCarac bonus :\t" + str(self.car_bonus)
        texte += "\nPrix :\t" + str(self.gold_price)
        return texte


class Armor(Equipments):
    """
    Armure que peut porter un joueur
    Peut être récupéré sur les monstres
    """
    def __init__(self):
        """
        Lorsque la classe est appellée l'armure est crée de façon aléatoire
        """
        DATA_PATH = "Item/"
        file = open(DATA_PATH + "Data_armor.json")
        data = json.load(file)

        list_armors = list()
        for armor in data:
            list_armors.append(armor)

        """On charge les données d'une armure aléatoire"""
        armor_choice = randint(0, len(list_armors) - 1)
        nom = list_armors[armor_choice]
        gold_price = data[list_armors[armor_choice]]["gold_price"]
        min_lvl = data[list_armors[armor_choice]]["min_lvl"]
        super().__init__(nom,gold_price,min_lvl)

        self.df_bonus = data[list_armors[armor_choice]]["df_bonus"]
        self.type = data[list_armors[armor_choice]]["type"]

    def __str__(self):
        """Ce qui doit être affiché"""
        texte = "Name :\t\t" + self.name + "\nlevel :\t\t" + str(self.lvl)
        texte += "\nDefence:\t" + str(self.df_bonus)
        texte += "\nPrice :\t\t" + str(self.gold_price)
        return texte

    def set_level(self, lvl_joueur):
        """Adapte les statistiques de l'arme au niveau du joueur"""
        self.lvl = lvl_joueur
        for i in range(0, lvl_joueur):
            self.df_bonus = int(self.df_bonus * 1.4)


class Jewels(Equipments):
    def __init__(self, nom, gold_price, min_lvl, new_power, carac_bonus):
        super().__init__(nom,gold_price,min_lvl)
        self.power_bonus = new_power
        self.car_bonus = carac_bonus




class Consumables(Item):
    """
    Classe pour les objets que peut consommer le joueur
    """
    def __init__(self, nom, gold_price):
        super().__init__(nom, gold_price)

    def __str__(self):
        return self.name

class Potion(Consumables):
    """
    Potion que peut boire le joueur
    Elle peut lui rendre des points de HP ou de MP
    Elle peut aussi ajouter 5 points de statistique
    """
    def __init__(self,  nom, gold_price, joueur):
        super().__init__(nom,gold_price)

        """Choisi une statistique aléatoire"""
        list_of_stat = ["HP","MP","dodge","parry"]
        stat_index = randint(0, len(list_of_stat) - 1)
        self.stat = list_of_stat[stat_index]
        self.name = "Potion for " + list_of_stat[stat_index]

        """Une potion pour dodge ou parry augmente au maximum de 5 la statistique"""
        """Les potions de HP ou MP augmentent de 30 points la jauge"""
        if(1 < stat_index):
            self.value = 5
        else:
            self.value = 30

        """Pour les potions de HP ou de MP on met au niveau du joueur la valeur de points rendus"""
        if(stat_index <= 1):
            for i in range(0, joueur.stat.level):
                self.value = int(self.value * 1.6)



    