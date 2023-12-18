# Agent class
import random

# Agent that chooses moves randomly.
class AgentRandom:
    def __init__(self):
        return

    # Choose move from a list of legal moves
    def ChooseMove(self, state, current_player, opposing_player):
        result = ""
        # Get legal moves
        legal_moves = state.GetPlayersLegalMoves(current_player, opposing_player)
        # Check that there is at least one legal move
        if legal_moves:
            result = random.choice(legal_moves)
        return result

# Agent that always captures if possible.
class AgentCapture:
    def __init__(self):
        return

    # Choose move from a list of legal moves
    def ChooseMove(self, state, current_player, opposing_player):
        result = ""
        # Get legal moves and captures
        legal_moves     = state.GetPlayersLegalMoves(current_player, opposing_player)
        legal_captures  = state.GetPlayersLegalCaptures(current_player, opposing_player)
        # Check if there are any legal captures
        if legal_captures:
            result = random.choice(legal_captures)
        # Check that there is at least one legal move
        elif legal_moves:
            result = random.choice(legal_moves)
        return result
