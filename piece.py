# Piece class and subclasses

# TODO:
# - Define how each type of piece is drawn
# - Define how each piece can move
# DONE:
# - Create piece class (superclass or base class)
# - Create subclass for each type of piece

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
    
    def PieceIsValid(self):
        abs_value = abs(self.value)
        if abs_value in self.chess_pieces:
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
    
    def SetupValueAndName(self, value):
        # first, set value
        sign = self.GetSign()
        self.SetValue(sign * value)
        # next, set name; value must already be set
        name = self.GetPieceName()
        self.SetName(name)
    
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(1)
    
    def Draw(self, game, screen, color, x_position, y_position, size):
        # pawn: small triangle
        points = [(x_position - size, y_position + size), (x_position + size, y_position + size), (x_position, y_position - size)]
        game.draw.polygon(screen, color, points, 0)
    
class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(2)

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(3)

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(4)

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(5)

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.SetupValueAndName(6)
