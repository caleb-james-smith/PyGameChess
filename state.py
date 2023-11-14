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

# class to define current game state (piece positions)
class State:
    def __init__(self, state=None):
        self.state = state
        # chess pieces
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

    # print the state with pretty formatting
    def PrintState(self):
        # number of dashes to match length of row string
        n_dashes = (8 * 3) - 1
        line = n_dashes * "-"

        print("State:")
        if self.state:
            print(line)
            for row in self.state:
                # fill with whitespace using string rjust()
                # forces positive and negative ints < 10 to use the same width
                row_formatted = [str(value).rjust(2) for value in row]
                row_string = ",".join(row_formatted)
                print(row_string)
            print(line)
        else:
            print(self.state)

    # set initial state (starting position)
    def SetInitialState(self):
        # initial state: chess starting position
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

    # get name of piece based on value
    def GetPieceName(self, value):
        result = ""
        
        # get name of piece based on value; use absolute value
        abs_value = abs(value)
        if abs_value in self.pieces:
            result = self.pieces[abs_value]
        else:
            print("ERROR: The value {0} does not represent a valid piece.".format(abs_value))
            return
        
        # assign white or black based on sign
        if value > 0:
            result = "white {0}".format(result)
        elif value < 0:
            result = "black {0}".format(result)
        
        return result
    
    # print types of pieces
    def PrintPieceTypes(self):
        # print types of pieces
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
