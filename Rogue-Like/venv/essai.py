from Include.Inventory import *
from Include.Objects import *
from Include.Character import *
from Include.Spells import *
from Include.Map import *


import json

def run():
    joueur = Joueur("Henri")
    monstre = Monster()
    armure = Armor()
    armure.lvl = 1

    joueur.inventory.add_object(armure)

    arme = Weapon()
    arme.lvl = 1

    arme2 = Weapon()
    arme.lvl = 1

    joueur.inventory.add_object(arme)
    joueur.inventory.add_object(arme2)

    #joueur.inventory.equip_armor(armure)
    #joueur.inventory.equip_weapon_G(arme)

    print(joueur.inventory.list_objects)
    joueur.inventory.equip_wa()
    print(joueur.inventory.list_objects)
    joueur.inventory.equip_wa()
    print(joueur.inventory.list_objects)
    return 0

run()
