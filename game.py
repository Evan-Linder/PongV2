import pygame

class Game:
    #create game constants (unmutable).
    WIDTH, HEIGHT = 700,500
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def run(self):
        # run the game.
        
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        
