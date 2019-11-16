import json

from Include.Objects import *

class Inventory():
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



    def remove_object(self,object):
        for objet in self.list_objects:
            if object == objet:
                self.list_objects.remove(objet)

    def save(self):
        data = {"objet":self.save_list(),"weapon":self.save_weapon(),"armor":self.save_armor()}
        SAVE_PATH = "Save/"
        file = open(SAVE_PATH + "inventory.json", 'w')
        json.dump(data, file)
        file.close()

    def load(self):
        DATA_PATH = "Save/"
        file = open(DATA_PATH + "inventory.json", 'r')
        data = json.load(file)
        file.close()
        for elem in data:

            if elem == "objet":
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
                indice = 0
                for weapon_name in data[elem]:
                    print(weapon_name)

                    if(data[elem][weapon_name]==0):
                        self.slot_weapon[indice] = 0
                    else:
                        weapon = Weapon()

                        weapon.load(weapon_name,data[elem][weapon_name])
                        weapon.set_level(self.proprio.stat.level)
                        self.slot_weapon[indice] = weapon
                    indice += 1

            elif elem == "armor":
                for armor_name in data[elem]:
                    armor = Armor()
                    armor.load(armor_name,data[elem][armor_name])
                    self.equip_armor(armor)

    def save_weapon(self):
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
        data_armor_equiped = {}
        for armor in self.list_equiped_armor():
            try:
                data_armor_equiped[armor.name] = armor.save()
            except:
                a = 1
        return data_armor_equiped



    def save_list(self):
        data_all_objects = {}

        for objet in self.list_objects:
            data_all_objects[objet.name] = objet.save()

        return data_all_objects

    def equip_weapon_R(self, weapon):
        if type(self.proprio).__name__ == "Joueur":
            if self.can_equip(weapon):
                if self.slot_weapon[1] == 0:
                    self.slot_weapon[1] = weapon
                    self.remove_object(weapon)
                    print("Right hand's weapon:", weapon.name)
                else:
                    choix_valide = False
                    print(self.slot_weapon[1])
                    texte = "Do you want to change your right hand's weapon ?"
                    texte += "\ny-yes\tn-no\n"

                    while not choix_valide:
                        replace = input(texte)
                        if(replace != 'y' and replace != 'n'):
                            print("Ce choix n'est pas valide")

                        elif(replace == "y"):
                            self.add_object(self.slot_weapon[1])
                            self.slot_weapon[1] = weapon
                            print("Weapon in right hand's :", weapon.name)

                            self.remove_object(weapon)
                            choix_valide = True
                        else:
                            print("Right hand's weapon hasn't been replaced")
                            choix_valide = True
            else:
                print("You can't equip this weapon")
        else:
            self.slot_weapon[1] = weapon



    def equip_weapon_G(self, weapon):
        if type(self.proprio).__name__ == "Joueur":
            if self.can_equip(weapon):
                if self.slot_weapon[0] == 0:
                    self.slot_weapon[0] = weapon
                    self.remove_object(weapon)
                    print("Left hand's weapon :", weapon.name)
                else:
                    choix_valide = False
                    print(self.slot_weapon[0])
                    texte = "Do you want to change your left hand's weapon ?"
                    texte += "\ny-yes\tn-no\n"

                    while not choix_valide:
                        replace = input(texte)
                        if(replace != 'y' and replace != 'n'):
                            print("Choice no available")

                        elif(replace == "o"):
                            self.add_object(self.slot_weapon[1])
                            self.slot_weapon[0] = weapon
                            print("Left hand's weapon :", weapon.name)
                            self.remove_object(weapon)
                            choix_valide = True
                        else:
                            print("Left hand's weapon hasn't been replaced")
                            choix_valide = True
            else:
                print("You can't equip this weapon")
        else:
            self.slot_weapon[0] = weapon


    def list_of_weapon(self):
        list_weapon = list()
        for objet in self.list_objects:
            if(type(objet).__name__ == "Weapon"):
                list_weapon.append(objet)

        return list_weapon

    def list_of_armor(self):
        list_armor = list()
        for objet in self.list_objects:
            if (type(objet).__name__ == "Armor"):
                list_armor.append(objet)

        return list_armor

    def list_equipment_possible(self):
        list_equip = list()
        for weapon in self.list_of_weapon():
            list_equip.append(weapon)

        for armor in self.list_of_armor():
            list_equip.append(armor)
        return list_equip

    def equip_wa(self):
        if len(self.list_objects) == 0:
            return 0
        list_equip = self.list_equipment_possible()
        print("Vous pouvez vous équiper des objets suivant :")
        indice = 1
        choix_possibles = list()
        for equip in list_equip:
            print('-------------',indice,'-------------')
            print(equip)
            choix_possibles.append(str(indice))
            indice += 1

        choix_valide = False
        texte = "Quel equipement choisissez vous?"
        texte += "\nEntrez le numéro\n"

        while not choix_valide:
            choix = input(texte)
            if not choix in choix_possibles:
                print("Choix non valide")

            else:
                choix_valide = True
                if(type(list_equip[int(choix) - 1]).__name__ == "Armor"):
                    self.equip_armor(list_equip[int(choix) - 1])
                    return 0
                else:
                    arme_choisie = int(choix)
                    break

        choix_valide = False

        texte = "Main droite ou gauche?"
        texte += "\nG - Gauche\tD - Droite\n"

        while not choix_valide:
            choix = input(texte)
            if (choix.upper() != 'G' and choix.upper() != 'D'):
                print("Choix non valide")

            elif choix.upper() == 'D':
                self.equip_weapon_R(list_equip[arme_choisie - 1])
                break

            elif choix.upper() == 'G':
                self.equip_weapon_G(list_equip[arme_choisie - 1])
                break

    def add_object(self, object):
        self.list_objects.append(object)

    def get_gold(self):
        return self.amount_gold

    def add_gold(self, quantity):
        self.amount_gold += quantity
        if(type(self.proprio).__name__ == 'Joueur'):
            print("You have now :", self.get_gold(),"gold")

    def can_spend(self, quantity):
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
            print("You have no :", self.get_gold(), "gold")

    def equip_armor(self, armor):
        if type(self.proprio).__name__ == "Joueur":
            if self.can_equip(armor):
                if self.slot_armor[armor.type]=="aucune":
                    self.slot_armor[armor.type] = armor

                    print("You are now equiped with :", self.slot_armor[armor.type].name)
                    self.remove_object(armor)
                else:
                    print("Actually you have ",self.slot_armor[armor.type].name,"equiped")
                    choix_valide = False
                    texte = "Do you want to change this armor ?"
                    texte += "\ny-yes\tn-no\n"

                    while not choix_valide:
                        replace = input(texte)
                        if (replace != 'y' and replace != 'n'):
                            print("Ce choix n'est pas valide")

                        elif (replace == "y"):
                            self.slot_armor[armor.type] = armor
                            print("You are now equiped with :", self.slot_armor[armor.type].name)
                            self.remove_object(armor)
                            choix_valide = True
                        else:
                            print("Armor hasn't been replaced")
                            choix_valide = True
            else:
                print(armor.name, " can't be equiped")

        else:
            self.slot_armor[armor.type] = armor




    def can_equip(self,equipment):
        if self.proprio.get_level() >= equipment.get_level():
            return True
        else:
            return False

    def armor_equiped(self):
        for elem in self.slot_armor.keys():
            try:
                texte = self.slot_armor.get(elem).get_name()
            except AttributeError :
                texte = self.slot_armor.get(elem)
            print(texte)

    def weapon_equiped(self):
        print("Equiped weapons :")

        print("\tLeft Hand : ", self.slot_weapon[0])
        print("\tRight Hand : ", self.slot_weapon[1])

    def sell_object(self, object):
        self.list_objects.remove(object)
        print("You selt :",object)
        self.add_gold(object.price)

    def list_equiped_weapon(self):
        return self.slot_weapon

    def list_of_objects(self):
        print("List of objects:")
        for object in self.list_objects:
            print(object)

    def get_all_objects(self):
        return self.list_objects

    def get_armor_point(self):
        armor_point = 0
        for armor in self.list_equiped_armor():
            try:
                armor_point += armor.df_bonus
            except:
                continue
        return armor_point

    def list_equiped_armor(self):
        list_equip = list()

        for elem in self.slot_armor.keys():
            list_equip.append(self.slot_armor[elem])

        return list_equip