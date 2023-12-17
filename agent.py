# Agent class
import random

class Agent:
    def __init__(self):
        return

    # Choose move from a list of legal moves
    def ChooseMove(self, state, current_player, opposing_player):
        legal_moves = state.GetPlayersLegalMoves(current_player, opposing_player)
        result = ""
        # Check that there is at least one legal move
        if legal_moves:
            result = random.choice(legal_moves)
        return result
