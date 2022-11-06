import pygame, math, random, sys

pygame.init()

## create the main window
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

WINDOW = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption("Hungry Hungry Hippos!")

## Game Constants and Files

FPS = 60

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 255, 255)

#Images
horizontal_rectangle = pygame.image.load("images/rectangle_horizontal.png")
vertical_rectangle = pygame.image.load("images/rectangle_vertical.png")

#Hippo Dimensions
MOUTH_LENGTH = 40
SIDE_LENGTH = 30


##Classes
"""
Hippo Class, will explain later
"""
class Hippo:
    def __init__(self, dimensions, color, is_vertical):
        self.x = dimensions[0]
        self.y = dimensions[1]
        self.color = color
        self.is_vertical = is_vertical
        if (is_vertical):
            self.width = MOUTH_LENGTH
            self.height = SIDE_LENGTH
        else:
            self.width = SIDE_LENGTH
            self.height = MOUTH_LENGTH
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        

"""
The Ball class creates all of the balls that the hippos will eat. 
There are four types of balls: small, medium, large, and xlarge. The size of the ball 
The balls are assigned a random velcoity via get_random_velocity() when initialized. 
When the balls hit any wall, they have a 20% chance of having their velocity modified randomly via change_velocity_randomly(initial).
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


def draw_all(window, balls, hippos):
    window.fill(BLACK)

    for hippo in hippos:
        hippo.draw(window)

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

    hippoStarts = {
        "top": (SCREEN_WIDTH//2 - MOUTH_LENGTH//2, 0),
        "bottom":(SCREEN_WIDTH//2 - MOUTH_LENGTH//2, SCREEN_HEIGHT - SIDE_LENGTH),
        "left": (0, SCREEN_HEIGHT//2 - MOUTH_LENGTH//2),
        "right": (SCREEN_WIDTH - SIDE_LENGTH, SCREEN_HEIGHT//2 - MOUTH_LENGTH//2)
    }

    top_hippo = Hippo(hippoStarts["top"], RED, True)
    bottom_hippo = Hippo(hippoStarts["bottom"], GREEN, True)
    left_hippo = Hippo(hippoStarts["left"], YELLOW, False)
    right_hippo = Hippo(hippoStarts["right"], BLUE, False)

    hippos = [top_hippo, bottom_hippo, left_hippo, right_hippo]

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

        draw_all(WINDOW, balls, hippos) ##NEEDS TO BE UPDATED
        move_all(balls)
        wall_collision(balls)
        #balls = goal_collision(balls, goal) ##NEEDS TO BE UPDATED

        keys = pygame.key.get_pressed()
        #move_hippos(events, hippos)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()