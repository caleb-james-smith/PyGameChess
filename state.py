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
    def __init__(self, state):
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
        print("State: {0}".format(self.state))

    def GetName(self, value):
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

def main():
    state = State("Checkers")
    state.PrintState()
    state.SetState("Chess")
    print("State: {0}".format(state.GetState()))
    print("State: {0}".format(state))
    for i in range(-10, 11):
        print("{0}: {1}".format(i, state.GetName(i)))

if __name__ == "__main__":
    main()
