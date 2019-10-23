from Include.Inventory import *

from random import randint

class Character():
    def __init__(self, nom):
        self.nom = nom
        self.inventory = Inventory(self)
        self.HP  = 100
        self.shield_point = 30
        self.dodge = randint(1, 101)
        self.parry = randint(1, 101)
        self.critical = randint(1, 101)
        self.MP = 100
        self.damage = (1,20)
        self.level = 1
        self.nextLevel = 10
        self.xpBar = self.nextLevel
        self.armor = 10

    def take_dmg(self, degats):
        self.HP -= degats

    def is_dead(self):
        if self.HP <= 0:
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
                degat = randin(self.damage[0], self.damage[1])

                degat += deg_weapon
                if self.is_critic():
                    degat *= 2
                degat -= cible.shield
                cible.take_dmg(degat)
            else:
                degat = 0

    def is_critic(self):
        chance = randint(1,101)
        if chance <= self.critical:
            return True
        else:
            return False

    def can_avoid(self):
        chance = randint(1, 101)
        if chance <= self.dodge:
            return True
        else:
            return False

    def can_parry(self):
        chance = randint(1, 101)
        if chance <= self.parry:
            return True
        else:
            return False

    def get_level(self):
        return self.level

    def __str__(self):
        texte = "Nom :\t\t" + self.nom + "\nLevel :\t\t" + str(self.level)
        texte += "\nType :\t\t" + type(self).__name__
        return texte

class Joueur(Character):
    def __init__(self, name):
        Character.__init__(self, name)

    def newLevel(self):
        self.HP +=  int(self.HP / 5)
        self.MP += int(self.MP / 5)
        self.level += 1
        self.nextLevel = 10 + pow(self.level, 2) * 10
        self.xpBar = self.nextLevel

        self.damage = (1,int(self.damage[1] * (1+1/4)))


    def addExp(self,xpPoint):

        self.xpBar -= xpPoint
        if(self.xpBar <= 0):
            surplus = self.xpBar

            self.newLevel()
            self.addExp(-surplus)
            return 0
        print("Your new level is ",self.level)


class Monster(Character):
    def __init__(self, nom):
        Character.__init__(self, nom)