# Board class

import tools

class Board:
    def __init__(self, game, screen, light_color, dark_color, squares_per_side, square_side):
        self.game               = game
        self.screen             = screen
        self.light_color        = light_color
        self.dark_color         = dark_color
        self.squares_per_side   = squares_per_side
        self.square_side        = square_side

    # Get squares per side
    def GetSquaresPerSide(self):
        return self.squares_per_side
    
    # Get square side
    def GetSquareSide(self):
        return self.square_side
    
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
    def DrawSquare(self, color, x_position, y_position, side_length=None):
        # Default: if side length is not specified, use the standard square side length
        if not side_length:
            side_length = self.square_side
        self.game.draw.rect(self.screen, color, [x_position, y_position, side_length, side_length], 0)

    # Draw a solid circle
    # x_position: x position measured from left edge
    # y_position: y position measured from top edge
    def DrawCircle(self, color, x_position, y_position, radius):
        self.game.draw.circle(self.screen, color, [x_position, y_position], radius, 0)

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
        square_x = tools.round_using_base(click_x, self.square_side)
        square_y = tools.round_using_base(click_y, self.square_side)
        return [square_x, square_y]
    
    # Get x, y coordinates (ints) based on square x, y position
    def GetSquareXYCoords(self, square_position):
        square_x = square_position[0]
        square_y = square_position[1]
        # Use integer division
        x = square_x // self.square_side
        y = square_y // self.square_side
        return [x, y]
    
    # Get square position based on x, y coordinates (ints)
    def GetSquarePosition(self, xy_position):
        x = xy_position[0]
        y = xy_position[1]
        square_x = x * self.square_side
        square_y = y * self.square_side
        return [square_x, square_y]
    
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
    
    # Given start and end (from and to) x, y positions, return move notation
    # Input: position from [x1, y1] and position to [x2, y2]
    # Output: string representing move "x1y1_x2y2"
    # Move notation: "<from>_<to>", "x1y1_x2y2"
    # For example, given [4, 6] and [4, 4], return "46_44"
    def GetMoveNotation(self, position_from, position_to):
        x1, y1 = position_from
        x2, y2 = position_to
        result = "{0}{1}_{2}{3}".format(x1, y1, x2, y2)
        return result
    
    # Given move notation, return start and end (from and to) x, y positions
    # Input: string representing move "x1y1_x2y2"
    # Output: position from [x1, y1] and position to [x2, y2]
    def GetMovePositions(self, move_notation):
        split_move = move_notation.split("_")
        move_start  = split_move[0]
        move_end    = split_move[1]
        x1 = int(move_start[0])
        y1 = int(move_start[1])
        x2 = int(move_end[0])
        y2 = int(move_end[1])
        position_from   = [x1, y1]
        position_to     = [x2, y2]
        return position_from, position_to
    
    # Reverse move using move notation
    # Input: string representing move "x1y1_x2y2"
    # Output: reversed move "x2y2_x1y1"
    def GetReverseMove(self, move_notation):
        reverse_move = ""
        split_move = move_notation.split("_")
        move_start  = split_move[0]
        move_end    = split_move[1]
        reverse_move = "{0}_{1}".format(move_end, move_start)
        return reverse_move

    # Get position string
    # Input: position as list [x, y]
    # Output: position as string "xy"
    def GetPositionString(self, position_list):
        result = ""
        # Ensure that position is not empty
        if position_list:
            x, y = position_list
            result = "{0}{1}".format(x, y)
        return result
    
    # Get position x, y
    # Input: position as string "xy"
    # Output: position as list [x, y]
    def GetPositionXY(self, position_string):
        result = []
        # Ensure that position is not empty
        if position_string:
            x, y = position_string
            result = [int(x), int(y)]
        return result

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
                x_values = tools.get_numbers_between_numbers(x_1, x_2)
                y_values = tools.get_numbers_between_numbers(y_1, y_2)
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
