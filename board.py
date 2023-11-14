# Board class

class Board:
    def __init__(self):
        return

    # get chess notation for given x, y coordinates
    # example: input = [2, 3], output = "d6"
    def GetChessNotation(self, location):
        chess_notation = None
        x = location[0]
        y = location[1]
        
        # check for valid location:
        if not self.locationIsValid(location):
            print("ERROR: The location [x, y] = {0} is not valid!".format(location))
            return chess_notation
        # chess notation
        # row:    integers 1 to 8, starting from the bottom row
        # column: letters "a" to "h", starting from the left column
        # Written as column + row
        row = str(8 - x)
        column = chr(ord('a') + y)
        chess_notation = column + row
        return chess_notation
    
    # get x, y coordinates based on chess notation
    def GetXY(self, chess_notation):
        x, y = None, None
        return [x, y]
    
    def locationIsValid(self, location):
        x = location[0]
        y = location[1]        
        if x < 0 or y < 0:
            return False
        if x > 7 or y > 7:
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
    print("{0}: {1}".format(location, chess_notation))

if __name__ == "__main__":
    main()
