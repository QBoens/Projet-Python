from Include.Map import Map
from Include.Character import Joueur
import os

SAVE_PATH = "./Save"
TITLE = " ______    _______  _______  __   __  _______    _______  __    _  _______ \n|    _ |  |       ||       ||  | |  ||       |  |       ||  |  | ||       |\n|   | ||  |   _   ||    ___||  | |  ||    ___|  |   _   ||   |_| ||    ___|\n|   |_||_ |  | |  ||   | __ |  |_|  ||   |___   |  | |  ||       ||   |___ \n|    __  ||  |_|  ||   ||  ||       ||    ___|  |  |_|  ||  _    ||    ___|\n|   |  | ||       ||   |_| ||       ||   |___   |       || | |   ||   |___ \n|___|  |_||_______||_______||_______||_______|  |_______||_|  |__||_______|"

if __name__ == "__main__":
    os.system("cls")
    player = Joueur("Link")
    map = Map(player)
    Input = ""
    print(TITLE+"\n\n\n1: New Game\n2: Load Game\n3: Quit")
    while(Input != "3"):
        Input = input("\n> ")
        os.system("cls")
        if(Input == "1"):
            map.Generate()
            map.Play()
            map.Save()
            os.system("cls")
            Input = ""
            print(TITLE+"\n\n\n1: New Game\n2: Load Game\n3: Quit")
        elif(Input == "2"):
            list_dir = os.listdir(SAVE_PATH)
            Player_load = False
            Map_load = False
            for i in range(0,len(list_dir)):
                if(list_dir[i] == "player.json"):
                    Player_load = True
                if(list_dir[i] == "map.json"):
                    Map_load = True
            if(Player_load == True and Map_load == True):
                player.load()
                map = Map(player)
                map.Load()
                map.Play()
                map.Save()
                os.system("cls")
                Input = ""
                print(TITLE+"\n\n\n1: New Game\n2: Load Game\n3: Quit")
            else:
                Input = ""
                print(TITLE+"\n\n\n1: New Game\n2: Load Game\n3: Quit")
                print("\nNo save file was found")
        elif(Input == "3"):
            print("Bye, thank you for playing! :)")
        else:
            Input = ""
            print(TITLE+"\n\n\n\n1: New Game\n2: Load Game\n3: Quit")
