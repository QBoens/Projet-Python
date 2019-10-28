from Include.Inventory import *
from Include.Objects import *
from Include.Character import *

def run():

    joueur = Joueur("Martin")
    joueur.addExp(3000000)

    joueur.stat.mons_killed(123)
    joueur.stat.new_game()
    joueur.stat.game_finish()
    joueur.stat.biome_found()
    joueur.stat.new_weapon()
    joueur.stat.new_armor()
    print(joueur)

    """
    arme = Weapon("Massue",14,1,25,[])
    arme2 = Weapon("Massue sacrée",14,1,25,[])


    #joueur.inventory.equip_weapon_R(arme)
    joueur.inventory.equip_weapon_R(arme2)

    joueur.inventory.equip_weapon_G(arme)
    #joueur.inventory.equip_weapon_G(arme2)

    liste_armure = Armor("Plastron lourd",13,1,34,[],2)
    joueur.inventory.equip_armor(liste_armure)

    joueur.inventory.weapon_equiped()
    """

    return 0

run()