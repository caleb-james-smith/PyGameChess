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
# - Connect "state" and "piece_state"
# - Eventually, only use "piece_state" (contains piece objects)
# - Make function to get "state" (values) from "piece_state" (objects)
# DONE:
# - Create a class for the game state
# - Define numbers and names for chess pieces
# - Create a class for the chess board
# - Make function to set initial piece state

from piece import Pawn, Knight, Bishop, Rook, Queen, King

# Class to define current game state (piece positions)
class State:
    def __init__(self, board, state=None, piece_state=None):
        self.board = board
        self.state = state
        self.piece_state = piece_state
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
    
    # Check if piece has a valid value
    def PieceIsValid(self, value):
        abs_value = abs(value)
        if abs_value in self.pieces:
            return True
        else:
            return False
    
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
            #Rook("white",   [0, 7]),
            #Knight("white", [1, 7]),
            #Bishop("white", [2, 7]),
            #Queen("white",  [3, 7]),
            #King("white",   [4, 7]),
            #Bishop("white", [5, 7]),
            #Knight("white", [6, 7]),
            #Rook("white",   [7, 7]),
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
            #Rook("black",   [0, 0]),
            #Knight("black", [1, 0]),
            #Bishop("black", [2, 0]),
            #Queen("black",  [3, 0]),
            #King("black",   [4, 0]),
            #Bishop("black", [5, 0]),
            #Knight("black", [6, 0]),
            #Rook("black",   [7, 0]),
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

    # FIXME: use light and dark colors
    def DrawPieces(self, game, screen, squares_per_side, square_side):
        # Draw pieces
        for x in range(squares_per_side):
            for y in range(squares_per_side):
                # Get piece based on position
                position = [x, y]
                piece = self.GetPieceInPosition(position)
                # Skip empty squares
                if not piece:
                    continue
                piece.Draw(game, screen, square_side)

    
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
        # Get value of piece in "from" position
        value = self.GetPieceValueInPosition(position_from)
        # Set "from" position to 0 for empty
        self.SetValue(position_from, 0)
        # Set "to" position to value of piece
        self.SetValue(position_to, value)

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
