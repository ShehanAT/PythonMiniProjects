import pygame 


GRAVITY = 0.2 

class Square(pygame.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        # SRCALPHA flag indicates the pixel format will include a per-pixel alpha 
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        # syntax is (image to use, (color in RGB), Rect(left, top, width, height))
        pygame.draw.rect(self.image, (30, 60, 90), pygame.Rect(50, 50, 1, 50))
        self.speed_y = 
        self.speed_x = 0
        self.pos_y = pos[1]
        self.pos_x = 10

