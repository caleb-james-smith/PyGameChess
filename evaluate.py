# Evaluate classes

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
    def Evaluate(self, state, current_player, opposing_player):
        current_player_piece_value  = self.GetTotalPieceValue(state, current_player)
        opposing_player_piece_value = self.GetTotalPieceValue(state, opposing_player)
        evaluation = current_player_piece_value - opposing_player_piece_value
        return evaluation
