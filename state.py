# State class

# Save the current game state
# - Use 8x8 matrix to represent squares on chess board
# - White pieces are positive
# - Black pieces are negative
# - 0: empty squares are 0
# - 1: pawn
# - 2: knight
# - 3: bishop
# - 4: rook
# - 5: queen
# - 6: king

class State:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return str(self.state)

    def GetState(self):
        return self.state

    def SetState(self, state):
        self.state = state

    def PrintState(self):
        print("State: {0}".format(self.state))

def main():
    state = State("Tacos.")
    state.PrintState()
    state.SetState("Burritos.")
    print("State: {0}".format(state.GetState()))
    print("State: {0}".format(state))

if __name__ == "__main__":
    main()
