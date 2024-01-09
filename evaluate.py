# Evaluate classes

# TODO:
# - Add evaluations for checkmate and stalemate
# - Add position evaluation maps for each piece
# - Plot position evaluation maps for each piece
# DONE

class EvaluateMaterial:
    def __init__(self):
        self.piece_values = {
            "pawn"      : 1,
            "knight"    : 3,
            "bishop"    : 3,
            "rook"      : 5,
            "queen"     : 9,
            "king"      : 0
        }
        self.counter = 0
    
    def GetCounter(self):
        return self.counter
    
    def SetCounter(self, counter):
        self.counter = counter

    def ResetCounter(self):
        self.counter = 0
    
    def IncrementCounter(self):
        self.counter += 1
    
    # Get total piece value: sum of piece values for a player
    def GetTotalPieceValue(self, state, player):
        total_piece_value = 0
        player_color = player.GetColor()
        pieces = state.GetPlayersPieces(player_color)
        for piece in pieces:
            piece_type = piece.GetType()
            value = self.piece_values[piece_type]
            total_piece_value += value
        return total_piece_value

    # Evaluation position: return difference in total piece values
    # - positive evaluation: good for white
    # - negative evaluation: good for black
    def Evaluate(self, state):
        white_piece_value = self.GetTotalPieceValue(state, state.white_player)
        black_piece_value = self.GetTotalPieceValue(state, state.black_player)
        evaluation = white_piece_value - black_piece_value
        self.IncrementCounter()
        return evaluation
    