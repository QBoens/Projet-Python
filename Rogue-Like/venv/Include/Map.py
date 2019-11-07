import random
import json
import os

SAVING_PATH = "../Save/"
INTRODUCTIONLINES_PATH = "../IntroductionLine/"

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
    #Activate the activable
    def Activate(self,Player):
        pass

    #Interact with the NPC/Monster (buy/sell or fight)
    def Interact(self,Player):
        pass

class Map():
    def __init__(self, Player):
        self.Player = Player #Pointer to the player
        self.Rooms = [] #Array of rooms
        self.PlayerPosition = None
        self.StartingRoom = None #Index
        self.Choices = [["Turn Left","Turn Right"],["Go upstair","Go downstair"]]
        self.Choices2 = ["Continue to the next room","Open the door and continue the adventure"]

    #Generates the rooms
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
                self.Rooms.append(Room(i,"","",js[intro_line]["IntroductionLine"])) #TODO

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
            chance -= 1
        
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
        #TO ADD: Call a function in player to save his stat and objects
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
            self.Rooms[self.PlayerPosition].Introduce()

            if(self.Rooms[self.PlayerPosition].get_Character() != ""):
                print("A MONSTER HAS APPEARED\n")
                print("What do you want to do?\n\n1: Fight\n2: Inventory\n3: Move to the next room\n4: Exit game") #Combat ou Marchand
            else:
                print("What do you want to do?\n\n1: Inventory\n2: Move to the next room\n3: Exit game")
                while(Input != "2" and Input != "3"):
                    Input = input()
                    if(Input == "1"):
                        os.system("cls")
                        print("THIS IS THE INVENTORY")
                    else:
                        os.system("cls")
                        print("1: Inventory\n2: Move to the next room\n3: Exit game")
                if(Input == "3"):
                    break
                Input = ""
            
            #TODO: Ask the player if it want to save and quit or continue

            os.system("cls")
            if(len(self.Rooms[self.PlayerPosition].get_NextRooms()) == 2):
                t = random.randint(0,1)
                while(Input != "1" and Input != "2"):
                    print("Choose a path\n")
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
                is_end = True