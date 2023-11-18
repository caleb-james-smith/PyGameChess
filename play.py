# Chess using the pygame library.
# - Author: Caleb Smith
# - Date: Project started on November 10, 2023

# TODO:
# - Move board parameters and drawing functions to board class
# - Make piece class
# DONE:
# - Draw colored square when clicked
# - Fix bug: use square location instead of click location
# - When a square is clicked, print out the x, y and chess notation coordinates
# - For clicked square, print number and name of piece in square (or empty).
# - Draw different shapes for all chess pieces

# Import the pygame library
import pygame
from board import Board
from state import State

# Round using a base
def round_using_base(number, base):
    result = number - (number % base)
    return result

# Draw a solid square
# x_position: x position measured from left edge
# y_position: y position measured from top edge
def draw_square(my_game, my_screen, color, x_position, y_position, side):
    my_game.draw.rect(my_screen, color, [x_position, y_position, side, side], 0)

# Draw a piece
# x_position: x position measured from left edge
# y_position: y position measured from top edge
def draw_piece(my_game, my_screen, color, x_position, y_position, size, type):
    # Piece Shapes
    # - pawn:   small triangle
    # - knight: triangle pointing left
    # - bishop: tall triangle
    # - rook:   tall rectangle
    # - queen:  pentagon
    # - king:   square

    # When drawing, recall that positive x is to the right and positive y is down.

    # pawn: small triangle
    if type == "pawn":
        points = [(x_position - size, y_position + size), (x_position + size, y_position + size), (x_position, y_position - size)]
        my_game.draw.polygon(my_screen, color, points, 0)
    # knight: triangle pointing left
    elif type == "knight":
        points = [(x_position + size, y_position - 1.5 * size), (x_position + size, y_position + 1.5 * size), (x_position - size, y_position)]
        my_game.draw.polygon(my_screen, color, points, 0)
    # bishop: tall triangle
    elif type == "bishop":
        points = [(x_position - size, y_position + 1.5 * size), (x_position + size, y_position + 1.5 * size), (x_position, y_position - 1.5 * size)]
        my_game.draw.polygon(my_screen, color, points, 0)
    # rook: tall rectangle
    elif type == "rook":
        points = [(x_position - size, y_position - 1.5 * size), (x_position + size, y_position - 1.5 * size), (x_position + size, y_position + 1.5 * size), (x_position - size, y_position + 1.5 * size)]
        my_game.draw.polygon(my_screen, color, points, 0)
    # queen: pentagon
    elif type == "queen":
        points = [(x_position - size, y_position + 1.5 * size), (x_position - 1.5 * size, y_position), (x_position, y_position - 1.5 * size), (x_position + 1.5 * size, y_position), (x_position + size, y_position + 1.5 * size)]
        my_game.draw.polygon(my_screen, color, points, 0)
    # king: square
    elif type == "king":
        points = [(x_position - size, y_position - size), (x_position + size, y_position - size), (x_position + size, y_position + size), (x_position - size, y_position + size)]
        my_game.draw.polygon(my_screen, color, points, 0)
    # any other piece: circle
    else:
        my_game.draw.circle(my_screen, color, [x_position, y_position], size, 0)

# Get position of clicked square based on click position
def get_clicked_square(click_position, side):
    click_x = click_position[0]
    click_y = click_position[1]
    # Find square x, y based on click x, y;
    # round using the side length as the base
    square_x = round_using_base(click_x, side)
    square_y = round_using_base(click_y, side)
    return [square_x, square_y]

# get x, y coordinates (ints) based on square x, y position
def get_square_xy_coords(square_position, side):
    square_x = square_position[0]
    square_y = square_position[1]
    # use integer division
    x = square_x // side
    y = square_y // side
    return [x, y]

# Get square color based on x, y coordinate indices
def get_square_color(x, y, light_color, dark_color):
    # Use parity to determine square color
    parity = (x + y) % 2
    # Odd parity: dark color
    if parity:
        return dark_color
    # Even parity: light color
    else:
        return light_color

# Draw the board
def draw_board(my_game, my_screen, light_color, dark_color, squares_per_side, square_side):
    # Draw squares
    for x in range(squares_per_side):
        for y in range(squares_per_side):
            # Get square color
            color = get_square_color(x, y, light_color, dark_color)
            # Get square position
            x_position = x * square_side
            y_position = y * square_side
            # Draw square
            draw_square(my_game, my_screen, color, x_position, y_position, square_side)

# Draw the pieces
def draw_pieces(my_game, my_screen, my_state, light_color, dark_color, squares_per_side, square_side):
    # Draw pieces
    for x in range(squares_per_side):
        for y in range(squares_per_side):            
            # Get piece name based on position (from game state)
            position    = [x, y]
            piece_name  = my_state.GetPieceNameInPosition(position)
            
            # Skip empty squares
            if piece_name == "empty":
                continue
            
            # Get piece color and type from name
            split_name  = piece_name.split()
            piece_color = split_name[0]
            piece_type  = split_name[1]
            # Determine color
            color = None
            if piece_color == "white":
                color = light_color
            if piece_color == "black":
                color = dark_color

            # Get piece position: note that this is different than the square position
            x_position = (x + 0.5) * square_side
            y_position = (y + 0.5) * square_side
            # Piece size should be smaller than square side
            size = square_side / 4
            # Draw piece
            draw_piece(my_game, my_screen, color, x_position, y_position, size, piece_type)

# Run the game
def run_game():
    # Define colors
    PURE_WHITE          = (255, 255, 255)
    PURE_BLACK          = (0, 0, 0)
    BOARD_LIGHT_COLOR   = (233, 237, 204)
    BOARD_DARK_COLOR    = (119, 153, 84)
    PIECE_LIGHT_COLOR   = (248, 248, 248)
    PIECE_DARK_COLOR    = (85, 83, 82)
    CLICK_COLOR         = PURE_BLACK

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
    # Initialize the game state
    state = State()
    state.SetInitialState()
    
    # Run until the user asks to quit
    running = True
    
    # Click position
    click_position = None

    while running:

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
                square_position = get_clicked_square(click_position, SQUARE_SIDE)
                square_x = square_position[0]
                square_y = square_position[1]
                # x, y coordinates
                xy_position = get_square_xy_coords(square_position, SQUARE_SIDE)
                x = xy_position[0]
                y = xy_position[1]
                # chess notation
                chess_notation = board.GetChessNotation(xy_position)
                # piece in position
                piece_value = state.GetPieceValueInPosition(xy_position)
                piece_name  = state.GetPieceNameInPosition(xy_position)

                print("click = ({0}, {1}); square = ({2}, {3}); (x, y) = ({4}, {5}); notation: {6}; piece = {7}: {8}".format(click_x, click_y, square_x, square_y, x, y, chess_notation, piece_value, piece_name))

        # Fill the background with white
        screen.fill(PURE_WHITE)
        
        # Draw the board
        #draw_board(pygame, screen, BOARD_LIGHT_COLOR, BOARD_DARK_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)
        board.DrawBoard()

        # If there was a click, draw the clicked square
        if click_position:
            square_position = get_clicked_square(click_position, SQUARE_SIDE)
            square_x = square_position[0]
            square_y = square_position[1]            

            #draw_square(pygame, screen, CLICK_COLOR, square_x, square_y, SQUARE_SIDE)
            board.DrawSquare(CLICK_COLOR, square_x, square_y)
                    
        # Draw the pieces
        draw_pieces(pygame, screen, state, PIECE_LIGHT_COLOR, PIECE_DARK_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

def main():
    run_game()

if __name__ == "__main__":
    main()
