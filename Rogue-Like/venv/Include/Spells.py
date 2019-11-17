import json

class Spell_book():
    """
    Classe pour l'ensemble des techniques utilisables par le joueur
    """
    def __init__(self):
        """
        On charge la liste des sorts à partir des fichiers nécessaires
        """
        self.list_spells = list()


        """Chargement des attaques physiques"""
        SAVE_PATH = "Physical_attack/"
        file = open(SAVE_PATH + "Data_attack_phy.json")
        data = json.load(file)
        for section in data:
            self.list_spells.append(Physical(section,data[section]["degat"]))

        """Chargement des attaques magiques"""
        SAVE_PATH = "Magical_attack/"
        file = open(SAVE_PATH + "Data_attack_mag.json")
        data = json.load(file)
        for section in data:
            self.list_spells.append(Magical(section, data[section]["degat"], data[section]["MP_cost"]))


    def new_level(self):
        """Adapte la puissance et le coûts des techniques lorsque le joueur monte de niveau"""
        for spell in self.list_spells:
            spell.dmg = int(spell.dmg * 1.6)
            if(type(spell).__name__ == "Magical"):
                spell.MP_cost = int(spell.MP_cost * 1.6)

    def list_of_spells(self):
        """Affiche la liste des techniques maitrisées"""
        for spell in self.list_spells:
            print(spell,end='\n\n')

    def get_list_of_spells(self):
        """Renvoie la liste des techniques maitrisées"""
        return self.list_spells


class Spell():
    """Classe correspondant aux techinques"""
    def __str__(self):
        """Le texte à afficher"""
        texte = "Name :\t\t" + self.name + "\nType :\t\t" + type(self).__name__
        texte += "\nDamage :\t" + str(self.dmg)
        if(type(self).__name__ == "Magical"):
            texte +="\nMP cost :\t" + str(self.MP_cost)
        return texte

class Physical(Spell):
    """
    Les techniques physiques
    """
    def __init__(self, nom, degat):
        self.name = nom
        self.dmg = degat


class Magical(Spell):
    """
    Les techniques magiques
    """
    def __init__(self, nom, degat, cost):
        self.name = nom
        self.dmg = degat
        self.MP_cost = cost
