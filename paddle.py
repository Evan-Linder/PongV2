import pygame


class Paddle:
    WHITE = (255, 255, 255)
    VELOCITY = 5

    # Initalize the paddles.
    def __init__ (self, x, y, width, height):

        # set the self attributes to the arugments passed.
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    # set the values of the dimensions in a tuple to avoid errors and make them unmutable.
    def draw_objects(self, win):
        pygame.draw.rect(win, self.WHITE, (self.x, self.y, self.width, self.height))

    # move the paddle up or down.
    def move(self, up = True):
        if up:
            self.y -= self.VELOCITY
        
        else:
            self.y += self.VELOCITY


    # Reset paddle positions
    def reset_paddles(self):
        self.x = self.original_x
        self.y = self.original_y
        










