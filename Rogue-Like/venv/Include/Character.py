from Include.Inventory import *

from random import randint

class Character():
    def __init__(self, nom):
        self.nom = nom
        self.inventory = Inventory()
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

    def attack(self, cible):



class Joueur(Character):
    def __init__(self, name):
        Character.__init(self, name)

    def newLevel(self):
        self.HP +=  self.HP / 5
        self.MP += self.MP / 5
        self.level += 1
        self.nextLevel += self.nextLevel
        self.xpBar = self.nextLevel

    def addExp(self,xpPoint):
        self.xpBar -= xpPoint
        if(xpBar <= 0):
            surplus = self.xpBar
            self.newLevel()
            self.xpBar = self.nextLevel + surplus

class Monster(Character):
    def __init__(self, nom):
        Character.__init__(self, nom)