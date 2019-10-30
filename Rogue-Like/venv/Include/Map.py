class Room():
    def __init__(self,is_End,Character,Activable,Intro):
        self.is_End = is_End
        self.Character = Character
        self.Activable = Activable
        self.Intro = Intro
        self.NextRooms = []


    #Set the array of the nextRooms
    def Set_NextRooms(self,NextRooms):
        self.NextRooms = NextRooms

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
        self.Player = Player
        self.Rooms = []
        self.PlayerPosition = None
        self.StartingRoom = None

    #Generates the rooms
    def Generate(self):
        pass

    #Load the map
    def Load(self):
        pass

    #Save the map
    def Save(self):
        pass

    #Run the game
    def Play(self):
        pass