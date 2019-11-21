import json

from Include.Objects import *

class Inventory():
    """
    Classe qui correspond à l'inventaire d'un Character
    """
    def __init__(self, proprio):
        self.proprio = proprio
        self.list_objects = list()
        self.amount_gold = 0
        self.slot_armor = dict()
        self.slot_armor = \
            {1:"aucune", #head
             2:"aucune", #chest
             3:"aucune", #pants
             4:"aucune", #arms
             5:"aucune"} #legs
        self.slot_jewels = list()
        self.slot_weapon = list()
        self.slot_weapon = [0,0]
        self.max_size = 10


    def equiped(self):
        self.weapon_equiped()
        self.armor_equiped()

    def remove_object(self,object):
        """Supprime object de la liste des objets"""
        if not object in self.list_objects:
            return 0
        for objet in self.list_objects:
            if object == objet:
                self.list_objects.remove(objet)

    def save(self):
        """Sauvegarde toutes les infos de l'inventaire"""
        data = {"objet":self.save_list(),"weapon":self.save_weapon(),"armor":self.save_armor()}
        SAVE_PATH = "Save/"
        file = open(SAVE_PATH + "inventory.json", 'w')
        json.dump(data, file)
        file.close()

    def load(self):
        """Charge toutes les infos sauvegardées dans le fichier"""
        DATA_PATH = "Save/"
        file = open(DATA_PATH + "inventory.json", 'r')
        data = json.load(file)
        file.close()
        for elem in data:

            if elem == "objet":
                """Chargement de self.list_object"""
                for objet_name in data[elem]:
                    if(data[elem][objet_name]["Classe"] == "Potion"):
                        objet = Potion("Nom",0,self.proprio)
                        objet.load(objet_name,data[elem][objet_name])
                        self.add_object(objet)
                    elif (data[elem][objet_name]["Classe"] == "Armor"):
                        objet = Armor()
                        objet.load(objet_name,data[elem][objet_name])
                        objet.set_level(self.proprio.stat.level)
                        self.add_object(objet)
                    elif (data[elem][objet_name]["Classe"] == "Weapon"):
                        objet = Weapon()
                        objet.load(objet_name,data[elem][objet_name])
                        objet.set_level(self.proprio.stat.level)
                        self.add_object(objet)

            elif elem == "weapon":
                """Chargement de self.slot_weapon"""
                indice = 0
                for weapon_name in data[elem]:

                    if(data[elem][weapon_name]==0):
                        self.slot_weapon[indice] = 0
                    else:
                        weapon = Weapon()

                        weapon.load(weapon_name,data[elem][weapon_name])
                        weapon.set_level(self.proprio.stat.level)
                        self.slot_weapon[indice] = weapon
                    indice += 1

            elif elem == "armor":
                """Chargement de self.slot_armor"""
                for armor_name in data[elem]:
                    armor = Armor()
                    armor.load(armor_name,data[elem][armor_name])
                    self.equip_armor(armor)

    def save_weapon(self):
        """Sauvegarde les infors sur les armes équipées"""
        data_weapon_equip={}
        indice_weapon = 0
        for weapon in self.list_equiped_weapon():
            if(weapon != 0):
                data_weapon_equip[weapon.name] = weapon.save()
            else:
                if(indice_weapon == 0):
                    data_weapon_equip["Gauche"] = 0
                else:
                    data_weapon_equip["Droite"] = 0
            indice_weapon +=1
        return data_weapon_equip

    def save_armor(self):
        """Sauvegarde les armures équipées"""
        data_armor_equiped = {}
        for armor in self.list_equiped_armor():
            try:
                data_armor_equiped[armor.name] = armor.save()
            except:
                a = 1
        return data_armor_equiped



    def save_list(self):
        """Sauvegarde la liste des objets de l'inventaire"""
        data_all_objects = {}

        for objet in self.list_objects:
            data_all_objects[objet.name] = objet.save()

        return data_all_objects

    def equip_weapon_R(self, weapon):
        """Equipe weapon dans la main droite"""

        if type(self.proprio).__name__ == "Joueur":
            """Vérifie si le joueur peut s'équiper de cette arme"""
            if self.can_equip(weapon):
                if self.slot_weapon[1] == 0:    #Cas où il n'y a pas d'arme équipée
                    self.slot_weapon[1] = weapon
                    self.remove_object(weapon)
                    print("Right hand's weapon:", weapon.name)
                else:                           #Cas où une arme est équipée

                    """Demande à l'utilisateur s'il veut changer son arme"""
                    choix_valide = False
                    print(self.slot_weapon[1])
                    texte = "Do you want to change your right hand's weapon ?"
                    texte += "\ny-yes\tn-no\n"

                    while not choix_valide:
                        replace = input(texte)
                        if(replace.lower() != 'y' and replace.lower() != 'n'):
                            print("Ce choix n'est pas valide")

                        elif(replace.lower() == "y"):   #L'utilisateur veut changer d'arme
                            """L'ancienne arme va dans self.list_objects"""
                            self.add_object(self.slot_weapon[1])
                            self.slot_weapon[1] = weapon
                            print("Weapon in right hand's :", weapon.name)

                            self.remove_object(weapon)
                            choix_valide = True
                        else:                   #L'utilisateur ne veut pas changer d'arme

                            print("Right hand's weapon hasn't been replaced")
                            choix_valide = True
            else:   #L'utilisateur ne peut pas s'équiper de l'arme
                print("You can't equip this weapon")
        else:
            self.slot_weapon[1] = weapon



    def equip_weapon_G(self, weapon):
        """Equipe weapon dans la main gauche"""
        if type(self.proprio).__name__ == "Joueur":
            """Vérifie si le joueur peut s'équiper de cette arme"""
            if self.can_equip(weapon):
                if self.slot_weapon[0] == 0:    #Cas où il n'y a pas d'arme équipée
                    self.slot_weapon[0] = weapon
                    self.remove_object(weapon)
                    print("Left hand's weapon :", weapon.name)
                else:                           #Cas où une arme est équipée
                    """Demande à l'utilisateur s'il veut changer son arme"""
                    choix_valide = False
                    print(self.slot_weapon[0])
                    texte = "Do you want to change your left hand's weapon ?"
                    texte += "\ny-yes\tn-no\n"

                    while not choix_valide:
                        replace = input(texte)
                        if(replace.lower() != 'y' and replace.lower() != 'n'):
                            print("Choice no available")

                        elif(replace.lower() == "y"):   #L'utilisateur veut changer d'arme
                            """L'ancienne arme va dans self.list_objects"""
                            self.add_object(self.slot_weapon[1])
                            self.slot_weapon[0] = weapon
                            print("Left hand's weapon :", weapon.name)
                            self.remove_object(weapon)
                            choix_valide = True
                        else:                           #L'utilisateur ne veut pas changer d'arme
                            print("Left hand's weapon hasn't been replaced")
                            choix_valide = True
            else:   #L'utilisateur ne peut pas s'équiper de l'arme
                print("You can't equip this weapon")
        else:
            self.slot_weapon[0] = weapon


    def list_of_weapon(self):
        """Renvoie la liste des armes possédées"""
        list_weapon = list()
        for objet in self.list_objects:
            if(type(objet).__name__ == "Weapon"):
                list_weapon.append(objet)

        return list_weapon

    def list_of_armor(self):
        """Renvoie la liste des armures possédées"""
        list_armor = list()
        for objet in self.list_objects:
            if (type(objet).__name__ == "Armor"):
                list_armor.append(objet)

        return list_armor

    def list_equipment_possible(self):
        """Renvoie la liste des objets pouvant être équipés"""
        list_equip = list()

        """Récupére la liste des armes possédées"""
        for weapon in self.list_of_weapon():
            list_equip.append(weapon)

        """Récupére la liste des armures possédées"""
        for armor in self.list_of_armor():
            list_equip.append(armor)
        return list_equip

    def equip_wa(self):
        """Fonction pour équiper un objet possédé"""

        self.equiped()

        if len(self.list_objects) == 0:
            return 0

        list_equip = self.list_equipment_possible()
        if len(list_equip) == 0:
            return 0

        print("Vous pouvez vous équiper des objets suivant :")
        indice = 1
        choix_possibles = list()

        for equip in list_equip:
            print('-------------',indice,'-------------')
            print(equip)
            choix_possibles.append(str(indice))
            indice += 1
        choix_possibles.append("quit")
        choix_valide = False
        texte = "Which item do you want to equip?"
        texte += "\nWrite the number, or quit"

        while not choix_valide:
            choix = input(texte)
            if not choix.lower() in choix_possibles:
                print("Invalide choice")

            else:
                choix_valide = True
                if choix.lower() == "quit":
                    return 0
                if(type(list_equip[int(choix) - 1]).__name__ == "Armor"):
                    self.equip_armor(list_equip[int(choix) - 1])
                    return 0
                else:
                    arme_choisie = int(choix)
                    break

        choix_valide = False

        texte = "Right or left hand?"
        texte += "\nL - Left\tR - Right\n"

        while not choix_valide:
            choix = input(texte)
            if (choix.upper() != 'L' and choix.upper() != 'R'):
                print("Invalid choice")

            elif choix.upper() == 'R':
                self.equip_weapon_R(list_equip[arme_choisie - 1])
                break

            elif choix.upper() == 'L':
                self.equip_weapon_G(list_equip[arme_choisie - 1])
                break

    def add_object(self, object):
        """Ajoute object à la liste des objets"""
        self.list_objects.append(object)

    def get_gold(self):
        """Renvoie les gold possédés"""
        return self.amount_gold

    def add_gold(self, quantity):
        """Ajoute quantity à aux gold possédés"""
        self.amount_gold += quantity
        if(type(self.proprio).__name__ == 'Joueur'):
            print("You have now :", self.get_gold(),"gold")

    def can_spend(self, quantity):
        """Vérifie si Character peut dépenser quantity de gold"""
        if(quantity <= self.amount_gold):
            return True
        else:
            return False

    def spend_gold(self, quantity):
        if self.can_spend(quantity):
            self.amount_gold -= quantity
            print("You still have :", self.get_gold(), "gold")
        else:
            print("You can't spend that much!")
            print("You have now :", self.get_gold(), "gold")

    def equip_armor(self, armor):
        """Equipe armor à Character"""

        """Vérifie si le propriétaire de l'inventaire est un joueur"""
        if type(self.proprio).__name__ == "Joueur":
            """Vérifie si le joueur peut s'équiper de l'armure"""
            if self.can_equip(armor):


                if self.slot_armor[armor.type]=="aucune":   #Cas où il n'y a pas d'armure équipée sur le slot d'armure
                    self.slot_armor[armor.type] = armor

                    print("You are now equiped with :", self.slot_armor[armor.type].name)
                    self.remove_object(armor)
                else:                                       #Cas où il y a une armure équipée sur le slot d'armure
                    print("Actually you have ",self.slot_armor[armor.type].name,"equiped")

                    """Demande au joueur s'il veut changer d'armure"""
                    choix_valide = False
                    texte = "Do you want to change this armor ?"
                    texte += "\ny-yes\tn-no\n"

                    while not choix_valide:
                        replace = input(texte)
                        if (replace != 'y' and replace != 'n'):
                            print("Ce choix n'est pas valide")

                        elif (replace == "y"):      #Cas où le joueur veut remplacer l'armure
                            self.slot_armor[armor.type] = armor
                            print("You are now equiped with :", self.slot_armor[armor.type].name)
                            self.remove_object(armor)
                            choix_valide = True
                        else:                       #Cas où le joueur ne veut pas remplacer l'armure
                            print("Armor hasn't been replaced")
                            choix_valide = True
            else:
                """L'armure ne peut pas être équipée"""
                print(armor.name, " can't be equiped")

        else:
            self.slot_armor[armor.type] = armor




    def can_equip(self,equipment):
        """Vérifie que le propriétaire peut s'équiper de cet equipment"""
        if self.proprio.get_level() >= equipment.get_level():
            return True
        else:
            return False

    def armor_equiped(self):
        """Affiche la liste des armures équipées"""
        print("Armors equiped")
        for elem in self.slot_armor.keys():
            try:
                texte = self.slot_armor.get(elem).get_name()
            except AttributeError :
                texte = ""
            print(texte)

    def weapon_equiped(self):
        """Affiche els armes équipées"""
        print("Equiped weapons :")
        if self.slot_weapon[0] == 0:
            texte = "aucune"
        else:
            texte = ""+ str(self.slot_weapon[0])
        print("Left Hand : \n", texte)

        if self.slot_weapon[1] == 0:
            texte = "aucune"
        else:
            texte = ""+ str(self.slot_weapon[1])
        print("Right Hand : \n", texte)

    def sell_object(self, object):
        """Permet de vendre object"""
        self.list_objects.remove(object)
        print("You selt :",object)
        self.add_gold(object.price)

    def list_equiped_weapon(self):
        """Renvoie la liste des armes équipées"""
        return self.slot_weapon

    def list_of_objects(self):
        """Affiche la liste des objets possédées"""
        print("List of objects:")
        for object in self.list_objects:
            print(object)

    def get_all_objects(self):
        """Renvoie la liste des objets possédées"""
        return self.list_objects

    def get_armor_point(self):
        """Récupére les points de défense fournies par l'armure"""
        armor_point = 0
        for armor in self.list_equiped_armor():
            try:
                armor_point += armor.df_bonus
            except:
                continue
        return armor_point

    def list_equiped_armor(self):
        """Renvoie la liste des armures équipes"""
        list_equip = list()

        for elem in self.slot_armor.keys():
            list_equip.append(self.slot_armor[elem])

        return list_equip