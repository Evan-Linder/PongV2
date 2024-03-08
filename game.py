import pygame
from paddle import Paddle
from ball import Ball

class Game:
    # create game constants (unmutable).
    WIDTH, HEIGHT = 700, 500
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
    BALL_RADIUS = 7

    # initalize the game.
    def __init__(self):
        pygame.init()

        # put width and height in a tuple to avoid errors and make it unmutable. 
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong game")

        # Create the left paddle by providing its initial position (10 pixels from the left edge, centered vertically)
        self.left_paddle = Paddle(10, self.HEIGHT * 0.5 - self.PADDLE_HEIGHT * 0.5, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)

        # Create the right paddle by providing its initial position (10 pixels from the left edge, centered vertically)
        self.right_paddle = Paddle(self.WIDTH - 10 - self.PADDLE_WIDTH, self.HEIGHT // 2 - self.PADDLE_HEIGHT//2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)

        # Create the ball and center it horizontally and vertically.
        self.ball = Ball(self.WIDTH * 0.5, self. HEIGHT * 0.5, self.BALL_RADIUS)

    def draw_objects(self):
        # set background to red.
        self.win.fill(self.RED)

        # draw the paddles in this list. 
        for paddle in (self.left_paddle , self.right_paddle):
            paddle.draw_objects(self.win)
        
        self.ball.draw_objects(self.win)

        # update the display.
        pygame.display.update()
    
    def paddle_movement(self, keys):
        # checks left paddle for key presses. (W and S)
        if keys[pygame.K_w] and self.left_paddle.y - self.left_paddle.VELOCITY >= 0:
            self.left_paddle.move(up=True)
        if keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.VELOCITY + self.left_paddle.height <= self.HEIGHT:
            self.left_paddle.move(up=False)

        # checks right paddle for key presses. (Up and down arrows)
        if keys[pygame.K_UP] and self.right_paddle.y - self.right_paddle.VELOCITY >= 0:
            self.right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.VELOCITY + self.right_paddle.height <= self.HEIGHT:
            self.right_paddle.move(up=False)


    def run_game(self):
        # run the game.
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            #wait for user input.
            keys = pygame.key.get_pressed()
            self.paddle_movement(keys)

            # update the balls position.
            self.ball.move()

            # draw the game objects.
            self.draw_objects()

            #update the display. 
            pygame.display.update()
        
