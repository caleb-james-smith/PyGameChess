# Play chess
# - Two computer players on one computer.

# Import the pygame library
import pygame
import time
from board import Board
from state import State
from player import Player
from agent import AgentRandom, AgentCapture

# Run the game
def run_game():
    # Define colors
    PURE_WHITE          = (255, 255, 255)
    PURE_BLACK          = (0, 0, 0)
    BOARD_LIGHT_COLOR   = (233, 237, 204)
    BOARD_DARK_COLOR    = (119, 153, 84)
    PIECE_LIGHT_COLOR   = (248, 248, 248)
    PIECE_DARK_COLOR    = (85, 83, 82)
    PIECE_BORDER_COLOR  = PURE_BLACK
    CLICK_COLOR_EMPTY   = (255, 113, 113)
    CLICK_COLOR_PIECE   = (74, 126, 176)
    CLICK_COLOR_MOVES   = (91, 175, 255)

    # Set up the drawing window (screen)
    #SCREEN_WIDTH        = 800
    #SCREEN_HEIGHT       = 800
    #SQUARE_SIDE         = 100
    SCREEN_WIDTH        = 600
    SCREEN_HEIGHT       = 600
    SQUARE_SIDE         = 75
    SQUARES_PER_SIDE    = 8

    # Initialize pygame
    pygame.init()    
    # Create the screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    # Initialize the board
    board = Board(pygame, screen, BOARD_LIGHT_COLOR, BOARD_DARK_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)
    # Create agents
    #white_agent = AgentRandom()
    #black_agent = AgentRandom()
    white_agent = AgentCapture()
    black_agent = AgentCapture()
    # Create players
    white_player = Player("Merry",  "white", white_agent)
    black_player = Player("Pippin", "black", black_agent)
    # Setup the game state
    state = State(board, white_player, black_player)
    state.SetInitialPieceState()
    # Set current and opposing players
    state.SetCurrentPlayer(white_player)
    state.SetOpposingPlayer(black_player)
    current_player  = state.GetCurrentPlayer()
    opposing_player = state.GetOpposingPlayer()
    # Print detailed game state
    state.PrintGameState()
    
    # Fill the background with white
    screen.fill(PURE_WHITE)
    # Draw the board
    board.DrawBoard()
    # Draw the pieces
    state.DrawPieces(pygame, screen, PIECE_LIGHT_COLOR, PIECE_DARK_COLOR, PIECE_BORDER_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)
    # Flip the display
    pygame.display.flip()
    
    # Game running condition
    running = True
    # Add a time delay... take a breathe. :)
    time.sleep(0.5)
    
    # Run until the user asks to quit
    while running:
        # Game event loop
        for event in pygame.event.get():
            # If the user clicks the window close button, stop running.
            if event.type == pygame.QUIT:
                running = False
        
        # Choose a legal move
        current_agent = current_player.GetAgent()
        chosen_move   = current_agent.ChooseMove(state, current_player, opposing_player)
        
        # Check that the move is not empty
        if chosen_move:
            print("Chosen move: {0}".format(chosen_move))
            # Get move positions
            position_from, position_to = state.board.GetMovePositions(chosen_move)
            print("position_from: {0}, position_to: {1}".format(position_from, position_to))
            # Get piece to move!
            piece_to_move = state.GetPieceInPosition(position_from)
            # Move piece
            state.MovePiece(chosen_move)
            # Promote pawn if necessary
            state.PromotePawn(piece_to_move)
            # Switch current and opposing players
            state.SwitchTurn()
            current_player  = state.GetCurrentPlayer()
            opposing_player = state.GetOpposingPlayer()
            # Print detailed game state
            state.PrintGameState()
            # Add a time delay... take a breathe. :)
            time.sleep(0.5)
        
        # Fill the background with white
        screen.fill(PURE_WHITE)
        # Draw the board
        board.DrawBoard()
        # Draw the pieces
        state.DrawPieces(pygame, screen, PIECE_LIGHT_COLOR, PIECE_DARK_COLOR, PIECE_BORDER_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)
        # Flip the display
        pygame.display.flip()
    
    # Game over! Time to quit.
    pygame.quit()

def main():
    run_game()

if __name__ == "__main__":
    main()
