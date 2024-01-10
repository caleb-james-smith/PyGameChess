# Evaluate classes

# TODO:
# - Piece tables assume that the player is white; need to fix for black player
# - Add position evaluation maps for each piece
# - Plot position evaluation maps for each piece
# - Switch between king middle game and end game tables
# DONE
# - Add evaluations for checkmate and stalemate

# Evaluation class: uses material (piece value) to determine evaluation.
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
    def GetTotalValue(self, state, player):
        total_value = 0
        player_color = player.GetColor()
        pieces = state.GetPlayersPieces(player_color)
        for piece in pieces:
            piece_type = piece.GetType()
            value = self.piece_values[piece_type]
            total_value += value
        return total_value

    # Evaluate position:
    # - Checkmate: +infinity (white checkmates black), -infinity (black checkmates white)
    # - Stalemate: 0 (white or black)
    # - Otherwise, return difference in total piece values
    # - positive evaluation: good for white
    # - negative evaluation: good for black
    def Evaluate(self, state):
        # Add to evaluation counter
        self.IncrementCounter()
        
        # Get players from the state
        current_player  = state.GetCurrentPlayer()
        opposing_player = state.GetOpposingPlayer()
        
        # Current player is in checkmate: the opposing player wins!
        if state.PlayerIsInCheckmate(current_player, opposing_player):
            # The current player is white
            if state.WhiteToMove():
                # Black has checkmated white
                return float('-inf')
            # The current player is black
            else:
                # White has checkmated black
                return float('inf')
        
        # Current player is in stalemate: both players get 0.
        if state.PlayerIsInStalemate(current_player, opposing_player):
            return 0

        # Get value of pieces
        white_total_value = self.GetTotalValue(state, state.white_player)
        black_total_value = self.GetTotalValue(state, state.black_player)
        evaluation = white_total_value - black_total_value    
        return evaluation
    
# Evaluation class: uses material (piece value) and position to determine evaluation.
class EvaluatePosition:
    def __init__(self, piece_table):
        self.piece_table = piece_table
        self.piece_values = {
            "pawn"      : 100,
            "knight"    : 300,
            "bishop"    : 300,
            "rook"      : 500,
            "queen"     : 900,
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
    # FIXME: Piece tables assume that the player is white; need to fix for black player
    def GetTotalValue(self, state, player):
        total_value = 0
        player_color = player.GetColor()
        pieces = state.GetPlayersPieces(player_color)
        for piece in pieces:
            piece_type      = piece.GetType()
            piece_position  = piece.GetPosition()
            table_name      = piece_type
            
            # FIXME: Switch between king middle game and end game tables
            if piece_type == "king":
                table_name = "king_middle_game"
                #table_name = "king_caleb"
            
            table = self.piece_table.GetTable(table_name)
            
            # Note: table assumes the player is white; for black we have to modify y (row)
            # For black, changing the row should be equivalent to flipping the table over the central horizontal axis
            piece_x, piece_y = piece_position
            row     = piece_y
            column  = piece_x
            if player_color == "black":
                row = 7 - piece_y
            # Note: index with y first (row), then x (column)
            position_value = table[row][column]
            material_value = self.piece_values[piece_type]
            all_the_value = material_value + position_value
            total_value += all_the_value
        
        return total_value

    # Evaluate position:
    # - Checkmate: +infinity (white checkmates black), -infinity (black checkmates white)
    # - Stalemate: 0 (white or black)
    # - Otherwise, return difference in total piece values
    # - positive evaluation: good for white
    # - negative evaluation: good for black
    def Evaluate(self, state):
        # Add to evaluation counter
        self.IncrementCounter()
        
        # Get players from the state
        current_player  = state.GetCurrentPlayer()
        opposing_player = state.GetOpposingPlayer()
        
        # Current player is in checkmate: the opposing player wins!
        if state.PlayerIsInCheckmate(current_player, opposing_player):
            # The current player is white
            if state.WhiteToMove():
                # Black has checkmated white
                return float('-inf')
            # The current player is black
            else:
                # White has checkmated black
                return float('inf')
        
        # Current player is in stalemate: both players get 0.
        if state.PlayerIsInStalemate(current_player, opposing_player):
            return 0

        # Get value of pieces
        white_total_value = self.GetTotalValue(state, state.white_player)
        black_total_value = self.GetTotalValue(state, state.black_player)
        evaluation = white_total_value - black_total_value    
        return evaluation