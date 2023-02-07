# Flippy (an Othello or Reversi clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Based on the "reversi.py" code that originally appeared in "Invent
# Your Own Computer Games with Python", chapter 15:
#   http://inventwithpython.com/chapter15.html

import random, sys, pygame, time, copy, pygame_menu, numpy
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
    def __init__(self, color, player):
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
        self.informant = False
        self.player = player

class cop_piece(pygame.sprite.Sprite):
    def __init__(self, color):
        super(cop_piece, self).__init__()
        self.surf = pygame.image.load('Cop.png')
        self.surf.convert()
        self.surf = pygame.transform.scale(self.surf, (SPACESIZE/2 - 5, SPACESIZE/2 - 5))
        pygame.Surface.set_colorkey(self.surf, (255,255,255))
        self.rect = self.surf.get_rect()
        self.bribe = None
        self.player = "cop"

class journalist_piece(pygame.sprite.Sprite):
    def __init__(self, color):
        super(journalist_piece, self).__init__()
        self.surf = pygame.image.load('Journalist.png')
        self.surf.convert()
        self.surf = pygame.transform.scale(self.surf, (SPACESIZE/2 - 5, SPACESIZE/2 - 5))
        pygame.Surface.set_colorkey(self.surf, (255,255,255))
        self.rect = self.surf.get_rect()
        self.bribe = None
        self.player = "journalist"

class no_piece_class(pygame.sprite.Sprite):
    def __init__(self):
        super(no_piece_class, self).__init__()
        self.player = None

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
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE, players, player_bank, cop_bribe_bank, journalist_bribe_bank, election_bank, jail, recruits, rat, no_piece, player11, player12, player13, player21, player22, player23, player31, player32, player33, player41, player42, player43, cop1, cop2, journalist
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

    player1Tile = None
    player2Tile = None
    player3Tile = None
    player4Tile = None

    players = ["player1", "player2"]
    player_bank = [0,0,0,0]
    cop_bribe_bank = [0,0,0,0]
    journalist_bribe_bank = [0,0,0,0]
    election_bank = [0,0,0,0]
    jail = [0,0,0,0]
    recruits = []
    rat = [0,0,0,0]

    no_piece = no_piece_class( )
    player11 = madeMan(BLACK, players[0])
    player12 = madeMan(BLACK, players[0])
    player13 = madeMan(BLACK, players[0])
    player21 = madeMan(BRIGHTBLUE, players[1])
    player22 = madeMan(BRIGHTBLUE, players[1])
    player23 = madeMan(BRIGHTBLUE, players[1])
    #player31 = madeMan(RED, players[2])
    #player32 = madeMan(RED, players[2])
   #player33 = madeMan(RED, players[2])
    #player41 = madeMan(GREEN, players[3])
    #player42 = madeMan(GREEN, players[3])
    #player43 = madeMan(GREEN, players[3])
    cop1 = cop_piece(BROWN)
    cop2 = cop_piece(BROWN)
    journalist = journalist_piece(BROWN)

    # Run the main game.
    while True:
        if runGame() == False:
            break


def runGame():
    # Plays a single game of reversi each time this function is called.

    turn = random.choice(players)


    # Reset the board and game.
    mainBoard = getNewBoard()
    pieces = getPieces()
    resetBoard(mainBoard)
    resetPieces(pieces)


    # Draw the starting board and ask the player what color they want.
    drawBoard(mainBoard, pieces)
    player1Tile = enterPlayerTile()
    player2Tile = enterPlayerTile()
    #player3Tile = enterPlayerTile()
    #print("player3Tile")
    #player4Tile = enterPlayerTile()
    #print("player4Tile")
    starting_pos = chooseStartingPositions(turn, players, mainBoard, pieces)



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

    action_count = 0
    round_count = 0
    copRegen = 0
    journalistRegen = False


    while True: # main game loop
        # Keep looping for player and computer's turns.
        player_idx = players.index(turn)
        movexy = None
        if action_count <= 1:
            # Player's turn:
            #getRevenues(mainBoard, pieces, players, player_bank, player1Tile, player2Tile, player3Tile, player4Tile)
            getRevenues(mainBoard, pieces, players, player_bank, player1Tile, player2Tile)
            print(player_bank)
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
                                    chargeAction = False
                                    mousex, mousey = event.pos
                                    if moveButtonRect.collidepoint((mousex,mousey)):
                                        #change to a seperate function, players, board, pieces
                                        move(turn, mainBoard, pieces)
                                        action_count += 1
                                    elif bribeButtonRect.collidepoint( (mousex,mousey)):
                                        copCount, journalistCount, chargeAction = bribe(turn, mainBoard, pieces)
                                        cop_bribe_bank[player_idx] += copCount
                                        journalist_bribe_bank[player_idx] += journalistCount
                                        player_bank[player_idx] -= (copCount + journalistCount)
                                        print(cop_bribe_bank)
                                        print(journalist_bribe_bank)
                                        if chargeAction == True:
                                            action_count += 1 
                                    elif hitButtonRect.collidepoint( (mousex,mousey)):
                                        jail, recruits, chargeAction, copRegen, journalistRegen= hit(turn, player_idx, mainBoard, pieces, copRegen, journalistRegen)
                                        if chargeAction == True:
                                            action_count += 1 
                                    elif jobButtonRect.collidepoint( (mousex,mousey)):
                                        action_count += 1 

                                    wait_for_selection = False
                                    print("action_count" + str(action_count))
                                    if action_count >= 2:
                                        if player_idx < len(players) - 1:
                                            turn = players[player_idx + 1]
                                            player_idx += 1
                                        else: 
                                            getRevenues(mainBoard, pieces, players, player_bank, player1Tile, player2Tile)
                                            print(player_bank)
                                            copMove(mainBoard,pieces)
                                            turn = players[0]
                                            player_idx = 0
                                            round_count += 1
                                            if round_count >= 5:
                                                print("elections!")
                                                election_bank = election(mainBoard, pieces)    
                                                print(election_bank)
                                                if journalist_regen == True:
                                                    pieces[2][2].append(journalist)          
                                                    journalist_regen = False          
                                                if cop_regen == 1:
                                                    pieces[2][2].append(cop1)
                                                    cop_regen == 0
                                                if cop_regen == 2:
                                                    pieces[2][2].append(cop2)  
                                                    cop_regen == 0                             
                                                round_count = 0

                                        action_count = 0
                                        break

                # Draw the game board.

                drawBoard(mainBoard, pieces)
                MAINCLOCK.tick(FPS)
                pygame.display.update()


def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)

#def getRevenues(board, pieces, players, player_bank, player1Tile, player2Tile, player3Tile, player4Tile):
def getRevenues(board, pieces, players, player_bank, player1Tile, player2Tile):

    player_bank[0] += 1
    player_bank[1] += 1
    player_bank[2] += 1
    player_bank[3] += 1

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            copFlag = copCheck(x, y, pieces)
            for player in players:
                for piece in pieces[x][y]:
                    if board[x][y] == SPEAK_EASY and piece.player == player:
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += 1
                        else:
                            player_bank[players.index(player)] += 2

                    elif board[x][y] == LOAN_SHARK and piece.player == player:
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += 1
                        else:
                            player_bank[players.index(player)] += 2
                
                    elif board[x][y] == PAWN_SHOP and piece.player == player:
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += 1
                        else:
                            player_bank[players.index(player)] += 2

                    elif board[x][y] == MOM_POP and piece.player == player:
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += 2
                        else:
                            player_bank[players.index(player)] += 4

                    elif board[x][y] == BANK and piece.player == player:
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += 2
                        else:
                            player_bank[players.index(player)] += 4

                    elif board[x][y] ==FINANCIAL_DISTRICT and piece.player == player:
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += 2
                        else:
                            player_bank[players.index(player)] += 4

                    elif board[x][y] == DISTILLERY and piece.player == player:
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += 2
                        else:
                            player_bank[players.index(player)] += 4

                    elif board[x][y] == RACE_TRACK and piece.player == player:
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += 2
                        else:
                            player_bank[players.index(player)] += 4



    return player_bank

def copCheck(x, y, pieces):
    copFlag = False
    xi = [-1, 0, 1]
    yj = [-1, 0, 1]

    for i in xi:
        for j in yj:
            if isOnBoard(x+i,y+j):
                for piece in pieces[x+i][y+j]:
                    if piece.player == "cop":
                        copFlag = True
                        break
    
    return copFlag
                    

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

            if len(pieces[x][y]) == 2:
                DISPLAYSURF.blit(pieces[x][y][1].surf, (centerx, centery))
            
            if len(pieces[x][y]) == 3:
                DISPLAYSURF.blit(pieces[x][y][2].surf, (centerx, centery))
                DISPLAYSURF.blit(pieces[x][y][1].surf, (centerx - int(SPACESIZE/2), centery - int(SPACESIZE/2)))

            if len(pieces[x][y]) == 4:
                DISPLAYSURF.blit(pieces[x][y][1].surf, (centerx, centery))
                DISPLAYSURF.blit(pieces[x][y][2].surf, (centerx - int(SPACESIZE/2), centery - int(SPACESIZE/2)))
                DISPLAYSURF.blit(pieces[x][y][3].surf, (centerx - int(SPACESIZE/2), centery))

            if len(pieces[x][y]) == 5:
                DISPLAYSURF.blit(pieces[x][y][1].surf, (centerx, centery))
                DISPLAYSURF.blit(pieces[x][y][2].surf, (centerx - int(SPACESIZE/2), centery - int(SPACESIZE/2)))
                DISPLAYSURF.blit(pieces[x][y][3].surf, (centerx - int(SPACESIZE/2), centery))
                DISPLAYSURF.blit(pieces[x][y][4].surf, (centerx, centery - int(SPACESIZE/2)))

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
            pieces[x][y] = [no_piece]
    pieces[1][2] = [no_piece, cop1]
    pieces[2][2] = [no_piece, journalist]
    pieces[3][2] = [no_piece, cop2]

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
        pieces.append([no_piece] * BOARDHEIGHT)

    return pieces

def chooseStartingPositions(turn, players, board, pieces):

    rounds = 0
    count = 0
    select_idx = players.index(turn)
    player1list = [player11,player12,player13]
    player2list = [player21,player22,player23]

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
                    
                    #while len(pieces[movexy[0]][movexy[1]]) != 1:
                    while bool(pieces[movexy[0]][movexy[1]]) == False:
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

            pieces[movexy[0]][movexy[1]].append(player1list.pop())

        elif selector == players[1]:

            pieces[movexy[0]][movexy[1]].append(player2list.pop())

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

def move(player,board,pieces):
    pieceWarning = BIGFONT.render('Choose your own piece', True, WHITE, BLACK)
    pieceWarningRect = pieceWarning.get_rect()

    moveWarning = BIGFONT.render('You cant move there', True, WHITE, BLACK)
    moveWarningRect = moveWarning.get_rect()
    wait_for_move = True
    drawBoard(board, pieces)
    MAINCLOCK.tick(FPS)
    pygame.display.update()
    while wait_for_move == True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                x,y = getSpaceClicked(mousex, mousey)
                x_old = x
                y_old = y
                for piece in pieces[x][y]:
                    if piece.player == player:
                        #UI - does this need a message or is this intuitive?
                        pieces[x][y].remove(piece)
                        drawBoard(board, pieces)
                        MAINCLOCK.tick(FPS)
                        pygame.display.update()
                        wait_for_space = True
                        while wait_for_space == True:
                            for event in pygame.event.get():
                                if event.type == MOUSEBUTTONUP:
                                    mousex, mousey = event.pos
                                    x,y = getSpaceClicked(mousex, mousey)
                                    if (x_old - 1) <= x <= (x_old + 1) and (y_old - 1) <= y <= (y_old + 1):
                                        pieces[x][y].append(piece)
                                        drawBoard(board, pieces)
                                        MAINCLOCK.tick(FPS)
                                        pygame.display.update()
                                        wait_for_space = False
                                        wait_for_move = False
                                    else:
                                        drawBoard(board, pieces)
                                        moveWarningRect = pygame.Rect(mousex, mousey, moveWarningRect[2],moveWarningRect[3])
                                        DISPLAYSURF.blit(moveWarning, moveWarningRect)
                                    MAINCLOCK.tick(FPS)
                                    pygame.display.update()
                    else:
                        drawBoard(board, pieces)
                        pieceWarningRect = pygame.Rect(mousex, mousey, pieceWarningRect[2],pieceWarningRect[3])
                        DISPLAYSURF.blit(pieceWarning, pieceWarningRect)
                        MAINCLOCK.tick(FPS)
                        pygame.display.update()



def bribe(player, board, pieces):
    #buggy

    #Action Menu objects - rect is (left,top,width,height)
    MENUWIDTH = WINDOWWIDTH / 6
    MENUHEIGHT = WINDOWHEIGHT / 3
    BUTTONWIDTH = MENUWIDTH / 1.2
    BUTTONHEIGHT = MENUHEIGHT / 8
    
    
    
    #Width and height do not appear to change anything in actionmenurect but i left them just in case
    cjMenuRect = pygame.Rect(100,100,MENUWIDTH,MENUHEIGHT)
    cjMenuSurf = pygame.Surface((MENUWIDTH, MENUHEIGHT))
    pygame.draw.rect(cjMenuSurf, WHITE, cjMenuSurf.get_rect())
    copButton = BIGFONT.render('Cop', True, WHITE, BLACK)
    copButtonRect = copButton.get_rect()
    journalistButton = BIGFONT.render('Journalist', True, WHITE, BLACK)
    journalistButtonRect = journalistButton.get_rect()

    pieceWarning = BIGFONT.render('Choose your own piece next to a cop or journalist', True, WHITE, BLACK)
    pieceWarningRect = pieceWarning.get_rect()
    cjWarning = BIGFONT.render('Choose your own piece next to a cop or journalist', True, WHITE, BLACK)
    cjWarningRect = pieceWarning.get_rect()
    cj = None
    copCount = 0
    journalistCount = 0
    count = copCount + journalistCount
    chargeAction = False
    countBox = BIGFONT.render(str(count), True, WHITE, BLACK)
    countBoxRect = countBox.get_rect()
    text_value = None
    wait_for_input = True
    wait_for_key = True
    drawBoard(board, pieces)
    MAINCLOCK.tick(FPS)
    pygame.display.update()
    while wait_for_input == True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                x,y = getSpaceClicked(mousex, mousey)
                if (cop1 in pieces[x][y] or cop2 in pieces[x][y]) and journalist_piece in pieces[x][y]:
                    while wait_for_selection == True:  
                            drawBoard(board, pieces)
                            DISPLAYSURF.blit(cjMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                            copButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 150, copButtonRect[2],copButtonRect[3])
                            journalistButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 115, journalistButtonRect[2],journalistButtonRect[3])
                            DISPLAYSURF.blit(copButton, copButtonRect)
                            DISPLAYSURF.blit(journalistButton, journalistButtonRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()

                            for event in pygame.event.get():
                                
                                #Action menu loop
                                if event.type == MOUSEBUTTONUP:

                                    mousex, mousey = event.pos
                                    if copButtonRect.collidepoint((mousex,mousey)):
                                        #change to a seperate function, players, board, pieces
                                        for piece in pieces[x][y]:
                        #if both journalist and cop then pop up menu "bribe journalist or cop?, take inputs"
                                            if piece.player == player:
                                                pygame.key.start_text_input()
                                                while wait_for_key == True:
                                                    for event in pygame.event.get():

                                                        if event.type == pygame.KEYDOWN:
                                                            if event.key == K_DOWN:
                                                                copCount -= 1
                                                            elif event.key == K_UP:
                                                                copCount += 1
                                                            elif event.key == K_RETURN:
                                                                pygame.key.stop_text_input()
                                                                wait_for_key == False
                                                                wait_for_input == False
                                                                chargeAction = True
                                                                return copCount, journalistCount, chargeAction
                                                        else:
                                                            drawBoard(board, pieces)
                                                            countBox = BIGFONT.render(str(copCount), True, WHITE, BLACK)
                                                            countBoxRect = countBox.get_rect()
                                                            countBoxRect = pygame.Rect(mousex, mousey, countBoxRect[2],countBoxRect[3])
                                                            DISPLAYSURF.blit(countBox, countBoxRect)
                                                            MAINCLOCK.tick(FPS)
                                                            pygame.display.update()

                                    elif journalistButtonRect.collidepoint( (mousex,mousey)):
                                        for piece in pieces[x][y]:
                        #if both journalist and cop then pop up menu "bribe journalist or cop?, take inputs"
                                            if piece.player == player:
                                                pygame.key.start_text_input()
                                                while wait_for_key == True:
                                                    for event in pygame.event.get():

                                                        if event.type == pygame.KEYDOWN:
                                                            if event.key == K_DOWN:
                                                                journalistCount -= 1
                                                            elif event.key == K_UP:
                                                                journalistCount += 1
                                                            elif event.key == K_RETURN:
                                                                pygame.key.stop_text_input()
                                                                wait_for_key == False
                                                                wait_for_input == False
                                                                chargeAction = True
                                                                return copCount, journalistCount, chargeAction
                                                        else:
                                                            drawBoard(board, pieces)
                                                            countBox = BIGFONT.render(str(journalistCount), True, WHITE, BLACK)
                                                            countBoxRect = countBox.get_rect()
                                                            countBoxRect = pygame.Rect(mousex, mousey, countBoxRect[2],countBoxRect[3])
                                                            DISPLAYSURF.blit(countBox, countBoxRect)
                                                            MAINCLOCK.tick(FPS)
                                                            pygame.display.update()


                                    wait_for_selection = False

                elif cop1 in pieces[x][y] or cop2 in pieces[x][y]:
                    for piece in pieces[x][y]:
                        #if both journalist and cop then pop up menu "bribe journalist or cop?, take inputs"
                        if piece.player == player:
                            pygame.key.start_text_input()
                            while wait_for_key == True:
                                for event in pygame.event.get():

                                    if event.type == pygame.KEYDOWN:
                                        if event.key == K_DOWN:
                                            copCount -= 1
                                        elif event.key == K_UP:
                                            copCount += 1
                                        elif event.key == K_RETURN:
                                            pygame.key.stop_text_input()
                                            wait_for_key == False
                                            wait_for_input == False
                                            chargeAction = True
                                            return copCount, journalistCount, chargeAction
                                    else:
                                        drawBoard(board, pieces)
                                        countBox = BIGFONT.render(str(copCount), True, WHITE, BLACK)
                                        countBoxRect = countBox.get_rect()
                                        countBoxRect = pygame.Rect(mousex, mousey, countBoxRect[2],countBoxRect[3])
                                        DISPLAYSURF.blit(countBox, countBoxRect)
                                        MAINCLOCK.tick(FPS)
                                        pygame.display.update()

                elif journalist in pieces[x][y]:
                    for piece in pieces[x][y]:
                        #if both journalist and cop then pop up menu "bribe journalist or cop?, take inputs"
                        if piece.player == player:
                            pygame.key.start_text_input()
                            while wait_for_key == True:
                                for event in pygame.event.get():

                                    if event.type == pygame.KEYDOWN:
                                        if event.key == K_DOWN:
                                            journalistCount -= 1
                                        elif event.key == K_UP:
                                            journalistCount += 1
                                        elif event.key == K_RETURN:
                                            pygame.key.stop_text_input()
                                            wait_for_key == False
                                            wait_for_input == False
                                            chargeAction = True
                                            return copCount, journalistCount, chargeAction
                                    else:
                                        drawBoard(board, pieces)
                                        countBox = BIGFONT.render(str(journalistCount), True, WHITE, BLACK)
                                        countBoxRect = countBox.get_rect()
                                        countBoxRect = pygame.Rect(mousex, mousey, countBoxRect[2],countBoxRect[3])
                                        DISPLAYSURF.blit(countBox, countBoxRect)
                                        MAINCLOCK.tick(FPS)
                                        pygame.display.update()
                                        #wait_for_key = False
                            #pop up input, user types in number, send input to bribe bank 
                        #elif journalist flag true do same
                        #if neither, then return to action menu, dont get charged an action 
                            #if both true choose 
                
                else:
                    drawBoard(board, pieces)
                    pieceWarningRect = pygame.Rect(mousex, mousey, pieceWarningRect[2],pieceWarningRect[3])
                    DISPLAYSURF.blit(pieceWarning, pieceWarningRect)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()
                    time.sleep(1)
                    wait_for_input = False
                    return count, chargeAction
    
def hit(player, player_idx, board, pieces, copRegen, journalistRegen):
    #Action Menu objects - rect is (left,top,width,height)
    MENUWIDTH = WINDOWWIDTH / 6
    MENUHEIGHT = WINDOWHEIGHT / 3
    BUTTONWIDTH = MENUWIDTH / 1.2
    BUTTONHEIGHT = MENUHEIGHT / 8
    
    
    
    #Width and height do not appear to change anything in actionmenurect but i left them just in case
    cjMenuRect = pygame.Rect(100,100,MENUWIDTH,MENUHEIGHT)
    cjMenuSurf = pygame.Surface((MENUWIDTH, MENUHEIGHT))
    pygame.draw.rect(cjMenuSurf, WHITE, cjMenuSurf.get_rect())
    copButton = BIGFONT.render('Cop', True, WHITE, BLACK)
    copButtonRect = copButton.get_rect()
    journalistButton = BIGFONT.render('Journalist', True, WHITE, BLACK)
    journalistButtonRect = journalistButton.get_rect()

    pieceWarning = BIGFONT.render('Choose your own piece next to a cop or journalist', True, WHITE, BLACK)
    pieceWarningRect = pieceWarning.get_rect()
    cjWarning = BIGFONT.render('Choose your own piece next to a cop or journalist', True, WHITE, BLACK)
    cjWarningRect = pieceWarning.get_rect()
    cj = None
    copCount = 0
    journalistCount = 0
    count = copCount + journalistCount
    chargeAction = False
    countBox = BIGFONT.render(str(count), True, WHITE, BLACK)
    countBoxRect = countBox.get_rect()
    destiny = random.random()
    text_value = None

    opponent_pieces = []
    targets = []
    for p in players:
        if p != player:
            opponent_pieces.append(p)


    wait_for_input = True
    wait_for_selection = True
    drawBoard(board, pieces)
    MAINCLOCK.tick(FPS)
    pygame.display.update()
    while wait_for_input == True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                x,y = getSpaceClicked(mousex, mousey)
                for piece in pieces[x][y]:
                    if piece.player in opponent_pieces:
                        targets.append(piece)
                print("targets " + str(targets))  
                print("bool targets" + str(bool(targets)))
                if (cop1 in pieces[x][y] or cop2 in pieces[x][y]) and journalist_piece in pieces[x][y] and bool(targets) == True:
                    print("test ")
                    tgtButton = []
                    tgtButtonRect = []
                    for tgt in enumerate(targets):
                        tgtButton.append(BIGFONT.render(tgt[1].player, True, WHITE, BLACK))
                        tgtButtonRect.append(tgtButton[tgt[0]].get_rect())
                        tgtButtonRect[tgt[0]] = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - (150 - tgt[0]*40), tgtButtonRect[tgt[0]][2],tgtButtonRect[tgt[0]][3])
                    while wait_for_selection == True:  
                        drawBoard(board, pieces)
                        copButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 40, copButtonRect[2],copButtonRect[3])
                        journalistButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 70, journalistButtonRect[2],journalistButtonRect[3])
                        DISPLAYSURF.blit(cjMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                        DISPLAYSURF.blit(copButton, copButtonRect)
                        DISPLAYSURF.blit(journalistButton, journalistButtonRect)
                        if len(tgtButton) == 1:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                        elif len(tgtButton) == 2:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                        elif len(tgtButton) == 3:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                            DISPLAYSURF.blit(tgtButton[2], tgtButtonRect[2])
                        MAINCLOCK.tick(FPS)
                        pygame.display.update()

                        for event in pygame.event.get():
                            
                            #Action menu loop
                            if event.type == MOUSEBUTTONUP:

                                mousex, mousey = event.pos

                                if copButtonRect.collidepoint((mousex,mousey)):
                                    if destiny >= .7:
                                        print("hit successful")
                                        remove_counter = False
                                        if cop1 in pieces[x][y] and remove_counter == False:
                                            pieces[x][y].remove(cop1)
                                            remove_counter = True
                                            cop_regen = 1
                                        if cop2 in pieces[x][y] and remove_counter == False:
                                            pieces[x][y].remove(cop2)
                                            remove_counter = True
                                            cop_regen = 2
                                        chargeAction = True
                                        return jail, recruits, chargeAction, copRegen, journalistRegen
                                    if destiny >= .4 and destiny <.7:
                                        print("HEADLINE: Cops shoot down gangster at distllery ")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                recruits.append(player.player)
                                                chargeAction = True
                                                return jail, recruits, chargeAction, copRegen, journalistRegen
                                    if destiny >= 0 and destiny <.4:
                                        print("HEADLINE: Cops arrest gangster for attempted murder")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                chargeAction = True
                                                return jail, recruits, chargeAction, copRegen, journalistRegen

                                elif journalistButtonRect.collidepoint((mousex,mousey)):
                                    if destiny >= .7:
                                        print("hit successful")
                                        pieces[x][y].remove(journalist)
                                        journalist_regen = True
                                        chargeAction = True
                                        return jail, recruits, chargeAction, copRegen, journalistRegen
                                    if destiny >= .4 and destiny <.7:
                                        print("HEADLINE: nearly-assasinated journalist begins campaign against would be killers")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                recruits.append(player.player)
                                                journalist_bribe_bank[player_idx] -= 10
                                                chargeAction = True
                                                return jail, recruits, chargeAction, copRegen, journalistRegen
                                    if destiny >= 0 and destiny <.4:
                                        print("HEADLINE: Cops arrest gangster for attempted murder")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                chargeAction = True
                                                return jail, recruits, chargeAction, copRegen, journalistRegen

                                for tgt in enumerate(targets):
                                    if tgtButtonRect[tgt[0]].collidepoint((mousex,mousey)):
                                        if destiny >= .7:
                                            print(str(player) + "sucessfully hit " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == tgt[1].player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(piece)
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                                        elif destiny >= .4 and destiny < .7:
                                            print(str(player) + " got shot down by " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(piece)
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                                        elif destiny >= 0 and destiny < .4:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen
                                    else: 
                                        drawBoard(board, pieces)
                                        copButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 40, copButtonRect[2],copButtonRect[3])
                                        journalistButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 70, journalistButtonRect[2],journalistButtonRect[3])
                                        DISPLAYSURF.blit(cjMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                                        DISPLAYSURF.blit(copButton, copButtonRect)
                                        DISPLAYSURF.blit(journalistButton, journalistButtonRect)
                                        if len(tgtButton) == 1:
                                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                                        elif len(tgtButton) == 2:
                                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                                        elif len(tgtButton) == 3:
                                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                                            DISPLAYSURF.blit(tgtButton[2], tgtButtonRect[2])
                                        MAINCLOCK.tick(FPS)
                                        pygame.display.update()

                elif (cop1 in pieces[x][y] or cop2 in pieces[x][y]) and journalist_piece in pieces[x][y]:
                    while wait_for_selection == True:  
                            drawBoard(board, pieces)
                            DISPLAYSURF.blit(cjMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                            copButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 150, copButtonRect[2],copButtonRect[3])
                            journalistButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 115, journalistButtonRect[2],journalistButtonRect[3])
                            DISPLAYSURF.blit(copButton, copButtonRect)
                            DISPLAYSURF.blit(journalistButton, journalistButtonRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()

                            for event in pygame.event.get():
                                
                                #Action menu loop
                                if event.type == MOUSEBUTTONUP:

                                    mousex, mousey = event.pos
                                    if copButtonRect.collidepoint((mousex,mousey)):
                                        if destiny >= .7:
                                            print("hit successful")
                                            remove_counter = False
                                            if cop1 in pieces[x][y] and remove_counter == False:
                                                pieces[x][y].remove(cop1)
                                                remove_counter = True
                                                cop_regen = 1
                                            if cop2 in pieces[x][y] and remove_counter == False:
                                                pieces[x][y].remove(cop2)
                                                remove_counter = True
                                                cop_regen = 2
                                            chargeAction = True
                                            return jail, recruits, chargeAction, copRegen, journalistRegen
                                        if destiny >= .4 and destiny <.7:
                                            print("HEADLINE: Cops shoot down gangster at distllery ")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(player.player)
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen
                                        if destiny >= 0 and destiny <.4:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                                    elif journalistButtonRect.collidepoint( (mousex,mousey)):
                                        if destiny >= .7:
                                            print("hit successful")
                                            pieces[x][y].remove(journalist)
                                            journalist_regen = True
                                            chargeAction = True
                                            return jail, recruits, chargeAction, copRegen, journalistRegen
                                        if destiny >= .4 and destiny <.7:
                                            print("HEADLINE: nearly-assasinated journalist begins campaign against would be killers")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(player.player)
                                                    journalist_bribe_bank[player_idx] -= 10
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen
                                        if destiny >= 0 and destiny <.4:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen


                                    else: 
                                        drawBoard(board, pieces)
                                        DISPLAYSURF.blit(cjMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                                        copButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 150, copButtonRect[2],copButtonRect[3])
                                        journalistButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 115, journalistButtonRect[2],journalistButtonRect[3])
                                        DISPLAYSURF.blit(copButton, copButtonRect)
                                        DISPLAYSURF.blit(journalistButton, journalistButtonRect)
                                        MAINCLOCK.tick(FPS)
                                        pygame.display.update()

                elif (cop1 in pieces[x][y] or cop2 in pieces[x][y]) and bool(targets) == True:
                    tgtButton = []
                    tgtButtonRect = []
                    for tgt in enumerate(targets):
                        tgtButton.append(BIGFONT.render(tgt[1].player, True, WHITE, BLACK))
                        tgtButtonRect.append(tgtButton[tgt[0]].get_rect())
                        tgtButtonRect[tgt[0]] = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - (150 - tgt[0]*40), tgtButtonRect[tgt[0]][2],tgtButtonRect[tgt[0]][3])
                    while wait_for_selection == True:  
                        drawBoard(board, pieces)
                        copButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 40, copButtonRect[2],copButtonRect[3])
                        DISPLAYSURF.blit(cjMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                        DISPLAYSURF.blit(copButton, copButtonRect)
                        if len(tgtButton) == 1:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                        elif len(tgtButton) == 2:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                        elif len(tgtButton) == 3:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                            DISPLAYSURF.blit(tgtButton[2], tgtButtonRect[2])
                        MAINCLOCK.tick(FPS)
                        pygame.display.update()

                        for event in pygame.event.get():
                            
                            #Action menu loop
                            if event.type == MOUSEBUTTONUP:

                                mousex, mousey = event.pos

                                if copButtonRect.collidepoint((mousex,mousey)):

                                    if destiny >= .7:
                                        print("hit successful")
                                        remove_counter = False
                                        if cop1 in pieces[x][y] and remove_counter == False:
                                            pieces[x][y].remove(cop1)
                                            remove_counter = True
                                            cop_regen = 1
                                        if cop2 in pieces[x][y] and remove_counter == False:
                                            pieces[x][y].remove(cop2)
                                            remove_counter = True
                                            cop_regen = 2
                                        chargeAction = True
                                        return jail, recruits, chargeAction, copRegen, journalistRegen
                                    elif destiny >= .4 and destiny <.7:
                                        print("HEADLINE: Cops shoot down gangster at distllery ")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                recruits.append(piece)
                                                chargeAction = True
                                                return jail, recruits, chargeAction, copRegen, journalistRegen
                                    elif destiny >= 0 and destiny <.4:
                                        print("HEADLINE: Cops arrest gangster for attempted murder")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                chargeAction = True
                                                return jail, recruits, chargeAction, copRegen, journalistRegen

                                for tgt in enumerate(targets):
                                    if tgtButtonRect[tgt[0]].collidepoint((mousex,mousey)):
                                        if destiny >= .7:
                                            print(str(player) + "sucessfully hit " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == tgt[1].player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(piece)
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                                        elif destiny >= .4 and destiny < .7:
                                            print(str(player) + " got shot down by " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(piece)
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                                        elif destiny >= 0 and destiny < .4:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen



                elif cop1 in pieces[x][y] or cop2 in pieces[x][y]:

                    if destiny >= .7:
                        print("hit successful")
                        remove_counter = False
                        if cop1 in pieces[x][y] and remove_counter == False:
                            pieces[x][y].remove(cop1)
                            remove_counter = True
                            cop_regen = 1
                        if cop2 in pieces[x][y] and remove_counter == False:
                            pieces[x][y].remove(cop2)
                            remove_counter = True
                            cop_regen = 2
                        chargeAction = True
                        return jail, recruits, chargeAction, copRegen, journalistRegen
                    if destiny >= .4 and destiny <.7:
                        print("HEADLINE: Cops shoot down gangster at distllery ")
                        for piece in pieces[x][y]:
                            if piece.player == player:
                                pieces[x][y].remove(piece)
                                recruits.append(piece)
                                chargeAction = True
                                return jail, recruits, chargeAction, copRegen, journalistRegen
                    if destiny >= 0 and destiny <.4:
                        print("HEADLINE: Cops arrest gangster for attempted murder")
                        for piece in pieces[x][y]:
                            if piece.player == player:
                                pieces[x][y].remove(piece)
                                jail[player_idx] += 1
                                chargeAction = True
                                return jail, recruits, chargeAction, copRegen, journalistRegen

                # Need entire elif loop for players hitting other players - cops always have 40% of arrest if sharing same space, informants have hidden cop effects
                elif journalist in pieces[x][y] and bool(targets) == True:
                    tgtButton = []
                    tgtButtonRect = []
                    for tgt in enumerate(targets):
                        tgtButton.append(BIGFONT.render(tgt[1].player, True, WHITE, BLACK))
                        tgtButtonRect.append(tgtButton[tgt[0]].get_rect())
                        tgtButtonRect[tgt[0]] = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - (150 - tgt[0]*40), tgtButtonRect[tgt[0]][2],tgtButtonRect[tgt[0]][3])
                    while wait_for_selection == True:  
                        drawBoard(board, pieces)
                        journalistButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 40, journalistButtonRect[2],journalistButtonRect[3])
                        DISPLAYSURF.blit(cjMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                        DISPLAYSURF.blit(journalistButton, journalistButtonRect)
                        if len(tgtButton) == 1:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                        elif len(tgtButton) == 2:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                        elif len(tgtButton) == 3:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                            DISPLAYSURF.blit(tgtButton[2], tgtButtonRect[2])
                        MAINCLOCK.tick(FPS)
                        pygame.display.update()

                        for event in pygame.event.get():
                                
                            #Action menu loop
                            if event.type == MOUSEBUTTONUP:

                                mousex, mousey = event.pos

                                if journalistButtonRect.collidepoint((mousex,mousey)):
                                    if destiny >= .7:
                                        print("hit successful")
                                        pieces[x][y].remove(journalist)
                                        journalist_regen = True
                                        chargeAction = True
                                        return jail, recruits, chargeAction, copRegen, journalistRegen
                                    if destiny >= .4 and destiny <.7:
                                        print("HEADLINE: nearly-assasinated journalist begins campaign against would be killers")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                recruits.append(piece)
                                                journalist_bribe_bank[player_idx] -= 10
                                                chargeAction = True
                                                return jail, recruits, chargeAction, copRegen, journalistRegen
                                    if destiny >= 0 and destiny <.4:
                                        print("HEADLINE: Cops arrest gangster for attempted murder")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                chargeAction = True
                                                return jail, recruits, chargeAction, copRegen, journalistRegen

                                for tgt in enumerate(targets):
                                    if tgtButtonRect[tgt[0]].collidepoint((mousex,mousey)):
                                        if destiny >= .7:
                                            print(str(player) + "sucessfully hit " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == tgt[1].player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(piece)
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                                        elif destiny >= .4 and destiny < .7:
                                            print(str(player) + " got shot down by " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(piece)
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                                        elif destiny >= 0 and destiny < .4:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                elif journalist in pieces[x][y]:
                    if destiny >= .7:
                        print("hit successful")
                        pieces[x][y].remove(journalist)
                        journalist_regen = True
                        chargeAction = True
                        return jail, recruits, chargeAction, copRegen, journalistRegen
                    if destiny >= .4 and destiny <.7:
                        print("HEADLINE: nearly-assasinated journalist begins campaign against would be killers")
                        for piece in pieces[x][y]:
                            if piece.player == player:
                                pieces[x][y].remove(piece)
                                recruits.append(piece)
                                journalist_bribe_bank[player_idx] -= 10
                                chargeAction = True
                                return jail, recruits, chargeAction, copRegen, journalistRegen
                    if destiny >= 0 and destiny <.4:
                        print("HEADLINE: Cops arrest gangster for attempted murder")
                        for piece in pieces[x][y]:
                            if piece.player == player:
                                pieces[x][y].remove(piece)
                                jail[player_idx] += 1
                                chargeAction = True
                                return jail, recruits, chargeAction, copRegen, journalistRegen
                
                elif targets:
                    tgtButton = []
                    tgtButtonRect = []
                    for tgt in enumerate(targets):
                        tgtButton.append(BIGFONT.render(tgt[1].player, True, WHITE, BLACK))
                        tgtButtonRect.append(tgtButton[tgt[0]].get_rect())
                        tgtButtonRect[tgt[0]] = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - (150 - tgt[0]*40), tgtButtonRect[tgt[0]][2],tgtButtonRect[tgt[0]][3])
                    while wait_for_selection == True:  
                        drawBoard(board, pieces)
                        DISPLAYSURF.blit(cjMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                        if len(tgtButton) == 1:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                        elif len(tgtButton) == 2:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                        elif len(tgtButton) == 3:
                            DISPLAYSURF.blit(tgtButton[0], tgtButtonRect[0])
                            DISPLAYSURF.blit(tgtButton[1], tgtButtonRect[1])
                            DISPLAYSURF.blit(tgtButton[2], tgtButtonRect[2])
                        #time.sleep(1)
                        MAINCLOCK.tick(FPS)
                        pygame.display.update()

                        for event in pygame.event.get():
                            
                            #Action menu loop
                            if event.type == MOUSEBUTTONUP:

                                mousex, mousey = event.pos

                                for tgt in enumerate(targets):
                                    if tgtButtonRect[tgt[0]].collidepoint((mousex,mousey)):
                                        if destiny >= .7:
                                            print(str(player) + "sucessfully hit " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == tgt[1].player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(piece)
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                                        elif destiny >= .4 and destiny < .7:
                                            print(str(player) + " got shot down by " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    recruits.append(piece)
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen

                                        elif destiny >= 0 and destiny < .4:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, recruits, chargeAction, copRegen, journalistRegen


                
                else:
                    drawBoard(board, pieces)
                    pieceWarningRect = pygame.Rect(mousex, mousey, pieceWarningRect[2],pieceWarningRect[3])
                    DISPLAYSURF.blit(pieceWarning, pieceWarningRect)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()
                    time.sleep(1)
                    wait_for_input = False
                    return jail, recruits, chargeAction, copRegen, journalistRegen

def spaceaction():
    print("doaction")

def copMove(board,pieces):
    
    delta_x = 200
    delta_y = 200
    copcount = 0

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            for piece in pieces[x][y]:
                if (piece.player == "cop" or piece.player == "journalist") and copcount <= 2:
                    while isOnBoard(x + delta_x, y + delta_y) != True:
                        delta_x = random.choice((-1,0,1))
                        delta_y = random.choice((-1,0,1))
                        pieces[x][y].remove(piece)
                        pieces[x + delta_x][y + delta_y].append(piece)
                    delta_x = 200
                    delta_y = 200
                    copcount += 1
                    drawBoard(board, pieces)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()

def election(mainBoard, pieces):

    MENUWIDTH = WINDOWWIDTH / 6
    MENUHEIGHT = WINDOWHEIGHT / 3
    BUTTONWIDTH = MENUWIDTH / 1.2
    BUTTONHEIGHT = MENUHEIGHT / 8
    
    
    
    #Width and height do not appear to change anything in actionmenurect but i left them just in case
    eMenuRect = pygame.Rect(200,200,MENUWIDTH,MENUHEIGHT)
    eMenuSurf = pygame.Surface((MENUWIDTH, MENUHEIGHT))
    pygame.draw.rect(eMenuSurf, WHITE, eMenuSurf.get_rect())
    player1Button = BIGFONT.render('Player 1', True, WHITE, BLACK)
    player1ButtonRect = player1Button.get_rect()
    player2Button = BIGFONT.render('Player 2', True, WHITE, BLACK)
    player2ButtonRect = player2Button.get_rect()
    player3Button = BIGFONT.render('Player 3', True, WHITE, BLACK)
    player3ButtonRect = player3Button.get_rect()
    player4Button = BIGFONT.render('Player 4', True, WHITE, BLACK)
    player4ButtonRect = player4Button.get_rect()
    voteHeader = BIGFONT.render('Vote for the new mayor!', True, WHITE, BLACK)
    voteHeaderRect = voteHeader.get_rect()
    player_eidx = 0
    popular_opinion = [0,0,0,0]
    vote_bank = [0,0,0,0]
    election_bank = [0,0,0,0]
    num_votes = 0
    player1ButtonRect = pygame.Rect(200 + MENUWIDTH/6, 200 + MENUHEIGHT - 150, player1ButtonRect[2],player1ButtonRect[3])
    player2ButtonRect = pygame.Rect(200 + MENUWIDTH/6, 200 + MENUHEIGHT - 115, player2ButtonRect[2],player2ButtonRect[3])
    player3ButtonRect = pygame.Rect(200 + MENUWIDTH/6, 200 + MENUHEIGHT - 80, player3ButtonRect[2],player3ButtonRect[3])
    player4ButtonRect = pygame.Rect(200 + MENUWIDTH/6, 200 + MENUHEIGHT - 45, player4ButtonRect[2],player4ButtonRect[3])
    voteHeaderRect = pygame.Rect(100 + MENUWIDTH/6, 200 + MENUHEIGHT - 200, player4ButtonRect[2],player4ButtonRect[3])

    p1, p2, p3, p4 = 0, 0, 0, 0

    while num_votes <= 3:  
        drawBoard(mainBoard, pieces)
        DISPLAYSURF.blit(eMenuSurf, (200,200,MENUWIDTH,MENUHEIGHT))
        DISPLAYSURF.blit(player1Button, player1ButtonRect)
        DISPLAYSURF.blit(player2Button, player2ButtonRect)
        DISPLAYSURF.blit(player3Button, player3ButtonRect)
        DISPLAYSURF.blit(player4Button, player4ButtonRect)
        DISPLAYSURF.blit(voteHeader, voteHeaderRect)
        MAINCLOCK.tick(FPS)
        pygame.display.update()

        for event in pygame.event.get():
            
            #Action menu loop
            if event.type == MOUSEBUTTONUP:

                mousex, mousey = event.pos
                if player1ButtonRect.collidepoint((mousex,mousey)):
                    #change to a seperate function, players, board, pieces
                    print("vote for player 1")
                    p1 += 1
                    vote_bank[0] = p1
                    num_votes += 1
                if player2ButtonRect.collidepoint((mousex,mousey)):
                    #change to a seperate function, players, board, pieces
                    print("vote for player 2")
                    p2 += 1
                    #vote_bank[1] =+ 1
                    num_votes += 1
                if player3ButtonRect.collidepoint((mousex,mousey)):
                    #change to a seperate function, players, board, pieces
                    print("vote for player 3")
                    #vote_bank[2] += 1
                    p3 += 1
                    num_votes += 1
                if player4ButtonRect.collidepoint((mousex,mousey)):
                    #change to a seperate function, players, board, pieces
                    print("vote for player 4")
                    #vote_bank[3] =+ 1
                    p4 += 1
                    num_votes += 1
    vote_bank = [p1,p2,p3,p4]

    total_j = sum(journalist_bribe_bank)
    i=0
    if total_j <= 5:
        player_opinion = [0,0,0,0]

    else:
        for player in journalist_bribe_bank:
            player_popular_opinion = player/total_j
            if player_popular_opinion >= .2 and player_popular_opinion < .4:
                popular_opinion[i] = 1
            elif player_popular_opinion >= .4 and player_popular_opinion < .6:
                popular_opinion[i] = 2
            elif player_popular_opinion >= .6 and player_popular_opinion < .8:
                popular_opinion[i] = 3
            elif player_popular_opinion >= .8:
                popular_opinion[i] = 4
            else:
                popular_opinion[i] = 0
            i+=1
    election_bank = numpy.add(vote_bank,popular_opinion)
    for player in election_bank:
        player_eidx +=1
        if player >= 5:
            print("player " + str(player_eidx) + " wins!")

    return election_bank

if __name__ == '__main__':
    main()
