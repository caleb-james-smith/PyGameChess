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

# TODO:
# - Make function to get "state" (values) from "piece_state" (objects)
# DONE:
# - Create a class for the game state
# - Define numbers and names for chess pieces
# - Create a class for the chess board
# - Make function to set initial piece state
# - Write function to determine if there are any pieces on squares between two positions
# - At the start of game, set state based on piece state
# - After any move, update state based on piece state
# - Make a function to get a list of all a player's pieces
# - Make a function to get possible moves for a piece with constraints:
#   no jumping, no capturing own pieces, pawn movement and captures.
# - Track opposing player
# - Make function to convert [x, y] position to "xy" string
# - Make function to get the position of a player's king

from piece import Pawn, Knight, Bishop, Rook, Queen, King

# Class to define current game state (piece positions)
class State:
    def __init__(self, board, white_player, black_player):
        self.board = board
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

    # Switch current and opposing players
    def SwitchTurn(self):
        if self.current_player == self.white_player:
            self.current_player = self.black_player
            self.opposing_player = self.white_player
        elif self.current_player == self.black_player:
            self.current_player = self.white_player
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
        # Note: index with y first (rows), then x (columns)
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
                # Draw piece (border color)
                piece.Draw(game, screen, border_color, x_position, y_position, size)
                # Draw piece (primary color)
                piece.Draw(game, screen, primary_color, x_position, y_position, 0.75 * size)
    
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
        print("In MovePiece(): move_notation: {0}".format(move_notation))
        print("In MovePiece(): position_from: {0}, position_to: {1}".format(position_from, position_to))
        
        # Get piece in "from" position
        piece = self.GetPieceInPosition(position_from)
        
        # Set "from" position to None for empty
        self.piece_state[y_from][x_from] = None
        
        # Set "to" position to piece and update piece position
        self.piece_state[y_to][x_to] = piece
        piece.SetPosition(position_to)

        # Update state based on piece state
        self.SetStateFromPieceState()

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
    
    # Draw possible moves for a piece based on its position; include captures
    def DrawMovesForPiece(self, primary_color, xy_position):        
        piece = self.GetPieceInPosition(xy_position)
        piece_moves = self.GetPiecePossibleMoves(piece)
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
        all_moves = []
        player_color = player.GetColor()
        pieces = self.GetPlayersPieces(player_color)
        # Loop over all pieces for a player
        for piece in pieces:            
            position_from = piece.GetPosition()
            piece_moves = self.GetPiecePossibleMoves(piece)
            for position_to in piece_moves:
                move_notation = self.board.GetMoveNotation(position_from, position_to)
                all_moves.append(move_notation)
        return all_moves

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
    def PlayerIsInCheck(self, player, opponent):
        result = False
        king_position = self.GetPlayersKingPosition(player)
        king_position_string = self.board.GetPositionString(king_position)
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
    
    # TODO
    # FIXME: Fix bug: program crashes when MoveResultsInCheck() is used
    # - Could be from not resetting piece object position!
    # - Could be if original piece state points to the original object or is a copy.
    # - One solution to revert (undo) a move:
    #   Record captured piece (if any) and put it back.
    #   Move the moved piece back to the original position.
    #   Test to make sure that piece state, state, piece positions were reverted.
    # Determine if a player's move would put himself in check
    def MoveResultsInCheck(self, player, opponent, move_notation):
        result = False
        
        # Save a copy of the original piece state
        original_piece_state = self.GetPieceState()
        
        # Move piece to test new game state
        self.MovePiece(move_notation)
        
        # Determine if player is now in check after move
        result = self.PlayerIsInCheck(player, opponent)
        
        # Revert to original piece state
        self.SetPieceState(original_piece_state)
        
        # Update state based on piece state
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
