# Memory Puzzle
# Version 1.0 By Al Sweigart al@inventwithpython.com
# Version 1.1 By Shehan Atukorala codinginformer.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import pygame
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
# BOARDWIDTH = 10 # number of columns of icons
# BOARDHEIGHT = 7 # number of rows of icons
BOARDWIDTH = 4 
BOARDHEIGHT = 3 
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
GAME_SCORE = 0


#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
# RED      = (255,   0,   0)
# GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
# YELLOW   = (255, 255,   0)
# ORANGE   = (255, 128,   0)
# PURPLE   = (255,   0, 255)
# CYAN     = (  0, 255, 255)


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

# ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLCOLORS_2 = (SPRITE_RED, SPRITE_GREEN, SPRITE_BLUE, SPRITE_YELLOW, SPRITE_TAN, SPRITE_GREY, SPRITE_TEAL)
# ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
ALLSHAPES_2 = (DIAMOND, HEXAGON, OCTAGON, SQUARE, TRIANGLE)

# assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."
assert len(ALLCOLORS_2) * len(ALLSHAPES_2) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def drawTestSprite(imagePath, left, top, width, height):
    gemImage = pygame.transform.scale(pygame.image.load(imagePath).convert_alpha(), (width, height))
    gem = Gem((left, top), gemImage)
    gem.draw(DISPLAYSURF)

def levelUp():
    global BOARDWIDTH, BOARDHEIGHT
    BOARDWIDTH += 1 
    BOARDHEIGHT += 1 

def displayTimer():
    # global TIMER_RUNNING, TIMER_PAUSED


    # while TIMER_RUNNING:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             TIMER_RUNNING = False 
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 TIMER_RUNNING = False 
    #             if event.key == pygame.K_SPACE:
    #                 TIMER_PAUSED = not TIMER_PAUSED

    #     if not TIMER_PAUSED:
            

    #         counting_minutes = str(counting_time/60000).zfill(2)
    #         counting_seconds = str((counting_time%60000)/1000).zfill(2)
    #         counting_millisecond = str(counting_time%1000).zfill(3)


    #     pygame.display.update()

    #     FPSCLOCK.tick(FPS)
    #     clock.tick(25)
    pass 

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
    

def main():
    global FPSCLOCK, DISPLAYSURF, GAME_SCORE 

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
        game_score_string = "Score: " + str(GAME_SCORE)
        game_score_text = font.render(game_score_string, 1, (255, 255, 255))
        game_score_rect = game_score_text.get_rect(center = (60, 10))

        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
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
    for color in ALLCOLORS_2:
        for shape in ALLSHAPES_2:
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
    print(transposeBoard)
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
    # Draw the shapes
    # if shape == DONUT:
    #     print(color);
    #     drawTestSprite(BLUEGEM_ASSETPATH, left + half, top + half, 40, 40)
    #     pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
    #     pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    # elif shape == SQUARE:
    #     print(color);
    #     drawTestSprite(BLUEGEM_ASSETPATH, left + half, top + half, 40, 40)
    #     # pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    # elif shape == DIAMOND:
    #     pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    # elif shape == LINES:
    #     for i in range(0, BOXSIZE, 4):
    #         pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
    #         pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    # elif shape == OVAL:
    #     pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))
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
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        # break;
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
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
    boxGroups = splitIntoGroupsOf(8, boxes)

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
    for i in revealedBoxes:
        if False in i:
            GAME_SCORE += 10
            return False # return False if any boxes are covered.
    return True



if __name__ == '__main__':
    main()