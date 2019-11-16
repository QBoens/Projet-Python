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


    def revive(self):
        self.stat.HP = self.stat.max_HP

    def print_HP(self):
        """Print Character HP"""
        print("HP :",self.stat.HP,"/",self.stat.max_HP)

    def print_MP(self):
        """Print Character MP"""
        print("MP :",self.stat.HP,"/",self.stat.max_MP)

    def get_HP(self):
        """Return Character HP"""
        return self.stat.HP
    
    def get_MaxHP(self):
        """Return Character MP"""
        return self.stat.max_HP

    def get_MaxMP(self):
        """Return Character max HP"""
        return self.stat.max_MP

    def get_MP(self):
        """Return Character max MP"""
        return self.stat.MP

    def get_level(self):
        """Return Character level"""
        return self.stat.level

    def take_dmg(self, degats):
        """HP points go downs by degats points"""
        self.stat.HP -= degats
        self.is_dead()

    def is_dead(self):
        """Check if character is dead"""
        if self.stat.HP <= 0:
            return True
        else:
            return False

    def weapon_equip(self):
        """Show Character equiped weapon"""
        return self.inventory.slot_weapon

    def attack_phy(self, attack, cible):
        """Character use a physical attack"""
        list_weapon = self.weapon_equip()
        deg_weapon = 0
        result = 3
        """
        On récupére les dégats qu'infligent les armes
        """
        for weapon in list_weapon:
            if not type(weapon).__name__== 'int':
                deg_weapon += weapon.dg_bonus

        if not cible.can_avoid():
            degat = randint(self.stat.damage[0], self.stat.damage[1])
            if (type(self).__name__ == 'Joueur'):
                degat += attack.dmg
            degat += deg_weapon
            if self.is_critic():
                result = 2
                degat *= 2

            if True:
            #if cible.can_parry():
                result = 1
                degat -= cible.stat.shield_point
                if (type(cible).__name__ == 'Joueur'):
                    degat -= self.inventory.get_armor_point()
                if(degat < 0):
                    degat = 0
            cible.take_dmg(degat)
        else:
            result = 0
        return result

    def attack_mag(self, spell, cible):
        degat = spell.dmg
        result = 3
        if not cible.can_avoid():
            if self.is_critic():
                result = 2
                degat *= 2

            if cible.can_parry():
                degat -= cible.stat.shield_point
                result = 1
                if(type(cible).__name__ == 'Joueur'):
                    degat -= self.inventory.get_armor_point()

            cible.take_dmg(degat)
        else:
            result = 0
        return result

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
        self.stat.max_HP =  int(self.stat.HP * 1.6)
        self.stat.HP = self.stat.max_HP
        self.stat.max_MP = int(self.stat.MP * 1.6)
        self.stat.MP = self.stat.max_MP
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
        self.inventory.remove_object(consumables_lists[choix_joueur - 1])
        save = self.stat.__getattribute__(use_conso.stat)
        self.stat.__setattr__(use_conso.stat, self.stat.__getattribute__(use_conso.stat) + use_conso.value)
        if(use_conso.stat == "HP"):
            if self.stat.HP > self.stat.max_HP :
                print("Surplus de HP")
                self.stat.HP = self.stat.max_HP

        elif(use_conso.stat == "MP"):
            if self.stat.MP > self.stat.max_MP :
                print("Surplus de MP")
                self.stat.MP = self.stat.max_MP
        
        elif(use_conso.stat == "dodge"):
            if self.stat.dodge > 99:
                print("Vous ne pouvez pas avoir une chance d'esquiver superieure a 99")
                self.stat.dodge = save

        elif(use_conso.stat == "parry"):
            if self.stat.parry > 99:
                print("Vous ne pouvez pas avoir une chance de parer superieure a 99")
                self.stat.parry = save

        print("Vous avez maintenant : ",self.stat.__getattribute__(use_conso.stat),use_conso.stat)

    def addExp(self,xpPoint):

        self.stat.xpBar -= xpPoint
        if(self.stat.xpBar <= 0):
            surplus = self.stat.xpBar

            self.newLevel()
            self.addExp(-surplus)
            return 0
        print("Your level is ",self.stat.level)

    def get_loot(self, monster):
        list_object = list()
        indice = 1
        for loot in monster.inventory.get_all_objects():
            print(indice,'-',loot.name)
            indice += 1
            list_object.append(loot)

        list_choice = list()
        for i in range(1, len(monster.inventory.get_all_objects()) + 1):
            list_choice.append(str(i))
        list_choice.append('passer')


        choix_valide = False
        while (not choix_valide):
            print("\nQuel objet voulez vous prendre?")
            choix_joueur = input("Ecrivez le numéro de l'objet ou écrivez passer si rien ne vous intéresse\n")
            choix_joueur = choix_joueur.lower()
            if (not list_choice.__contains__(choix_joueur)):
                print("Ce n'est pas un choix valide")
                continue

            if list_choice.__contains__(choix_joueur) and choix_joueur != "passer":
                break

            if choix_joueur == "passer":
                print("Au revoir")
                return 0

        self.inventory.add_object(list_object[int(choix_joueur) - 1])


class Monster(Character):
    def __init__(self):
        name = "Nouveau"
        super().__init__(name)
        self.set_stat()
        self.add_loot()

    def add_loot(self):
        for i in range(0, self.get_level()):
            self.inventory.add_gold(randint(20, 100))

        equip_number = randint(1,3)
        for i in range(0,equip_number):
            type_equip = randint(1,3)
            if(type_equip == 1):
                object = Weapon()
            elif(type_equip == 2):
                object = Armor()
            else:
                object = Potion("new",100,self)
            try:
                object.set_level(self.get_level())
            except:
                a = 1
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
        self.max_HP = 100
        self.HP = self.max_HP
        self.max_MP = 100
        self.MP = self.max_MP
        self.shield_point = 5
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
        texte += "HP : " + str(self.HP) + "/" + str(self.max_HP)
        texte += "\nMP : " + str(self.MP) + "/" + str(self.max_MP)
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
