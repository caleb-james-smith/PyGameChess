# Chess using the pygame library.
# - Author: Caleb Smith
# - Date: Project started on November 10, 2023

# TODO:
# - Save all moves made in chess game
# - Information to save for each move: piece, position from, position to, and piece captured (or empty)
# - Define allowed piece movement and captures
# - Differentiate pawn movement and capture
# - Do not let pieces jump other pieces (except for knights)
# - Define check
# - Define checkmate
# - Define castling
# - Define pawn promotion
# - Define pawn en passant
# - Get set of legal moves for current player
# DONE:
# - Draw colored square when clicked
# - Fix bug: use square location instead of click location
# - When a square is clicked, print out the x, y and chess notation coordinates
# - For clicked square, print number and name of piece in square (or empty).
# - Draw different shapes for all chess pieces
# - Move board parameters and drawing functions to board class
# - Change click color depending on whether square is empty or occupied
# - Make it possible to move pieces
# - Make piece class
# - Draw pieces using piece classes
# - Move some functions to board class
# - Define player class
# - Track current player turn in state class
# - Switch between players
# - Add black borders to chess pieces
# - Do not let a player capture his own pieces

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
    CLICK_COLOR_PIECE   = (91, 175, 255)

    # Set up the drawing window (screen)
    #SCREEN_WIDTH        = 800
    #SCREEN_HEIGHT       = 800
    #SQUARE_SIDE         = 100
    SCREEN_WIDTH        = 600
    SCREEN_HEIGHT       = 600
    SQUARE_SIDE         = 75
    SQUARES_PER_SIDE    = 8
    BOARD_SIDE          = SQUARES_PER_SIDE * SQUARE_SIDE
    
    # Initialize pygame
    pygame.init()    
    # Create the screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    # Initialize the board
    board = Board(pygame, screen, BOARD_LIGHT_COLOR, BOARD_DARK_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)
    # Create players
    white_player = Player("Bilbo", "white")
    black_player = Player("Gollum", "black")    
    # Setup the game state
    state = State(board, white_player, black_player)
    state.SetInitialPieceState()
    state.SetCurrentPlayer(white_player)
    current_player = state.GetCurrentPlayer()
    print("Current player: {0} - {1}".format(current_player.GetName(), current_player.GetColor()))
    
    # Run until the user asks to quit
    running = True
    
    # Click position
    click_position = None
    position_from  = None
    position_to    = None
    clicked_square_exists   = False
    clicked_square_is_empty = False

    # Game running condition
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
                        # Move piece
                        current_player_color = current_player.GetColor()
                        # Get piece to move and to capture
                        position_to = [x, y]
                        piece_to_move       = state.GetPieceInPosition(position_from)
                        piece_to_capture    = state.GetPieceInPosition(position_to)
                        piece_to_move_name      = piece_to_move.GetName()
                        piece_to_move_color     = piece_to_move.GetColor()
                        piece_of_opposite_color = False
                        
                        # Only if piece to capture exists (not empty square)
                        if piece_to_capture:
                            piece_to_capture_name   = piece_to_capture.GetName()
                            piece_to_capture_color  = piece_to_capture.GetColor()
                            piece_of_opposite_color = (current_player_color != piece_to_capture_color)
                            print("piece to move: {0}; piece to capture: {1}".format(piece_to_move_name, piece_to_capture_name))
                        else:
                            print("piece to move: {0}".format(piece_to_move_name))
                        
                        move_is_valid = piece_to_move.MoveIsValid(position_to)

                        # Check if move is valid
                        # - Player can only move his own pieces (player color must match the color of the piece being moved)
                        # - Player cannot capture his own pieces (player color cannot match the color of the piece being captured)
                        # - Player can move to empty squares
                        # - Move must be valid for the piece being moved
                        if (current_player_color == piece_to_move_color) and move_is_valid:
                            # Either empty square or piece of opposite color
                            if piece_name == "empty" or piece_of_opposite_color:
                                state.MovePiece(position_from, position_to)
                                state.SwitchTurn()
                                current_player = state.GetCurrentPlayer()
                                print("Current player: {0} - {1}".format(current_player.GetName(), current_player.GetColor()))
                        
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
            square_position = board.GetClickedSquare(click_position)
            square_x = square_position[0]
            square_y = square_position[1]
            # Use different colors based on whether square is empty or occupied
            if clicked_square_is_empty:
                board.DrawSquare(CLICK_COLOR_EMPTY, square_x, square_y)
            else:
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
