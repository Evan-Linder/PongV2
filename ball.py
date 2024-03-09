import pygame

class Ball:
    MAX_VELOCITY = 5
    WHITE = (255, 255, 255)

    # set the self attributes to the arguments passed.
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

     # Draw the ball on the window, make x and y unmutable and use circle instead of rect. 
    def draw_objects(self, win):
        pygame.draw.circle(win, self.WHITE, (self.x, self.y), self.radius) 
    
    # move the ball
    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
    
    # resets the ball position and changes the velocity.
    def reset_ball(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1

    

    




    