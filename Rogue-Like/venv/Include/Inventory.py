import json

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

    def save(self):
        data = {"objet":self.save_list(),"weapon":self.save_weapon(),"armor":{}}
        SAVE_PATH = "Save/"
        file = open(SAVE_PATH + "inventory.json", 'w')
        json.dump(data, file)

    def save_weapon(self):
        data_weapon_equip={}
        indice_weapon = 0
        for weapon in self.list_equiped_weapon():
            print(weapon)
            if(weapon != 0):
                data_weapon_equip[weapon.name] = weapon.save()
            else:
                if(indice_weapon == 0):
                    data_weapon_equip["Gauche"] = 0
                else:
                    data_weapon_equip["Droite"] = 0
            indice_weapon +=1
        return data_weapon_equip

    def save_list(self):
        data_all_objects = {}

        for objet in self.list_objects:
            '''data_object = {}
            for attr in objet.__dict__.keys():
                if (attr !="name"):
                    data_object[attr] = objet.__getattribute__(attr)'''

            data_all_objects[objet.name] = objet.save()

        return data_all_objects

    def equip_weapon_R(self, weapon):
        if type(self.proprio).__name__ == "Joueur":
            if self.can_equip(weapon):
                if self.slot_weapon[1] == 0:
                    self.slot_weapon[1] = weapon
                    print("Right hand's weaopn:", weapon.name)
                else:
                    choix_valide = False
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
                    print("Left hand's weaopn :", weapon.name)
                else:
                    choix_valide = False
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
                            choix_valide = True
                        else:
                            print("Left hand's weapon hasn't been replaced")
                            choix_valide = True
            else:
                print("You can't equip this weapon")
        else:
            self.slot_weapon[0] = weapon

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
        print("\tLeft Hand : ", self.slot_weapon[0].get_name())
        print("\tRight Hand : ", self.slot_weapon[1].get_name())

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

