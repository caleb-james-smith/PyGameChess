# Simple pygame program

# Import the pygame library
import pygame

# Draw a solid square
# x: x position measured from left edge
# y: y position measured from top edge
def draw_square(my_game, my_screen, color, x, y, side):
    my_game.draw.rect(my_screen, color, [x, y, side, side], 0)

def run_game():
    # Initialize pygame
    pygame.init()

    # Define colors
    #LIGHT_COLOR = (255, 255, 255)
    #DARK_COLOR = (0, 0, 0)
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
        screen.fill(LIGHT_COLOR)

        # draw black squares
        for row in range(SQUARES_PER_SIDE):
            y = row * SQUARE_SIDE
            # determine starting x value for each row
            if row % 2 == 0:
                x_start = SQUARE_SIDE
            else:
                x_start = 0
            for x in range(x_start, BOARD_SIDE, 2 * SQUARE_SIDE):
                draw_square(pygame, screen, DARK_COLOR, x, y, SQUARE_SIDE)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

def main():
    run_game()

if __name__ == "__main__":
    main()
