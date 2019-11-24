import random
import json
import time
import os
import sys
from Include.Character import Monster
from Include.Character import Joueur

SAVING_PATH = "./Save/"
INTRODUCTIONLINES_PATH = "./IntroductionLine/"

#Class of the rooms of the dungeon
class Room():
    def __init__(self, ID,Character,Activable,IntroductionLine):
        self.ID = ID #ID of the Room (in the array containing every rooms of the dungeon)
        self.Character = Character #Name of the monster presence ("monster" or "")
        self.Activable = Activable #Name of the activable                                                   NOT USED
        self.IntroductionLine = IntroductionLine   #Name of the sentence describing the room the player enter
        self.NextRooms = [] #IDs of the next rooms

    #Return the ID of the room
    def get_ID(self):
        return self.ID

    #Return the monster presence of the room
    def get_Character(self):
        return self.Character

    #Return the activable of the room                                  NOT USED
    def get_Activable(self):
        return self.Activable

    #Return the introduction sentence of the Room
    def get_IntroductionLine(self):
        return self.IntroductionLine

    #Return the IDs of the next Rooms of the dungeon
    def get_NextRooms(self):
        return self.NextRooms

    #Set the array of the next Rooms
    def Set_NextRooms(self,NextRooms):
        self.NextRooms = NextRooms

    #Add a Room to the array of the next Rooms
    def Add_NextRoom(self,NextRoom):
        self.NextRooms.append(NextRoom)
    
    #Display the introduction sentence of the room
    def Introduce(self):
        print(self.IntroductionLine+"\n")

#Class containing the entire dungeon and the position of the player in it
class Map():
    def __init__(self, Player):
        self.Player = Player #Pointer to the player
        self.Rooms = [] #Array of the Rooms of the dungeon
        self.PlayerPosition = None #Index of player position
        self.StartingRoom = None #Index of the first room of the dungeon
        self.Choices = [["Turn Left","Turn Right"],["Go upstair","Go downstair"]] #Array containing the sentences of the next room choice
        self.Choices2 = ["Continue to the next room","Open the door and continue the adventure"] #Array2 containing the array of choices
    
    #Display the player stat (Name+LVL+HP+MP)
    def Print_PlayerStat(self):
        print(str(self.Player.nom)+"\nLVL: "+str(self.Player.get_level())+"\nHP: "+str(self.Player.get_HP())+"/"+str(self.Player.get_MaxHP())+"\nMP: "+str(self.Player.get_MP())+"/"+str(self.Player.get_MaxMP())+"\n")
    
    #Animation of the text displaying letter by letter
    def Slow_Display(self, txt):
        for i in txt:
            print(i, end='')
            sys.stdout.flush()
            time.sleep(0.04)
        print("")

    #Generates the dungeon (in a Tree, from the root to one of the ends possible)
    def Generate(self):
        depth = random.randint(5,15) #Depth of the dungeon (by Rooms)
        intro_lines = [] #Array containing the introduction lines of the Rooms
        f = open(INTRODUCTIONLINES_PATH+'Lines.json')
        js = json.load(f)
        for el in js:
            intro_lines.append(el) #Append to the array every introduction lines existing in the Line.json file
        buffer = [[0,depth]] #File containing every branch to create
        chance = 25 #Chance of adding a new Branch starting from a room (decrease over time)
        while(len(buffer) != 0): #Add new branch of Rooms to the array self.Rooms
            for i in range(0,buffer[0][1]): #For each rooms of the new branch
                intro_line = intro_lines[random.randint(0,len(intro_lines)-1)] #Choose a random introduction line for the room
                if(random.randint(0,100) <= 75): #75% chance to have a monster in this room
                    monster = "monster"
                else:
                    monster = ""
                self.Rooms.append(Room(i,str(monster),"",js[intro_line]["IntroductionLine"])) #Create the room and append it to the Rooms array
                if(i != buffer[0][1]-1):
                    another_path = random.randint(0,100)
                    if(another_path <= chance): #Check if a new branch will be created from this actual room
                        buffer.append([len(self.Rooms)-1,random.randint(1,depth)])
                if( len(self.Rooms)-1 != 0): #Set the Nextroom array of the previous room
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

    #Load the map in the save folder
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

    #Save the map in a Json file in the save folder
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
        Input = "" #Choice of the player
        while(is_end == False): #While the game is not over
            os.system("cls")

            self.Print_PlayerStat()
            self.Rooms[self.PlayerPosition].Introduce()
            if(self.Rooms[self.PlayerPosition].get_Character() != ""):    #IF THERE IS A MONSTER IN THE ROOM
                self.Slow_Display("A MONSTER HAS APPEARED")
                self.Slow_Display("What do you want to do ?")
                print("\n1: Fight\n2: Inventory\n3: Potion\n4: Exit game")
                while(Input != "1" and Input != "4"):
                    Input = input("\n> ")
                    if(Input == "2"):   #CHOICE: EQUIP FROM INVENTORY
                        os.system("cls")
                        self.Player.inventory.equip_wa()
                        time.sleep(2)
                        Input = ""
                        os.system("cls")
                        self.Print_PlayerStat()
                        self.Slow_Display("A MONSTER HAS APPEARED")
                        self.Slow_Display("What do you want to do ?")
                        print("\n1: Fight\n2: Inventory\n3: Potion\n4: Exit game")
                    elif(Input == "3"):     #CHOICE: DRINK POTION
                        os.system("cls")
                        Input = ""
                        self.Player.use_consumable()
                        os.system("cls")
                        self.Print_PlayerStat()
                        self.Slow_Display("A MONSTER HAS APPEARED")
                        self.Slow_Display("What do you want to do ?")
                        print("\n1: Fight\n2: Inventory\n3: Potion\n4: Exit game")
                    elif(Input != "4" and Input != "1"):
                        os.system("cls")    #CHOICE DOESN'T EXIST
                        Input = ""
                        self.Print_PlayerStat()
                        self.Slow_Display("A MONSTER HAS APPEARED")
                        self.Slow_Display("What do you want to do ?")
                        print("\n1: Fight\n2: Inventory\n3: Potion\n4: Exit game")
                if(Input == "4"):            #CHOICE: QUIT
                    break
                if(Input == "1"):            #CHOICE: FIGHT THE MONSTER
                    os.system("cls")
                    Input = ""
                    monster = Monster()
                    monster.set_level(self.Player.get_level())
                    player_Turn = True
                    code = 3
                    while(monster.is_dead() == False and self.Player.is_dead() == False): #WHILE THE FIGHT ISN'T OVER LOOP
                        if(player_Turn):                     #PLAYER TURN
                            Input = ""
                            self.Print_PlayerStat()
                            print(str(monster.nom)+"\nLVL: "+str(monster.get_level())+"\nHP: "+str(monster.get_HP())+"/"+str(monster.get_MaxHP())+"\n\n"+str(monster.show()))
                            self.Slow_Display("What do you want to do ?")
                            print("\n1: Slam\n2: Furious Slash\n3: Estoc\n4: Bladestorm\n5: Fireball\n6: Lightning\n7: Ice Spear\n8: Earth Fist") #PLAYER ATTACK CHOICES
                            while(Input != "1" and Input != "2" and Input != "3" and Input != "4" and Input != "5" and Input != "6" and Input != "7" and Input != "8"): #CHOOSE SPELL
                                Input = input("\n> ")
                                if(Input != "1" and Input != "2" and Input != "3" and Input != "4" and Input != "5" and Input != "6" and Input != "7" and Input != "8"):
                                    os.system("cls")
                                    self.Print_PlayerStat()
                                    print(str(monster.nom)+"\nLVL: "+str(monster.get_level())+"\nHP: "+str(monster.get_HP())+"/"+str(monster.get_MaxHP())+"\n\n"+str(monster.show()))
                                    self.Slow_Display("What do you want to do ?")
                                    print("\n1: Slam\n2: Furious Slash\n3: Estoc\n4: Bladestorm\n5: Fireball\n6: Lightning\n7: Ice Spear\n8: Earth Fist")
                                    Input = ""
                            spell_list = self.Player.spell_book.get_list_of_spells() #ATTACK THE MONSTER
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
                            if(monster.get_HP() < 0): #MODIFY PRINTED HEALTH IF MONSTER IS DEAD (SO IT DOES NOT PRINT NEGATIF HEALTH)
                                M_HP = 0
                            else:
                                M_HP = monster.get_HP()
                            print(str(monster.nom)+"\nLVL: "+str(monster.get_level())+"\nHP: "+str(M_HP)+"/"+str(monster.get_MaxHP())+"\n\n"+str(monster.show()))
                            if(code == 3):
                                self.Slow_Display(str(monster.nom)+" TOOK DAMAGE")
                            elif(code == 2):
                                self.Slow_Display(str(monster.nom)+" TOOK CRITICAL DAMAGE")
                            elif(code == 1):
                                self.Slow_Display(str(monster.nom)+" COUNTERED YOUR ATTACK")
                            elif(code == 0):
                                self.Slow_Display(str(monster.nom)+" DIDN'T TAKE DAMAGE")
                            time.sleep(1)
                            os.system("cls")
                            player_Turn = False
                        else:                       #MONSTER TURN
                            player_Turn = True
                            code = monster.attack_phy("",self.Player) #MONSTER ATTACK PLAYER
                            os.system("cls")
                            self.Print_PlayerStat()
                            print(str(monster.nom)+"\nLVL: "+str(monster.get_level())+"\nHP: "+str(monster.get_HP())+"/"+str(monster.get_MaxHP())+"\n\n"+str(monster.show()))
                            self.Slow_Display(str(monster.nom)+" ATTACKED")
                            if(code == 3):
                                self.Slow_Display("YOU TOOK DAMAGE")
                            elif(code == 2):
                                self.Slow_Display("YOU TOOK CRITICAL DAMAGE")
                            elif(code == 1):
                                self.Slow_Display("YOU COUNTER THE ATTACK")
                            elif(code == 0):
                                self.Slow_Display("YOU DIDN'T TAKE DAMAGE")
                            time.sleep(1)
                            os.system("cls")
                    if(monster.is_dead()):             #CHECK IF MONSTER IS DEAD
                        self.Player.get_loot(monster)
                        self.Player.getExp()
                        self.Rooms[self.PlayerPosition].Character = ""
                        player_Turn = True
                        os.system("cls")
                    else:                             #CHECK IF CHARACTER IS DEAD
                        os.system("cls")
                        self.Player.revive() #REVIVE THE PLAYER
                        self.Generate() #CREATE A NEW DUNGEON
                        Input = ""
                        while(Input != "1" and Input != "2"):     #GAME OVER MENU
                            os.system("cls")
                            self.Slow_Display("GAME OVER")
                            print("")
                            self.Slow_Display("1: Continue")
                            print("")
                            self.Slow_Display("2: Quit")
                            Input = input("\n> ")
                        if(Input == "1"):
                            os.system("cls")
                            self.Play()
                            break
                        if(Input == "2"):
                            os.system("cls")
                            break
                    Input = ""
                self.Print_PlayerStat()                      
                self.Slow_Display("What do you want to do ?")
                print("\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                while(Input != "3" and Input != "4"):               #IF PLAYER IS ALIVE FROM THE FIGHT AND MONSTER IS DEAD MENU
                    Input = input("\n> ")
                    if(Input == "1"):                #CHOICE: EQUIP FROM INVENTORY
                        os.system("cls")
                        self.Player.inventory.equip_wa()
                        time.sleep(2)
                        Input = ""
                        os.system("cls")
                        self.Print_PlayerStat()
                        self.Slow_Display("What do you want to do ?")
                        print("\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                    elif(Input == "2"):          #CHOICE: DRINK POTION
                        os.system("cls")
                        Input = ""
                        self.Player.use_consumable()
                        os.system("cls")
                        self.Print_PlayerStat()
                        self.Slow_Display("What do you want to do ?")
                        print("\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                    elif(Input != "3" and Input != "4"):   #CHOICE DOESN'T EXIST
                        os.system("cls")
                        Input = ""
                        self.Print_PlayerStat()
                        self.Slow_Display("What do you want to do ?")
                        print("\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                if(Input == "4"): #CHOICE: QUIT
                    break
                Input = ""
            else:      #IF THERE IS NO MONSTER IN THE ROOM
                self.Slow_Display("What do you want to do ?")
                print("\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                while(Input != "3" and Input != "4"):          #MENU
                    Input = input("\n> ")
                    if(Input == "1"):          #CHOICE: EQUIP FROM INVENTORY
                        os.system("cls")
                        self.Player.inventory.equip_wa()
                        time.sleep(2)
                        Input = ""
                        os.system("cls")
                        self.Print_PlayerStat()
                        self.Slow_Display("What do you want to do ?")
                        print("\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                    elif(Input == "2"):    #CHOICE: DRINK POTION
                        os.system("cls")
                        Input = ""
                        self.Player.use_consumable()
                        os.system("cls")
                        self.Print_PlayerStat()
                        self.Slow_Display("What do you want to do ?")
                        print("\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                    elif(Input != "3" and Input != "4"): #CHOICE DOESN'T EXIST
                        os.system("cls")
                        Input = ""
                        self.Print_PlayerStat()
                        self.Slow_Display("What do you want to do ?")
                        print("\n1: Inventory\n2: Potion\n3: Move to the next room\n4: Exit game")
                if(Input == "4"):
                    break
                Input = ""

            os.system("cls")
            if(len(self.Rooms[self.PlayerPosition].get_NextRooms()) == 2): #CHECK IF THERE IS ONE OR TWO NEXT ROOMS AVAILABLE
                t = random.randint(0,1)
                while(Input != "1" and Input != "2"): #TWO ROOMS CHOICE
                    os.system("cls")
                    self.Print_PlayerStat()
                    self.Slow_Display("Two directions appears before you")
                    print("")
                    self.Slow_Display("which path do you choose ?")
                    print("")
                    print("1: "+str(self.Choices[self.Rooms[self.PlayerPosition].get_NextRooms()[0][1]][0]))
                    print("2: "+str(self.Choices[self.Rooms[self.PlayerPosition].get_NextRooms()[0][1]][1]))
                    Input = input("\n> ")
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
            elif(len(self.Rooms[self.PlayerPosition].get_NextRooms()) == 1):     #ONE ROOM CHOICE
                self.PlayerPosition = self.Rooms[self.PlayerPosition].get_NextRooms()[0][0]
            else:                #NO ROOMS NEXT, DUNGEON IS FINISHED
                os.system("cls")
                self.Generate() #CREATE A NEW DUNGEON
                Input = ""
                while(Input != "1" and Input != "2"): #GAME OVER CHOICE
                    os.system("cls")
                    self.Slow_Display("GAME OVER")
                    print("")
                    self.Slow_Display("1: Continue")
                    print("")
                    self.Slow_Display("2: Quit")
                    Input = input("\n> ")
                if(Input == "1"):
                    os.system("cls")
                    self.Generate()
                    self.Play()
                    break
                if(Input == "2"):
                    os.system("cls")
                    break