# State class

# Save the current game state
# - Use 8x8 matrix to represent squares on chess board
# - White pieces are positive
# - Black pieces are negative
# - 0: empty
# - 1: pawn
# - 2: knight
# - 3: bishop
# - 4: rook
# - 5: queen
# - 6: king

from piece import Pawn, Knight, Bishop, Rook, Queen, King

# Class to define current game state (piece positions)
class State:
    def __init__(self, board, piece_theme, white_player, black_player):
        self.board = board
        self.piece_theme = piece_theme
        self.state = None
        self.piece_state = None
        self.white_player = white_player
        self.black_player = black_player
        self.current_player = None
        self.opposing_player = None
        # Chess pieces
        self.chess_pieces = {
            0: "empty",
            1: "pawn",
            2: "knight",
            3: "bishop",
            4: "rook",
            5: "queen",
            6: "king"
        }
        # Chess piece images
        # The svg files are from this webpage:
        # https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces
        self.chess_piece_images = {
            "white pawn"    : "images/white_pawn.svg",
            "white knight"  : "images/white_knight.svg",
            "white bishop"  : "images/white_bishop.svg",
            "white rook"    : "images/white_rook.svg",
            "white queen"   : "images/white_queen.svg",
            "white king"    : "images/white_king.svg",
            "black pawn"    : "images/black_pawn.svg",
            "black knight"  : "images/black_knight.svg",
            "black bishop"  : "images/black_bishop.svg",
            "black rook"    : "images/black_rook.svg",
            "black queen"   : "images/black_queen.svg",
            "black king"    : "images/black_king.svg"
        }
        # Supported piece themes
        self.piece_themes = [
            "standard",
            "shapes"
        ]
        # Print an error message if the piece theme is not supported
        if self.piece_theme not in self.piece_themes:
            print("ERROR: The piece theme '{0}' is not supported.".format(self.piece_theme))

    def __str__(self):
        return str(self.state)

    def GetState(self):
        return self.state

    def SetState(self, state):
        self.state = state
    
    def GetPieceState(self):
        return self.piece_state
    
    def SetPieceState(self, piece_state):
        self.piece_state = piece_state
    
    def GetCurrentPlayer(self):
        return self.current_player
    
    def SetCurrentPlayer(self, current_player):
        self.current_player = current_player

    def GetOpposingPlayer(self):
        return self.opposing_player
    
    def SetOpposingPlayer(self, opposing_player):
        self.opposing_player = opposing_player

    # Determine if it is white to move
    def WhiteToMove(self):
        return self.current_player == self.white_player
    
    # Determine if it is white to move
    def BlackToMove(self):
        return self.current_player == self.black_player 

    # Switch current and opposing players
    def SwitchTurn(self):
        if self.WhiteToMove():
            self.current_player  = self.black_player
            self.opposing_player = self.white_player
        # Note: else or elif is required; if alone does not work!
        elif self.BlackToMove():
            self.current_player  = self.white_player
            self.opposing_player = self.black_player
    
    # Check if piece has a valid value
    def PieceIsValid(self, value):
        abs_value = abs(value)
        if abs_value in self.chess_pieces:
            return True
        else:
            return False
    
    # Print current player
    def PrintCurrentPlayer(self):
        print("----------------------------------")
        print("Current player: {0} - {1}".format(self.current_player.GetName(), self.current_player.GetColor()))
        print("----------------------------------")
    
    # Print the state with pretty formatting
    def PrintState(self):
        # Number of dashes to match length of row string
        n_dashes = (8 * 3) - 1
        line = n_dashes * "-"

        print("State:")
        if self.state:
            print(line)
            for row in self.state:
                # Fill with whitespace using string rjust()
                # Forces positive and negative integers < 10 to use the same width
                row_formatted = [str(value).rjust(2) for value in row]
                row_string = ",".join(row_formatted)
                print(row_string)
            print(line)
        else:
            print(self.state)

    # Print a detailed game state
    def PrintGameState(self, evaluator=None):
        current_player_is_in_check      = self.PlayerIsInCheck(self.current_player, self.opposing_player)
        current_player_is_in_checkmate  = self.PlayerIsInCheckmate(self.current_player, self.opposing_player)
        current_player_is_in_stalemate  = self.PlayerIsInStalemate(self.current_player, self.opposing_player)
        game_is_over                    = self.GameIsOver(self.current_player, self.opposing_player)
        legal_moves                     = self.GetPlayersLegalMoves(self.current_player, self.opposing_player)
        n_legal_moves                   = len(legal_moves)
        if evaluator:            
            white_total_value = evaluator.GetTotalValue(self, self.white_player)
            black_total_value = evaluator.GetTotalValue(self, self.black_player)
            evaluation = evaluator.Evaluate(self)
        
        # Print game state information
        #self.PrintState()
        print("------------------------------------------")
        print("Current player: {0} - {1}".format(self.current_player.GetName(), self.current_player.GetColor()))
        print("------------------------------------------")
        print(" - Current player is in check:       {0}".format(current_player_is_in_check))
        print(" - Current player is in checkmate:   {0}".format(current_player_is_in_checkmate))
        print(" - Current player is in stalemate:   {0}".format(current_player_is_in_stalemate))
        print(" - Game is over:                     {0}".format(game_is_over))
        print(" - Number of legal moves:            {0}".format(n_legal_moves))
        #print(" - Legal moves:                      {0}".format(legal_moves))
        if evaluator:
            print(" - White total value:                {0}".format(white_total_value))
            print(" - Black total value:                {0}".format(black_total_value))
            print(" - Evaluation:                       {0}".format(evaluation))
        print("------------------------------------------")

    # Set the state based on the piece state
    def SetStateFromPieceState(self):
        self.SetEmptyState()
        for x in range(8):
            for y in range(8):
                piece = self.piece_state[y][x]
                if piece:
                    self.state[y][x] = piece.GetValue()
                else:
                    self.state[y][x] = 0

    # Set state to an empty board (all entries are 0)
    def SetEmptyState(self):
        state = [[0 for x in range(8)] for y in range (8)]
        self.SetState(state)

    # Set piece state to a empty board (all entries are None)
    def SetEmptyPieceState(self):
        piece_state = [[None for x in range(8)] for y in range (8)]
        self.SetPieceState(piece_state)

    # Set initial state (starting position)
    def SetInitialState(self):
        # Start with empty state
        self.SetEmptyState()
        # Initial state: chess starting position
        # Note: index with y first (row), then x (column)
        state = [
            [-4, -2, -3, -5, -6, -3, -2, -4],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 1,  1,  1,  1,  1,  1,  1,  1],
            [ 4,  2,  3,  5,  6,  3,  2,  4]
        ]
        self.SetState(state)

    # Set initial piece state (starting position)
    def SetInitialPieceState(self):
        # Start with empty piece state
        self.SetEmptyPieceState()
        
        # Initial state: chess starting position
        
        # White pieces
        white_pieces = [
            Rook("white",   [0, 7]),
            Knight("white", [1, 7]),
            Bishop("white", [2, 7]),
            Queen("white",  [3, 7]),
            King("white",   [4, 7]),
            Bishop("white", [5, 7]),
            Knight("white", [6, 7]),
            Rook("white",   [7, 7]),
            Pawn("white",   [0, 6]),
            Pawn("white",   [1, 6]),
            Pawn("white",   [2, 6]),
            Pawn("white",   [3, 6]),
            Pawn("white",   [4, 6]),
            Pawn("white",   [5, 6]),
            Pawn("white",   [6, 6]),
            Pawn("white",   [7, 6]),
        ]
        
        # Black pieces
        black_pieces = [
            Rook("black",   [0, 0]),
            Knight("black", [1, 0]),
            Bishop("black", [2, 0]),
            Queen("black",  [3, 0]),
            King("black",   [4, 0]),
            Bishop("black", [5, 0]),
            Knight("black", [6, 0]),
            Rook("black",   [7, 0]),
            Pawn("black",   [0, 1]),
            Pawn("black",   [1, 1]),
            Pawn("black",   [2, 1]),
            Pawn("black",   [3, 1]),
            Pawn("black",   [4, 1]),
            Pawn("black",   [5, 1]),
            Pawn("black",   [6, 1]),
            Pawn("black",   [7, 1]),
        ]
        
        for piece in white_pieces:
            self.PlacePiece(piece)
        
        for piece in black_pieces:
            self.PlacePiece(piece)

        # Set state based on piece state
        self.SetStateFromPieceState()

    # Draw the pieces
    def DrawPieces(self, game, screen, light_color, dark_color, border_color, squares_per_side, square_side):
        # Draw pieces
        for x in range(squares_per_side):
            for y in range(squares_per_side):
                # Get piece based on position
                position = [x, y]
                piece = self.GetPieceInPosition(position)
                
                # Skip empty squares
                if not piece:
                    continue
                
                # Determine color
                piece_color = piece.GetColor()
                piece_name  = piece.GetName()
                primary_color = None
                if piece_color == "white":
                    primary_color = light_color
                if piece_color == "black":
                    primary_color = dark_color

                # Get piece position: note that this is different than the square position
                x_position = (x + 0.5) * square_side
                y_position = (y + 0.5) * square_side
                # Piece size should be smaller than square side
                size = square_side / 4
                if self.piece_theme == "shapes":
                    # Draw piece (border color)
                    piece.Draw(game, screen, border_color, x_position, y_position, size)
                    # Draw piece (primary color)
                    piece.Draw(game, screen, primary_color, x_position, y_position, 0.75 * size)
                elif self.piece_theme == "standard":
                    piece_image = self.chess_piece_images[piece_name]
                    screen.blit(game.image.load(piece_image), (x_position, y_position))
    
    # Place a piece in the piece state
    def PlacePiece(self, piece):
        position = piece.GetPosition()
        value = piece.GetValue()
        if self.board.LocationIsValid(position):
            if self.PieceIsValid(value):
                piece_state = self.GetPieceState()
                x = position[0]
                y = position[1]
                piece_state[y][x] = piece
                self.SetPieceState(piece_state)
            else:
                print("ERROR: The piece value {0} is not valid!".format(value))
        else:
            print("ERROR: The position [x, y] = {0} is not valid!".format(position))
        return

    # Set a position to a value
    # Check if position and value are valid
    def SetValue(self, position, value):
        if self.board.LocationIsValid(position):
            if self.PieceIsValid(value):
                state = self.GetState()
                x = position[0]
                y = position[1]
                state[y][x] = value
                self.SetState(state)
            else:
                print("ERROR: The piece value {0} is not valid!".format(value))
        else:
            print("ERROR: The position [x, y] = {0} is not valid!".format(position))
        return

    # Move piece from one position to another
    def MovePiece(self, move_notation):
        position_from, position_to = self.board.GetMovePositions(move_notation)
        x_from, y_from = position_from
        x_to, y_to     = position_to
        #print("In MovePiece(): move_notation: {0}".format(move_notation))
        #print("In MovePiece(): position_from: {0}, position_to: {1}".format(position_from, position_to))
        
        # Get piece in "from" position
        piece = self.GetPieceInPosition(position_from)
        
        # Set "from" position to None for empty
        self.piece_state[y_from][x_from] = None
        
        # Set "to" position to piece and update piece position
        self.piece_state[y_to][x_to] = piece
        piece.SetPosition(position_to)

        # Update state based on piece state
        self.SetStateFromPieceState()

    # Pawn promotion
    # - For now, always promote pawns to queens
    def PromotePawn(self, piece):
        piece_name      = piece.GetName()
        piece_color     = piece.GetColor()
        piece_type      = piece.GetType()
        piece_position  = piece.GetPosition()
        x, y = piece_position
        
        # The final row is based on the color
        final_row = {"white": 0, "black": 7}
        
        # Check if the piece is a pawn
        if piece_type == "pawn":
            #print("{0} found at {1}...".format(piece_name, piece_position))
            # Check if the pawn is on the final row
            if y == final_row[piece_color]:
                print("Promoting the {0} at {1} to a queen!".format(piece_name, piece_position))
                new_piece = Queen(piece_color, piece_position)
                self.PlacePiece(new_piece)
                self.SetStateFromPieceState()

    # Make move
    # - Move piece
    # - Promote pawn if applicable
    # - Switch current and opposing players
    def MakeMove(self, move):
        # Get move positions
        position_from, position_to = self.board.GetMovePositions(move)
        # Get piece to move
        piece_to_move = self.GetPieceInPosition(position_from)
        # Move piece
        self.MovePiece(move)
        # Promote pawn if applicable
        self.PromotePawn(piece_to_move)
        # Switch current and opposing players
        self.SwitchTurn()
    
    # Undo move
    # - Place original piece to move (to undo pawn promotion)
    # - Reverse move
    # - Place piece to capture
    # - Update state
    # - Switch current and opposing players
    def UndoMove(self, move, piece_to_move, piece_to_capture):
        # Get reverse move
        reverse_move = self.board.GetReverseMove(move)
        # Place original piece to move (to undo pawn promotion)
        self.PlacePiece(piece_to_move)
        self.SetStateFromPieceState()
        # Reverse move
        self.MovePiece(reverse_move)
        # If there was a piece to capture, put it back
        if piece_to_capture:
            self.PlacePiece(piece_to_capture)
            self.SetStateFromPieceState()
        # Switch current and opposing players
        self.SwitchTurn()

    # Check if at least one piece occupies a square between two positions
    def PieceIsInBetween(self, position_1, position_2):
        result = False
        # Get in between squares
        in_between_squares = self.board.GetInBetweenSquares(position_1, position_2)
        for square in in_between_squares:
            # Check if there is a piece on this square
            piece = self.GetPieceInPosition(square)            
            if piece:
                result = True
        return result
    
    # Determine if move is valid
    # - A player can only move his own pieces
    # - A player can move to empty squares
    # - A player can capture an opponent's piece
    # - A player cannot capture one of his own pieces
    # - Move must be valid for the piece being moved
    # - Pieces (except for knights) cannot jump other pieces (knights are allowed to jump)
    # - Pawns can move forward, but not capture forward
    # - Pawns cannot move diagonally, but can capture diagonally
    
    # Get possible moves for a piece
    def GetPiecePossibleMoves(self, piece):
        all_moves       = []
        valid_moves     = []
        valid_captures  = []

        position_from = piece.GetPosition()
        
        # Only check for moves if the piece exists
        if piece:
            piece_color = piece.GetColor()
            piece_type  = piece.GetType()
            valid_moves = piece.GetValidMoves()

            for position_to in valid_moves:
                piece_of_opposite_color = False
                square_is_empty         = False
                # Piece to capture
                piece_to_capture = self.GetPieceInPosition(position_to)
                if piece_to_capture:
                    piece_to_capture_color  = piece_to_capture.GetColor()
                    piece_of_opposite_color = (piece_color != piece_to_capture_color)
                else:
                    square_is_empty = True
                # Check if a piece occupies a square in between two positions
                piece_is_in_between = self.PieceIsInBetween(position_from, position_to)
                
                if square_is_empty or piece_of_opposite_color:
                    # Pawn movement: pawns can only move to empty squares
                    if piece_type == "pawn":
                        if square_is_empty and not piece_is_in_between:
                            all_moves.append(position_to)
                    # Knights can jump over pieces
                    elif piece_type == "knight":
                        all_moves.append(position_to)
                    # Other piece cannot jump over pieces
                    else:
                        if not piece_is_in_between:
                            all_moves.append(position_to)
            
            # Include pawn captures
            if piece_type == "pawn":
                valid_captures = piece.GetValidCaptures()
                for position_to in valid_captures:
                    piece_of_opposite_color = False
                    # Piece to capture
                    piece_to_capture = self.GetPieceInPosition(position_to)
                    # Check if a piece occupies a square in between two positions
                    piece_is_in_between = self.PieceIsInBetween(position_from, position_to)
                    if piece_to_capture:
                        piece_to_capture_color  = piece_to_capture.GetColor()
                        piece_of_opposite_color = (piece_color != piece_to_capture_color)
                        # Pawn capture: pawns can only capture pieces of opposite color
                        if piece_of_opposite_color and not piece_is_in_between:
                            all_moves.append(position_to)
        
        return all_moves
    
    # Get legal moves for a piece
    def GetPieceLegalMoves(self, piece, player, opponent):
        legal_moves = []
        position_from = piece.GetPosition()
        possible_moves = self.GetPiecePossibleMoves(piece)
        for position_to in possible_moves:
            move_notation = self.board.GetMoveNotation(position_from, position_to)
            # Determine if a player's move would put himself in check
            move_results_in_check = self.MoveResultsInCheck(player, opponent, move_notation)
            if not move_results_in_check:
                legal_moves.append(position_to)
        return legal_moves

    # Draw legal moves for a piece based on its position; include captures
    def DrawMovesForPiece(self, primary_color, xy_position, player, opponent):
        piece = self.GetPieceInPosition(xy_position)
        piece_moves = self.GetPieceLegalMoves(piece, player, opponent)
        for move in piece_moves:
            square_position = self.board.GetSquarePosition(move)
            square_x, square_y = square_position
            
            # Highlight moves using circles
            square_side = self.board.GetSquareSide()
            center_x = square_x + 0.5 * square_side
            center_y = square_y + 0.5 * square_side
            radius = 0.40 * square_side
            self.board.DrawCircle(primary_color, center_x, center_y, radius)

    # Get a list of all of a player's pieces
    def GetPlayersPieces(self, player_color):
        pieces = []
        for x in range(8):
            for y in range(8):
                piece = self.piece_state[y][x]
                if piece:
                    piece_color = piece.GetColor()
                    # Check if piece color is the same as player color
                    if piece_color == player_color:
                        pieces.append(piece)
        return pieces
    
    # Get all possible moves for a player
    # Move contains both "from" and "to" locations
    # Format for move: "<from>_<to>" using x, y or chess notation; for example, "46_44" or "e2_e4"
    def GetPlayersPossibleMoves(self, player):
        player_moves = []
        player_color = player.GetColor()
        pieces = self.GetPlayersPieces(player_color)
        # Loop over all pieces for a player
        for piece in pieces:            
            position_from = piece.GetPosition()
            # Get possible moves for piece
            piece_moves = self.GetPiecePossibleMoves(piece)
            for position_to in piece_moves:
                move_notation = self.board.GetMoveNotation(position_from, position_to)
                player_moves.append(move_notation)
        return player_moves
    
    # Get all legal moves for a player
    # Move contains both "from" and "to" locations
    # Format for move: "<from>_<to>" using x, y or chess notation; for example, "46_44" or "e2_e4"
    def GetPlayersLegalMoves(self, player, opponent):
        player_moves = []
        player_color = player.GetColor()
        pieces = self.GetPlayersPieces(player_color)
        # Loop over all pieces for a player
        for piece in pieces:            
            position_from = piece.GetPosition()
            # Get legal moves for piece
            piece_moves = self.GetPieceLegalMoves(piece, player, opponent)
            for position_to in piece_moves:
                move_notation = self.board.GetMoveNotation(position_from, position_to)
                player_moves.append(move_notation)
        return player_moves
    
    # Get all legal captures for a player (subset of legal moves)
    def GetPlayersLegalCaptures(self, player, opponent):
        captures = []
        moves = self.GetPlayersLegalMoves(player, opponent)
        for move in moves:
            # position_from, position_to = self.board.GetMovePositions(move)
            # piece_to_capture = self.GetPieceInPosition(position_to)
            # # Check if there is a piece to capture
            # if piece_to_capture:
            #     captures.append(move)
            if self.IsCapture(move):
                captures.append(move)
        return captures

    # Determine if a move is a pawn promotion; assume the move is a legal move
    def IsPromotion(self, move):
        position_from, position_to = self.board.GetMovePositions(move)
        target_x, target_y = self.board.GetPositionXY(position_to)
        piece_to_move = self.GetPieceInPosition(position_from)
        
        piece_color     = piece_to_move.GetColor()
        piece_type      = piece_to_move.GetType()
        
        # The final row is based on the color
        final_row = {"white": 0, "black": 7}

        if piece_type == "pawn" and target_y == final_row[piece_color]:
            return True
        else:
            return False

    # Determine if a move is a capture; assume the move is a legal move
    def IsCapture(self, move):
        position_from, position_to = self.board.GetMovePositions(move)
        piece_to_capture = self.GetPieceInPosition(position_to)
        # Check if there is a piece to capture
        if piece_to_capture:
            return True
        else:
            return False
        
    # Determine if a move put the opponent in check; assume the move is a legal move
    def IsCheck(self, move):
        current_player  = self.GetCurrentPlayer()
        opposing_player = self.GetOpposingPlayer()
        position_from, position_to = self.board.GetMovePositions(move)
        piece_to_move       = self.GetPieceInPosition(position_from)
        piece_to_capture    = self.GetPieceInPosition(position_to)
        
        self.MakeMove(move)
        result = self.PlayerIsInCheck(opposing_player, current_player)
        self.UndoMove(move, piece_to_move, piece_to_capture)
        
        return result

    # Get position of player's king
    def GetPlayersKingPosition(self, player):
        king_position = []
        player_color    = player.GetColor()
        player_pieces   = self.GetPlayersPieces(player_color)
        for piece in player_pieces:
            piece_type = piece.GetType()
            if piece_type == "king":
                king_position = piece.GetPosition()
                # Return now to speed up
                return king_position
        
        return king_position

    # Define check!
    # - The player's king is under attack
    # - Pinned pieces (pinned to a king) can still deliver check
    def PlayerIsInCheck(self, player, opponent):
        result = False
        king_position = self.GetPlayersKingPosition(player)
        king_position_string = self.board.GetPositionString(king_position)
        # Get opponent's possible moves (not legal moves); pinned pieces still apply check!
        opponent_possible_moves = self.GetPlayersPossibleMoves(opponent)

        # Loop over opponent's possible moves and captures
        for move in opponent_possible_moves:
            split_move = move.split("_")
            move_start, move_end = split_move
            # Determine if opponent can capture the player's king
            if move_end == king_position_string:
                result = True
                # Return now to speed up
                return result

        return result
    
    # Define checkmate!!
    # - Player is in check
    # - Player has no legal moves
    def PlayerIsInCheckmate(self, player, opponent):
        result = False
        
        player_is_in_check = self.PlayerIsInCheck(player, opponent)
        legal_moves = self.GetPlayersLegalMoves(player, opponent)
        n_legal_moves = len(legal_moves)
        
        if player_is_in_check and n_legal_moves == 0:
            result = True
        
        return result
    
    # Define stalemate...
    # - Player is not in check
    # - Player has not legal moves
    def PlayerIsInStalemate(self, player, opponent):
        result = False

        player_is_in_check = self.PlayerIsInCheck(player, opponent)
        legal_moves = self.GetPlayersLegalMoves(player, opponent)
        n_legal_moves = len(legal_moves)

        if not player_is_in_check and n_legal_moves == 0:
            result = True

        return result
    
    # Define game over conditions.
    def GameIsOver(self, player, opponent):
        result = False
        
        if self.PlayerIsInCheckmate(player, opponent):
            result = True
        
        if self.PlayerIsInStalemate(player, opponent):
            result = True
        
        return result

    # Determine if a player's move would put himself in check
    # - Get piece to capture (if any).
    # - Move piece (updates state and piece state).
    # - After move, check if player is in check.
    # - Move piece back to original position (updates state and piece state).
    # - If there was a piece to capture for this move, put it back and update state.
    # - Does not apply pawn promotion; this should be ok...
    # FIXME: update with MakeMove and UndoMove functions
    def MoveResultsInCheck(self, player, opponent, move_notation):
        result = False
        reverse_move = self.board.GetReverseMove(move_notation)
        position_from, position_to = self.board.GetMovePositions(move_notation)

        # Piece to capture
        piece_to_capture = self.GetPieceInPosition(position_to)
        
        # Move piece to test new game state
        self.MovePiece(move_notation)
        
        # Determine if player is now in check after move
        result = self.PlayerIsInCheck(player, opponent)

        # Reverse move
        self.MovePiece(reverse_move)
        # If there was a piece to capture, put it back
        if piece_to_capture:
            self.PlacePiece(piece_to_capture)
            self.SetStateFromPieceState()
        
        return result

    # Get piece type based on value
    def GetPieceType(self, value):
        result = ""

        if self.PieceIsValid(value):
            abs_value = abs(value)
            result = self.chess_pieces[abs_value]
        else:
            print("ERROR: The value {0} does not represent a valid piece.".format(value))

        return result

    # Get full name of piece (color and type) based on value
    def GetPieceName(self, value):
        # Get piece type
        result = self.GetPieceType(value)
        
        # Assign white or black based on sign
        if value > 0:
            result = "white {0}".format(result)
        elif value < 0:
            result = "black {0}".format(result)
        
        return result
    
    # Get piece object in position
    def GetPieceInPosition(self, position):
        x = position[0]
        y = position[1]
        piece = self.piece_state[y][x]
        return piece

    # Get piece value in position
    def GetPieceValueInPosition(self, position):
        x = position[0]
        y = position[1]
        # note: index with y first (rows), then x (columns)
        piece_value = self.state[y][x]
        return piece_value
    
    # Get piece name in position
    def GetPieceNameInPosition(self, position):        
        piece = self.GetPieceInPosition(position)
        piece_name = piece.GetName()
        return piece_name

    # Print types of pieces
    def PrintPieceTypes(self):
        # Print types of pieces
        for i in range(-6, 7):
            print("{0}: {1}".format(i, self.GetPieceName(i)))

def main():
    state = State(None, None, None)
    state.PrintState()
    state.SetInitialState()
    state.PrintState()
    state.PrintPieceTypes()

if __name__ == "__main__":
    main()
