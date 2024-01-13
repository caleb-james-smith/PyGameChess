# Search classes

class Search:
    def __init__(self, evaluator, max_depth):
        self.evaluator = evaluator
        self.max_depth = max_depth
    
    # The minimax algorithm
    def Minimax(self, state, depth, isMaximizingPlayer):
        # Get players from the state
        current_player  = state.GetCurrentPlayer()
        opposing_player = state.GetOpposingPlayer()
        
        # if depth is 0 or the game is over, return the current evaluation
        if depth == 0 or state.GameIsOver(current_player, opposing_player):
            return self.evaluator.Evaluate(state)
        
        # Get legal moves
        legal_moves = state.GetPlayersLegalMoves(current_player, opposing_player)

        if isMaximizingPlayer:
            max_eval = float('-inf')
            for move in legal_moves:
                position_from, position_to = state.board.GetMovePositions(move)
                piece_to_move       = state.GetPieceInPosition(position_from)
                piece_to_capture    = state.GetPieceInPosition(position_to)
                state.MakeMove(move)
                eval = self.Minimax(state, depth - 1, False)
                state.UndoMove(move, piece_to_move, piece_to_capture)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                position_from, position_to = state.board.GetMovePositions(move)
                piece_to_move       = state.GetPieceInPosition(position_from)
                piece_to_capture    = state.GetPieceInPosition(position_to)
                state.MakeMove(move)
                eval = self.Minimax(state, depth - 1, True)
                state.UndoMove(move, piece_to_move, piece_to_capture)
                min_eval = min(min_eval, eval)
            return min_eval

    # The minimax algorithm with alpha-beta pruning
    def MinimaxAlphaBeta(self, state, depth, alpha, beta, isMaximizingPlayer):
        # Get players from the state
        current_player  = state.GetCurrentPlayer()
        opposing_player = state.GetOpposingPlayer()
        
        # if depth is 0 or the game is over, return the current evaluation
        if depth == 0 or state.GameIsOver(current_player, opposing_player):
            return self.evaluator.Evaluate(state)
        
        # Get legal moves
        legal_moves = state.GetPlayersLegalMoves(current_player, opposing_player)

        if isMaximizingPlayer:
            max_eval = float('-inf')
            for move in legal_moves:
                position_from, position_to = state.board.GetMovePositions(move)
                piece_to_move       = state.GetPieceInPosition(position_from)
                piece_to_capture    = state.GetPieceInPosition(position_to)
                state.MakeMove(move)
                eval = self.MinimaxAlphaBeta(state, depth - 1, alpha, beta, False)
                state.UndoMove(move, piece_to_move, piece_to_capture)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                position_from, position_to = state.board.GetMovePositions(move)
                piece_to_move       = state.GetPieceInPosition(position_from)
                piece_to_capture    = state.GetPieceInPosition(position_to)
                state.MakeMove(move)
                eval = self.MinimaxAlphaBeta(state, depth - 1, alpha, beta, True)
                state.UndoMove(move, piece_to_move, piece_to_capture)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
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
            position_from, position_to = state.board.GetMovePositions(move)
            piece_to_move       = state.GetPieceInPosition(position_from)
            piece_to_capture    = state.GetPieceInPosition(position_to)
            state.MakeMove(move)
            eval = self.Minimax(state, self.max_depth, opposingPlayerIsMaximizing)
            state.UndoMove(move, piece_to_move, piece_to_capture)

            if currentPlayerIsMaximizing:
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
            else:
                if eval < best_eval:
                    best_eval = eval
                    best_move = move

        return best_move

    # Get the best move, using alpha-beta pruning
    # - Use correct current / opposing players
    # - Use correct starting best evaluations
    # - Use correct minimizing / maximizing players
    # - Use alpha-beta pruning
    def GetBestMoveAlphaBeta(self, state, current_player, opposing_player):
        best_move = ""
        
        # Get legal moves
        legal_moves = state.GetPlayersLegalMoves(current_player, opposing_player)
        ordered_moves = self.OrderMoves(state, legal_moves)

        # Determine if the current player is the maximizing player
        # Define white as the maximizing player
        currentPlayerIsMaximizing = state.WhiteToMove()
        opposingPlayerIsMaximizing = not currentPlayerIsMaximizing
        
        # Set starting best evaluations
        if currentPlayerIsMaximizing:
            best_eval = float('-inf')
        else:
            best_eval = float('inf')
        
        # Loop over ordered moves
        for move in ordered_moves:
            position_from, position_to = state.board.GetMovePositions(move)
            piece_to_move       = state.GetPieceInPosition(position_from)
            piece_to_capture    = state.GetPieceInPosition(position_to)
            state.MakeMove(move)
            eval = self.MinimaxAlphaBeta(state, self.max_depth, float('-inf'), float('inf'), opposingPlayerIsMaximizing)
            state.UndoMove(move, piece_to_move, piece_to_capture)

            if currentPlayerIsMaximizing:
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
            else:
                if eval < best_eval:
                    best_eval = eval
                    best_move = move

        print("Best evaluation: {0}".format(best_eval))
        print("Best move: {0}".format(best_move))
        
        return best_move
    
    # Order moves to improve the efficiency of alpha-beta pruning
    def OrderMoves(self, state, moves):
        # pawn promotions (includes captures and checks)
        promotion_moves = []
        # captures (includes checks)
        capture_moves = []
        # checks (not promotions or captures)
        check_moves = []
        # other moves
        other_moves = []
        for move in moves:
            if state.IsPromotion(move):
                promotion_moves.append(move)
            elif state.IsCapture(move):
                capture_moves.append(move)
            elif state.IsCheck(move):
                check_moves.append(move)
            else:
                other_moves.append(move)

        result = capture_moves + check_moves + other_moves
        
        n_result    = len(result)
        n_moves     = len(moves)
        
        # Check that the number of results is equal to the number of moves.
        if n_result != n_moves:
            print("ERROR: The number of results {0} is not equal to the number of moves {1}.".format(n_result, n_moves))

        return result

