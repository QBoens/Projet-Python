from Include.Inventory import *
from Include.Objects import *
from Include.Character import *
from Include.Spells import *
from Include.Map import *


import json

def run():
    joueur = Joueur("Henri")
    monstre = Monster("Fistiland")
    print(joueur.spell_book.list_spells)
    #joueur.spell_book.new_level()
    '''
    potion_sacre = Potion("Potion soin sacrée", 600, joueur)
    potion_MP = Potion("Potion mana", 50, joueur)

    joueur.inventory.add_object(potion_MP)
    joueur.inventory.add_object(potion_sacre)
    joueur.inventory.list_of_objects()
    joueur.inventory.sell_object(potion_MP)
    joueur.inventory.list_of_objects()
    '''
    """
    monstre = Monster('Monstre1')
    print(monstre)
    merchant = Merchant("Merchant1")
    print(merchant)
    #merchant.discute_client(joueur)
    """
    #joueur.addExp(300000)
    return 0

run()