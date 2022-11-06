import pygame
import sys
import random

pygame.init()

# create the main window
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

WINDOW = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption("Hungry Hungry Hippos!")


# Game Constants
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#Globals

global player_1_score
player_1_score = 0
"""
The goal is a stationary object in the field that will increase the score when an object comes in contact with it. 
"""
class Goal:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.width = 100
        self.height = 100
    def draw(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y, self.width, self.height))

def goal_collision(balls, goal):
    global player_1_score
    goal_left_x = goal.x
    goal_right_x = goal.x + goal.width
    goal_top_y = goal.y
    goal_bottom_y = goal.y + goal.height
    

    for ball in balls:
        ball_x = ball.x
        ball_y = ball.y
        

        if( (ball_x <= goal_right_x) and (ball_x >= goal_left_x) ):
            if( (ball_y >= goal_top_y) and (ball_y <= goal_bottom_y) ):
                if (ball.size == "small"):
                    player_1_score += 3
                if (ball.size == "medium"):
                    player_1_score += 2
                if (ball.size == "large" or ball.size == "xlarge"):
                    player_1_score += 1
                balls.remove(ball) 
                print("Score: " + str(player_1_score))
                

    return balls




"""
The Ball class creates all of the balls that the hippos will eat. 
There are four types of balls: small, medium, large, and xlarge. The size of the ball 
The balls are assigned a random velcoity via get_random_velocity() when initialized. 
When the balls hit any wall, they have a 10% chance of having their velocity modified randomly via change_velocity_randomly(initial).
"""
class Ball:
    COLOR = WHITE
    

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.x_vel = get_random_velocity()
        self.y_vel = get_random_velocity()
        self.size = size

        if (size == "small"):
            self.radius = 2
        if (size == "medium"):
            self.radius = 4
        if (size == "large"):
            self.radius = 6
        if (size == "xlarge"):
            self.radius = 10

    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.y += self.y_vel
        self.x += self.x_vel

def get_random_velocity():
    retVal = random.randint(-10, 10)
    return retVal

def change_velocity_randomly(initial):
    push = random.randint(-10, 10)
    sum = push + initial
    will_change = random.randint(-10, 40)
    if (will_change < 0):
        if ( (sum != 0) and (sum >= -10) and (sum <= 10) ):
            return sum
        else:
            return initial
    else:
        return initial


def draw_all(window, balls, goal):
    window.fill(BLACK)

    goal.draw(window)

    for ball in balls:
        ball.draw(window)
    


    pygame.display.update()

def wall_collision(the_balls):


    for the_ball in the_balls:

        # handle ball collision with the ceiling
        if the_ball.y - the_ball.radius <= 0:
            the_ball.y_vel *= -1
            the_ball.y_vel = change_velocity_randomly(the_ball.y_vel)
        # handle ball collision with the floor
        elif the_ball.y + the_ball.radius >= SCREEN_HEIGHT:
            the_ball.y_vel *= -1
            the_ball.y_vel = change_velocity_randomly(the_ball.y_vel)

        # handle the ball hitting the left wall
        if the_ball.x - the_ball.radius <= 0:
            the_ball.x_vel *= -1
            the_ball.x_vel = change_velocity_randomly(the_ball.x_vel)
        # handle the ball hitting the right wall
        elif the_ball.x + the_ball.radius >= SCREEN_WIDTH:
            the_ball.x_vel *= -1
            the_ball.x_vel = change_velocity_randomly(the_ball.x_vel)

def move_all(balls):
    for ball in balls:
        ball.move()


def main():

    run = True
    clock = pygame.time.Clock()

    center_x = SCREEN_WIDTH//2
    center_y = SCREEN_HEIGHT//2

    goal = Goal()

    balls = []
    for s in range(90):
        balls.append(Ball(center_x, center_y, "small"))

    for m in range(50):
        balls.append(Ball(center_x, center_y, "medium"))

    for l in range(10):
        balls.append(Ball(center_x, center_y, "large"))

    for xl in range(5):
        balls.append(Ball(center_x, center_y, "xlarge"))

    

    

    running = True
    while running:
        clock.tick(FPS)

        draw_all(WINDOW, balls, goal)
        move_all(balls)
        wall_collision(balls)
        balls = goal_collision(balls, goal)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


