import json

class Spell_book():
    def __init__(self):
        self.list_spells = list()

        SAVE_PATH = "Physical_attack/"
        file = open(SAVE_PATH + "Data_attack_phy.json")
        data = json.load(file)
        for section in data:
            self.list_spells.append(Physical(section,data[section]["degat"]))

        SAVE_PATH = "Magical_attack/"
        file = open(SAVE_PATH + "Data_attack_mag.json")
        data = json.load(file)
        for section in data:
            self.list_spells.append(Magical(section, data[section]["degat"]))


    def new_level(self):
        for spell in self.list_spells:
            spell.dmg

    def list_spells(self):


class Spell():
    def __str__(self):
        texte = "Nom :\t\t" + self.name + "\nType :\t\t" + type(self).__name__
        texte += "\nDégats :\t" + str(self.dmg)
        return texte

class Physical(Spell):
    def __init__(self, nom, degat):
        self.name = nom
        self.dmg = degat

class Magical(Spell):
    def __init__(self, nom, degat):
        self.name = nom
        self.dmg = degat