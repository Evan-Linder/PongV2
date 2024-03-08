import pygame


class Paddle:
    WHITE = (255, 255, 255)
    # Initalize the paddles.
    def __init__ (self, x, y, width, height):

        # set the self attributes to the arugments passed.
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw_objects(self, win):
        # set the values of the dimensions in a tuple to avoid errors and make them unmutable.
        pygame.draw.rect(win, self.WHITE, (self.x, self.y, self.width, self.height))






