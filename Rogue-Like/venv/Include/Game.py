import Map
import Character
import os

if __name__ == "__main__":
    os.system("cls")
    player = Character.Joueur("Link")
    map = Map.Map(player)
    Input = ""
    while(Input != "2"):
        print("1: Play\n2: Quit")
        Input = input()
        os.system("cls")
        if(Input == "1"):
            Input = ""
            while(Input != "1" and Input != "2" and Input != "3"):
                print("1: New Game\n2: Load Game\n3: Back")
                Input = input()
            if(Input == "1"):
                map.Generate()
                map.Play()
                map.Save()
                os.system("cls")
            elif(Input == "2"):
                if(map.Load()):
                    map.Play()
                    map.Save()
                    os.system("cls")
                else:
                    os.system("cls")
                    print("Error there is no existing save")
            elif(Input == "3"):
                os.system("cls")
            Input = ""
