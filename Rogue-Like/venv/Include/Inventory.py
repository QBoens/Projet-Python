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

    def equip_weapon_R(self, weapon):
        if type(self.proprio).__name__ == "Joueur":
            if self.can_equip(weapon):
                if self.slot_weapon[1] == 0:
                    self.slot_weapon[1] = weapon
                    print("Arme équipée main droite :", weapon.name)
                else:
                    choix_valide = False
                    texte = "Voulez vous remplacer l'arme dans la main droite ?"
                    texte += "\no-oui\tn-non\n"

                    while not choix_valide:
                        replace = input(texte)
                        if(replace != 'o' and replace != 'n'):
                            print("Ce choix n'est pas valide")

                        elif(replace == "o"):
                            self.list_objects.append(self.slot_weapon[1])
                            self.slot_weapon[1] = weapon
                            print("Arme équipée main droite :", weapon.name)
                            choix_valide = True
                        else:
                            print("L'arme dans la main droite n'a pas été remplacée")
                            choix_valide = True
            else:
                print("Vous ne pouvez pas vous équipez de cette arme")
        else:
            self.slot_weapon[1] = weapon

    def equip_weapon_G(self, weapon):
        if type(self.proprio).__name__ == "Joueur":
            if self.can_equip(weapon):
                if self.slot_weapon[0] == 0:
                    self.slot_weapon[0] = weapon
                    print("Arme équipée main gauche :", weapon.name)
                else:
                    choix_valide = False
                    texte = "Voulez vous remplacer l'arme dans la main gauche ?"
                    texte += "\no-oui\tn-non\n"

                    while not choix_valide:
                        replace = input(texte)
                        if(replace != 'o' and replace != 'n'):
                            print("Ce choix n'est pas valide")

                        elif(replace == "o"):
                            self.list_objects.append(self.slot_weapon[0])
                            self.slot_weapon[0] = weapon
                            print("Arme équipée main gauche :", weapon.name)
                            choix_valide = True
                        else:
                            print("L'arme dans la main gauche n'a pas été remplacée")
                            choix_valide = True
        else:
            self.slot_weapon[0] = weapon



    def get_gold(self):
        return self.amount_gold

    def add_gold(self, quantity):
        self.amount_gold += quantity
        print("Vous avez maintenant :", self.get_gold(),"gold")

    def can_spend(self, quantity):
        if(quantity <= self.amount_gold):
            return True
        else:
            return False

    def spend_gold(self, quantity):
        if self.can_spend(quantity):
            self.amount_gold -= quantity
            print("Il vous reste :", self.get_gold(), "gold")
        else:
            print("Vous ne pouvez pas dépenser une telle somme!")
            print("Actuellement vous avez :", self.get_gold(), "gold")

    def equip_armor(self, armor):
        if type(self.proprio).__name__ == "Joueur":
            if self.can_equip(armor):
                if self.slot_armor[armor.type]=="aucune":

                    self.slot_armor[armor.type] = armor
            else:
                print(armor.name, " ne peut pas etre équipé")
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
        print("Armes équipées :")
        print("\tMain gauche : ", self.slot_weapon[0].get_name())
        print("\tMain droite : ", self.slot_weapon[1].get_name())