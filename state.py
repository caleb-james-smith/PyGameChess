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

    def PrintState(self):
        print("State:")
        if self.state:
            for row in self.state:
                print(row)
        else:
            print(self.state)

    def SetInitialState(self):
        state = [
            [-4, -2, -3, -5, -6, -3, -2, -4],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [4, 2, 3, 5, 6, 3, 2, 4]
        ]
        self.SetState(state)

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
