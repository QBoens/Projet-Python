import configparser

'''Création de l'objet fichier.ini'''
config = configparser.ConfigParser()

'''Ecriture section Monstre1'''
config['Monstre1'] = {
    'Nom':'Chokobo',
    'HP':100,
    'shield_point':30,
    'dodge':25,
    'parry':25,
    'critical':25,
    'damage_inf':1,
    'damage_sup':20,
    'level': 1
    }



with open('Fichier_conf.ini','w') as configfile:
    config.write(configfile)

config = configparser.ConfigParser()
config.read('Fichier_conf.ini')

for sections in config:
    if(sections !='DEFAULT'):
        for (key, value) in config.items(sections):
            print(key,':',value)
    





