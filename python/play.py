# Play chess
# - Two human players on one computer.

# -------------------------------------------- #
# Chess using the pygame library.
# - Author: Caleb Smith
# - Date: Project started on November 10, 2023
# -------------------------------------------- #

# Import the pygame library
import pygame
from board import Board
from state import State
from player import Player

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
    # Create players
    white_player = Player("Bilbo",  "white")
    black_player = Player("Gollum", "black")    
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
    state.PrintGameState()
    
    # Click position
    click_position  = None
    square_position = None
    xy_position     = None
    position_from   = None
    position_to     = None
    clicked_square_exists   = False
    clicked_square_is_empty = False

    # Game running condition
    running = True

    # Run until the user asks to quit
    while running:
        # Game event loop
        for event in pygame.event.get():
            # If the user clicks the window close button, stop running.
            if event.type == pygame.QUIT:
                running = False
            # Get position of click
            if event.type == pygame.MOUSEBUTTONDOWN:
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
                            # Move piece
                            state.MovePiece(move_notation)
                            # Promote pawn if necessary
                            state.PromotePawn(piece_to_move)
                            # Switch current and opposing players
                            state.SwitchTurn()
                            current_player  = state.GetCurrentPlayer()
                            opposing_player = state.GetOpposingPlayer()
                            # Print detailed game state
                            state.PrintGameState()
                                                    
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
