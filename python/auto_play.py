# Play chess
# - Two computer players on one computer.

# Import the pygame library
import pygame
import time
from board import Board
from state import State
from player import Player
from tables import PieceTable
from evaluate import EvaluateMaterial, EvaluatePosition
from agent import AgentRandom, AgentCapture, AgentMinimax

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

    # Define themes
    #piece_theme = "shapes"
    #piece_theme = "standard"
    piece_theme = "neo"
    #piece_theme = "dummy"

    # Initialize pygame
    pygame.init()    
    # Create the screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    # Initialize the board
    board = Board(pygame, screen, BOARD_LIGHT_COLOR, BOARD_DARK_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)
    # Create evaluators
    piece_table = PieceTable()
    
    #game_evaluator = EvaluateMaterial()
    game_evaluator = EvaluatePosition(piece_table)
    
    #white_evaluator = EvaluateMaterial()
    white_evaluator = EvaluatePosition(piece_table)
    
    #black_evaluator = EvaluateMaterial()
    black_evaluator = EvaluatePosition(piece_table)
    
    # Create agents
    time_delay  = 0.0
    max_depth   = 1
    
    black_agent = AgentRandom()
    #black_agent = AgentCapture()
    #black_agent = AgentMinimax(black_evaluator, max_depth)
    
    #white_agent = AgentRandom()
    #white_agent = AgentCapture()
    white_agent = AgentMinimax(white_evaluator, max_depth)
    
    # Create players
    white_player = Player("Merry",  "white", white_agent)
    black_player = Player("Pippin", "black", black_agent)
    # Setup the game state
    state = State(board, piece_theme, white_player, black_player)
    state.LoadPieceImages(pygame, SQUARE_SIDE)
    state.SetInitialPieceState()
    # Set current and opposing players
    state.SetCurrentPlayer(white_player)
    state.SetOpposingPlayer(black_player)
    current_player  = state.GetCurrentPlayer()
    opposing_player = state.GetOpposingPlayer()
    # Print detailed game state
    state.PrintGameState(game_evaluator)
    
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
    if time_delay:
        time.sleep(time_delay)
    
    # Run until the user asks to quit
    while running:
        # Game event loop
        for event in pygame.event.get():
            # If the user clicks the window close button, stop running.
            if event.type == pygame.QUIT:
                running = False
        
        # Let the agent choose a move
        current_agent = current_player.GetAgent()
        start_time  = time.time()
        chosen_move = current_agent.ChooseMove(state, current_player, opposing_player)
        end_time    = time.time()
        calc_time   = end_time - start_time
        
        # Check that the move is not empty
        if chosen_move:
            print("Chosen move: {0}".format(chosen_move))
            print("Calculation time: {0:.3f} seconds".format(calc_time))
            # Get move positions
            position_from, position_to = state.board.GetMovePositions(chosen_move)
            agent_move_position = position_to
            #print("position_from: {0}, position_to: {1}".format(position_from, position_to))
            
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
            state.PrintGameState(game_evaluator)
            # Add a time delay... take a breathe. :)
            if time_delay:
                time.sleep(time_delay)
        
        # Fill the background with white
        screen.fill(PURE_WHITE)
        
        # Draw the board
        board.DrawBoard()

        # Draw the latest agent move
        if agent_move_position:
            agent_square_position = board.GetSquarePosition(agent_move_position)
            square_x = agent_square_position[0]
            square_y = agent_square_position[1]
            board.DrawSquare(CLICK_COLOR_PIECE, square_x, square_y)
        
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
