# Board class

# TODO:
# DONE:
# - Define a mapping between x, y coordinates and chess notation coordinates
# - Define valid x, y coordinates
# - Define valid chess notation
# - Fix bug: x, y coordinates (rows, columns) are inverted for notation!

class Board:
    def __init__(self):
        return

    # get chess notation for given x, y coordinates
    # example: input = [2, 3], output = "c5"
    def GetChessNotation(self, location):
        chess_notation = None
        
        # check for valid location:
        if not self.locationIsValid(location):
            print("ERROR: The location [x, y] = {0} is not valid!".format(location))
            return chess_notation

        x = location[0]
        y = location[1]
        
        # chess notation
        # column: letters "a" to "h", starting from the left column
        # row:    integers 1 to 8, starting from the bottom row
        # columns correspond to x coordinate!
        # rows correspond to y coordinate!
        # Notation is written as column + row
        column = chr(ord('a') + x)
        row = str(8 - y)
        chess_notation = column + row
        return chess_notation
    
    # get x, y coordinates based on chess notation
    # example: input = "c5", output = [2, 3]
    def GetXY(self, chess_notation):
        x, y = None, None
        
        # check for valid notation:
        if not self.notationIsValid(chess_notation):
            print("ERROR: The chess notation coordinate '{0}' is not valid!".format(chess_notation))
            return [x, y]
        
        column = chess_notation[0]
        row    = chess_notation[1]
        
        # invert the conversion to notation; solve for x and y
        x = ord(column) - ord('a')
        y = 8 - int(row)

        return [x, y]
    
    # check if location coordinate (x, y) is valid
    def locationIsValid(self, location):
        if not location:
            return False
        if len(location) != 2:
            return False
        
        x = location[0]
        y = location[1]        
        if x < 0 or y < 0:
            return False
        if x > 7 or y > 7:
            return False
        return True
    
    # check if chess notation coordinate is valid
    def notationIsValid(self, chess_notation):
        if not chess_notation:
            return False
        if len(chess_notation) != 2:
            return False
        
        column = chess_notation[0]
        row    = chess_notation[1]
        
        # columns: "a" to "h"
        try:
            if ord(column) < ord('a') or ord(column) > ord('h'):
                return False
        except TypeError:
            return False
        
        # rows: 1 to 8
        try:
            if int(row) < 1 or int(row) > 8:
                return False
        except ValueError:
            return False
        
        return True
    

def main():
    board = Board()
    #location = [0, 0]
    #location = [7, 7]
    location = [2, 3]
    #location = [4, 3]
    #location = [4, 4]
    chess_notation = board.GetChessNotation(location)
    xy = board.GetXY(chess_notation)
    print("{0}: {1}".format(location, chess_notation))
    print("{0}: {1}".format(chess_notation, xy))
    
    chess_notation = "c5"
    xy = board.GetXY(chess_notation)
    print("{0}: {1}".format(chess_notation, xy))

if __name__ == "__main__":
    main()
