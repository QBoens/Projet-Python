import configparser

class Spell_book():
    def __init__(self):
        self.list_spells = list()

        file = "Physical_attack/Fichier_conf_Phys.ini"
        config = configparser.ConfigParser()
        config.read(file)
        list_Phys = config.sections()

        file = "Magical_attack/Fichier_conf_Magic.ini"
        config = configparser.ConfigParser()
        config.read(file)
        list_Mag = config.sections()

        for section in list_Phys:
            self.list_spells.append(Physical(section))

        for section in list_Mag:
            self.list_spells.append(Magical(section))

    def new_level(self):
        for spell in self.list_spells:
            print(spell)


class Spell():
    def __str__(self):
        texte = "Nom :\t\t" + self.name + "\nType :\t\t" + type(self).__name__
        texte += "\nDégats :\t" + str(self.dmg) + "\nCible(s) :\t" + str(self.target)
        return texte

class Physical(Spell):
    def __init__(self, section):
        file = "Physical_attack/Fichier_conf_Phys.ini"
        config = configparser.ConfigParser()
        config.read(file)
        self.name = config.get(section, 'nom')
        self.dmg = config.get(section, 'dmg')
        self.target = config.get(section, 'target')

class Magical(Spell):
    def __init__(self, section):
        file = "Magical_attack/Fichier_conf_Magic.ini"
        config = configparser.ConfigParser()
        config.read(file)
        self.name = config.get(section, 'nom')
        self.dmg = config.get(section, 'dmg')
        self.target = config.get(section, 'target')