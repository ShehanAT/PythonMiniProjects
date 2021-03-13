import pygame, sys, os 
import pygame.examples.chimp
from pygame.locals import * 
'''
initialize the pygame module: pygame.init()
create screen: pygame.display.set_mode((x, y))
set logo: pygame.display.set_icon(logo)
get all events from the event queue: for event in pygame.event.get():
get type of event: event.type

'''

GRAVITY = 0.2 # variable that represents gravity 


def main():
    # initialize game variable 
    x = 234
    y = 0
    step = 5
    fpsclock = pygame.time.Clock()
    fps = 30 
    window_height = 468
    window_width = 468 
    window_bottom = 415 
    # initialize the pygame module 
    pygame.init()
    blue_background = (0, 0, 0)
    window = pygame.display.set_mode((window_height, window_width))
 
    # create a surface on screen that has the size of 240 x 180 
    screen = pygame.display.get_surface()
    

    # fliping the screen updates the display, the reason for needing to flip the screen 
    # is to tell pygame that you're finished making changes for the current frame 
    # and now want to show the changes on screen 
    # pygame.display.flip()


    # define a variable to control the main loop 
    falling = True 
    running = True 
    # main loop 
    while running:
        while falling:
            window.fill(blue_background)
            pygame.draw.rect(window, (255, 0, 0), (x, y, 70, 65))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_LEFT]:
                x -= step 
            if key_input[pygame.K_RIGHT]:
                x += step 
            y += step 
            if(y == window_bottom):
                falling = False  
            pygame.display.update()
            fpsclock.tick(fps)
        falling = True 

# run the main function only if thi smodule is executed as the main script 
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function 
    main()

          