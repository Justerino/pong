import pygame
import sys
import random

# define global variables
screen_width = 1280
screen_height = 800

# gameplay variables
ball_speed_x = 6
ball_speed_y = 6
player_speed = 0
cpu_speed = 4

# initializing shapes for display objects
ball = pygame.Rect(0, 0, 30, 30)
player = pygame.Rect(0, 0, 20, 100)
cpu = pygame.Rect(0, 0, 20, 100)

# set points to 0
cpu_points, player_points = 0, 0


def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width/2 - 10
    ball.y = random.randint(10, 100)
    ball_speed_x *= random.choice([-1,1])
    ball_speed_y *= random.choice([-1, 1])


def point_won(winner):
    global cpu_points, player_points

    if winner == "cpu":
        cpu_points += 1
    if winner == "player":
        player_points += 1

    reset_ball()


def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.right >= screen_width:
        point_won("cpu")

    if ball.left <= 0:
        point_won("player")

    if ball.colliderect(player) or ball.colliderect(cpu):
        ball_speed_x *= -1


def animate_player():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height


def animate_cpu():
    global cpu_speed
    cpu.y += cpu_speed

    if ball.centery <= cpu.centery:
        cpu_speed = -5
    if ball.centery >= cpu.centery:
        cpu_speed = 5

    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height

def main():

    pygame.init()

    # display screen and set caption
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pong")

    # initialize clock
    clock = pygame.time.Clock()

    # establish starting points
    ball.center = (screen_width / 2, screen_height / 2)
    cpu.centery = screen_height / 2
    player.midright = (screen_width, screen_height / 2)

    # set font
    score_font = pygame.font.Font(None, 100)

    # declare necessary global variable in scope for controls
    global player_speed

    # gameplay loop
    while True:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # while player holds down a key, provide speed to paddle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed = -6
                if event.key == pygame.K_DOWN:
                    player_speed = 6
            # while player is not pressing key, stop movement on paddle
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_speed = 0
                if event.key == pygame.K_DOWN:
                    player_speed = 0

        # Change the position of the game objects
        animate_ball()
        animate_player()
        animate_cpu()

        # Draw the game objects
        screen.fill('black')

        cpu_score_surface = score_font.render(str(cpu_points), True, "white")
        player_score_surface = score_font.render(str(player_points), True, "white")
        screen.blit(cpu_score_surface, (screen_width/4, 20))
        screen.blit(player_score_surface, (3*screen_width/4, 20))

        pygame.draw.aaline(screen, 'white', (screen_width / 2, 0), (screen_width / 2, screen_height))
        pygame.draw.ellipse(screen, 'white', ball)
        pygame.draw.rect(screen, 'white', cpu)
        pygame.draw.rect(screen, 'white', player)

        # Update the display
        pygame.display.update()
        clock.tick(60)


# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    main()
