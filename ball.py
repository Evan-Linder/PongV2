import pygame

class Ball:
    MAX_VELOCITY = 4
    WHITE = (255, 255, 255)

    def __init__(self, x, y, radius):
        # set the self attributes to the arguments passed.
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw_objects(self, win):
        # Draw the ball on the window, make x and y unmutable and use circle instead of rect. 
        pygame.draw.circle(win, self.WHITE, (self.x, self.y), self.radius) 
    
    def move(self):
        #move the ball
        self.x += self.x_velocity
        self.y += self.y_velocity




    