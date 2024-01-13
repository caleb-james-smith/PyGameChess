# Player class

class Player:
    def __init__(self, name, color, agent=None):
        self.name = name
        self.color = color
        self.agent = agent
    
    def GetName(self):
        return self.name
    
    def SetName(self, name):
        self.name = name

    def GetColor(self):
        return self.color
    
    def SetColor(self, color):
        self.color = color

    def GetAgent(self):
        return self.agent
    
    def SetAgent(self, agent):
        self.agent = agent
