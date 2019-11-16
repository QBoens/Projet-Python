from Include.Inventory import *
from Include.Objects import *
from Include.Character import *
from Include.Spells import *
from Include.Map import *


import json

def run():
    joueur = Joueur("Henri")
    monstre = Monster()
    joueur.addExp(5000)
    armure = Armor()
    armure2 = Armor()

    arme = Weapon()
    arme2 = Weapon()
    arme2.set_level(joueur.get_level())

    arme.lvl = 1
    arme2.lvl = 1


    Potion1 = Potion("Nouveau",12,joueur)
    Potion2 = Potion("Nouveau", 12, joueur)
    Potion3 = Potion("Nouveau", 12, joueur)

    joueur.inventory.add_object(Potion1)
    #joueur.inventory.add_object(armure)

    armure.set_level(joueur.get_level())
    armure2.set_level(joueur.get_level())
    armure.lvl = 1
    armure2.lvl = 1
    joueur.inventory.equip_armor(armure)
    joueur.inventory.equip_armor(armure2)
    """
    joueur.inventory.add_object(arme)
    joueur.inventory.add_object(arme2)
    """
    """
    joueur.inventory.equip_weapon_R(arme)
    joueur.inventory.equip_weapon_G(arme2)
    """
    joueur.inventory.add_object(Potion3)
    joueur.save()

    joueur2 = Joueur("Nouveau")
    joueur2.load()

    joueur2.stat.HP = 1
    joueur2.stat.parry = 96
    joueur2.stat.dodge = 96
    joueur2.use_consumable()
    return 0

run()
