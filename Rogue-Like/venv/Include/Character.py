from Include.Inventory import *
from Include.Objects import *
from Include.Spells import *
from os import listdir
from random import randint

import json

class Character():
    def __init__(self, nom):
        self.nom = nom
        self.inventory = Inventory(self)
        self.stat = Statistic(type(self).__name__)

    def get_level(self):
        return self.stat.level

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
                degat = randint(self.stat.damage[0], self.stat.damage[1])

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

        texte = "Nom : " + self.nom
        texte += "\nLevel : " + str(self.stat.level)
        texte += "\nType : " + type(self).__name__ + '\n'
        texte += str(self.stat)

        return texte



class Joueur(Character):
    def __init__(self, name):
        super().__init__(name)
        self.spell_book = Spell_book()

    def save(self):
        data={"nom":self.nom,"stat":self.stat.save()}
        self.inventory.save()
        SAVE_PATH = "Save/"
        file = open(SAVE_PATH+"player.json",'w')
        json.dump(data,file)

    def load(self):

        DATA_PATH = "Save/"
        file = open(DATA_PATH+"player.json",'r')
        data = json.load(file)
        self.nom = data["nom"]
        self.stat.load(data["stat"])
        self.inventory.load()


    def newLevel(self):
        self.stat.HP =  int(self.stat.HP * 1.6)
        self.stat.MP = int(self.stat.MP * 1.6)
        self.stat.level += 1
        self.stat.nextLevel = pow(self.stat.level, 2) * 10
        self.stat.xpBar = self.stat.nextLevel
        self.stat.shield_point = int(self.stat.shield_point * 1.5)
        self.stat.damage = (1,int(self.stat.damage[1] * 1.6))

        self.spell_book.new_level()

    def use_consumable(self):
        if(len(self.inventory.list_objects) == 0):
            print("You don't have anything in your inventory")
            return 0

        consumables_lists = list()
        id_conso = 0
        for object in self.inventory.list_objects:
            if(type(object).__name__ == "Potion" or type(object).__name__ == "Food"):
                consumables_lists.append(object)

        print("Here is the list of consumables :")
        for conso in consumables_lists:
            print(str(id_conso + 1), ' - ', conso)
            id_conso += 1

        choix_valide = False

        while(not choix_valide):
            print("Which object do you choose ?")
            choix_joueur = input("Give a number between 1 and "+str(len(consumables_lists))+"\n")
            choix_joueur = int(choix_joueur)
            if(choix_joueur < 1 or len(consumables_lists) < choix_joueur):
                print("You didn't write an authorized value")
            else:
                choix_valide = True

        use_conso = consumables_lists[choix_joueur - 1]
        print(use_conso.stat)
        self.stat.__setattr__(use_conso.stat, self.stat.__getattribute__(use_conso.stat) + use_conso.value)

    def addExp(self,xpPoint):

        self.stat.xpBar -= xpPoint
        if(self.stat.xpBar <= 0):
            surplus = self.stat.xpBar

            self.newLevel()
            self.addExp(-surplus)
            return 0
        print("Your level is ",self.stat.level)


class Monster(Character):
    def __init__(self):
        name = "Nouveau"
        super().__init__(name)
        self.set_stat()
        self.inventory.add_gold(randint(20,100))

    def add_loot(self):
        for i in range(0, self.get_level()):
            self.inventory.add_gold(randint(20, 100))

        equip_number = randint(1,3)
        for i in range(0,equip_number):
            type_equip = randint(1,4)
            if(type_equip == 1):
                object = Weapon()
            else:
                object = Armor()
            object.set_level(self.get_level())
            self.inventory.add_object(object)

    def load(self, nom, level_player):
        DATA_PATH = "Monster/"
        file = open(DATA_PATH + "Data_monstre.json")
        data = json.load(file)

        self.nom = nom

        list_attr = self.stat.__dict__.items()
        for attr in list_attr:
            if (attr[0] == "level"):
                break

            if(attr[0] != "damage"):
                self.stat.__setattr__(attr[0], data[nom][attr[0]])
            else:
                dmg_inf = data[nom]["damage_inf"]
                dmg_sup = data[nom]["damage_sup"]
                self.stat.__setattr__(attr[0], (dmg_inf, dmg_sup))

        self.set_level(level_player)
        
    def set_stat(self):
        DATA_PATH = "Monster/"
        file = open(DATA_PATH + "Data_monstre.json")
        data = json.load(file)

        list_monsters = list()
        for monstre in data:
            list_monsters.append(monstre)

        monster_choice = randint(0,len(list_monsters) - 1)

        self.nom = list_monsters[monster_choice]

        list_attr = self.stat.__dict__.items()
        for attr in list_attr:
            if (attr[0] == "level"):
                break

            if(attr[0] != "damage"):
                self.stat.__setattr__(attr[0], data[list_monsters[monster_choice]][attr[0]])
            else:
                dmg_inf = data[list_monsters[monster_choice]]["damage_inf"]
                dmg_sup = data[list_monsters[monster_choice]]["damage_sup"]
                self.stat.__setattr__(attr[0], (dmg_inf, dmg_sup))

    def set_level(self,joueur_level):
        self.stat.level = joueur_level
        for i in range(0, joueur_level):
            self.stat.HP = int(self.stat.HP * 1.6)
            self.stat.MP = int(self.stat.MP * 1.4)
            self.stat.shield_point += int(self.stat.shield_point / 4)
            self.stat.damage = (1, int(self.stat.damage[1] * (1.6)))


class Merchant(Character):
    def __init__(self, section):
        config = configparser.ConfigParser()
        config.read("NPC/Fichier_conf_NPC.ini")
        super().__init__( config.get(section, 'nom'))
        self.set_stat(section, "NPC/Fichier_conf_NPC.ini")
        self.inventory.add_gold(5000)
        self.init_list_objects()

    def discute_client(self,joueur):
        print("Bonjour bienvenu à mon échoppe")
        print("Je possède les objets suivants :")
        num_objet = 1
        list_choice = ['1','2','3','quitter']
        for items in self.inventory.list_objects:
            print(num_objet, "-", items)
            num_objet += 1

        choix_valide = False
        while(not choix_valide):
            print("\nQuel objet voulez vous achetez?")
            choix_joueur = input("Ecrivez le numéro de l'objet ou écrivez quitter si rien ne vous intéresse\n")
            choix_joueur = choix_joueur.lower()
            if(not list_choice.__contains__(choix_joueur)):
                print("Ce n'est pas un choix valide")
                continue

            if(choix_joueur == "quitter"):
                print("Au revoir")
                break

class Statistic():
    def __init__(self,type_proprio):
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
        self.bonus_stat = list()
        self.armor = 10
        self.games_finished = 0
        self.games_played = 0
        self.biome_disc = 0
        self.mons_kills = 0
        self.weapon_found = 0
        self.armor_found = 0
        self.type_proprio = type_proprio

    def save(self):
        data ={}
        for attr in self.__dict__.keys():
            data[attr] = self.__getattribute__(attr)
        return data

    def load(self, data):
        for attr in self.__dict__.keys():
            self.__setattr__(attr,data[attr])




    def __str__(self):
        texte = ""
        texte += "HP : " + str(self.HP)
        texte += "\nMP : " + str(self.MP)
        texte += "\nShield points : " + str(self.shield_point)
        texte += "\nChance of dodging : " + str(self.dodge)
        texte += "\nChance of parry : " + str(self.parry)
        texte += "\nChance of critical : " + str(self.critical)
        texte += "\nRange of damages : [" + str(self.damage[0]) + '-' + str(self.damage[1]) + ']'
        if(self.type_proprio == 'Joueur'):
            texte += "\n\n<<<<<STATISTICS>>>>>\n\n"
            texte += "Games played : " + str(self.games_played)
            texte += "\nGames finished : " + str(self.games_finished)
            texte += "\nBiome discovered : " + str(self.biome_disc)
            texte += "\nMonster killed : " + str(self.mons_kills)
            texte += "\nWeapon founded : " + str(self.weapon_found)
            texte += "\nArmor founded : " + str(self.armor_found)

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

    def add_bonus(self, stat, value):
        if (len(self.bonus_stat) == 0):
            self.bonus_stat.append((stat,value))
        else :
            return 0
