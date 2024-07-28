import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Item class definition
class Item:
    def __init__(self, name, cost, effect):
        self.name = name
        self.cost = cost
        self.effect = effect

# Ball class definition
class Ball:
    def __init__(self, speed):
        self.radius = 20
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT // 2)
        self.x_speed = speed * random.choice([-1, 1])
        self.y_speed = speed * random.choice([-1, 1])

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        # Change direction when hitting the wall
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.x_speed = -self.x_speed
        if self.y <= self.radius:
            self.y_speed = -self.y_speed

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

# Floor class definition
class Floor:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 10
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

# Brick class definition
class Brick:
    def __init__(self, x, y):
        self.width = 60
        self.height = 20
        self.x = x
        self.y = y
        self.hit = False

    def draw(self, screen):
        if not self.hit:
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

# Shop screen display function
def show_shop(score, items):
    shop_running = True
    while shop_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        shop_title = font.render("Shop", True, WHITE)
        text_rect = shop_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(shop_title, text_rect)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Current Coins: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        for i, item in enumerate(items):
            item_text = font.render(f"{item.name} ({item.cost} coins)", True, WHITE)
            screen.blit(item_text, (10, 70 + i * 30))

            # Check purchase availability
            if score >= item.cost:
                available_text = font.render("Available", True, GREEN)
                screen.blit(available_text, (300, 70 + i * 30))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_1 + i]:  # Buy with 1, 2 keys
                    score -= item.cost
                    item.effect()  # Apply item effect

        back_text = font.render("Press ESC to go back", True, WHITE)
        screen.blit(back_text, (10, HEIGHT - 50))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Exit shop with ESC key
            shop_running = False

# Game loop
def game_loop():
    clock = pygame.time.Clock()
    level = 1
    speed = 5
    score = 0
    ball = Ball(speed)
    floor = Floor()

    # Create bricks
    bricks = create_bricks(level)

    # Create items
    items = [
        Item("Speed Boost", 50, lambda: increase_speed(ball)),
        Item("Jump Height Boost", 30, lambda: increase_jump(ball)),
    ]

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # If game over
        if game_over:
            screen.fill(BLACK)
            font = pygame.font.Font(None, 74)
            game_over_text = font.render("Game Over!", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            screen.blit(game_over_text, text_rect)

            # Show shop button
            shop_text = font.render("Press SPACE to go to shop", True, WHITE)
            shop_rect = shop_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            screen.blit(shop_text, shop_rect)

            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                show_shop(score, items)  # Call shop function
                game_over = False  # Restart game
                score = 0
                level = 1
                speed = 5
                ball = Ball(speed)
                bricks = create_bricks(level)  # Regenerate bricks

            continue

        # Draw background
        screen.fill(BLACK)

        # Move and draw ball
        ball.move()
        ball.draw(screen)

        # Move and draw floor
        floor.move()
        floor.draw(screen)

        # Handle ball and floor collision
        if (floor.x < ball.x < floor.x + floor.width) and (floor.y < ball.y + ball.radius < floor.y + floor.height):
            ball.y_speed = -ball.y_speed
            ball.y = floor.y - ball.radius

        # If ball goes below the screen, game over
        if ball.y - ball.radius > HEIGHT:
            game_over = True

        # Handle ball and brick collision
        for brick in bricks:
            if not brick.hit:
                if (brick.x < ball.x < brick.x + brick.width) and (brick.y < ball.y - ball.radius < brick.y + brick.height):
                    brick.hit = True
                    ball.y_speed = -ball.y_speed  # Bounce off the brick
                    score += 10  # Increase score for breaking brick

        # Draw bricks
        for brick in bricks:
            brick.draw(screen)

        # Level up if all bricks are destroyed
        if all(brick.hit for brick in bricks):
            level += 1
            speed += 1  # Increase ball speed
            ball = Ball(speed)  # Create new ball
            bricks = create_bricks(level)  # Generate new bricks

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display coins
        coins = score // 10
        coin_text = font.render(f"Coins: {coins}", True, WHITE)
        screen.blit(coin_text, (10, 40))

        # Update the screen
        pygame.display.flip()
        clock.tick(60)  # 60 frames per second

    pygame.quit()

# Speed boost effect
def increase_speed(ball):
    ball.x_speed *= 1.5
    ball.y_speed *= 1.5

# Jump height boost effect
def increase_jump(ball):
    ball.y_speed *= 1.2  # Increase jump height

# Brick creation function
def create_bricks(level):
    bricks = []
    for i in range(5 + level):  # Increase number of bricks based on level
        for j in range(4):  # 4 rows
            bricks.append(Brick(i * 120 + 50, j * 30 + 50))
    return bricks

# Start the game
game_loop()
