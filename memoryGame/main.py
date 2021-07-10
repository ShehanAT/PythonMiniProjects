# Memory Puzzle
# Version 1.0 By Al Sweigart al@inventwithpython.com
# Version 1.1 By Shehan Atukorala codinginformer.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import pygame
import pygame_menu 
import random 
import sys 

DIAMOND_ASSETPATH = {
    "red": "./assets/red_diamond.png",
    "green": "./assets/green_diamond.png",
    "blue": "./assets/blue_diamond.png",
    "yellow": "./assets/yellow_diamond.png",
    "tan": "./assets/tan_diamond.png",
    "grey": "./assets/grey_diamond.png",
    "teal": "./assets/teal_diamond.png"
}
HEXAGON_ASSETPATH = {
    "red": "./assets/red_hexagon.png",
    "green": "./assets/green_hexagon.png",
    "blue": "./assets/blue_hexagon.png",
    "yellow": "./assets/yellow_hexagon.png",
    "tan": "./assets/tan_hexagon.png",
    "grey": "./assets/grey_hexagon.png",
    "teal": "./assets/teal_hexagon.png"
}
OCTAGON_ASSETPATH = {
    "red": "./assets/red_octagon.png",
    "green": "./assets/green_octagon.png",
    "blue": "./assets/blue_octagon.png",
    "yellow": "./assets/yellow_octagon.png",
    "tan": "./assets/tan_octagon.png",
    "grey": "./assets/grey_octagon.png",
    "teal": "./assets/teal_octagon.png"
}
SQUARE_ASSETPATH = {
    "red": "./assets/red_square.png",
    "green": "./assets/green_square.png",
    "blue": "./assets/blue_square.png",
    "yellow": "./assets/yellow_square.png",
    "tan": "./assets/tan_square.png",
    "grey": "./assets/grey_square.png",
    "teal": "./assets/teal_square.png"
}
TRIANGLE_ASSETPATH = {
    "red": "./assets/red_triangle.png",
    "green": "./assets/green_triangle.png",
    "blue": "./assets/blue_triangle.png",
    "yellow": "./assets/yellow_triangle.png",
    "tan": "./assets/tan_triangle.png",
    "grey": "./assets/grey_triangle.png",
    "teal": "./assets/teal_triangle.png"
}


FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 4 # number of columns of icons
BOARDHEIGHT = 3 # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
GAME_SCORE = 0
GAME_LEVEL = 1 
GAME_PAUSED = False 


#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)


BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

TIMER_PAUSED = False 
TIMER_RUNNING = True 

SQUARE = 'square'
DIAMOND = 'diamond'
HEXAGON = 'hexagon'
OCTAGON = 'octagon'
TRIANGLE = 'triangle'

SPRITE_RED = "red"
SPRITE_GREEN = "green"
SPRITE_BLUE = "blue"
SPRITE_YELLOW = "yellow"
SPRITE_TAN = "tan"
SPRITE_GREY = "grey"
SPRITE_TEAL = "teal"

ALLCOLORS = (SPRITE_RED, SPRITE_GREEN, SPRITE_BLUE, SPRITE_YELLOW, SPRITE_TAN, SPRITE_GREY, SPRITE_TEAL)
ALLSHAPES = (DIAMOND, HEXAGON, OCTAGON, SQUARE, TRIANGLE)

def levelUp():
    global BOARDWIDTH, BOARDHEIGHT
    BOARDWIDTH += 1 
    BOARDHEIGHT += 1 


def drawDiamondSprite(color, left, top, width, height):
    diamondImage = None; 
    if(DIAMOND_ASSETPATH[color]):
        diamondImage = DIAMOND_ASSETPATH[color];
    diamondImage = pygame.transform.scale(pygame.image.load(diamondImage).convert_alpha(), (width, height))
    diamond = Gem((left, top), diamondImage)
    diamond.draw(DISPLAYSURF)

def drawHexagonSprite(color, left, top, width, height):
    hexagonImage = None; 
    if(HEXAGON_ASSETPATH[color]):
        hexagonImage = HEXAGON_ASSETPATH[color];
    hexagonImage = pygame.transform.scale(pygame.image.load(hexagonImage).convert_alpha(), (width, height))
    hexagon = Gem((left, top), hexagonImage)
    hexagon.draw(DISPLAYSURF)

def drawOctagonSprite(color, left, top, width, height):
    octagonImage = None; 
    if(OCTAGON_ASSETPATH[color]):
        octagonImage = OCTAGON_ASSETPATH[color];
    octagonImage = pygame.transform.scale(pygame.image.load(octagonImage).convert_alpha(), (width, height))
    octagon = Gem((left, top), octagonImage)
    octagon.draw(DISPLAYSURF)

def drawSquareSprite(color, left, top, width, height):
    squareImage = None; 
    if(SQUARE_ASSETPATH[color]):
        squareImage = SQUARE_ASSETPATH[color];
    squareImage = pygame.transform.scale(pygame.image.load(squareImage).convert_alpha(), (width, height))
    square = Gem((left, top), squareImage)
    square.draw(DISPLAYSURF)

def drawTriangleSprite(color, left, top, width, height):
    triangleImage = None; 
    if(TRIANGLE_ASSETPATH[color]):
        triangleImage =TRIANGLE_ASSETPATH[color];
    triangleImage = pygame.transform.scale(pygame.image.load(triangleImage).convert_alpha(), (width, height))
    triangle = Gem((left, top), triangleImage)
    triangle.draw(DISPLAYSURF)

class Gem(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image 
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect);

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(DISPLAYSURF, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    DISPLAYSURF.blit(textSurf, textRect)

def unpause():
    global GAME_PAUSED 
    GAME_PAUSED = False 

def quit_game():
    pygame.quit()
    sys.exit()

def pause():
    font = pygame.font.SysFont("Consolas", 32)
    while GAME_PAUSED:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pause_text = font.render("Game Paused", 1, (255, 255, 255))
        pause_rect = pause_text.get_rect(center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 - 210))
        print(pause_text.get_size())
        pause_surface = pygame.Surface((210, 145))
        pause_surface.fill((0, 0, 0))
        pause_surface.blit(pause_text, (0, 0))
        DISPLAYSURF.blit(pause_surface, pause_rect)
        button("Resume", WINDOWWIDTH/2 - 35, WINDOWHEIGHT/2 - 140, 100, 50, NAVYBLUE, GRAY, unpause)
        button("Quit", WINDOWWIDTH/2 - 35, WINDOWHEIGHT/2 - 190, 100, 50, NAVYBLUE, GRAY, quit_game)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def main():
    global FPSCLOCK, DISPLAYSURF, GAME_SCORE, GAME_LEVEL, GAME_PAUSED 

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)
    start_time = pygame.time.get_ticks()

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)
        font = pygame.font.SysFont(None, 32)
        game_score_string = "Score: " + str(GAME_SCORE) + "     Level: " + str(GAME_LEVEL)
        game_score_text = font.render(game_score_string, 1, (255, 255, 255))
        game_score_rect = game_score_text.get_rect(center = (120, 10))

        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT:
            # or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                GAME_PAUSED = True  
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            pause()
        DISPLAYSURF.fill((0, 0, 0), (0, 0, 250, 30))
        DISPLAYSURF.blit(game_score_text, game_score_rect)
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): # check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)
                        levelUp()
                        GAME_LEVEL += 1
                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        
                        drawBoard(mainBoard, revealedBoxes)

                        pygame.display.update()
                        pygame.time.wait(1000)
                        # Replay the start game animation.
                        startGameAnimation(mainBoard)
                    
                    firstSelection = None # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        
        pygame.display.update()
       
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )
    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    transposeBoard = [*zip(*board)]
    # print(transposeBoard)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half = int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    if shape == DIAMOND:
        drawDiamondSprite(color, left + half, top + half, BOXSIZE, BOXSIZE)
    elif shape == HEXAGON:
        drawHexagonSprite(color, left + half, top + half, BOXSIZE, BOXSIZE)
    elif shape == OCTAGON:
        drawOctagonSprite(color, left + half, top + half, BOXSIZE, BOXSIZE)
    elif shape == SQUARE:
        drawSquareSprite(color, left + half, top + half, BOXSIZE, BOXSIZE)
    elif shape == TRIANGLE:
        drawTriangleSprite(color, left + half, top + half, BOXSIZE, BOXSIZE)


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    pauseDisplay = False 
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        # break;
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
        # elif coverage <= 0 and pauseDisplay == False:
        #     pauseDisplay = True 
        #     pygame.time.wait(1000);
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    # for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        print(coverage);
        if(coverage < 0):
            pygame.time.wait(1000);
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(BOARDWIDTH*BOARDHEIGHT, boxes)
    # boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    global GAME_SCORE
    # Returns True if all the boxes have been revealed, otherwise False
    GAME_SCORE += 10
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True



if __name__ == '__main__':
    main()