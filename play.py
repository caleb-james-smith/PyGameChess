# Chess using the pygame library.
# - Author: Caleb Smith
# - Date: Project started on November 10, 2023

# TODO:
# - Draw different shapes for all chess pieces
# - Move board parameters and drawing functions to board class
# - Make piece class
# DONE:
# - Draw colored square when clicked
# - Fix bug: use square location instead of click location
# - When a square is clicked, print out the x, y and chess notation coordinates
# - For clicked square, print number and name of piece in square (or empty).

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
    if type == "circle":
        my_game.draw.circle(my_screen, color, [x_position, y_position], size, 0)
    elif type == "triangle":
        my_game.draw.polygon(my_screen, color, [(x_position - size, y_position + size), (x_position + size, y_position + size), (x_position, y_position - size)], 0)

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
def draw_pieces(my_game, my_screen, light_color, dark_color, squares_per_side, square_side):
    # Draw pieces
    for x in range(squares_per_side):
        for y in range(squares_per_side):
            half_n_squares    = squares_per_side / 2
            quarter_n_squares = squares_per_side / 4
            # do not draw pieces in the central rows; depends on the squares per side
            if quarter_n_squares <= y < 3 * quarter_n_squares:
                continue
            # choose piece color
            if y < half_n_squares:
                color = dark_color
            else:
                color = light_color
            # choose piece type
            if y == 0 or y == squares_per_side - 1:
                type = "circle"
            else:
                type = "triangle"
            # Get piece position and size; note that this is different than the square position
            x_position = (x + 0.5) * square_side
            y_position = (y + 0.5) * square_side
            # Size should be smaller than square side
            size = square_side / 3
            # Draw piece
            draw_piece(my_game, my_screen, color, x_position, y_position, size, type)

# Run the game
def run_game():
    # Initialize pygame
    pygame.init()

    board = Board()
    state = State()
    state.SetInitialState()

    # Define colors
    PURE_WHITE  = (255, 255, 255)
    PURE_BLACK  = (0, 0, 0)
    #BOARD_LIGHT_COLOR = PURE_WHITE
    #BOARD_DARK_COLOR  = PURE_BLACK
    #PIECE_LIGHT_COLOR = PURE_WHITE
    #PIECE_DARK_COLOR  = PURE_BLACK
    BOARD_LIGHT_COLOR = (233, 237, 204)
    BOARD_DARK_COLOR  = (119, 153, 84)
    PIECE_LIGHT_COLOR = (248, 248, 248)
    PIECE_DARK_COLOR  = (85, 83, 82)
    CLICK_COLOR       = PURE_BLACK

    # Set up the drawing window (screen)
    SCREEN_WIDTH        = 800
    SCREEN_HEIGHT       = 800
    SQUARE_SIDE         = 100
    SQUARES_PER_SIDE    = 8
    BOARD_SIDE          = SQUARES_PER_SIDE * SQUARE_SIDE
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

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
        draw_board(pygame, screen, BOARD_LIGHT_COLOR, BOARD_DARK_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)
        
        # If click, draw clicked square
        if click_position:
            square_position = get_clicked_square(click_position, SQUARE_SIDE)
            square_x = square_position[0]
            square_y = square_position[1]            

            draw_square(pygame, screen, CLICK_COLOR, square_x, square_y, SQUARE_SIDE)
                    
        # Draw the pieces
        draw_pieces(pygame, screen, PIECE_LIGHT_COLOR, PIECE_DARK_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

def main():
    run_game()

if __name__ == "__main__":
    main()
