# Flippy (an Othello or Reversi clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Based on the "reversi.py" code that originally appeared in "Invent
# Your Own Computer Games with Python", chapter 15:
#   http://inventwithpython.com/chapter15.html

import random, sys, pygame, time, copy, pygame_menu
from pygame.locals import *

FPS = 10 # frames per second to update the screen
WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels
SPACESIZE = 100 # width & height of each space on the board, in pixels
BOARDWIDTH = 5 # how many columns of spaces on the game board
BOARDHEIGHT = 5 # how many rows of spaces on the game board
BLUE_TILE = 'BLUE_TILE' # an arbitrary but unique value
BLACK_TILE = 'BLACK_TILE' # an arbitrary but unique value
RED_TILE = 'RED_TILE'
GREEN_TILE = 'GREEN_TILE'
CITY_HALL = 'CITY_HALL'
SPEAK_EASY = "SPEAK_EASY"
LOAN_SHARK = 'LOAN_SHARK'
MOM_POP = 'MOM_POP'
PAWN_SHOP = 'PAWN_SHOP'
BANK = "BANK"
FINANCIAL_DISTRICT = 'FINANCIAL_DISTRICT'
RACE_TRACK = 'RACE_TRACK'
DISTILLERY = "DISTILLERY"
CASINO = "CASINO"
EMPTY_SPACE = 'EMPTY_SPACE' # an arbitrary but unique value
HINT_TILE = 'HINT_TILE' # an arbitrary but unique value
ANIMATIONSPEED = 25 # integer from 1 to 100, higher is faster animation

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)
RED        = (255, 0, 0)
YELLOW     = (255, 255, 0)
ORANGE     = (255, 69, 0)


class madeMan(pygame.sprite.Sprite):
    def __init__(self, color):
        super(madeMan, self).__init__()
        #self.Rect = pygame.Rect(100,100,SPACESIZE/2 - 5,SPACESIZE/2 - 5)
        #self.surf = pygame.Surface((SPACESIZE/2 -5, SPACESIZE/2 - 5))
        #pygame.draw.rect(self.surf, color, (0, 0, SPACESIZE/2 -5, SPACESIZE/2 - 5))
        self.surf = pygame.image.load('MadeMan.png')
        self.surf.convert()
        self.surf = pygame.transform.scale(self.surf, (SPACESIZE/2 - 5, SPACESIZE/2 - 5))
        self.colorim = pygame.Surface(self.surf.get_size()).convert_alpha()
        self.colorim.fill(color)
        self.surf.blit(self.colorim, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
        self.rect = self.surf.get_rect()

class cop_piece(pygame.sprite.Sprite):
    def __init__(self, color):
        super(cop_piece, self).__init__()
        self.surf = pygame.image.load('Cop.png')
        self.surf.convert()
        self.surf = pygame.transform.scale(self.surf, (SPACESIZE/2 - 5, SPACESIZE/2 - 5))
        pygame.Surface.set_colorkey(self.surf, (255,255,255))
        self.rect = self.surf.get_rect()



# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

#XMARGIN = 0
#YMARGIN = 0



TEXTBGCOLOR1 = BLACK
TEXTBGCOLOR2 = BRIGHTBLUE
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN



def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE, no_piece, player1, player2, player3, player4, cop

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Gangster')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)   

    # Set up the background image.
    boardImage = pygame.image.load('whiteboard.png')
    # Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('blackboard.png')
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)

    no_piece= "NO_PIECE"
    player1 = madeMan(BLACK)
    player2 = madeMan(BRIGHTBLUE)
    player3 = madeMan(RED)
    player4 = madeMan(GREEN)
    cop = cop_piece(BROWN)


    # Run the main game.
    while True:
        if runGame() == False:
            break


def runGame():
    # Plays a single game of reversi each time this function is called.
    player1Tile = None
    player2Tile = None
    player3Tile = None
    player4Tile = None
 
    # Reset the board and game.
    mainBoard = getNewBoard()
    pieces = getPieces()
    resetBoard(mainBoard)
    resetPieces(pieces)
    showHints = False
    players = ['player1', 'player2']
    turn = random.choice(players)

    # Draw the starting board and ask the player what color they want.
    drawBoard(mainBoard, pieces)
    player1Tile = enterPlayerTile()
    print("player1Tile")
    player2Tile = enterPlayerTile()
    print("player2Tile")
    #player3Tile = enterPlayerTile()
    #print("player3Tile")
    #player4Tile = enterPlayerTile()
    #print("player4Tile")
    starting_pos = chooseStartingPositions(turn, players, mainBoard, pieces)
    print("START GAME!")

    


    # Make the Surface and Rect objects for the "New Game" and "Hints" buttons
    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)
    hintsSurf = FONT.render('Hints', True, TEXTCOLOR, TEXTBGCOLOR2)
    hintsRect = hintsSurf.get_rect()
    hintsRect.topright = (WINDOWWIDTH - 8, 40)

    #Action Menu objects - rect is (left,top,width,height)
    MENUWIDTH = WINDOWWIDTH / 6
    MENUHEIGHT = WINDOWHEIGHT / 3
    BUTTONWIDTH = MENUWIDTH / 1.2
    BUTTONHEIGHT = MENUHEIGHT / 8
    
    
    
    #Width and height do not appear to change anything in actionmenurect but i left them just in case
    actionMenuRect = pygame.Rect(100,100,MENUWIDTH,MENUHEIGHT)
    actionMenuSurf = pygame.Surface((MENUWIDTH, MENUHEIGHT))
    pygame.draw.rect(actionMenuSurf, WHITE, actionMenuSurf.get_rect())
    moveButton = BIGFONT.render('Move', True, WHITE, BLACK)
    moveButtonRect = moveButton.get_rect()
    bribeButton = BIGFONT.render('Bribe', True, WHITE, BLACK)
    bribeButtonRect = bribeButton.get_rect()
    hitButton = BIGFONT.render('Hit', True, WHITE, BLACK)
    hitButtonRect = hitButton.get_rect()
    jobButton = BIGFONT.render('Job', True, WHITE, BLACK)
    jobButtonRect = jobButton.get_rect()

    pieceWarning = BIGFONT.render('Choose your own piece', True, WHITE, BLACK)
    pieceWarningRect = pieceWarning.get_rect()

    moveWarning = BIGFONT.render('You cant move there', True, WHITE, BLACK)
    moveWarningRect = moveWarning.get_rect()


    while True: # main game loop
        # Keep looping for player and computer's turns.
        if turn == 'player1':
            # Player's turn:

            movexy = None
            while movexy == None:
                # Keep looping until the player clicks on a valid space.


                checkForQuit()
                for event in pygame.event.get(): # event handling loop
                    if event.type == MOUSEBUTTONUP and event.button == 3: 
                        wait_for_selection = True
                        mousex, mousey = event.pos
                        while wait_for_selection == True:  
                            drawBoard(mainBoard, pieces)
                            DISPLAYSURF.blit(actionMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                            moveButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 150, moveButtonRect[2],moveButtonRect[3])
                            bribeButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 115, bribeButtonRect[2],bribeButtonRect[3])
                            hitButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 80, hitButtonRect[2],hitButtonRect[3])
                            jobButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 45, jobButtonRect[2],jobButtonRect[3])
                            DISPLAYSURF.blit(moveButton, moveButtonRect)
                            DISPLAYSURF.blit(bribeButton, bribeButtonRect)
                            DISPLAYSURF.blit(hitButton, hitButtonRect)
                            DISPLAYSURF.blit(jobButton, jobButtonRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()

                            for event in pygame.event.get():
                                
                                #Action menu loop
                                if event.type == MOUSEBUTTONUP:

                                    mousex, mousey = event.pos
                                    if moveButtonRect.collidepoint((mousex,mousey)):
                                        #change to a seperate function, players, board, pieces
                                        wait_for_move = True
                                        drawBoard(mainBoard, pieces)
                                        MAINCLOCK.tick(FPS)
                                        pygame.display.update()
                                        while wait_for_move == True:
                                            for event in pygame.event.get():
                                                if event.type == MOUSEBUTTONUP:
                                                    mousex, mousey = event.pos
                                                    x,y = getSpaceClicked(mousex, mousey)
                                                    x_old = x
                                                    y_old = y
                                                    print(x)
                                                    print(y)
                                                    print(pieces[x][y])
                                                    if player1 in pieces[x][y]:
                                                        #UI - does this need a message or is this intuitive?
                                                        #print("where to move?")
                                                        pieces[x][y] = [no_piece,no_piece]
                                                        drawBoard(mainBoard, pieces)
                                                        MAINCLOCK.tick(FPS)
                                                        pygame.display.update()
                                                        wait_for_space = True
                                                        while wait_for_space == True:
                                                            for event in pygame.event.get():
                                                                if event.type == MOUSEBUTTONUP:
                                                                    mousex, mousey = event.pos
                                                                    x,y = getSpaceClicked(mousex, mousey)
                                                                    if (x_old - 1) <= x <= (x_old + 1) and (y_old - 1) <= y <= (y_old + 1):
                                                                        pieces[x][y] = [player1,no_piece]
                                                                        drawBoard(mainBoard, pieces)
                                                                        MAINCLOCK.tick(FPS)
                                                                        pygame.display.update()
                                                                        wait_for_space = False
                                                                        wait_for_move = False
                                                                    else:
                                                                        drawBoard(mainBoard, pieces)
                                                                        moveWarningRect = pygame.Rect(mousex, mousey, moveWarningRect[2],moveWarningRect[3])
                                                                        DISPLAYSURF.blit(moveWarning, moveWarningRect)
                                                                    MAINCLOCK.tick(FPS)
                                                                    pygame.display.update()
                                                    else:
                                                        drawBoard(mainBoard, pieces)
                                                        pieceWarningRect = pygame.Rect(mousex, mousey, pieceWarningRect[2],pieceWarningRect[3])
                                                        DISPLAYSURF.blit(pieceWarning, pieceWarningRect)
                                                    MAINCLOCK.tick(FPS)
                                                    pygame.display.update()
                                        print("Move")
                                    elif bribeButtonRect.collidepoint( (mousex,mousey)):
                                        print("Bribe")
                                    elif hitButtonRect.collidepoint( (mousex,mousey)):
                                        print("Hit")
                                    elif jobButtonRect.collidepoint( (mousex,mousey)):
                                        print("Job")

                                    wait_for_selection = False
                        
                
                        #menu.mainloop(DISPLAYSURF, bgfun=drawBoard(mainBoard, pieces))

                    #if event.type == MOUSEBUTTONUP:
                        ## Handle mouse click events
                        #mousex, mousey = event.pos
                        #if newGameRect.collidepoint( (mousex, mousey) ):
                            ## Start a new game
                            #return True
                        #elif hintsRect.collidepoint( (mousex, mousey) ):
                            # Toggle hints mode
                            #showHints = not showHints
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        #movexy = getSpaceClicked(mousex, mousey)
                        

                # Draw the game board.
                drawBoard(mainBoard, pieces)
                #drawInfo(mainBoard, player1Tile, computerTile, turn)

                # Draw the "New Game" and "Hints" buttons.
                

                MAINCLOCK.tick(FPS)
                pygame.display.update()

            # Make the move and end the turn.
            #makeMove(mainBoard, player1Tile, movexy[0], movexy[1], True)

            
            pieces[movexy[0]][movexy[1]] = [player1, no_piece]

            turn = 'player2'

        if turn == 'player2':
            # Player's turn:

            movexy = None
            while movexy == None:
                # Keep looping until the player clicks on a valid space.


                checkForQuit()
                for event in pygame.event.get(): # event handling loop
                    if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint( (mousex, mousey) ):
                            # Start a new game
                            return True
                        elif hintsRect.collidepoint( (mousex, mousey) ):
                            # Toggle hints mode
                            showHints = not showHints
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        movexy = getSpaceClicked(mousex, mousey)
                        

                # Draw the game board.
                drawBoard(mainBoard, pieces)
                #drawInfo(mainBoard, player1Tile, computerTile, turn)

                # Draw the "New Game" and "Hints" buttons.
                

                MAINCLOCK.tick(FPS)
                pygame.display.update()

            # Make the move and end the turn.
            #makeMove(mainBoard, player1Tile, movexy[0], movexy[1], True)

            
            pieces[movexy[0]][movexy[1]] = [player2, no_piece]

            turn = 'player1'
            #if getValidMoves(mainBoard, computerTile) != []:
                # Only set for the computer's turn if it can make a move.
                #turn = 'computer'
        
        #else:
            # Computer's turn:
            #if getValidMoves(mainBoard, computerTile) == []:
                # If it was set to be the computer's turn but
                # they can't move, then end the game.
                #break

            # Draw the board.
            #drawBoard(mainBoard)
            #drawInfo(mainBoard, player1Tile, computerTile, turn)

            # Draw the "New Game" and "Hints" buttons.
            #DISPLAYSURF.blit(newGameSurf, newGameRect)
            #DISPLAYSURF.blit(hintsSurf, hintsRect)

            # Make it look like the computer is thinking by pausing a bit.
            #pauseUntil = time.time() + random.randint(5, 15) * 0.1
            #while time.time() < pauseUntil:
                #pygame.display.update()

            # Make the move and end the turn.
            #x, y = getComputerMove(mainBoard, computerTile)
            #makeMove(mainBoard, computerTile, x, y, True)
            #if getValidMoves(mainBoard, player1Tile) != []:
                # Only set for the player's turn if they can make a move.
                #turn = 'player'

    # Display the final score.
    #drawBoard(mainBoard)
    #scores = getScoreOfBoard(mainBoard)

    # Determine the text of the message to display.
   # if scores[player1Tile] > scores[computerTile]:
       # text = 'You beat the computer by %s points! Congratulations!' % \
               #(scores[player1Tile] - scores[computerTile])
    #elif scores[player1Tile] < scores[computerTile]:
       # text = 'You lost. The computer beat you by %s points.' % \
               #(scores[computerTile] - scores[player1Tile])
    #else:
        #text = 'The game was a tie!'

    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(textSurf, textRect)

    # Display the "Play again?" text with Yes and No buttons.
    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

    # Make "Yes" button.
    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)

    # Make "No" button.
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)

    while True:
        # Process events until the user clicks on Yes or No.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    return True
                elif noRect.collidepoint( (mousex, mousey) ):
                    return False
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)

def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)


def animateTileChange(tilesToFlip, tileColor, additionalTile):
    # Draw the additional tile that was just laid down. (Otherwise we'd
    # have to completely redraw the board & the board info.)
    if tileColor == BLUE_TILE:
        additionalTileColor = BRIGHTBLUE
    else:
        additionalTileColor = BLACK
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if tileColor == BLUE_TILE:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif tileColor == BLACK_TILE:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        for x, y in tilesToFlip:
            centerx, centery = translateBoardToPixelCoord(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        checkForQuit()


def drawBoard(board, pieces):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for x in range(BOARDWIDTH + 1):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT + 1):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    # Draw the black & white tiles or hint spots.
    #Image scaling is weird; small additions and subtractions are quick workaround to preserve lines drawn cause I dont know how layers work
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == BLUE_TILE or board[x][y] == BLACK_TILE or board[x][y] == RED_TILE or board[x][y] == GREEN_TILE:
                if board[x][y] == BLUE_TILE:
                    BP_IMAGE = pygame.image.load('BigTony.png')
                    BP_IMAGE.convert()
                    BP_IMAGE = pygame.transform.scale(BP_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                    DISPLAYSURF.blit(BP_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))
                elif board[x][y] == RED_TILE:
                    RP_IMAGE = pygame.image.load('Stephanie.png')
                    RP_IMAGE.convert()
                    RP_IMAGE = pygame.transform.scale(RP_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                    DISPLAYSURF.blit(RP_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))
                elif board[x][y] == BLACK_TILE:
                    BKP_IMAGE = pygame.image.load('NumberOne.png')
                    BKP_IMAGE.convert()
                    BKP_IMAGE = pygame.transform.scale(BKP_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                    DISPLAYSURF.blit(BKP_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))
                elif board[x][y] == GREEN_TILE:
                    GP_IMAGE = pygame.image.load('Virginia.png')
                    GP_IMAGE.convert()
                    GP_IMAGE = pygame.transform.scale(GP_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                    DISPLAYSURF.blit(GP_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))
            elif board[x][y] == CITY_HALL:
                
                CH_IMAGE = pygame.image.load('CityHall.png')
                CH_IMAGE.convert()
                CH_IMAGE = pygame.transform.scale(CH_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                DISPLAYSURF.blit(CH_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))
                
            elif board[x][y] == SPEAK_EASY:
                SE_IMAGE = pygame.image.load('Speakeasy.png')
                SE_IMAGE.convert()
                SE_IMAGE = pygame.transform.scale(SE_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                DISPLAYSURF.blit(SE_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))

            elif board[x][y] == LOAN_SHARK:
                LS_IMAGE = pygame.image.load('Loanshark.png')
                LS_IMAGE.convert()
                LS_IMAGE = pygame.transform.scale(LS_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                DISPLAYSURF.blit(LS_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))

            elif board[x][y] == PAWN_SHOP:
                PS_IMAGE = pygame.image.load('PawnShop.png')
                PS_IMAGE.convert()
                PS_IMAGE = pygame.transform.scale(PS_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                DISPLAYSURF.blit(PS_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))

            elif board[x][y] == MOM_POP:
                MP_IMAGE = pygame.image.load('MomPopShop.png')
                MP_IMAGE.convert()
                MP_IMAGE = pygame.transform.scale(MP_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                DISPLAYSURF.blit(MP_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))
            
            elif board[x][y] == BANK:
                BA_IMAGE = pygame.image.load('Bank.png')
                BA_IMAGE.convert()
                BA_IMAGE = pygame.transform.scale(BA_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                DISPLAYSURF.blit(BA_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))

            elif board[x][y] ==FINANCIAL_DISTRICT:
                FD_IMAGE = pygame.image.load('FinancialDistrict.png')
                FD_IMAGE.convert()
                FD_IMAGE = pygame.transform.scale(FD_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                DISPLAYSURF.blit(FD_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))

            elif board[x][y] == DISTILLERY:
                DI_IMAGE = pygame.image.load('Distillery.png')
                DI_IMAGE.convert()
                DI_IMAGE = pygame.transform.scale(DI_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                DISPLAYSURF.blit(DI_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))

            elif board[x][y] == RACE_TRACK:
                RT_IMAGE = pygame.image.load('Racetrack.png')
                RT_IMAGE.convert()
                RT_IMAGE = pygame.transform.scale(RT_IMAGE, (SPACESIZE - 5, SPACESIZE - 5))
                DISPLAYSURF.blit(RT_IMAGE, (centerx - SPACESIZE/2 + 5, centery - SPACESIZE/2 + 5))

            if pieces[x][y] == [player1, no_piece] or pieces[x][y] == [player2, no_piece]  or pieces[x][y] == [player3, no_piece]  or pieces[x][y] == [player4, no_piece]:
                DISPLAYSURF.blit(pieces[x][y][0].surf, (centerx, centery))

            if pieces[x][y] == [no_piece, cop] or pieces[x][y] == [no_piece, cop]  or pieces[x][y] == [no_piece, cop]  or pieces[x][y] == [no_piece, cop]:
                DISPLAYSURF.blit(pieces[x][y][1].surf, (centerx, centery))
            
            if pieces[x][y] == [player1, cop] or pieces[x][y] == [player2, cop]  or pieces[x][y] == [player3, cop]  or pieces[x][y] == [player4, cop]:
                DISPLAYSURF.blit(pieces[x][y][0].surf, (centerx, centery))
                DISPLAYSURF.blit(pieces[x][y][1].surf, (centerx - int(SPACESIZE/2), centery - int(SPACESIZE/2)))

            if pieces[x][y] == [cop, cop]:
                DISPLAYSURF.blit(pieces[x][y][0].surf, (centerx, centery))
                DISPLAYSURF.blit(pieces[x][y][1].surf, (centerx - int(SPACESIZE/2), centery - int(SPACESIZE/2)))

def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > x * SPACESIZE + XMARGIN and \
               mousex < (x + 1) * SPACESIZE + XMARGIN and \
               mousey > y * SPACESIZE + YMARGIN and \
               mousey < (y + 1) * SPACESIZE + YMARGIN:
                return (x, y)
    return None


def drawInfo(board, player1Tile, computerTile, turn):
    # Draws scores and whose turn it is at the bottom of the screen.
    scores = getScoreOfBoard(board)
    scoreSurf = FONT.render("Player Score: %s    Computer Score: %s    %s's Turn" % (str(scores[player1Tile]), str(scores[computerTile]), turn.title()), True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def resetBoard(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTY_SPACE

    # Add starting pieces to the center
    board[0][0] = BLUE_TILE
    board[4][0] = RED_TILE
    board[0][4] = GREEN_TILE
    board[4][4] = BLACK_TILE
    board[2][2] = CITY_HALL

    rev_spots = [SPEAK_EASY,LOAN_SHARK,MOM_POP,PAWN_SHOP,BANK,FINANCIAL_DISTRICT,DISTILLERY,RACE_TRACK,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE,EMPTY_SPACE]
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY_SPACE:
                idx = random.randint(0,len(rev_spots)-1)
                #spot = random.sample(rev_spots,1)
                #spot_idx = rev_spots.index(spot[0])
                #print(spot_idx)
                #rev_spots.pop(spot_idx)
                spot = rev_spots.pop(idx)
                board[x][y] = spot

def resetPieces(pieces):
    # Blanks out the board it is passed, and sets up starting tiles.

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            pieces[x][y] = [no_piece, no_piece]
    pieces[2][2] = [cop, cop]

    return pieces
    
def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)

    return board

def getPieces():
    # Creates a brand new, empty board data structure.
    pieces = []
    for i in range(BOARDWIDTH):
        pieces.append([EMPTY_SPACE] * BOARDHEIGHT)

    return pieces

def chooseStartingPositions(turn, players, board, pieces):

    rounds = 0
    count = 0
    select_idx = players.index(turn)

    while rounds <= 2:

        
        selector = players[select_idx]
        movexy = None
        while movexy == None:
                # Keep looping until the player clicks on a valid space.
            
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                    mousex, mousey = event.pos
                    #if newGameRect.collidepoint( (mousex, mousey) ):
                            # Start a new game
                        #return True
                    #elif hintsRect.collidepoint( (mousex, mousey) ):
                            # Toggle hints mode
                        # movexy is set to a two-item tuple XY coordinate, or None value
                    movexy = getSpaceClicked(mousex, mousey)
                    print(pieces[movexy[0]][movexy[1]])
                    
                    while pieces[movexy[0]][movexy[1]] != [no_piece, no_piece]:
                        #print("choose a spot with no other made men on it")
                        for event in pygame.event.get(): # event handling loop
                            if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                                mousex, mousey = event.pos
                    #if newGameRect.collidepoint( (mousex, mousey) ):
                            # Start a new game
                        #return True
                    #elif hintsRect.collidepoint( (mousex, mousey) ):
                            # Toggle hints mode
                        # movexy is set to a two-item tuple XY coordinate, or None value
                                movexy = getSpaceClicked(mousex, mousey)
            drawBoard(board, pieces)
            MAINCLOCK.tick(FPS)
            pygame.display.update()
            
        if selector == players[0]:

            pieces[movexy[0]][movexy[1]] = [player1, no_piece]

        elif selector == players[1]:

            pieces[movexy[0]][movexy[1]] = [player2, no_piece]

           # if selector == players[2]:

               # pieces[movexy[0]][movexy[1]] = [player1, no_piece]

            #if selector == players[3]:

                #pieces[movexy[0]][movexy[1]] = [player1, no_piece]
                # Draw the game board.
        
        if select_idx != len(players) - 1:
            select_idx += 1 
            count += 1

        else:
            select_idx = 0 
            count += 1
                #drawInfo(mainBoard, player1Tile, computerTile, turn)

                # Draw the "New Game" and "Hints" buttons.
        
        if count == len(players):

            rounds +=1
            count = 0
            print(rounds)




def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == BLUE_TILE:
        otherTile = BLACK_TILE
    else:
        otherTile = BLUE_TILE

    tilesToFlip = []
    # check each of the eight directions:
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # The piece belongs to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break # break out of while loop, continue in for loop
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse
                # direction until we reach the original space, noting all
                # the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = EMPTY_SPACE # make space empty
    if len(tilesToFlip) == 0: # If no tiles flipped, this move is invalid
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT


def getBoardWithValidMoves(board, tile):
    # Returns a new board with hint markings.
    dupeBoard = copy.deepcopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = HINT_TILE
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of (x,y) tuples of all valid moves.
    validMoves = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append((x, y))
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles.
    xscore = 0
    oscore = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLUE_TILE:
                xscore += 1
            if board[x][y] == BLACK_TILE:
                oscore += 1
    return {BLUE_TILE:xscore, BLACK_TILE:oscore}

#def chooseStartingPos():


def enterPlayerTile():
    # Draws the text and handles the mouse click events for letting
    # the player choose which color they want to be.  Returns
    # [BLUE_TILE, BLACK_TILE] if the player chooses to be White,
    # [BLACK_TILE, BLUE_TILE] if Black.
    # Create the text.
    textSurf = FONT.render('Which crime boss do you want to be?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))


    nSurf = BIGFONT.render('"Lucky"', True, TEXTCOLOR, BRIGHTBLUE)
    nSurf = nSurf.convert()
    nSurf.set_alpha(50)
    nRect = nSurf.get_rect()
    nx, ny = translateBoardToPixelCoord(0,0)
    nRect.center = (nx, ny + 50)

    eSurf = BIGFONT.render('"Queenie"', True, TEXTCOLOR, RED)
    eRect = eSurf.get_rect()
    eSurf = eSurf.convert()
    eSurf.set_alpha(50)
    ex, ey = translateBoardToPixelCoord(4,0)
    eRect.center = (ex - 20 , ey + 50 )

    sSurf = BIGFONT.render('"Number One"', True, TEXTCOLOR, BLACK)
    sRect = sSurf.get_rect()
    sSurf = sSurf.convert()
    sSurf.set_alpha(50)
    sx, sy = translateBoardToPixelCoord(4,4)
    sRect.center = (sx, sy - 50 )

    wSurf = BIGFONT.render('"Calamity Jane"', True, TEXTCOLOR, GREEN)
    wRect = wSurf.get_rect()
    wSurf = wSurf.convert()
    wSurf.set_alpha(50)
    wx, wy = translateBoardToPixelCoord(0,4)
    wRect.center = (wx, wy - 50)


    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if nRect.collidepoint( (mousex, mousey) ):
                    return BLACK_TILE
                elif eRect.collidepoint( (mousex, mousey) ):
                    return BLUE_TILE
                elif sRect.collidepoint( (mousex, mousey) ):
                    return RED_TILE
                elif wRect.collidepoint( (mousex, mousey) ):
                    return GREEN_TILE

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(nSurf, nRect)
        DISPLAYSURF.blit(eSurf, eRect)
        DISPLAYSURF.blit(sSurf, sRect)
        DISPLAYSURF.blit(wSurf, wRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def makeMove(board, tile, xstart, ystart, realMove=False):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or \
           (x == BOARDWIDTH and y == 0) or \
           (x == 0 and y == BOARDHEIGHT) or \
           (x == BOARDWIDTH and y == BOARDHEIGHT)


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all possible moves and remember the best scoring move
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = copy.deepcopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

def move():
    print("move")

def bribe():
    print("bribe")
    
def hit():
    print("hit")

def spaceaction():
    print("doaction")
    

if __name__ == '__main__':
    main()
