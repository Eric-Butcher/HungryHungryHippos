import pygame, math, random, sys, time

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
global ball_color
ball_color = (255, 255, 255)


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
    def __init__(self, dimensions, color, is_vertical, name):
        self.x = dimensions[0]
        self.y = dimensions[1]
        self.x_initial = dimensions[0]
        self.y_initial = dimensions[1]
        self.color = color
        self.is_chewing = False
        self.is_vertical = is_vertical
        self.score = 0
        self.name = name
        if (is_vertical):
            self.width = MOUTH_LENGTH
            self.height = SIDE_LENGTH
            self.width_initial = MOUTH_LENGTH
            self.height_initial = SIDE_LENGTH
        else:
            self.width = SIDE_LENGTH
            self.height = MOUTH_LENGTH
            self.width_initial = SIDE_LENGTH
            self.height_initial = MOUTH_LENGTH
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
    def activate_chomp(self):
        self.is_chewing = True
        if (self.name == "top"):
            self.height = self.height_initial * 2
        elif (self.name == "left"):
            self.width = self.width_initial * 2
        elif (self.name == "right"):
            self.x = self.x_initial - SIDE_LENGTH
            self.width = self.width_initial + SIDE_LENGTH
        elif (self.name == "bottom"):
            self.y = self.y_initial - SIDE_LENGTH
            self.height = self.height_initial + SIDE_LENGTH
    def deactivate_chomp(self):
        self.is_chewing = False
        if (self.name == "top"):
            self.height = self.height_initial
        elif (self.name == "left"):
            self.width = self.width_initial
        elif (self.name == "right"):
            self.x = self.x_initial
            self.width = self.width_initial 
        elif (self.name == "bottom"):
            self.y = self.y_initial 
            self.height = self.height_initial 

"""
The Ball class creates all of the balls that the hippos will eat. 
There are four types of balls: small, medium, large, and xlarge. The size of the ball 
The balls are assigned a random velcoity via get_random_velocity() when initialized. 
When the balls hit any wall, they have a 20% chance of having their velocity modified randomly via change_velocity_randomly(initial).
"""
class Ball:
    DEFAULT_COLOR = WHITE
    

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
        pygame.draw.circle(window, ball_color, (self.x, self.y), self.radius)

    def move(self):
        self.y += self.y_vel
        self.x += self.x_vel

def get_random_velocity():
    retVal = random.randint(-10, 10)
    if retVal == 0:
        retVal += 1
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
        hippo.deactivate_chomp()

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

def hippo_collision(balls, hippos):
    for hippo in hippos:
            boundries = calcualte_hippo_boundries(hippo)
            for ball in balls:
                ball_x = ball.x
                ball_y = ball.y
                if (ball_x < boundries["right"]) and (ball.x > boundries["left"]):
                    if (ball_y > boundries["top"]) and (ball_y < boundries["bottom"]):
                        ball.x_vel *= -1
                        ball.y_vel *= -1

def move_all(balls):
    for ball in balls:
        ball.move()

def hippo_chomp(events, hippos):
    for event in events:
        if event.type == pygame.KEYDOWN:

            #Top hippo
            if event.key == pygame.K_q and not hippos[0].is_chewing:
                hippos[0].activate_chomp()
                #print("Acitvated!")

            #Left Hippo
            if event.key == pygame.K_z and not hippos[2].is_chewing:
                hippos[2].activate_chomp()
                #print("Acitvated!")

            #Right Hippo
            if event.key == pygame.K_p and not hippos[3].is_chewing:
                hippos[3].activate_chomp()
                # print("Acitvated!")

            #Bottom Hippo
            if event.key == pygame.K_m and not hippos[1].is_chewing:
                hippos[1].activate_chomp()
                #print("Acitvated!")

def calcualte_hippo_boundries(hippo):
    boundries = {
        "left":hippo.x, 
        "right": (hippo.x + hippo.width),
        "top":hippo.y, 
        "bottom" :(hippo.y + hippo.height)
    }
    return boundries

def hippo_eat(balls, hippos):
    for hippo in hippos:
        if hippo.is_chewing:
            boundries = calcualte_hippo_boundries(hippo)
            for ball in balls:
                ball_x = ball.x
                ball_y = ball.y
                if (ball_x < boundries["right"]) and (ball.x > boundries["left"]):
                    if (ball_y > boundries["top"]) and (ball_y < boundries["bottom"]):

                        if (ball.size == "small"):
                            hippo.score += 3
                        if (ball.size == "medium"):
                            hippo.score += 2
                        if (ball.size == "large" or ball.size == "xlarge"):
                            hippo.score += 1
                        balls.remove(ball)
                        #hippo.score += 1
                        #print("Scored!")


        
        


def main():

    ball_amounts = {
        "small":90, 
        "medium":50, 
        "large":10, 
        "xlarge":5
    }

    game_end_code = 0
    clock = pygame.time.Clock()

    center_x = SCREEN_WIDTH//2
    center_y = SCREEN_HEIGHT//2

    hippoStarts = {
        "top": (SCREEN_WIDTH//2 - MOUTH_LENGTH//2, 0),
        "bottom":(SCREEN_WIDTH//2 - MOUTH_LENGTH//2, SCREEN_HEIGHT - SIDE_LENGTH),
        "left": (0, SCREEN_HEIGHT//2 - MOUTH_LENGTH//2),
        "right": (SCREEN_WIDTH - SIDE_LENGTH, SCREEN_HEIGHT//2 - MOUTH_LENGTH//2)
    }

    top_hippo = Hippo(hippoStarts["top"], RED, True, "top")
    bottom_hippo = Hippo(hippoStarts["bottom"], GREEN, True, "bottom")
    left_hippo = Hippo(hippoStarts["left"], YELLOW, False, "left")
    right_hippo = Hippo(hippoStarts["right"], BLUE, False, "right")

    hippos = [top_hippo, bottom_hippo, left_hippo, right_hippo]

    balls = []
    for s in range(ball_amounts["small"]):
        balls.append(Ball(center_x, center_y, "small"))

    for m in range(ball_amounts["medium"]):
        balls.append(Ball(center_x, center_y, "medium"))

    for l in range(ball_amounts["large"]):
        balls.append(Ball(center_x, center_y, "large"))

    for xl in range(ball_amounts["xlarge"]):
        balls.append(Ball(center_x, center_y, "xlarge"))

    

    
    start_time = time.time()
    running = True
    while running:
        clock.tick(FPS)

        time_elapsed = time.time() - start_time
        ball_color_variation = 2 * int(time_elapsed)
        global ball_color
        ball_color = (255, 255 - ball_color_variation, 255)
        #ball_color = (255 - ball_color_variation, 255 - ball_color_variation, 255 - ball_color_variation)
        print(ball_color_variation)
        
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        pygame.key.set_repeat(5000)

        hippo_chomp(events, hippos)
        hippo_eat(balls, hippos)
        draw_all(WINDOW, balls, hippos) ##NEEDS TO BE UPDATED
        move_all(balls)
        hippo_collision(balls, hippos)
        wall_collision(balls)
        #balls = goal_collision(balls, goal) ##NEEDS TO BE UPDATED

        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break

        if (len(balls) <= 0 or time_elapsed >= 120):
            running = False
            game_end_code = 3
            break

    if (game_end_code == 3):
        ending = True
        print("#################")
        for hippo in hippos:
            print("Hippo " + hippo.name + " scored: " + str(hippo.score) + "!")
        print("#################")
        while ending:
            #show end screen
            for event in events:
                if event.type == pygame.QUIT:
                    ending = False
                    break
    
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()