# Import the necessary modules and set up the game window
import pygame
import random


pygame.init()
window_size = (600, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pac-Man")

# Load the Pac-Man image and create a Pac-Man sprite
pacman_image = pygame.transform.rotozoom(pygame.image.load('./Resources/FlappyJuan.png'), 0, 0.3)
pacman = pygame.sprite.Sprite()
pacman.image = pacman_image
pacman.rect = pacman_image.get_rect()

# Set the frame rate and clock
fps = 60
clock = pygame.time.Clock()

# Set the running flag to True
running = True

# Set the movement speed and initial direction
speed = 5
direction = "right"


class Wall:
    def __init__(self, x, y, width, height, orientation):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 0, 255)
        self.orientation = orientation # orientation can be "horizontal" or "vertical"
        self.rect = pygame.Rect(x, y, self.width, self.height)

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self.rect)

        def create_walls(num_walls, width, height):
            walls = []
            for i in range(num_walls):
                # Choose a random position for the wall
                x = random.randrange(0, width - 50)
                y = random.randrange(0, height - 50)
                # Choose a random orientation for the wall
                if random.random() < 0.5:
                    orientation = "horizontal"
                    wall = Wall(x, y, 50, 10, orientation)
                else:
                    orientation = "vertical"
                    wall = Wall(x, y, 10, 50, orientation)
                walls.append(wall)
            return walls


# Set the wall positions
walls = [
    pygame.Rect(200, 100, 50, 50),
    pygame.Rect(300, 400, 50, 50),
    pygame.Rect(100, 500, 50, 50),
]


class Ghost:
    def __init__(self, x, y, size, color, direction):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.direction = direction
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.timer = 0

    def increase_timer(self, interval):
        self.timer += interval

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, [(self.x, self.y), (self.x + self.size, self.y + self.size // 2),
                                                 (self.x, self.y + self.size)])
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


# Create the ghosts
ghosts = [
    Ghost(200, 200, 20, (255, 0, 0), "left"),
    Ghost(400, 200, 20, (0, 255, 0), "right"),
    Ghost(200, 400, 20, (0, 0, 255), "up"),
    Ghost(400, 400, 20, (255, 255, 0), "down"),
]


def increase_ghost_timers(ghosts, interval):
    for ghost in ghosts:
        ghost.increase_timer(interval)


def get_new_direction(ghost, directions):
    # Get the current direction of the ghost
    current_direction = ghost.direction
    # Remove the opposite direction from the list of possible directions
    if current_direction == "left":
        directions.remove("right")
    elif current_direction == "right":
        directions.remove("left")
    elif current_direction == "up":
        directions.remove("down")
    elif current_direction == "down":
        directions.remove("up")
    # Choose a random direction from the remaining possible directions
    new_direction = random.choice(directions)
    return new_direction


def check_collision(obj, screen_rect, walls, ghosts=[]):
    """
    Check for collision with the edges of the screen, the walls, and the ghosts.

    Parameters:
        obj (object): An instance of a class with a rect field representing the object to check for collision.
        screen_rect (pygame.Rect): The rect of the screen.
        walls (list): A list of wall rects.
        ghosts (list, optional): A list of instances of a class with a rect field representing the ghosts. Defaults to an empty list.

    Returns:
        tuple: A tuple containing a boolean indicating whether a collision occurred and a string indicating the direction of the collision.
    """
    # Check for collision with the edges of the screen
    if obj.rect.left < 0:
        return (True, "left")
    if obj.rect.right > screen_rect.right:
        return (True, "right")
    if obj.rect.top < 0:
        return (True, "top")
    if obj.rect.bottom > screen_rect.bottom:
        return (True, "bottom")

    # Check for collision with the walls
    for wall in walls:
        if obj.rect.colliderect(wall):
            return (True, "wall")

    # Check for collision with the ghosts
    for ghost in ghosts:
        if obj.rect.colliderect(ghost.rect):
            return (True, "ghost")

    # No collision occurred
    return (False, "none")


# Set the timer interval in milliseconds
timer_interval = 1000

# Run the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = "left"
            elif event.key == pygame.K_RIGHT:
                direction = "right"
            elif event.key == pygame.K_UP:
                direction = "up"
            elif event.key == pygame.K_DOWN:
                direction = "down"

    # Update the game state
    if direction == "left":
        pacman.rect.x -= speed
    elif direction == "right":
        pacman.rect.x += speed
    elif direction == "up":
        pacman.rect.y -= speed
    elif direction == "down":
        pacman.rect.y += speed

    # Update the position of the ghosts
    for ghost in ghosts:
        print(ghost, ghost.timer)
        # Check if the timer has reached the interval or if the ghost has hit a wall or the edge of the screen
        if ghost.timer >= timer_interval or check_collision(ghost, screen.get_rect(), walls)[0]:            # If a collision occurred, change the direction of the ghost to go in the opposite direction
            if check_collision(ghost, screen.get_rect(), walls)[0]:
                # Get the current direction of the ghost
                curr_direction = ghost.direction
                # Change the direction of the ghost to go in the opposite direction
                if curr_direction == "left":
                    ghost.direction = "right"
                elif curr_direction == "right":
                    ghost.direction = "left"
                elif curr_direction == "up":
                    ghost.direction = "down"
                elif curr_direction == "down":
                    ghost.direction = "up"
            # If no collision occurred, choose a new direction for the ghost randomly based on the timer
            else:
                # Get a list of possible directions for the ghost
                possible_directions = ["left", "right", "up", "down"]
                ghost.direction = get_new_direction(ghost, possible_directions)
            # Reset the timer
            ghost.timer = 0

        # Update the position of the ghost
        if ghost.direction == "left":
            ghost.x -= speed
        elif ghost.direction == "right":
            ghost.x += speed
        elif ghost.direction == "up":
            ghost.y -= speed
        elif ghost.direction == "down":
            ghost.y += speed

    collision = check_collision(pacman, screen.get_rect(), walls, ghosts)
    if collision[0]:
        # If a collision occurs, stop movement in the direction of the collision
        if collision[1] == "left" or collision[1] == "right" or collision[1] == "wall":
            direction = "none"
        elif collision[1] == "top" or collision[1] == "bottom" or collision[1] == "wall":
            direction = "none"
        # If a collision with a ghost occurs, display "Game Over" and quit the game
        elif collision[1] == "ghost":
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", 1, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = screen.get_rect().centerx
            text_rect.centery = screen.get_rect().centery
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()

    # Draw the game
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, wall_color, wall)
    for ghost in ghosts:
        ghost.draw(screen)
    screen.blit(pacman.image, pacman.rect)
    pygame.display.flip()

    # Increase the timers of the ghosts
    increase_ghost_timers(ghosts, clock.tick(fps))



