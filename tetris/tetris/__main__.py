import pygame, sys, os, random 
from time import sleep 
from pygame.math import Vector2
from pygame.locals import *  


HEIGHT = 400 
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
    counter = 0
    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if pygame.event == pygame.K_ESCAPE:
                running = False 
                sys.exit(0)
            if pygame.event == pygame.KEYDOWN:
                print(pygame.key.name(event.key))
        keys = pygame.key.get_pressed()
        # this enables continous movement 
        square.control((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED)
        if square.atBottom == True:
            square = Square()
            all_sprites.add(square)
        window.fill((20, 40, 70))
        all_sprites.update() # runs Square's update()
        all_sprites.draw(window)
        pygame.display.flip()


class Square(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        sizeX = random.randrange(1, 20, 5)
        sizeY = random.randrange(1, 20)
        self.image = pygame.Surface((sizeX, sizeY))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (HEIGHT/2, 0)
        self.speed = 10 
        self.atBottom = False 

    def control(self, speed):
        # if statements prevent square from going off screen in x-axis
        if self.rect.x <= 5 and speed < 0: 
            return 
        if self.rect.x >= (HEIGHT - 15) and speed > 0:
            return 
        else:
            self.rect.x += speed 

    def update(self):
        self.rect.y += self.speed   
        if self.rect.y > (WIDTH - 20):
            self.speed = 0
            self.atBottom = True 
      
        # set bounds for left and right edges of screen 




# run the main function only if thi smodule is executed as the main script 
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function 
    main()

      