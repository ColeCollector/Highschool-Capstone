import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 400))

# Define colors
white = (255, 255, 255)

# Define transparency level (0 is fully transparent, 255 is fully opaque)
transparency = 128

# Create a surface for the circle
circle_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
circle_surface.set_alpha(transparency)

# Draw a circle on the surface
pygame.draw.circle(circle_surface, white, (100, 100), 100)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Blit the circle surface onto the main screen
    screen.blit(circle_surface, (100, 100))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
