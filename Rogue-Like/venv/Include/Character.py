from Include.Inventory import *
from Include.Objects import *
from Include.Spells import *
from os import listdir
from random import randint

import json

class Character():
    """
    Classe qui permet de créer les différents personnages du jeu
    """
    def __init__(self, nom):
        self.nom = nom
        self.inventory = Inventory(self)
        self.stat = Statistic(type(self).__name__)


    def revive(self):
        self.stat.HP = self.stat.max_HP

    def print_HP(self):
        """Affiche Character HP"""
        print("HP :",self.stat.HP,"/",self.stat.max_HP)

    def print_MP(self):
        """Affiche Character MP"""
        print("MP :",self.stat.MP,"/",self.stat.max_MP)

    def get_HP(self):
        """Renvoie Character HP"""
        return self.stat.HP
    
    def get_MaxHP(self):
        """Renvoie Character MP"""
        return self.stat.max_HP

    def get_MaxMP(self):
        """Renvoie Character max HP"""
        return self.stat.max_MP

    def get_MP(self):
        """Renvoie Character max MP"""
        return self.stat.MP

    def get_level(self):
        """Renvoie Character level"""
        return self.stat.level

    def take_dmg(self, degats):
        """Les points d'HP diminues de degats"""
        self.stat.HP -= degats
        self.is_dead()

    def is_dead(self):
        """Vérifie si Character est mort"""
        if self.stat.HP <= 0:
            return True
        else:
            return False

    def weapon_equip(self):
        """Affiche les armes équipées de Character"""
        return self.inventory.slot_weapon

    def attack_phy(self, attack, cible):
        """Character utilise une attaque physique"""
        list_weapon = self.weapon_equip()
        deg_weapon = 0
        result = 3
        """
        On récupére les dégats qu'infligent les armes
        """
        for weapon in list_weapon:
            if not type(weapon).__name__== 'int':
                deg_weapon += weapon.dg_bonus

        """On vérifie si la cible esquive"""
        if not cible.can_avoid():
            degat = randint(self.stat.damage[0], self.stat.damage[1])

            """Seul le joueur possède un panel d'attaque différentes"""
            if (type(self).__name__ == 'Joueur'):
                degat += attack.dmg
            degat += deg_weapon

            """On vérifie si l'attaque est critique"""
            if self.is_critic():
                result = 2
                degat *= 2

            """On vérifie si la cible pare"""
            if cible.can_parry():
                result = 1
                degat -= int(cible.stat.shield_point * 0.7)

                """Le joueur a un bonus d'armure"""
                if (type(cible).__name__ == 'Joueur'):
                    degat -= int(cible.inventory.get_armor_point() * 0.7)

                """Cas où l'armure peut encaisser plus que les dégats"""
                if(degat < 0):
                    degat = 0
            cible.take_dmg(degat)
        else:
            result = 0
        return result

    def attack_mag(self, spell, cible):
        """Character utilise une attaque magique"""
        if not self.can_use_spell(spell):
            print("here")
            return -1

        self.stat.MP -= spell.MP_cost
        self.print_MP()
        degat = spell.dmg
        result = 3

        """On vérifie si la cible esquive"""
        if not cible.can_avoid():

            """On vérifie si l'attaque est critique"""
            if self.is_critic():
                result = 2
                degat *= 2

            """On vérifie si la cible pare"""
            if cible.can_parry():
                degat -= int(cible.stat.shield_point * 0.7)
                print(cible.nom,"pare")
                result = 1
                if(type(cible).__name__ == 'Joueur'):
                    degat -= self.inventory.get_armor_point()

            cible.take_dmg(degat)
        else:
            print(cible.nom, "pare")
            result = 0
        return result


    def can_use_spell(self, spell):
        """Vérifie si Character peut lancer un sort"""
        if(self.stat.MP < spell.MP_cost):
            return False
        else:
            return True

    def is_critic(self):
        """Vérifie si Character fait un coup critique"""
        chance = randint(1,101)
        if chance <= self.stat.critical:
            return True
        else:
            return False

    def can_avoid(self):
        """Vérifie si Character réussi à esquiver"""
        chance = randint(1, 101)
        if chance <= self.stat.dodge:
            return True
        else:
            return False

    def can_parry(self):
        """Vérifie si Character pare une attaque"""
        chance = randint(1, 101)
        if chance <= self.stat.parry:
            return True
        else:
            return False

    def get_level(self):
        """Renvoie le level de Character"""
        return self.stat.level

    def __str__(self):
        """Renvoie le texte à afficher"""
        texte = "Nom : " + self.nom
        texte += "\nLevel : " + str(self.stat.level)
        texte += "\nType : " + type(self).__name__ + '\n'
        texte += str(self.stat)

        return texte



class Joueur(Character):
    """
    Classe qui correspond au joueur
    """
    def __init__(self, name):
        super().__init__(name)
        self.spell_book = Spell_book()


    def save(self):
        """Permet de sauvegarder les informations de Joueur"""
        data={"nom":self.nom,"stat":self.stat.save()}
        self.inventory.save()
        SAVE_PATH = "Save/"
        file = open(SAVE_PATH+"player.json",'w')
        json.dump(data,file)
        file.close()

    def load(self):
        """Permet de charger les informations de la Dernière sauvegarde"""
        DATA_PATH = "Save/"
        file = open(DATA_PATH+"player.json",'r')
        data = json.load(file)
        self.nom = data["nom"]
        self.stat.load(data["stat"])
        self.inventory.load()
        file.close()

    def newLevel(self):
        """Appelle les fonctions nécessaires pour que les statistiques et les sorts s'adaptent au niveau du Joueur"""
        self.stat.newLevel()
        self.spell_book.new_level()

    def use_consumable(self):
        """Permet d'utiliser une potion"""

        """Le Joueur n'a rien dans son inventaire"""
        if(len(self.inventory.list_objects) == 0):
            print("You don't have anything in your inventory")
            return 0

        consumables_lists = list()
        id_conso = 0

        """On récupére la liste des consommables"""
        for object in self.inventory.list_objects:
            if(type(object).__name__ == "Potion" or type(object).__name__ == "Food"):
                consumables_lists.append(object)

        """Le joueur n'a pas de potion"""
        if (len(consumables_lists) == 0):
            print("You don't have any consumables")
            return 0

        """Affichage de la liste des potions possibles"""
        print("Here is the list of consumables :")
        for conso in consumables_lists:
            print(str(id_conso + 1), ' - ', conso)
            id_conso += 1

        """On demande au joueur de choisir une potion"""
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

        """On vérifie que la potion consommée n'augemente pas trop la statistique concernée"""
        if(use_conso.stat == "HP"): #Cas des HP
            if self.stat.HP > self.stat.max_HP :
                print("Surplus de HP")
                self.stat.HP = self.stat.max_HP


        elif(use_conso.stat == "MP"): #Cas des MP
            if self.stat.MP > self.stat.max_MP :
                print("Surplus de MP")
                self.stat.MP = self.stat.max_MP
        
        elif(use_conso.stat == "dodge"): #Cas de dodge
            if self.stat.dodge > 99:
                print("Vous ne pouvez pas avoir une chance d'esquiver superieure a 99")
                self.stat.dodge = save

        elif(use_conso.stat == "parry"): #Cas de parry
            if self.stat.parry > 99:
                print("Vous ne pouvez pas avoir une chance de parer superieure a 99")
                self.stat.parry = save

        print("Vous avez maintenant : ",self.stat.__getattribute__(use_conso.stat),use_conso.stat)

    def getExp(self):
        """Ajouter à l'utilisateur les points d'expérience nécessaires"""
        self.addExp(self.stat.addExp)

    def addExp(self,xpPoint):
        """Ajoute xpPoint à xpBar"""
        self.stat.xpBar -= xpPoint

        """Si xpBar est <= 0 le joueur va passer un niveau"""
        if(self.stat.xpBar <= 0):
            surplus = self.stat.xpBar

            self.newLevel()

            '''Il peut y avoir un surplus d'xpPoint'''
            self.addExp(-surplus)
            return 0
        print("Your level is ",self.stat.level)

    def get_loot(self, monster):
        """
        Récupére l'équipement que possède monster
        Il ne peut reprendre qu'un seul équipement
        L'or que possède monster est automatiquement ajouté
        """
        self.inventory.add_gold(monster.inventory.get_gold())

        """Afficher les objets de monster"""
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

        """Choix du joueur"""
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
    """
    Classe des monstres qu'affronte le joueur
    """
    def __init__(self):
        name = "Nouveau"
        super().__init__(name)
        self.set_stat()
        self.add_loot()
        self.display = ""


    def add_loot(self):
        """
        Ajoute le loot que laisse Monster
        """

        """Ajoute de l'or suivant le niveau du joueur"""
        for i in range(0, self.get_level()):
            self.inventory.add_gold(randint(20, 100))

        equip_number = randint(1,3)
        """Ajoute entre 1 et 3 objets à l'inventaire de Monster"""
        for i in range(0,equip_number):
            type_equip = randint(1,3)


            if(type_equip == 1):    #Ajoute une arme
                object = Weapon()
            elif(type_equip == 2):  #Ajoute une armure
                object = Armor()
            else:                   #Ajoute une potion
                object = Potion("new",100,self)

            try:                    #Met au niveau du joueur l'équipement
                object.set_level(self.get_level())
            except:
                a = 1
            self.inventory.add_object(object)

    def show(self):
        return self.display

    def load(self, nom, level_player):
        """
        Charge les données d'un monstre s'appelant nom
        Puis met ses statistiques au niveau du joueur
        """

        DATA_PATH = "Monster/"
        file = open(DATA_PATH + "Data_monstre.json")
        data = json.load(file)
        file.close()

        self.nom = nom

        list_attr = self.stat.__dict__.items()

        """Extrait les informations du fichier"""
        for attr in list_attr:
            if (attr[0] == "level"):
                break

            if(attr[0] != "damage"):
                self.stat.__setattr__(attr[0], data[nom][attr[0]])
            else:
                dmg_inf = data[nom]["damage_inf"]
                dmg_sup = data[nom]["damage_sup"]
                self.stat.__setattr__(attr[0], (dmg_inf, dmg_sup))

        """Appelle la fonction de mise à niveau de Monster"""
        self.set_level(level_player)

        
    def set_stat(self):
        """
        Utilisée dans la fonction init permet de créer un monstre aléatoire
        """
        DATA_PATH = "Monster/"
        file = open(DATA_PATH + "Data_monstre.json")
        data = json.load(file)
        file.close()

        list_monsters = list()
        """Récupére la liste des monstres dans le fichier"""
        for monstre in data:
            list_monsters.append(monstre)

        """Choisi un monstre au hasard"""
        monster_choice = randint(0,len(list_monsters) - 1)

        self.nom = list_monsters[monster_choice]

        """Récupére les informations"""
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
        """Met les statistiques de Monster au même niveau que le joueur"""
        self.stat.level = joueur_level
        for i in range(0, joueur_level):
            self.stat.HP = int(self.stat.HP * 1.6)
            self.stat.max_HP = int(self.stat.max_HP * 1.6)
            self.stat.MP = int(self.stat.MP * 1.4)
            self.stat.max_MP = int(self.stat.max_MP * 1.4)
            self.stat.shield_point += int(self.stat.shield_point / 4)
            self.stat.damage = (1, int(self.stat.damage[1] * (1.6)))


class Merchant(Character):
    """
    Classe du marchant qui peut vendre au joueur des objets
    N'a pas été implémentée dans le jeu
    """
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
    """
    Classe qui contient toutes les statistiques d'un Character
    """
    def __init__(self,type_proprio):
        self.max_HP = 100
        self.HP = self.max_HP
        self.max_MP = 100
        self.MP = self.max_MP
        self.dodge = randint(1, 101)
        self.shield_point = 10
        self.dodge = randint(1, 25)
        self.parry = randint(25, 75)
        self.critical = randint(1, 101)
        self.damage = (1, 20)
        self.level = 1
        self.nextLevel = 10
        self.addExp = 10
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
        """
        Sauvegarde les statistiques
        :return: dictionnaire avec les différentes informations
        """
        data ={}
        for attr in self.__dict__.keys():
            data[attr] = self.__getattribute__(attr)
        return data

    def load(self, data):
        """Charge les statistiques via les infos fournies dans data"""
        for attr in self.__dict__.keys():
            self.__setattr__(attr,data[attr])

    def newLevel(self):
        """
        Montée de niveau
        Les statistiques sont augmentées
        """
        self.max_HP = int(self.max_HP * 1.6)
        self.HP = self.max_HP
        self.max_MP = int(self.max_MP * 1.6)
        self.MP = self.max_MP
        self.level += 1
        self.nextLevel = pow(self.level, 2) * 10
        self.xpBar = self.nextLevel
        self.addExp = int(pow(self.level, 2) * 10 * 0.4)
        self.shield_point = int(self.shield_point * 1.5)
        self.damage = (1, int(self.damage[1] * 1.6))

    def __str__(self):
        """Le texte à afficher"""
        texte = ""
        texte += "HP : " + str(self.HP) + "/" + str(self.max_HP)
        texte += "\nMP : " + str(self.MP) + "/" + str(self.max_MP)
        texte += "\nShield points : " + str(self.shield_point)
        texte += "\nChance of dodging : " + str(self.dodge)
        texte += "\nChance of parry : " + str(self.parry)
        texte += "\nChance of critical : " + str(self.critical)
        texte += "\nRange of damages : [" + str(self.damage[0]) + '-' + str(self.damage[1]) + ']'

        """Si le propriétaire est un Joueur on affiche certaine informations"""
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
        """Augmente la statistique nombre de monstres tués"""
        self.mons_kills += nb

    def biome_found(self):
        """Augmente la statistique nombre de salles visitées"""
        self.biome_disc += 1

    def new_game(self):
        """Augmente la statistique nombre de jeux réalisés"""
        self.games_played += 1

    def game_finish(self):
        """Augmente la statistique nombre de donjons finis"""
        self.games_finished += 1

    def new_weapon(self):
        """Augmente la statistique nombre d'armes trouvées"""
        self.weapon_found += 1

    def new_armor(self):
        """Augmente la statistique nombre d'armures trouvées"""
        self.armor_found += 1

    def add_bonus(self, stat, value):
        if (len(self.bonus_stat) == 0):
            self.bonus_stat.append((stat,value))
        else :
            return 0
