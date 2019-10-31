from Include.Inventory import *
from Include.Objects import *
from Include.Character import *

def run():

    joueur = Joueur("Martin")
    '''
    potion_sacre = Potion("Potion soin sacrée", 600, joueur)
    potion_MP = Potion("Potion mana", 50, joueur)

    joueur.inventory.add_object(potion_MP)
    joueur.inventory.add_object(potion_sacre)
    joueur.inventory.list_of_objects()
    joueur.inventory.sell_object(potion_MP)
    joueur.inventory.list_of_objects()
    '''
    #monstre = Monster('Monstre1')

    merchant = Merchant('Merchant1')
    merchant.discute_client(joueur)
    return 0

run()