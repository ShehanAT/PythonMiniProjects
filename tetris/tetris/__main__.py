import pygame, sys, os, random 
from time import sleep 
from pygame.math import Vector2
from pygame.locals import *  


HEIGHT = 800 
WIDTH = 600
BACKGROUND = (0, 0, 0)
FALL_SPEED = 5
GRAVITY = 0.2 # variable that represents gravity 
SPEED = 5
# colors 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

window = pygame.display.set_mode((HEIGHT, WIDTH))
update_rect = pygame.Rect(HEIGHT/2, WIDTH/2, 500, 400)
def main():
    pygame.init()
    window_rect = window.get_rect()
    window.fill((20, 40, 70))
    clock = pygame.time.Clock()
    pygame.display.update() 
    all_sprites = pygame.sprite.Group()

    running = True
    square = Square()
    all_sprites.add(square) 
    
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if pygame.event == pygame.K_ESCAPE:
                sys.exit(0)
            if pygame.key.get_pressed()[K_LEFT]:
                square.control(-SPEED, 0)
            if pygame.key.get_pressed()[K_RIGHT]:
                square.control(SPEED, 0)
        window.fill((20, 40, 70))
        all_sprites.update() # runs Square's update()
        all_sprites.draw(window)
        pygame.display.flip()


class Square(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (250, 250)
        self.speed = 5 

    def control(self, moveX, moveY):
        self.rect.x += moveX
        self.rect.y += moveY 
        

    def update(self):
        self.rect.y += self.speed   
        if self.rect.y > 600:
            self.rect.y = 0   


# run the main function only if thi smodule is executed as the main script 
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function 
    main()

      