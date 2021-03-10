import pygame 

'''
initialize the pygame module: pygame.init()
create screen: pygame.display.set_mode((x, y))
set logo: pygame.display.set_icon(logo)
get all events from the event queue: for event in pygame.event.get():
get type of event: event.type

'''

def main():

    # initialize the pygame module 
    pygame.init()
    # load and set the logo 
    logo = pygame.image.load("logo.jpg")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")

    # create a surface on screen that has the size of 240 x 180 
    screen = pygame.display.set_mode((480,360))

    # define a variable to control the main loop 
    running = True 

    # main loop 
    while running:
        # event handling, gets all event from the event queue 
        for event in pygame.event.get():
            # only do something if the event is of type QUIT 
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop 
                running = False 
# run the main function only if thi smodule is executed as the main script 
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function 
    main()           