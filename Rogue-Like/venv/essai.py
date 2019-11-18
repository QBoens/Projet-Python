from Include.Inventory import *
from Include.Objects import *
from Include.Character import *
from Include.Spells import *
from Include.Map import *


import json

def run():
    joueur = Joueur("Quentin")
    joueur.save()

    arme = Weapon()
    arme.lvl = 1

    arme2 = Weapon()
    arme2.lvl = 1

    joueur.inventory.add_object(arme)
    joueur.inventory.add_object(arme2)

    joueur.inventory.equip_weapon_R(arme2)

    joueur.inventory.equiped()
    return 0

    '''
    print("xpBar", joueur.stat.xpBar)
    print("Next Level", joueur.stat.nextLevel)
    print("Add exp :", joueur.stat.addExp)
    '''

    monstre = Monster()

    monstre.load("Fistiland",1)
    print("|",monstre.show(),"|")
    return  0
    armure = Armor()
    armure.lvl = 1

    joueur.inventory.add_object(armure)




    print(len(joueur.inventory.get_all_objects()))
    joueur.inventory.equip_wa()

    print(len(joueur.inventory.get_all_objects()))
    joueur.inventory.equip_wa()






    joueur.save()
    joueur2 = Joueur("")
    joueur2.load()
    return 0

run()
