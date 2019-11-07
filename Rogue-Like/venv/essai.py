from Include.Inventory import *
from Include.Objects import *
from Include.Character import *
from Include.Spells import *
from Include.Map import *


import json

def run():
    joueur = Joueur("Henri")
    monstre = Monster("Nouveau")
    joueur.addExp(4000)

    armure = Armor()
    armure2 = armure
    armure.set_level(joueur.get_level())

    arme = Weapon()
    arme2 = Weapon()
    arme2.set_level(joueur.get_level())

    arme2.lvl = 1


    Potion1 = Potion("Nouveau",12,joueur)
    Potion2 = Potion("Nouveau", 12, joueur)
    Potion3 = Potion("Nouveau", 12, joueur)

    joueur.inventory.add_object(Potion1)
    joueur.inventory.add_object(armure)

    joueur.inventory.equip_armor(armure)
    joueur.inventory.equip_armor(armure2)

    joueur.inventory.add_object(arme)
    joueur.inventory.add_object(arme2)

    #joueur.inventory.equip_weapon_R(arme)
    joueur.inventory.equip_weapon_G(arme2)

    joueur.inventory.add_object(Potion3)
    joueur.save()
    return 0

run()