import random
import json

SAVING_PATH = "../Saving/"

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
    def Introduce(self,Player):
        pass
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

    #Generates the rooms
    def Generate(self):
        altLength = []
        depth = random.randint(3,10)
        for i in range(0,depth):
            another_path = random.randint(0,100)
            if(another_path <= 30):
                altLength.append(random.randint(0,depth-(i+1)))
            else:
                altLength.append(0)
            if(i != depth -1):
                self.Rooms.append(Room(i,"","",""))
            else:
                self.Rooms.append(Room(i,"","",""))
            if(i != 0):
                self.Rooms[i-1].Add_NextRoom([self.Rooms[i].get_ID(),"Chemin1"])
        
        print(altLength)
        self.StartingRoom = 0 
        self.PlayerPosition = self.StartingRoom
        self.Save()

    #Load the map
    def Load(self):
        f = open(SAVING_PATH+'map.json')
        js = json.load(f)
        self.Rooms = []
        for i in range(0,len(js["Rooms"])):
            self.Rooms.append(js["Rooms"][i]["ID"], js["Rooms"][i]["Character"], js["Rooms"][i]["Activable"], js["Rooms"][i]["IntroductionLine"])
            self.Rooms[i].Set_NextRooms(js["Rooms"][i]["NextRooms"])

    #Save the map in a Json file
    def Save(self):
        #TO ADD: Call a function in player to save his stat and objects
        js = {"Rooms":[]}
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
        self.Rooms[self.PlayerPosition].Introduce() #Display the intro line of the room
        if(self.Rooms[self.PlayerPosition].get_Character() != ""):
            pass #Combat ou Marchand

        #TO ADD: Ask the player if it want to save and quit or continue

        if(self.Rooms[self.PlayerPosition].get_Activable() != ""):
            pass #Activable (chest, button, trap)
        
        #TO ADD: Ask the player if it want to save and quit or continue

        if len(self.Rooms[self.PlayerPosition].get_NextRooms()) == 0:
            return True #Check if the dungeon is finished 

        else:
            for j in range(0, len(self.Rooms[self.PlayerPosition].get_NextRooms())):
                pass #Display the message associated to each path and ask the player to make a choice


        

#if __name__ == "__main__":
    #map = Map("test")
    #map.Generate()
    #map.Load()