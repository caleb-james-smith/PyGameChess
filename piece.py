# Piece class and subclasses

# TODO:
# DONE:
# - Create piece class (superclass or base class)
# - Create subclass for each type of piece
# - Define how each type of piece is drawn
# - Define how each piece can move

class Piece:
    def __init__(self, color, position):
        self.color      = color
        self.position   = position
        self.value      = None
        self.name       = None
        self.chess_pieces = {
            0: "empty",
            1: "pawn",
            2: "knight",
            3: "bishop",
            4: "rook",
            5: "queen",
            6: "king"            
        }

    def GetColor(self):
        return self.color
    
    def SetColor(self, color):
        self.color = color

    def GetPosition(self):
        return self.position

    def SetPosition(self, position):
        self.position = position
    
    def GetValue(self):
        return self.value
    
    def SetValue(self, value):
        self.value = value
    
    def GetName(self):
        return self.name
    
    def SetName(self, name):
        self.name = name
    
    # Determine if piece value is valid
    def PieceIsValid(self):
        abs_value = abs(self.value)
        if abs_value in self.chess_pieces:
            return True
        else:
            return False

    # Determine if moving to a position is valid    
    def MoveIsValid(self, position_to):
        moves = self.GetValidMoves()
        if position_to in moves:
            return True
        else:
            return False

    def GetSign(self):
        if self.color == "white":
            return 1
        elif self.color == "black":
            return -1
        else:
            print("ERROR: The color '{0}' is not valid!".format(self.color))
            return None
    
    # Get piece name based on value
    def GetPieceName(self):
        result = ""
        
        # Get name of piece based on value; use absolute value
        if self.PieceIsValid():
            abs_value = abs(self.value)
            result = self.chess_pieces[abs_value]
        else:
            print("ERROR: The value {0} does not represent a valid chess piece.".format(self.value))
            return result
        
        # Assign white or black based on sign
        if self.value > 0:
            result = "white {0}".format(result)
        elif self.value < 0:
            result = "black {0}".format(result)
        
        return result
    
    # Set piece value and name
    def SetupValueAndName(self, value):
        # first, set value
        sign = self.GetSign()
        self.SetValue(sign * value)
        # next, set name; value must already be set
        name = self.GetPieceName()
        self.SetName(name)
    
# Drawing pieces
# x_position: x position measured from left edge
# y_position: y position measured from top edge
# When drawing, recall that positive x is to the right and positive y is down.
#
# Piece Shapes
# - pawn:   small triangle
# - knight: triangle pointing left
# - bishop: tall triangle
# - rook:   tall rectangle
# - queen:  pentagon
# - king:   square

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(1)
    
    def Draw(self, game, screen, color, x_position, y_position, size):
        # pawn: small triangle
        points = [(x_position - size, y_position + size), (x_position + size, y_position + size), (x_position, y_position - size)]
        game.draw.polygon(screen, color, points, 0)
    
    # Get valid moves
    # - Constrained to an empty board
    # - Independent of other pieces (empty board)
    def GetValidMoves(self):
        moves = []
        color = self.GetColor()
        position = self.GetPosition()
        piece_x, piece_y = position
        # Movement for pawn
        # Assume white pawns move up (decreasing y)
        if color == "white":
            for y in range(8):
                y_diff = y - piece_y
                # Move forward one square
                if y_diff == -1:
                    moves.append([piece_x, y])
                # Move forward two squares
                if piece_y == 6:
                    if y_diff == -2:
                        moves.append([piece_x, y])
        # Assume black pawns move down (increasing y)
        if color == "black":
            for y in range(8):
                y_diff = y - piece_y
                # Move forward one square
                if y_diff == 1:
                    moves.append([piece_x, y])
                # Move forward two squares
                if piece_y == 1:
                    if y_diff == 2:
                        moves.append([piece_x, y])
        return moves

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(2)

    def Draw(self, game, screen, color, x_position, y_position, size):
        # knight: triangle pointing left
        points = [(x_position + size, y_position - 1.5 * size), (x_position + size, y_position + 1.5 * size), (x_position - size, y_position)]
        game.draw.polygon(screen, color, points, 0)

    # Get valid moves
    # - Constrained to an empty board
    # - Independent of other pieces (empty board)
    def GetValidMoves(self):
        moves = []
        position = self.GetPosition()
        piece_x, piece_y = position
        # Movement for knight
        # Check all x, y positions on the board
        for x in range(8):
            for y in range(8):
                x_diff = x - piece_x
                y_diff = y - piece_y
                if (abs(x_diff) == 2 and abs(y_diff) == 1) or (abs(x_diff) == 1 and abs(y_diff) == 2):
                    # Cannot move to current position
                    if not (x_diff == 0 and y_diff == 0):
                        moves.append([x, y])
        return moves

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(3)

    def Draw(self, game, screen, color, x_position, y_position, size):
        # bishop: tall triangle
        points = [(x_position - size, y_position + 1.5 * size), (x_position + size, y_position + 1.5 * size), (x_position, y_position - 1.5 * size)]
        game.draw.polygon(screen, color, points, 0)

    # Get valid moves
    # - Constrained to an empty board
    # - Independent of other pieces (empty board)
    def GetValidMoves(self):
        moves = []
        position = self.GetPosition()
        piece_x, piece_y = position
        # Movement for bishop
        # Check all x, y positions on the board
        for x in range(8):
            for y in range(8):
                x_diff = x - piece_x
                y_diff = y - piece_y
                if abs(x_diff) == abs(y_diff):
                    # Cannot move to current position
                    if not (x_diff == 0 and y_diff == 0):
                        moves.append([x, y])
        return moves

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(4)

    def Draw(self, game, screen, color, x_position, y_position, size):
        # rook: tall rectangle
        points = [(x_position - size, y_position - 1.5 * size), (x_position + size, y_position - 1.5 * size), (x_position + size, y_position + 1.5 * size), (x_position - size, y_position + 1.5 * size)]
        game.draw.polygon(screen, color, points, 0)

    # Get valid moves
    # - Constrained to an empty board
    # - Independent of other pieces (empty board)
    def GetValidMoves(self):
        moves = []
        position = self.GetPosition()
        piece_x, piece_y = position
        
        # Movement for rook
        for x in range(8):
            # Cannot move to current position
            if not x == piece_x:
                moves.append([x, piece_y])
        for y in range(8):
            # Cannot move to current position
            if not y == piece_y:
                moves.append([piece_x, y])
        return moves
    
class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(5)

    def Draw(self, game, screen, color, x_position, y_position, size):
        # queen: pentagon
        points = [(x_position - size, y_position + 1.5 * size), (x_position - 1.5 * size, y_position), (x_position, y_position - 1.5 * size), (x_position + 1.5 * size, y_position), (x_position + size, y_position + 1.5 * size)]
        game.draw.polygon(screen, color, points, 0)

    # Get valid moves
    # - Constrained to an empty board
    # - Independent of other pieces (empty board)
    def GetValidMoves(self):
        moves = []
        position = self.GetPosition()
        piece_x, piece_y = position
        # Movement for queen
        # Check all x, y positions on the board
        for x in range(8):
            for y in range(8):
                x_diff = x - piece_x
                y_diff = y - piece_y
                if abs(x_diff) == abs(y_diff) or x_diff == 0 or y_diff == 0:
                    # Cannot move to current position
                    if not (x_diff == 0 and y_diff == 0):
                        moves.append([x, y])
        return moves

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(6)

    def Draw(self, game, screen, color, x_position, y_position, size):
        # king: square
        points = [(x_position - size, y_position - size), (x_position + size, y_position - size), (x_position + size, y_position + size), (x_position - size, y_position + size)]
        game.draw.polygon(screen, color, points, 0)

    # Get valid moves
    # - Constrained to an empty board
    # - Independent of other pieces (empty board)
    def GetValidMoves(self):
        moves = []
        position = self.GetPosition()
        piece_x, piece_y = position
        # Movement for king
        # Check all x, y positions on the board
        for x in range(8):
            for y in range(8):
                x_diff = x - piece_x
                y_diff = y - piece_y
                if abs(x_diff) <= 1 and abs(y_diff) <= 1:
                    # Cannot move to current position
                    if not (x_diff == 0 and y_diff == 0):
                        moves.append([x, y])
        return moves
