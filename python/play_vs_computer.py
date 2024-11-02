# Play chess
# - One human player against one computer player on one computer.

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
    #evaluator = EvaluateMaterial()
    evaluator = EvaluatePosition(piece_table)
    # Create agents
    time_delay  = 0.0
    max_depth   = 1
    #black_agent = AgentRandom()
    #black_agent = AgentCapture()
    black_agent = AgentMinimax(evaluator, max_depth)
    # Create players
    white_player = Player("Bilbo",  "white")
    black_player = Player("Gollum", "black", black_agent)
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
    state.PrintGameState(evaluator)
    
    # Click position
    click_position  = None
    square_position = None
    xy_position     = None
    position_from   = None
    position_to     = None
    clicked_square_exists   = False
    clicked_square_is_empty = False
    agent_move_position = None

    # Game running condition
    running = True

    # Run until the user asks to quit
    while running:
        # Game event loop
        for event in pygame.event.get():
            # If the user clicks the window close button, stop running.
            if event.type == pygame.QUIT:
                running = False
            
            # Get the current agent
            current_agent = current_player.GetAgent()
            
            # Check if the player has an agent (is a computer player)
            if current_agent:
                # Let the agent choose a move
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
                                        
                    # Make move
                    state.MakeMove(chosen_move)
                    # Switch current and opposing players
                    current_player  = state.GetCurrentPlayer()
                    opposing_player = state.GetOpposingPlayer()
                    # Print detailed game state
                    state.PrintGameState(evaluator)
                    # Add a time delay... take a breathe. :)
                    if time_delay:
                        time.sleep(time_delay)
            
            # For human player (without agent), get position of click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # click position
                click_position = pygame.mouse.get_pos()
                click_x = click_position[0]
                click_y = click_position[1]
                # clicked square position
                square_position = board.GetClickedSquare(click_position)
                square_x = square_position[0]
                square_y = square_position[1]
                # x, y coordinates
                xy_position = board.GetSquareXYCoords(square_position)
                x = xy_position[0]
                y = xy_position[1]
                # chess notation
                chess_notation = board.GetChessNotation(xy_position)
                # piece in position
                piece = state.GetPieceInPosition(xy_position)
                if piece:
                    piece_value = piece.GetValue()
                    piece_name  = piece.GetName()
                else:
                    piece_value = 0
                    piece_name  = "empty"
                
                # Move piece; this gets complicated!
                # - Use clicked_square_exists and clicked_square_is_empty from previous click
                # - Be careful about when to set clicked_square_exists
                # - Need to keep track of "from" and "to" positions
                # - Do not move empty squares
                # - Piece can move to its current position

                # Check if previously clicked square exists
                if clicked_square_exists:
                    # Check if previously clicked square is empty
                    # Do not move empty squares!
                    # However, we do need to update clicked_square_exists and position_from,
                    # as the current square may contain a piece.
                    if clicked_square_is_empty:
                        clicked_square_exists = True
                        position_from = [x, y]
                    else:
                        # Determine if move is valid
                        all_systems_go = False
                        position_to = [x, y]
                        move_notation = board.GetMoveNotation(position_from, position_to)
                        current_player_color = current_player.GetColor()
                        piece_to_move = state.GetPieceInPosition(position_from)
                        piece_to_move_color = piece_to_move.GetColor()
                        piece_moves = state.GetPiecePossibleMoves(piece_to_move)

                        # Determine if a player's move would put himself in check
                        move_results_in_check = state.MoveResultsInCheck(current_player, opposing_player, move_notation)

                        # A player can only move his own piece
                        if current_player_color == piece_to_move_color:
                            # Determine if move is possible for the piece
                            if position_to in piece_moves:
                                # Enforce that move does not result in check for the current player
                                if not move_results_in_check:
                                    all_systems_go = True

                        # All systems go: move the piece!
                        if all_systems_go:                            
                            # Make move
                            state.MakeMove(move_notation)
                            # Switch current and opposing players
                            current_player  = state.GetCurrentPlayer()
                            opposing_player = state.GetOpposingPlayer()
                            # Print detailed game state
                            state.PrintGameState(evaluator)
                                                    
                        # Reset clicked square and position from
                        # Do this whether or not we moved a piece
                        clicked_square_exists = False
                        position_from = None
                
                else:
                    clicked_square_exists = True
                    position_from = [x, y]
                
                # Record if square is empty; do this after moving piece
                if piece_name == "empty":
                    clicked_square_is_empty = True
                else:
                    clicked_square_is_empty = False
                
                print("click = ({0}, {1}); square = ({2}, {3}); (x, y) = ({4}, {5}); notation: {6}; piece = {7}: {8}".format(click_x, click_y, square_x, square_y, x, y, chess_notation, piece_value, piece_name))

        # Fill the background with white
        screen.fill(PURE_WHITE)
        
        # Draw the board
        board.DrawBoard()

        # Draw the agent move
        if agent_move_position:
            agent_square_position = board.GetSquarePosition(agent_move_position)
            square_x = agent_square_position[0]
            square_y = agent_square_position[1]
            board.DrawSquare(CLICK_COLOR_PIECE, square_x, square_y)

        # If there was a click, draw the clicked square
        if click_position:
            square_x = square_position[0]
            square_y = square_position[1]
            # Use different colors based on whether square is empty or occupied
            if clicked_square_is_empty:
                board.DrawSquare(CLICK_COLOR_EMPTY, square_x, square_y)
            else:
                board.DrawSquare(CLICK_COLOR_PIECE, square_x, square_y)
                state.DrawMovesForPiece(CLICK_COLOR_MOVES, xy_position, current_player, opposing_player)

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
