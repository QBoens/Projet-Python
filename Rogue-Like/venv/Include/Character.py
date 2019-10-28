from Include.Inventory import *

from random import randint

class Character():
    def __init__(self, nom):
        self.nom = nom
        self.inventory = Inventory(self)
        self.stat = Statistic()

    def take_dmg(self, degats):
        self.stat.HP -= degats

    def is_dead(self):
        if self.stat.HP <= 0:
            return True
        else:
            return False

    def weapon_equip(self):
        return self.inventory.slot_weapon

    def attack_phy(self, cible):
        list_weapon = self.weapon_equip()
        deg_weapon = 0

        for weapon in list_weapon:
            deg_weapon += weapon.dg_bonus

        if not cible.can_avoid():
            if not cible.can_parry():
                degat = randin(self.stat.damage[0], self.stat.damage[1])

                degat += deg_weapon
                if self.is_critic():
                    degat *= 2
                degat -= cible.stat.shield
                cible.take_dmg(degat)
            else:
                degat = 0

    def is_critic(self):
        chance = randint(1,101)
        if chance <= self.stat.critical:
            return True
        else:
            return False

    def can_avoid(self):
        chance = randint(1, 101)
        if chance <= self.stat.dodge:
            return True
        else:
            return False

    def can_parry(self):
        chance = randint(1, 101)
        if chance <= self.stat.parry:
            return True
        else:
            return False

    def get_level(self):
        return self.stat.level

    def __str__(self):
        texte = "Nom :\t\t\t\t\t\t\t" + self.nom
        texte += "\nLevel :\t\t\t\t\t\t\t" + str(self.stat.level)
        texte += "\nType :\t\t\t\t\t\t\t" + type(self).__name__ + '\n'
        texte += str(self.stat)
        return texte

class Joueur(Character):
    def __init__(self, name):
        Character.__init__(self, name)

    def newLevel(self):
        self.stat.HP +=  int(self.stat.HP / 5)
        self.stat.MP += int(self.stat.MP / 5)
        self.stat.level += 1
        self.stat.nextLevel = 10 + pow(self.stat.level, 2) * 10
        self.stat.xpBar = self.stat.nextLevel

        self.stat.damage = (1,int(self.stat.damage[1] * (1+1/4)))


    def addExp(self,xpPoint):

        self.stat.xpBar -= xpPoint
        if(self.stat.xpBar <= 0):
            surplus = self.stat.xpBar

            self.newLevel()
            self.addExp(-surplus)
            return 0
        print("Your level is ",self.stat.level)


class Monster(Character):
    def __init__(self, nom):
        Character.__init__(self, nom)



class Statistic():
    def __init__(self):
        self.HP = 100
        self.MP = 100
        self.shield_point = 30
        self.dodge = randint(1, 101)
        self.parry = randint(1, 101)
        self.critical = randint(1, 101)
        self.damage = (1, 20)
        self.level = 1
        self.nextLevel = 10
        self.xpBar = self.nextLevel
        self.armor = 10
        self.games_finished = 0
        self.games_played = 0
        self.biome_disc = 0
        self.mons_kills = 0
        self.weapon_found = 0
        self.armor_found = 0

    def __str__(self):
        texte = ""
        texte += "HP : \t\t\t\t\t\t\t" + str(self.HP)
        texte += "\nMP : \t\t\t\t\t\t\t" + str(self.MP)
        texte += "\nShield points : \t\t\t\t" + str(self.shield_point)
        texte += "\nChance of dodging : \t\t\t" + str(self.dodge)
        texte += "\nChance of parry : \t\t\t\t" + str(self.parry)
        texte += "\nChance of critical : \t\t\t" +  str(self.critical)
        texte += "\nRange of damages : \t\t\t\t[" + str(self.damage[0]) + '-' + str(self.damage[1]) + ']'

        texte += "\n\n<<<<<STATISTICS>>>>>\n\n"
        texte += "Games played : \t\t\t" + str(self.games_played)
        texte += "\nGames finished : \t\t" + str(self.games_finished)
        texte += "\nBiome discovered : \t\t" + str(self.biome_disc)
        texte += "\nMonster killed : \t\t" + str(self.mons_kills)
        texte += "\nWeapon founded : \t\t" + str(self.weapon_found)
        texte += "\nArmor founded : \t\t" + str(self.armor_found)
        return texte

    def mons_killed(self,nb):
        self.mons_kills += nb

    def biome_found(self):
        self.biome_disc += 1

    def new_game(self):
        self.games_played += 1

    def game_finish(self):
        self.games_finished += 1

    def new_weapon(self):
        self.weapon_found += 1

    def new_armor(self):
        self.armor_found += 1