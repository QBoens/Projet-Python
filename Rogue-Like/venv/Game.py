from Include.Map import Map
from Include.Character import Joueur
import os

if __name__ == "__main__":
    os.system("cls")
    player = Joueur("Link")
    map = Map(player)
    Input = ""
    print("1: New Game\n2: Load Game\n3: Quit")
    while(Input != "4"):
        Input = input()
        os.system("cls")
        if(Input == "1"):
            map.Generate()
            map.Play()
            map.Save()
            os.system("cls")
            Input = ""
            print("\n1: New Game\n2: Load Game\n3: Quit")
        elif(Input == "2"):
            if(map.Load()):
                map.Play()
                map.Save()
                os.system("cls")
                Input = ""
                print("\n1: New Game\n2: Load Game\n3: Quit")
            else:
                print("Error there is no existing save")
                Input = ""
                print("\n1: New Game\n2: Load Game\n3: Quit")
        elif(Input != "3"):
            Input = ""
            print("1: New Game\n2: Load Game\n3: Quit")
