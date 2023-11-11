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
    PURE_WHITE  = (255, 255, 255)
    PURE_BLACK  = (0, 0, 0)
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

        # draw squares
        for x in range(SQUARES_PER_SIDE):
            for y in range(SQUARES_PER_SIDE):
                parity = (x + y) % 2
                # odd parity: dark color
                if(parity):
                    color = DARK_COLOR
                # even parity: light color
                else:
                    color = LIGHT_COLOR
                draw_square(pygame, screen, color, x * SQUARE_SIDE, y * SQUARE_SIDE, SQUARE_SIDE)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

def main():
    run_game()

if __name__ == "__main__":
    main()
