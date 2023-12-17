# Agent class
import random

class Agent:
    def __init__(self, player):
        self.player = player

    def GetPlayer(self):
        return self.player
    
    def SetPlayer(self, player):
        self.player = player

    # Choose move from a list of legal moves
    def ChooseMove(self, legal_moves):
        result = ""
        # Check that there is at least one legal move
        if legal_moves:
            result = random.choice(legal_moves)
        return result