import pygame
from paddle import Paddle
from ball import Ball

import os

class Game:
    # create game constants (immutable).
    WIDTH, HEIGHT = 700, 500
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
    BALL_RADIUS = 7
    FPS = 60
    MAX_SCORE = 5

    # initialize the game.
    def __init__(self):
        pygame.init()

        # put width and height in a tuple to avoid errors and make it immutable. 
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong game")
        self.font = pygame.font.SysFont(None, 36)

        # fps controller
        self.clock = pygame.time.Clock()
        
        # prompt the user to load a saved game or start a new one
        self.load_saved_game = self.prompt_load_game()
        
        #if there is a saved game
        if self.load_saved_game and os.path.exists("game_state.txt"):
            self.load_game("game_state.txt")
        else:
            # Create the left paddle by providing its initial position (10 pixels from the left edge, centered vertically)
            self.left_paddle = Paddle(10, self.HEIGHT * 0.5 - self.PADDLE_HEIGHT * 0.5, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)

            # Create the right paddle by providing its initial position (10 pixels from the left edge, centered vertically)
            self.right_paddle = Paddle(self.WIDTH - 10 - self.PADDLE_WIDTH, self.HEIGHT // 2 - self.PADDLE_HEIGHT//2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)

            # Create the ball and center it horizontally and vertically.
            self.ball = Ball(self.WIDTH * 0.5, self. HEIGHT * 0.5, self.BALL_RADIUS)

            # set scores to 0
            self.left_score = 0
            self.right_score = 0

    def prompt_load_game(self):
        # Check if saved game file exists
        if not os.path.exists("game_state.txt"):
            return False
        
        # Ask if user wants to load saved game.
        text = self.font.render("Do you want to load your previous game? (Y/N)", True, self.WHITE)
        self.win.fill(self.RED)
        self.win.blit(text, (self.WIDTH//2 - text.get_width() // 2, self.HEIGHT//2 - text.get_height() // 2))
        pygame.display.update()
        
        # Check for y (yes) or n (no)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    elif event.key == pygame.K_n:
                        return False


    
    # save the current game state to a dictionary for later use.
    def save_game(self, filename):
        game_state = {
            "left_score": self.left_score,
            "right_score": self.right_score,
            "left_paddle": self.left_paddle,
            "right_paddle": self.right_paddle,
            "ball": self.ball
        }
		# save the game state to the specified file.
        save_game_state(game_state, filename)
	
	# load the current saved game.
    def load_game(self, filename):
		
		#set game state to the current saved game
        game_state = load_game_state(filename)
        if game_state:
            self.left_score = game_state["left_score"]
            self.right_score = game_state["right_score"]
            self.left_paddle = game_state["left_paddle"]
            self.right_paddle = game_state["right_paddle"]
            self.ball = game_state["ball"]
    
    def draw_objects(self):
        # set background to red.
        self.win.fill(self.RED)


        # draw the paddles in this list. 
        for paddle in (self.left_paddle , self.right_paddle):
            paddle.draw_objects(self.win)
        
        # draw and position the scoring text.
        left_score_text = self.font.render(f'P1: {self.left_score}', 1, self.WHITE)
        right_score_text = self.font.render(f'P2: {self.right_score}', 1, self.WHITE)
        self.win.blit(left_score_text, (self.WIDTH // 4 - left_score_text.get_width() * 0.5, 20))
        self.win.blit(right_score_text, (self.WIDTH * 0.75 - right_score_text.get_width() * 0.5, 20))
        # draw the ball.       
        self.ball.draw_objects(self.win)

        # update the display.
        pygame.display.update()


    def collision(self):
        # Check if the ball has gone out of bounds. If true, reverse the velocity.
        if self.ball.y + self.ball.radius >= self.HEIGHT:
            self.ball.y_velocity *= -1
        elif self.ball.y - self.ball.radius <= 0:
            self.ball.y_velocity *= -1

         # Check if the ball is moving left. If true, check for collision with the left paddle.
        if self.ball.x_velocity < 0:
            if self.ball.y >= self.left_paddle.y and self.ball.y <= self.left_paddle.y + self.left_paddle.height:
                 if self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:
                    self.ball.x_velocity *= -1

                    # check how far the ball is from the middle of the paddle. Adjust the velocity accordingly.
                    middle_y = self.left_paddle.y + self.left_paddle.height / 2

                    # find the difference of the middle point and balls y coordinate.
                    difference_in_y = middle_y - self.ball.y

                    # scale down difference to match velocity of the ball
                    reduction_factor = (self.left_paddle.height / 2) / self.ball.MAX_VELOCITY
                    y_velocity = difference_in_y / reduction_factor

                    #reverse velocity
                    self.ball.y_velocity = -1 * y_velocity
                    


        # Check if the ball is moving right. If true, check for collision with the right paddle.
        else:
            if self.ball.y >= self.right_paddle.y and self.ball.y <= self.right_paddle.y + self.right_paddle.height:
                if self.ball.x + self.ball.radius >= self.right_paddle.x:
                    self.ball.x_velocity *= -1

                    # same logic as the left paddle.
                    middle_y = self.right_paddle.y + self.left_paddle.height / 2 
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = (self.right_paddle.height / 2) / self.ball.MAX_VELOCITY
                    y_velocity = difference_in_y / reduction_factor
                    self.ball.y_velocity = -1 * y_velocity

        
        

    def paddle_movement(self, keys):
        # checks left paddle for key presses (W and S).
        if keys[pygame.K_w] and self.left_paddle.y - self.left_paddle.VELOCITY >= 0:
            self.left_paddle.move(up=True)
        if keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.VELOCITY + self.left_paddle.height <= self.HEIGHT:
            self.left_paddle.move(up=False)

        # checks right paddle for key presses (Up and down arrows).
        if keys[pygame.K_UP] and self.right_paddle.y - self.right_paddle.VELOCITY >= 0:
            self.right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.VELOCITY + self.right_paddle.height <= self.HEIGHT:
            self.right_paddle.move(up=False)


    def run_game(self):

        #initalize the starting screen.
        start_text = self.font.render("Click to start the game!", True, self.WHITE)
        self.win.fill(self.RED)

        #position text on the window. (tuple to avoid error).
        self.win.blit(start_text, (self.WIDTH//2 - start_text.get_width() * 0.5, self.HEIGHT * 0.5 - start_text.get_height() * 0.5))
        pygame.display.update()
        
        # Waiting for mouse click to start game.
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_click = False
                    pygame.quit()
                
                # if user clicks break loop.
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False

        # run the game after click.
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.save_game("game_state.txt")

            #wait for user input.
            keys = pygame.key.get_pressed()
            self.paddle_movement(keys)

            # update the balls position.
            self.ball.move()

            # update collision
            self.collision()

            # check if ball has gone out of bounds on the left, if so, reset ball and add 1 to right score (left side use 0).
            if self.ball.x < 0:
                self.right_score += 1

                # check if max score is reached, if so, reset game.
                if self.right_score >= self.MAX_SCORE:
                    self.display_winner("Player 2 is the winner!")
                    break

                    

                # else reset ball.    
                else:   
                    self.ball.reset_ball()
            
            # same logic as before, reversed. (right side use width.)
            elif self.ball.x > self.WIDTH:
                self.left_score += 1

                if self.left_score >= self.MAX_SCORE:
                    self.display_winner("Player 1 is the winner!")
                    break
                    

                else: 
                    self.ball.reset_ball()

            # draw the game objects.
            self.draw_objects()

            #update the display. 
            pygame.display.update()

            # set fps to 60
            pygame.time.Clock().tick(self.FPS)

    def display_winner(self, winner):
        # set winner text according to the argument passed.
        winner_text = self.font.render(f'{winner}', 1, self.WHITE)

        # positioning of the winner text.
        winner_text_rect = winner_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        # Fill the window with the red color.
        self.win.fill(self.RED)

        # Blit the winner text onto the window.
        self.win.blit(winner_text, winner_text_rect)

        # display countdown till next game starts (5 seconds)
        for i in range(5, 0, -1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            timer_text = self.font.render(f'Restarting in {i} seconds', 1, self.WHITE)
            text_rect = timer_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT * 0.75))
        
            # Clear the area where the timer text is drawn
            pygame.draw.rect(self.win, self.RED, text_rect)
        
            # Draw the timer text
            self.win.blit(timer_text, text_rect)
            pygame.display.update()

            # delete saved game file if it exists
            if os.path.exists("game_state.txt"):
                os.remove("game_state.txt")

            # create a 1 second pause between each iteration of the loop
            pygame.time.delay(1000) 

        # Reset window and run game again.
        self.left_score = 0
        self.right_score = 0
        self.ball.reset_ball()
        self.left_paddle.reset_paddles()
        self.right_paddle.reset_paddles()
        self.run_game()


    

            
        
