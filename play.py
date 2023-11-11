# Simple pygame program

# Import the pygame library
import pygame

# Draw a solid square
# x_position: x position measured from left edge
# y_position: y position measured from top edge
def draw_square(my_game, my_screen, color, x_position, y_position, side):
    my_game.draw.rect(my_screen, color, [x_position, y_position, side, side], 0)

# Draw a piece
# x_position: x position measured from left edge
# y_position: y position measured from top edge
def draw_piece(my_game, my_screen, color, x_position, y_position, size):
    my_game.draw.circle(my_screen, color, [x_position, y_position], size, 0)

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
            # FIXME: draw pieces using both colors
            color = light_color
            # Get piece position and size; probably different than square position (FIXME)
            x_position = x * square_side
            y_position = y * square_side
            # FIXME: size should be smaller than square side
            size = square_side / 2
            # Draw piece
            draw_piece(my_game, my_screen, color, x_position, y_position, size)

# Run the game
def run_game():
    # Initialize pygame
    pygame.init()

    # Define colors
    PURE_WHITE  = (255, 255, 255)
    PURE_BLACK  = (0, 0, 0)
    #LIGHT_COLOR = PURE_WHITE
    #DARK_COLOR  = PURE_BLACK
    LIGHT_COLOR = (233, 237, 204)
    DARK_COLOR  = (119, 153, 84)

    # Set up the drawing window (screen)
    SCREEN_WIDTH        = 800
    SCREEN_HEIGHT       = 800
    SQUARE_SIDE         = 100
    SQUARES_PER_SIDE    = 8
    BOARD_SIDE          = SQUARES_PER_SIDE * SQUARE_SIDE
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill(PURE_WHITE)

        # Draw the board
        draw_board(pygame, screen, LIGHT_COLOR, DARK_COLOR, SQUARES_PER_SIDE, SQUARE_SIDE)
        
        # Draw the pieces
        draw_pieces(pygame, screen, PURE_WHITE, PURE_BLACK, SQUARES_PER_SIDE, SQUARE_SIDE)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

def main():
    run_game()

if __name__ == "__main__":
    main()
