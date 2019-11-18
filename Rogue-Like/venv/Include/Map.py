import random
import json
import time
import os
from Include.Character import Monster
from Include.Character import Joueur

SAVING_PATH = "./Save/"
INTRODUCTIONLINES_PATH = "./IntroductionLine/"

class Room():
    def __init__(self, ID,Character,Activable,IntroductionLine):
        self.ID = ID
        self.Character = Character #Name of the character
        self.Activable = Activable #Name of the activable
        self.IntroductionLine = IntroductionLine   #Name of the introduction line
        self.NextRooms = [] #index of the next rooms

    def get_ID(self):
        return self.ID

    def get_Character(self):
        return self.Character

    def get_Activable(self):
        return self.Activable

    def get_IntroductionLine(self):
        return self.IntroductionLine

    def get_NextRooms(self):
        return self.NextRooms

    #Set the array of the nextRooms
    def Set_NextRooms(self,NextRooms):
        self.NextRooms = NextRooms

    #Add to the array of the nextRooms
    def Add_NextRoom(self,NextRoom):
        self.NextRooms.append(NextRoom)
    

    #Display the intro sentence of the room
    def Introduce(self):
        print(self.IntroductionLine+"\n")

class Map():
    def __init__(self, Player):
        self.Player = Player #Pointer to the player
        self.Rooms = [] #Array of rooms
        self.PlayerPosition = None #Index of player position
        self.StartingRoom = None #Index of the first room of the dungeon
        self.Choices = [["Turn Left","Turn Right"],["Go upstair","Go downstair"]]
        self.Choices2 = ["Continue to the next room","Open the door and continue the adventure"]
    
    #Print the player stat
    def Print_PlayerStat(self):
        print(str(self.Player.nom)+"\nLVL: "+str(self.Player.get_level())+"\nHP: "+str(self.Player.get_HP())+"/"+str(self.Player.get_MaxHP())+"\nMP: "+str(self.Player.get_MP())+"/"+str(self.Player.get_MaxMP())+"\n")

    #Generates the dungeon
    def Generate(self):
        depth = random.randint(5,15)
        intro_lines = []
        f = open(INTRODUCTIONLINES_PATH+'Lines.json')
        js = json.load(f)
        for el in js:
            intro_lines.append(el)
        buffer = [[0,depth]]
        chance = 25
        while(len(buffer) != 0):
            for i in range(0,buffer[0][1]):
                intro_line = intro_lines[random.randint(0,len(intro_lines)-1)]
                if(random.randint(0,100) <= 75):
                    monster = "monster"
                else:
                    monster = ""
                self.Rooms.append(Room(i,str(monster),"",js[intro_line]["IntroductionLine"]))
                if(i != buffer[0][1]-1):
                    another_path = random.randint(0,100)
                    if(another_path <= chance):
                        buffer.append([len(self.Rooms)-1,random.randint(1,depth)])
                if( len(self.Rooms)-1 != 0):
                    if(i == 0):
                        if( len(self.Rooms[buffer[0][0]].get_NextRooms()) == 0):
                            self.Rooms[buffer[0][0]].Add_NextRoom([self.Rooms[len(self.Rooms)-1].get_ID(),random.randint(0,len(self.Choices)-1)])
                        else:
                            self.Rooms[buffer[0][0]].Add_NextRoom([self.Rooms[len(self.Rooms)-1].get_ID(),self.Rooms[buffer[0][0]].get_NextRooms()[0][1]])
                    else:
                        if(len(self.Rooms[len(self.Rooms)-2].get_NextRooms()) == 0 ):
                            self.Rooms[len(self.Rooms)-2].Add_NextRoom([self.Rooms[len(self.Rooms)-1].get_ID(),random.randint(0,len(self.Choices)-1)])
                        else:
                            self.Rooms[len(self.Rooms)-2].Add_NextRoom([self.Rooms[len(self.Rooms)-1].get_ID(),self.Rooms[len(self.Rooms)-2].get_NextRooms()[0][1]])
            buffer.pop(0)
            chance -= 2
        
        self.StartingRoom = 0 
        self.PlayerPosition = self.StartingRoom
        self.Save()

    #Load the map
    def Load(self):
        if(os.path.exists(SAVING_PATH+'map.json')):
            f = open(SAVING_PATH+'map.json')
        else:
            return False
        js = json.load(f)
        self.StartingRoom = js["StartingRoom"]
        self.PlayerPosition = js["PlayerPosition"]
        self.Rooms = []
        for i in range(0,len(js["Rooms"])):
            self.Rooms.append(Room(js["Rooms"][i]["ID"], js["Rooms"][i]["Character"], js["Rooms"][i]["Activable"], js["Rooms"][i]["IntroductionLine"]))
            self.Rooms[i].Set_NextRooms(js["Rooms"][i]["NextRooms"])
        return True

    #Save the map in a Json file
    def Save(self):
        self.Player.save()
        js = {"StartingRoom" : 0, "PlayerPosition" : 0, "Rooms":[]}
        js["StartingRoom"] = self.StartingRoom
        js["PlayerPosition"] = self.PlayerPosition
        for a in range(0,len(self.Rooms)):
            tmp = {}
            tmp["ID"] = self.Rooms[a].get_ID()
            tmp["Character"] = self.Rooms[a].get_Character()
            tmp["Activable"] = self.Rooms[a].get_Activable()
            tmp["IntroductionLine"] = self.Rooms[a].get_IntroductionLine()
            tmp["NextRooms"] = self.Rooms[a].get_NextRooms()
            js["Rooms"].append(tmp)
        
        with open(SAVING_PATH+'map.json', 'w') as f:
            json.dump(js, f)
    
    #Run the game
    def Play(self):
        is_end = False
        Input = ""
        while(is_end == False):
            os.system("cls")

            self.Print_PlayerStat()
            self.Rooms[self.PlayerPosition].Introduce()
            if(self.Rooms[self.PlayerPosition].get_Character() != ""):    #CHECK IF THERE IS A MONSTER IN THE ROOM
                print("A MONSTER HAS APPEARED")
                print("What do you want to do?\n\n1: Fight\n2: Inventory\n3: Potion\n4: Exit game")
                while(Input != "1" and Input != "4"):
                    Input = input()
                    if(Input == "2"):
                        os.system("cls")    #EQUIP FROM INVENTORY
                        self.Player.inventory.equip_wa()
                        time.sleep(2)
                        Input = ""
                        os.system("cls")
                        self.Print_PlayerStat()
                        print("A MONSTER HAS APPEARED")
                        print("What do you want to do?\n\n1: Fight\n2: Inventory\n3: Potion\n4: Exit game")
                    elif(Input == "3"):     #DRINK POTION
                        os.system("cls")
                        Input = ""
                        self.Player.use_consumable()
                        os.system("cls")
                        self.Print_PlayerStat()
                        print("A MONSTER HAS APPEARED")
                        print("What do you want to do?\n\n1: Fight\n2: Inventory\n3: Potion\n4: Exit game")
                    elif(Input != "4" and Input != "1"):
                        os.system("cls")    #CLEAR SCREEN
                        Input = ""
                        self.Print_PlayerStat()
                        print("A MONSTER HAS APPEARED")
                        print("What do you want to do?\n\n1: Fight\n2: Inventory\n3: Potion\n4: Exit game")
                if(Input == "4"):            #QUIT
                    break
                if(Input == "1"):            #FIGHT
                    os.system("cls")
                    Input = ""
                    monster = Monster()
                    player_Turn = True
                    code = 3
                    while(monster.is_dead() == False and self.Player.is_dead() == False):
                        if(player_Turn):
                            Input = ""
                            self.Print_PlayerStat()
                            print(str(monster.nom)+"\nLVL: "+str(monster.get_level())+"\nHP: "+str(monster.get_HP())+"/"+str(monster.get_MaxHP())+"\n\n"+str(monster.show()))
                            print("What do you do?\n\n1: Slam\n2: Furious Slash\n3: Estoc\n4: Bladestorm\n5: Fireball\n6: Lightning\n7: Ice Spear\n8: Earth Fist")
                            while(Input != "1" and Input != "2" and Input != "3" and Input != "4" and Input != "5" and Input != "6" and Input != "7" and Input != "8"):
                                Input = input()
                                if(Input != "1" and Input != "2" and Input != "3" and Input != "4" and Input != "5" and Input != "6" and Input != "7" and Input != "8"):
                                    os.system("cls")
                                    self.Print_PlayerStat()
                                    print(str(monster.nom)+"\nLVL: "+str(monster.get_level())+"\nHP: "+str(monster.get_HP())+"/"+str(monster.get_MaxHP())+"\n\n"+str(monster.show()))
                                    print("What do you do?\n\n1: Slam\n2: Furious Slash\n3: Estoc\n4: Bladestorm\n5: Fireball\n6: Lightning\n7: Ice Spear\n8: Earth Fist")
                                    Input = ""
                            spell_list = self.Player.spell_book.get_list_of_spells()
                            if(Input == "1"):
                                code = self.Player.attack_phy(spell_list[0],monster)
                            elif(Input == "2"):
                                code = self.Player.attack_phy(spell_list[1],monster)
                            elif(Input == "3"):
                                code = self.Player.attack_phy(spell_list[2],monster)
                            elif(Input == "4"):
                                code = self.Player.attack_phy(spell_list[3],monster)
                            elif(Input == "5"):
                                code = self.Player.attack_mag(spell_list[4],monster)
                            elif(Input == "6"):
                                code = self.Player.attack_mag(spell_list[5],monster)
                            elif(Input == "7"):
                                code = self.Player.attack_mag(spell_list[6],monster)
                            elif(Input == "8"):
                                code = self.Player.attack_mag(spell_list[7],monster)
                            Input = ""
                            os.system("cls")
                            self.Print_PlayerStat()
                            print(str(monster.nom)+"\nLVL: "+str(monster.get_level())+"\nHP: "+str(monster.get_HP())+"/"+str(monster.get_MaxHP())+"\n\n"+str(monster.show()))
                            if(code == 3):
                                print(str(monster.nom)+" TOOK DAMAGE")
                            elif(code == 2):
                                print(str(monster.nom)+" TOOK CRITICAL DAMAGE")
                            elif(code == 1):
                                print(str(monster.nom)+" COUNTERED YOUR ATTACK")
                            elif(code == 0):
                                print(str(monster.nom)+" TOOK NO DAMAGE")
                            time.sleep(2)
                            os.system("cls")
                            player_Turn = False
                        else:
                            player_Turn = True
                            code = monster.attack_phy("",self.Player)
                            os.system("cls")
                            self.Print_PlayerStat()
                            print(str(monster.nom)+"\nLVL: "+str(monster.get_level())+"\nHP: "+str(monster.get_HP())+"/"+str(monster.get_MaxHP())+"\n\n"+str(monster.show()))
                            if(code == 3):
                                print("YOU TOOK DAMAGE")
                            elif(code == 2):
                                print("YOU TOOK CRITICAL DAMAGE")
                            elif(code == 1):
                                print("YOU COUNTER THE ATTACK")
                            elif(code == 0):
                                print("YOU TOOK NO DAMAGE")
                            time.sleep(2)
                            os.system("cls")
                    if(monster.is_dead()):
                        self.Player.get_loot(monster)
                        self.Player.getExp()
                        self.Rooms[self.PlayerPosition].Character = ""
                        player_Turn = True
                        os.system("cls")
                    else:
                        os.system("cls")
                        self.Player.revive() #REVIVE THE PLAYER
                        self.Generate() #CREATE A NEW DUNGEON
                        Input = ""
                        while(Input != "1" and Input != "2"):
                            os.system("cls")
                            print("GAME OVER\n\n1: Continue\n2: Quit")
                            Input = input()
                        if(Input == "1"):
                            os.system("cls")
                            self.Play()
                            break
                        if(Input == "2"):
                            os.system("cls")
                            break
                    Input = ""
                self.Print_PlayerStat()
                print("What do you want to do?\n\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                while(Input != "3" and Input != "4"):
                    Input = input()
                    if(Input == "1"):
                        os.system("cls")
                        self.Player.inventory.equip_wa()
                        time.sleep(2)
                        Input = ""
                        os.system("cls")
                        self.Print_PlayerStat()
                        print("What do you want to do?\n\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                    elif(Input == "2"):
                        os.system("cls")
                        Input = ""
                        self.Player.use_consumable()
                        os.system("cls")
                        self.Print_PlayerStat()
                        print("What do you want to do?\n\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                    elif(Input != "3" and Input != "4"):
                        os.system("cls")
                        Input = ""
                        self.Print_PlayerStat()
                        print("What do you want to do?\n\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                if(Input == "4"):
                    break
                Input = ""
            else:      #IF THER IS NO MONSTER
                print("What do you want to do?\n\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                while(Input != "3" and Input != "4"):
                    Input = input()
                    if(Input == "1"):
                        os.system("cls")
                        self.Player.inventory.equip_wa()
                        time.sleep(2)
                        Input = ""
                        os.system("cls")
                        self.Print_PlayerStat()
                        print("What do you want to do?\n\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                    elif(Input == "2"):
                        os.system("cls")
                        Input = ""
                        self.Player.use_consumable()
                        os.system("cls")
                        self.Print_PlayerStat()
                        print("What do you want to do?\n\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                    elif(Input != "3" and Input != "4"):
                        os.system("cls")
                        Input = ""
                        self.Print_PlayerStat()
                        print("What do you want to do?\n\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                if(Input == "4"):
                    break
                Input = ""

            os.system("cls")
            if(len(self.Rooms[self.PlayerPosition].get_NextRooms()) == 2): #CHECK THE NEXT ROOMS
                t = random.randint(0,1)
                while(Input != "1" and Input != "2"):
                    os.system("cls")
                    self.Print_PlayerStat()
                    print("Two directions appears before you\n\nwhich path do you choose?\n")
                    print("1: "+str(self.Choices[self.Rooms[self.PlayerPosition].get_NextRooms()[0][1]][0]))
                    print("2: "+str(self.Choices[self.Rooms[self.PlayerPosition].get_NextRooms()[0][1]][1]))
                    Input = input()
                    if( t == 0):
                        if(Input == "1"):
                            self.PlayerPosition = self.Rooms[self.PlayerPosition].get_NextRooms()[0][0]
                        if(Input == "2"):
                            self.PlayerPosition = self.Rooms[self.PlayerPosition].get_NextRooms()[0][1]
                    else:
                        if(Input == "1"):
                            self.PlayerPosition = self.Rooms[self.PlayerPosition].get_NextRooms()[0][1]
                        if(Input == "2"):
                            self.PlayerPosition = self.Rooms[self.PlayerPosition].get_NextRooms()[0][0]
                Input = ""
            elif(len(self.Rooms[self.PlayerPosition].get_NextRooms()) == 1):
                self.PlayerPosition = self.Rooms[self.PlayerPosition].get_NextRooms()[0][0]
            else:
                os.system("cls")
                self.Generate() #CREATE A NEW DUNGEON
                Input = ""
                while(Input != "1" and Input != "2"):
                    os.system("cls")
                    print("GAME OVER\n\n1: Continue\n2: Quit")
                    Input = input()
                if(Input == "1"):
                    os.system("cls")
                    self.Generate()
                    self.Play()
                    break
                if(Input == "2"):
                    os.system("cls")
                    break