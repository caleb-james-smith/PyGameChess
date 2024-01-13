# Agent classes

import random
from search import Search

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

# Agent that uses the minimax algorithm.
class AgentMinimax:
    def __init__(self, evaluator, max_depth):
        self.evaluator  = evaluator
        self.max_depth  = max_depth
        self.search = Search(self.evaluator, self.max_depth)

    # Choose move
    def ChooseMove(self, state, current_player, opposing_player):
        result = ""
        self.evaluator.ResetCounter()
        #result  = self.search.GetBestMove(state, current_player, opposing_player)
        result  = self.search.GetBestMoveAlphaBeta(state, current_player, opposing_player)
        counter = self.evaluator.GetCounter()
        print("Number of evaluations: {0}".format(counter))
        print("Result: {0}".format(result))
        return result
