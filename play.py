# Simple pygame program

# Import the pygame library
import pygame

# Draw a solid square
def draw_square(my_game, my_screen, color, x, y, side):
    my_game.draw.rect(my_screen, color, [x, y, side, side], 0)

def run_game():
    # Initialize pygame
    pygame.init()

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Set up the drawing window (screen)
    SCREEN_WIDTH  = 800
    SCREEN_HEIGHT = 800
    BOARD_SIDE    = 800
    SQUARE_SIDE   = 100
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill(WHITE)

        # Draw a solid blue circle in the center
        #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Draw a rectangle using rect()
        # parameters: surface, color, [x, y, width, height]
        # x: x position measured from left edge
        # y: y position measured from top edge
        #pygame.draw.rect(screen, BLACK, [0, 0, 100, 200], 0)

        #for x in range(0, 800, 200):
        #    draw_square(pygame, screen, BLACK, x, 0, 100)
        #for x in range(100, 800, 200):
        #    draw_square(pygame, screen, BLACK, x, 100, 100)

        # draw black squares
        for row in range(8):
            y = row * SQUARE_SIDE
            # determine starting x value for each row
            if row % 2 == 0:
                x_start = SQUARE_SIDE
            else:
                x_start = 0
            for x in range(x_start, BOARD_SIDE, 2 * SQUARE_SIDE):
                draw_square(pygame, screen, BLACK, x, y, SQUARE_SIDE)

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

def main():
    run_game()

if __name__ == "__main__":
    main()
