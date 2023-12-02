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
        # Chess pieces
        self.pieces = {
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

    # Switch current player to opposite player
    def SwitchTurn(self):
        if self.current_player == self.white_player:
            self.current_player = self.black_player
        elif self.current_player == self.black_player:
            self.current_player = self.white_player
    
    # Check if piece has a valid value
    def PieceIsValid(self, value):
        abs_value = abs(value)
        if abs_value in self.pieces:
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
                # Forces positive and negative ints < 10 to use the same width
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
                color = None
                if piece_color == "white":
                    color = light_color
                if piece_color == "black":
                    color = dark_color

                # Get piece position: note that this is different than the square position
                x_position = (x + 0.5) * square_side
                y_position = (y + 0.5) * square_side
                # Piece size should be smaller than square side
                size = square_side / 4
                # Draw piece (border color)
                piece.Draw(game, screen, border_color, x_position, y_position, size)
                # Draw piece (primary color)
                piece.Draw(game, screen, color, x_position, y_position, 0.75 * size)
    
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
    def MovePiece(self, position_from, position_to):
        x_from, y_from = position_from
        x_to, y_to     = position_to
        
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
    
    # Get name of piece based on value
    def GetPieceName(self, value):
        result = ""
        
        # Get name of piece based on value; use absolute value
        if self.PieceIsValid(value):
            abs_value = abs(value)
            result = self.pieces[abs_value]
        else:
            print("ERROR: The value {0} does not represent a valid piece.".format(value))
            return result
        
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
        piece_value = self.GetPieceValueInPosition(position)
        piece_name  = self.GetPieceName(piece_value)
        return piece_name

    # Print types of pieces
    def PrintPieceTypes(self):
        # Print types of pieces
        for i in range(-6, 7):
            print("{0}: {1}".format(i, self.GetPieceName(i)))

def main():
    state = State()
    state.PrintState()
    state.SetInitialState()
    state.PrintState()
    state.PrintPieceTypes()

if __name__ == "__main__":
    main()
