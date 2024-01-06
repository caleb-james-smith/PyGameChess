# Search classes

# TODO:
# - Create and use game over function
# - When moving, we probably need to switch current/opposing players
# - Each call if Minimax() is for a certain player; need to switch current/opposing players
# - Need to include pawn promotion in search
# - Create and use an undo move function
# - Undoing move: update pieces, state, piece to move and capture
# - Undo pawn promotion
# DONE:

class Search:
    def __init__(self, evaluator, max_depth):
        self.evaluator = evaluator
        self.max_depth = max_depth
    
    # THe minimax algorithm
    def Minimax(self, state, depth, isMaximizingPlayer):
        # Get players from the state
        current_player  = state.GetCurrentPlayer()
        opposing_player = state.GetOpposingPlayer()        
        
        # if depth is 0 or the game is over, return the current evaluation
        # FIXME: add game over condition
        #if depth == 0 or state.gameIsOver():
        if depth == 0:
            return self.evaluator.Evaluate(state)
        
        # Get legal moves
        legal_moves = state.GetPlayersLegalMoves(current_player, opposing_player)

        if isMaximizingPlayer:
            max_eval = float('-inf')
            for move in legal_moves:
                state.MovePiece(move)
                # FIXME: promote pawn
                # FIXME: switch turn
                eval = self.Minimax(state, depth - 1, False)
                # FIXME: undo move
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                state.MovePiece(move)
                # FIXME: promote pawn
                # FIXME: switch turn
                eval = self.Minimax(state, depth - 1, True)
                # FIXME: undo move
                min_eval = min(min_eval, eval)
            return min_eval

    # Get the best move
    # - Use correct current / opposing players
    # - Use correct starting best evaluations
    # - Use correct minimizing / maximizing players
    def GetBestMove(self, state, current_player, opposing_player):
        best_move = ""
        
        # Get legal moves
        legal_moves = state.GetPlayersLegalMoves(current_player, opposing_player)

        # Determine if the current player is the maximizing player
        # Define white as the maximizing player
        currentPlayerIsMaximizing = state.WhiteToMove()
        opposingPlayerIsMaximizing = not currentPlayerIsMaximizing
        
        # Set starting best evaluations
        if currentPlayerIsMaximizing:
            best_eval = float('-inf')
        else:
            best_eval = float('inf')
        
        # Check each legal move
        for move in legal_moves:
            state.MovePiece(move)
            # FIXME: promote pawn
            # FIXME: switch turn
            eval = self.Minimax(state, self.max_depth, opposingPlayerIsMaximizing)
            # FIXME: undo move

            if currentPlayerIsMaximizing:
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
            else:
                if eval < best_eval:
                    best_eval = eval
                    best_move = move

        return best_move
    

