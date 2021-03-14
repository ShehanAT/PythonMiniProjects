import pygame, sys, os, random 
from time import sleep 
from pygame.math import Vector2
from pygame.locals import *  


HEIGHT = 800 
WIDTH = 600
BACKGROUND = (0, 0, 0)
FALL_SPEED = 5
GRAVITY = 0.2 # variable that represents gravity 
window = pygame.display.set_mode((HEIGHT, WIDTH))

def main():
    pygame.init()
    window_rect = window.get_rect()
    window.fill((0, 0, 0))
    clock = pygame.time.Clock()
    pygame.display.update() 
    all_sprites = pygame.sprite.Group()
    # Pass this rect to pygame.display.update() to update only this area
    update_rect = pygame.Rect(0, 0, 500, 500) 
    square1 = Square(window_rect)
    all_sprites.add(square1)
    all_sprites.update()
    all_sprites.draw(window)
    window.blit(square1.image, (square1.rect.x, square1.rect.y))
    pygame.display.update()
    clock.tick(60)
    sleep(2)
   # window.fill((20, 50, 90)) # fill Surface with solid color 
    #sleep(2)
    #square1.update()
   # all_sprites.update() # this calls Square.update()
    #all_sprites.draw(window)

   # pygame.display.update()
   # sleep(2)

class Square(pygame.sprite.Sprite):

    def __init__(self, window_rect):
        super().__init__()
        self.window_rect = window_rect
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=window_rect.center)
        self.speed = Vector2(10, 10)
        self.pos = Vector2(self.rect.center)
        pygame.draw.rect(self.image, (255, 0, 0), self.rect) 
       

    def update(self):
        self.yMoveAmt = 100
        self.pos += self.speed 
        self.rect.center = self.pos

    def drawChar(self):
        pygame.display.update()
        fpsclock.tick(fps)

    def moveChar(self):
        self.rect.update(window, self.yMoveAmt)
        pygame.display.update() 
        fpsclock.tick(fps)


# run the main function only if thi smodule is executed as the main script 
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function 
    main()

          