# Board class

# TODO:
# DONE:
# - Define a mapping between x, y coordinates and chess notation coordinates
# - Define valid x, y coordinates
# - Define valid chess notation
# - Fix bug: x, y coordinates (rows, columns) are inverted for notation!
# - Write function to return squares that are in between two positions

# Round using a base
def round_using_base(number, base):
    result = number - (number % base)
    return result

# Get integers between two integers
def get_numbers_between_numbers(a, b):
    numbers = []
    if a == b:
        return numbers
    elif a < b:
        numbers = [x for x in range(a + 1, b)]
    elif a > b:
        numbers = [x for x in range(b + 1, a)]
    return numbers

class Board:
    def __init__(self, game, screen, light_color, dark_color, squares_per_side, square_side):
        self.game               = game
        self.screen             = screen
        self.light_color        = light_color
        self.dark_color         = dark_color
        self.squares_per_side   = squares_per_side
        self.square_side        = square_side

    # Get square color based on x, y coordinate indices
    def GetSquareColor(self, x, y):
        # Use parity to determine square color
        parity = (x + y) % 2
        # Odd parity: dark color
        if parity:
            return self.dark_color
        # Even parity: light color
        else:
            return self.light_color

    # Draw a solid square
    # x_position: x position measured from left edge
    # y_position: y position measured from top edge
    def DrawSquare(self, color, x_position, y_position):
        self.game.draw.rect(self.screen, color, [x_position, y_position, self.square_side, self.square_side], 0)

    # Draw the board
    def DrawBoard(self):
        # Draw squares
        for x in range(self.squares_per_side):
            for y in range(self.squares_per_side):
                # Get square color
                color = self.GetSquareColor(x, y)
                # Get square position
                x_position = x * self.square_side
                y_position = y * self.square_side
                # Draw square
                self.DrawSquare(color, x_position, y_position)

    # Get position of clicked square based on click position
    def GetClickedSquare(self, click_position):
        click_x = click_position[0]
        click_y = click_position[1]
        # Find square x, y based on click x, y;
        # round using the side length as the base.
        square_x = round_using_base(click_x, self.square_side)
        square_y = round_using_base(click_y, self.square_side)
        return [square_x, square_y]
    
    # Get x, y coordinates (ints) based on square x, y position
    def GetSquareXYCoords(self, square_position):
        square_x = square_position[0]
        square_y = square_position[1]
        # Use integer division
        x = square_x // self.square_side
        y = square_y // self.square_side
        return [x, y]
    
    # Get chess notation for given x, y coordinates
    # Example: input = [2, 3], output = "c5"
    def GetChessNotation(self, location):
        chess_notation = None
        
        # Check for valid location:
        if not self.LocationIsValid(location):
            print("ERROR: The location [x, y] = {0} is not valid!".format(location))
            return chess_notation

        x = location[0]
        y = location[1]
        
        # Chess notation
        # column: letters "a" to "h", starting from the left column
        # row:    integers 1 to 8, starting from the bottom row
        # columns correspond to x coordinate!
        # rows correspond to y coordinate!
        # Notation is written as column + row
        column = chr(ord('a') + x)
        row = str(8 - y)
        chess_notation = column + row
        return chess_notation
    
    # Get x, y coordinates based on chess notation
    # Example: input = "c5", output = [2, 3]
    def GetXY(self, chess_notation):
        x, y = None, None
        
        # Check for valid notation:
        if not self.NotationIsValid(chess_notation):
            print("ERROR: The chess notation coordinate '{0}' is not valid!".format(chess_notation))
            return [x, y]
        
        column = chess_notation[0]
        row    = chess_notation[1]
        
        # Invert the conversion to notation; solve for x and y
        x = ord(column) - ord('a')
        y = 8 - int(row)

        return [x, y]
    
    # Check if location coordinate (x, y) is valid
    def LocationIsValid(self, location):
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
    
    # Check if chess notation coordinate is valid
    def NotationIsValid(self, chess_notation):
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
    
    # Get squares that are in between two positions
    # In between squares only exist for positions in the same column, row, or diagonal
    def GetInBetweenSquares(self, position_1, position_2):
        squares = []
        if self.LocationIsValid(position_1) and self.LocationIsValid(position_2):
            x_1, y_1 = position_1
            x_2, y_2 = position_2
            x_diff = x_2 - x_1
            y_diff = y_2 - y_1
            # If the positions are the same, there are no in between squares
            if x_diff == 0 and y_diff == 0:
                return squares
            else:
                # Get in between x and y values
                x_values = get_numbers_between_numbers(x_1, x_2)
                y_values = get_numbers_between_numbers(y_1, y_2)
                # Positions are in the same column
                if x_diff == 0:
                    squares = [[x_1, y] for y in y_values]
                # Positions are in the same row
                elif y_diff == 0:
                    squares = [[x, y_1] for x in x_values]
                # Positions are in the same diagonal
                elif abs(x_diff) == abs(y_diff):
                    # Reverse y values for opposite diagonal cases
                    if x_diff * y_diff < 0:
                        y_values.reverse()
                    squares = [[x_values[i], y_values[i]] for i in range(len(x_values))]
        return squares

def main():
    board = Board()
    #location = [0, 0]
    #location = [7, 7]
    #location = [2, 3]
    location = [3, 2]
    #location = [4, 3]
    #location = [4, 4]
    chess_notation = board.GetChessNotation(location)
    xy = board.GetXY(chess_notation)
    print("{0}: {1}".format(location, chess_notation))
    print("{0}: {1}".format(chess_notation, xy))
    
    chess_notation = "d6"
    xy = board.GetXY(chess_notation)
    print("{0}: {1}".format(chess_notation, xy))

if __name__ == "__main__":
    main()
