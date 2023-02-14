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
        self.rat = False
        self.player = player
        self.pc = "pc"

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
        self.rat = False
        self.pc = "npc"

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
        self.rat = False
        self.pc = "npc"

class no_piece_class(pygame.sprite.Sprite):
    def __init__(self):
        super(no_piece_class, self).__init__()
        self.player = None
        self.rat = False
        self.pc = "npc"

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
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE, players, player_bank, cop_bribe_bank, journalist_bribe_bank, election_bank, jail, rat, no_piece, player11, player12, player13, player21, player22, player23, player31, player32, player33, player41, player42, player43, cop1, cop2, journalist, journalistRegen, copRegen
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
    rat = [0,0,0,0]


    no_piece = no_piece_class()
    player11 = madeMan(BLACK, players[0])
    player12 = madeMan(BLACK, players[0])
    player13 = madeMan(BLACK, players[0])
    rat1 = madeMan(BLACK,players[0])
    rat1.rat = True
    player21 = madeMan(BRIGHTBLUE, players[1])
    player22 = madeMan(BRIGHTBLUE, players[1])
    player23 = madeMan(BRIGHTBLUE, players[1])
    rat2 = madeMan((BRIGHTBLUE),players[1])
    rat2.rat = True
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
    bailButton = BIGFONT.render('Bail', True, WHITE, BLACK)
    bailButtonRect = jobButton.get_rect()

    pieceWarning = BIGFONT.render('Choose your own piece', True, WHITE, BLACK)
    pieceWarningRect = pieceWarning.get_rect()

    moveWarning = BIGFONT.render('You cant move there', True, WHITE, BLACK)
    moveWarningRect = moveWarning.get_rect()

    action_count = 0
    round_count = 0
    copRegen = 0
    journalistRegen = False

    election_bank = [0,0,0,0]
    jail = [0,0,0,0]
    rat = [0,0,0,0]


    while True: # main game loop
        # Keep looping for player and computer's turns.
        player_idx = players.index(turn)
        movexy = None
        if action_count <= 1:
            # Player's turn:
            #getRevenues(mainBoard, pieces, players, player_bank, player1Tile, player2Tile, player3Tile, player4Tile)
            getRevenues(mainBoard, pieces, players, player_bank, player1Tile, player2Tile)

            while movexy == None:
                # Keep looping until the player clicks on a valid space.
                drawBoard(mainBoard, pieces)
                turnBanner = BIGFONT.render((str(turn) + "'s turn"), True, WHITE, BLACK)
                bankBanner = BIGFONT.render("Bank", True, WHITE, BLACK)
                bank1Banner = BIGFONT.render(str(player_bank[0]), True, WHITE, BLACK)
                bank2Banner = BIGFONT.render(str(player_bank[1]), True, WHITE, BLACK)
                bank3Banner = BIGFONT.render(str(player_bank[2]), True, WHITE, BLACK)
                bank4Banner = BIGFONT.render(str(player_bank[3]), True, WHITE, BLACK)
                ebankBanner = BIGFONT.render("Polls", True, WHITE, BLACK)
                ebank1Banner = BIGFONT.render(str(election_bank[0]), True, WHITE, BLACK)
                ebank2Banner = BIGFONT.render(str(election_bank[1]), True, WHITE, BLACK)
                ebank3Banner = BIGFONT.render(str(election_bank[2]), True, WHITE, BLACK)
                ebank4Banner = BIGFONT.render(str(election_bank[3]), True, WHITE, BLACK)
                jailBanner = BIGFONT.render("Jail", True, WHITE, BLACK)
                jail1Banner = BIGFONT.render(str(jail[0]), True, WHITE, BLACK)
                jail2Banner = BIGFONT.render(str(jail[1]), True, WHITE, BLACK)
                jail3Banner = BIGFONT.render(str(jail[2]), True, WHITE, BLACK)
                jail4Banner = BIGFONT.render(str(jail[3]), True, WHITE, BLACK)
                turnBannerRect = turnBanner.get_rect()
                bankBannerRect = bankBanner.get_rect()
                bank1BannerRect = bank1Banner.get_rect()
                bank2BannerRect = bank2Banner.get_rect()
                bank3BannerRect = bank3Banner.get_rect()
                bank4BannerRect = bank4Banner.get_rect()
                ebankBannerRect = ebankBanner.get_rect()
                ebank1BannerRect = ebank1Banner.get_rect()
                ebank2BannerRect = ebank2Banner.get_rect()
                ebank3BannerRect = ebank3Banner.get_rect()
                ebank4BannerRect = ebank4Banner.get_rect()
                jailBannerRect = jailBanner.get_rect()
                jail1BannerRect = jail1Banner.get_rect()
                jail2BannerRect = jail2Banner.get_rect()
                jail3BannerRect = jail3Banner.get_rect()
                jail4BannerRect = jail4Banner.get_rect()
                turnBannerRect = pygame.Rect(WINDOWWIDTH/3, 0, turnBannerRect[2],turnBannerRect[3])
                bankBannerRect = pygame.Rect(0, 0, bankBannerRect[2],bankBannerRect[3])
                bank1BannerRect = pygame.Rect(20, 30, bank1BannerRect[2],bank1BannerRect[3])
                bank2BannerRect = pygame.Rect(20, 60, bank2BannerRect[2],bank2BannerRect[3])
                bank3BannerRect = pygame.Rect(20, 90, bank3BannerRect[2],bank3BannerRect[3])
                bank4BannerRect = pygame.Rect(20, 120, bank4BannerRect[2],bank4BannerRect[3])
                ebankBannerRect = pygame.Rect(0, WINDOWHEIGHT-30, ebankBannerRect[2],ebankBannerRect[3])
                ebank1BannerRect = pygame.Rect(30, WINDOWHEIGHT - 150, ebank1BannerRect[2],ebank1BannerRect[3])
                ebank2BannerRect = pygame.Rect(30, WINDOWHEIGHT - 120, ebank2BannerRect[2],ebank2BannerRect[3])
                ebank3BannerRect = pygame.Rect(30, WINDOWHEIGHT - 90, ebank3BannerRect[2],ebank3BannerRect[3])
                ebank4BannerRect = pygame.Rect(30, WINDOWHEIGHT - 60, ebank4BannerRect[2],ebank4BannerRect[3])
                jailBannerRect = pygame.Rect(WINDOWWIDTH - 50, WINDOWHEIGHT - 30, jailBannerRect[2],jailBannerRect[3])
                jail1BannerRect = pygame.Rect(WINDOWWIDTH - 50, WINDOWHEIGHT - 150, jail1BannerRect[2],jail1BannerRect[3])
                jail2BannerRect = pygame.Rect(WINDOWWIDTH - 50, WINDOWHEIGHT - 120, jail2BannerRect[2],jail2BannerRect[3])
                jail3BannerRect = pygame.Rect(WINDOWWIDTH - 50, WINDOWHEIGHT - 90, jail3BannerRect[2],jail3BannerRect[3])
                jail4BannerRect = pygame.Rect(WINDOWWIDTH - 50, WINDOWHEIGHT - 60, jail4BannerRect[2],jail4BannerRect[3])
                DISPLAYSURF.blit(turnBanner, turnBannerRect)
                DISPLAYSURF.blit(bankBanner, bankBannerRect)
                DISPLAYSURF.blit(bank1Banner, bank1BannerRect)
                DISPLAYSURF.blit(bank2Banner, bank2BannerRect)
                DISPLAYSURF.blit(bank3Banner, bank3BannerRect)
                DISPLAYSURF.blit(bank4Banner, bank4BannerRect)
                DISPLAYSURF.blit(ebankBanner, ebankBannerRect)
                DISPLAYSURF.blit(ebank1Banner, ebank1BannerRect)
                DISPLAYSURF.blit(ebank2Banner, ebank2BannerRect)
                DISPLAYSURF.blit(ebank3Banner, ebank3BannerRect)
                DISPLAYSURF.blit(ebank4Banner, ebank4BannerRect)
                DISPLAYSURF.blit(jailBanner, jailBannerRect)
                DISPLAYSURF.blit(jail1Banner, jail1BannerRect)
                DISPLAYSURF.blit(jail2Banner, jail2BannerRect)
                DISPLAYSURF.blit(jail3Banner, jail3BannerRect)
                DISPLAYSURF.blit(jail4Banner, jail4BannerRect)
                MAINCLOCK.tick(FPS)
                pygame.display.update()
                checkForQuit()
                for event in pygame.event.get(): # event handling loop

                    if event.type == MOUSEBUTTONUP and event.button == 3: 
                        wait_for_selection = True
                        mousex, mousey = event.pos
                        space_clickedx = mousex
                        space_clickedy = mousey
                        while wait_for_selection == True:  
                            drawBoard(mainBoard, pieces)
                            DISPLAYSURF.blit(actionMenuSurf, (mousex,mousey,MENUWIDTH,MENUHEIGHT))
                            moveButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 150, moveButtonRect[2],moveButtonRect[3])
                            bribeButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 120, bribeButtonRect[2],bribeButtonRect[3])
                            hitButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 90, hitButtonRect[2],hitButtonRect[3])
                            jobButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 60, jobButtonRect[2],jobButtonRect[3])
                            bailButtonRect = pygame.Rect(mousex + MENUWIDTH/6, mousey + MENUHEIGHT - 30, bailButtonRect[2],bailButtonRect[3])
                            DISPLAYSURF.blit(moveButton, moveButtonRect)
                            DISPLAYSURF.blit(bribeButton, bribeButtonRect)
                            DISPLAYSURF.blit(hitButton, hitButtonRect)
                            DISPLAYSURF.blit(jobButton, jobButtonRect)
                            DISPLAYSURF.blit(bailButton, bailButtonRect)
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
                                        if copCount <= 0:
                                            copCount = 0
                                        elif copCount >= player_bank[player_idx]:
                                            copCount = player_bank[player_idx]
                                        if journalistCount <= 0:
                                            journalistCount = 0
                                        elif journalistCount >= player_bank[player_idx]:
                                            journalistCount = player_bank[player_idx]
                                        cop_bribe_bank[player_idx] += copCount
                                        journalist_bribe_bank[player_idx] += journalistCount
                                        player_bank[player_idx] -= (copCount + journalistCount)
                                        if chargeAction == True:
                                            action_count += 1 
                                    elif hitButtonRect.collidepoint( (mousex,mousey)):
                                        jail, chargeAction, copRegen, journalistRegen= hit(turn, player_idx, mainBoard, pieces, copRegen, journalistRegen)
                                        if chargeAction == True:
                                            action_count += 1 
                                    elif jobButtonRect.collidepoint( (mousex,mousey)):
                                        job(turn, mainBoard, pieces)
                                        action_count += 1 
                                    elif bailButtonRect.collidepoint( (mousex,mousey)):
                                        if jail[player_idx] >= 1 and player_bank[player_idx] >= 10:
                                            bail(turn,pieces)
                                            jail[player_idx] -= 1
                                            player_bank[player_idx] -=10
                                            action_count +=1
                                        else:
                                            continue

                                    wait_for_selection = False
                                    if action_count >= 2:
                                        if player_idx < len(players) - 1:
                                            turn = players[player_idx + 1]
                                            player_idx += 1
                                        else: 
                                            drawBoard(mainBoard, pieces)
                                            MAINCLOCK.tick(FPS)
                                            pygame.display.update()
                                            getRevenues(mainBoard, pieces, players, player_bank, player1Tile, player2Tile)
                                            copMove(mainBoard,pieces)
                                            turn = players[0]
                                            player_idx = 0
                                            round_count += 1
                                            if round_count >= 5:
                                                election_bank = election(mainBoard, pieces)    
                                                if journalistRegen == True:
                                                    pieces[2][2].append(journalist)          
                                                    journalistRegen = False          
                                                if copRegen == 1:
                                                    pieces[2][2].append(cop1)
                                                    copRegen == 0
                                                if copRegen == 2:
                                                    pieces[2][2].append(cop2)  
                                                    copRegen == 0                             
                                                round_count = 0

                                        action_count = 0
                                        break



def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)

#def getRevenues(board, pieces, players, player_bank, player1Tile, player2Tile, player3Tile, player4Tile):
def getRevenues(board, pieces, players, player_bank, player1Tile, player2Tile):

    player_bank[0] += 1
    player_bank[1] += 1
    player_bank[2] += 1
    player_bank[3] += 1
    pcCount = 0
    lowSpace = 2
    highSpace = 4
    copDamping = 0.5
    copSum = 0
    for cb in cop_bribe_bank:
        copSum += cb

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            copFlag = copCheck(x, y, pieces)
            for player in players:
                player_idx = players.index(player)
                if copSum > 0:
                    if cop_bribe_bank[player_idx]/copSum >= .4:
                        copFlag = False

                for piece in pieces[x][y]:
                    if board[x][y] == SPEAK_EASY and piece.player == player:
                        for piece in pieces[x][y]:
                            if piece.pc == "pc":
                                pcCount += 1
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += (lowSpace/pcCount)*copDamping
                        else:
                            player_bank[players.index(player)] += lowSpace/pcCount

                    elif board[x][y] == LOAN_SHARK and piece.player == player:
                        for piece in pieces[x][y]:
                            if piece.pc == "pc":
                                pcCount += 1
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += (lowSpace/pcCount)*copDamping
                        else:
                            player_bank[players.index(player)] += lowSpace/pcCount
                
                    elif board[x][y] == PAWN_SHOP and piece.player == player:
                        for piece in pieces[x][y]:
                            if piece.pc == "pc":
                                pcCount += 1
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += (lowSpace/pcCount)*copDamping
                        else:
                            player_bank[players.index(player)] += lowSpace/pcCount

                    elif board[x][y] == MOM_POP and piece.player == player:
                        for piece in pieces[x][y]:
                            if piece.pc == "pc":
                                pcCount += 1
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += (lowSpace/pcCount)*copDamping
                        else:
                            player_bank[players.index(player)] += lowSpace/pcCount

                    elif board[x][y] == BANK and piece.player == player:
                        for piece in pieces[x][y]:
                            if piece.pc == "pc":
                                pcCount += 1
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += (highSpace/pcCount)*copDamping
                        else:
                            player_bank[players.index(player)] += (highSpace/pcCount)

                    elif board[x][y] ==FINANCIAL_DISTRICT and piece.player == player:
                        for piece in pieces[x][y]:
                            if piece.pc == "pc":
                                pcCount += 1
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += (highSpace/pcCount)*copDamping
                        else:
                            player_bank[players.index(player)] += (highSpace/pcCount)

                    elif board[x][y] == DISTILLERY and piece.player == player:
                        for piece in pieces[x][y]:
                            if piece.pc == "pc":
                                pcCount += 1
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += (highSpace/pcCount)*copDamping
                        else:
                            player_bank[players.index(player)] += (highSpace/pcCount)

                    elif board[x][y] == RACE_TRACK and piece.player == player:
                        for piece in pieces[x][y]:
                            if piece.pc == "pc":
                                pcCount += 1
                        if copFlag == True:
                            #if player.copbribe = true then effect dampened, 
                            player_bank[players.index(player)] += (highSpace/pcCount)*copDamping
                        else:
                            player_bank[players.index(player)] += (highSpace/pcCount)
    i = 0
    for pb in player_bank:
        player_bank[i] = round(pb, 1)
        i +=1


    return player_bank

def copCheck(x, y, pieces):
    copFlag = False
    xi = [-1, 0, 1]
    yj = [-1, 0, 1]

    for i in xi:
        for j in yj:
            if isOnBoard(x+i,y+j):
                for piece in pieces[x+i][y+j]:
                    if piece.player == "cop" or piece.rat == True:
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
            try:
            
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

            except TypeError:
                continue
            
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
        try:
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
        except TypeError:
            continue



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
                    return copCount, journalistCount, chargeAction
    
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
                                            copRegen = 1
                                        if cop2 in pieces[x][y] and remove_counter == False:
                                            pieces[x][y].remove(cop2)
                                            remove_counter = True
                                            copRegen = 2
                                        chargeAction = True
                                        return jail, chargeAction, copRegen, journalistRegen
                                    if destiny >= 0 and destiny <.7:
                                        print("HEADLINE: Cops arrest gangster for attempted murder")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                chargeAction = True
                                                return jail, chargeAction, copRegen, journalistRegen

                                elif journalistButtonRect.collidepoint((mousex,mousey)):
                                    if destiny >= .7:
                                        print("hit successful")
                                        pieces[x][y].remove(journalist)
                                        journalistRegen = True
                                        chargeAction = True
                                        return jail, chargeAction, copRegen, journalistRegen
            
                                    if destiny >= 0 and destiny <.7:
                                        print("HEADLINE: nearly-assasinated journalist begins campaign against would be killers")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                journalist_bribe_bank[player_idx] -= 10
                                                chargeAction = True
                                                return jail, chargeAction, copRegen, journalistRegen

                                for tgt in enumerate(targets):
                                    if tgtButtonRect[tgt[0]].collidepoint((mousex,mousey)):
                                        if destiny >= .7:
                                            print(str(player) + "sucessfully hit " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == tgt[1].player:
                                                    pieces[x][y].remove(piece)
                                                    chargeAction = True
                                                    return jail, chargeAction, copRegen, journalistRegen

                                        elif destiny >= 0 and destiny < .4:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, chargeAction, copRegen, journalistRegen
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
                                            copRegen = 1
                                        if cop2 in pieces[x][y] and remove_counter == False:
                                            pieces[x][y].remove(cop2)
                                            remove_counter = True
                                            copRegen = 2
                                        chargeAction = True
                                        return jail, chargeAction, copRegen, journalistRegen

                                    if destiny >= 0 and destiny <.7:
                                        print("HEADLINE: Cops arrest gangster for attempted murder")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                chargeAction = True
                                                return jail, chargeAction, copRegen, journalistRegen

                                elif journalistButtonRect.collidepoint( (mousex,mousey)):
                                    if destiny >= .7:
                                        print("hit successful")
                                        pieces[x][y].remove(journalist)
                                        journalistRegen = True
                                        chargeAction = True
                                        return jail, chargeAction, copRegen, journalistRegen

                                    if destiny >= 0 and destiny <.7:
                                        print("HEADLINE: nearly-assasinated journalist begins campaign against would be killers")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                chargeAction = True
                                                return jail, chargeAction, copRegen, journalistRegen


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
                                            copRegen = 1
                                        if cop2 in pieces[x][y] and remove_counter == False:
                                            pieces[x][y].remove(cop2)
                                            remove_counter = True
                                            copRegen = 2
                                        chargeAction = True
                                        return jail, chargeAction, copRegen, journalistRegen

                                    elif destiny >= 0 and destiny <.7:
                                        print("HEADLINE: Cops arrest gangster for attempted murder")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                chargeAction = True
                                                return jail, chargeAction, copRegen, journalistRegen

                                for tgt in enumerate(targets):
                                    if tgtButtonRect[tgt[0]].collidepoint((mousex,mousey)):
                                        if destiny >= .7:
                                            print(str(player) + "sucessfully hit " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == tgt[1].player:
                                                    pieces[x][y].remove(piece)
                                                    chargeAction = True
                                                    return jail, chargeAction, copRegen, journalistRegen

                                        elif destiny >= 0 and destiny < .7:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, chargeAction, copRegen, journalistRegen



                elif cop1 in pieces[x][y] or cop2 in pieces[x][y]:

                    if destiny >= .7:
                        print("hit successful")
                        remove_counter = False
                        if cop1 in pieces[x][y] and remove_counter == False:
                            pieces[x][y].remove(cop1)
                            remove_counter = True
                            copRegen = 1
                        if cop2 in pieces[x][y] and remove_counter == False:
                            pieces[x][y].remove(cop2)
                            remove_counter = True
                            copRegen = 2
                        chargeAction = True
                        return jail, chargeAction, copRegen, journalistRegen

                    if destiny >= 0 and destiny <.7:
                        print("HEADLINE: Cops arrest gangster for attempted murder")
                        for piece in pieces[x][y]:
                            if piece.player == player:
                                pieces[x][y].remove(piece)
                                jail[player_idx] += 1
                                chargeAction = True
                                return jail, chargeAction, copRegen, journalistRegen

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
                                        journalistRegen = True
                                        chargeAction = True
                                        return jail, chargeAction, copRegen, journalistRegen

                                    if destiny >= 0 and destiny <.7:
                                        print("HEADLINE: nearly-assasinated journalist begins campaign against would be killers")
                                        for piece in pieces[x][y]:
                                            if piece.player == player:
                                                pieces[x][y].remove(piece)
                                                jail[player_idx] += 1
                                                chargeAction = True
                                                return jail, chargeAction, copRegen, journalistRegen

                                for tgt in enumerate(targets):
                                    if tgtButtonRect[tgt[0]].collidepoint((mousex,mousey)):
                                        if destiny >= .7:
                                            print(str(player) + "sucessfully hit " + str(tgt[1].player))
                                            for piece in pieces[x][y]:
                                                if piece.player == tgt[1].player:
                                                    pieces[x][y].remove(piece)
                                                    chargeAction = True
                                                    return jail, chargeAction, copRegen, journalistRegen

                                        elif destiny >= 0 and destiny < .7:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, chargeAction, copRegen, journalistRegen

                elif journalist in pieces[x][y]:
                    if destiny >= .7:
                        print("hit successful")
                        pieces[x][y].remove(journalist)
                        journalistRegen = True
                        chargeAction = True
                        return jail, chargeAction, copRegen, journalistRegen

                    if destiny >= 0 and destiny <.4:
                        print("HEADLINE: nearly-assasinated journalist begins campaign against would be killers")
                        for piece in pieces[x][y]:
                            if piece.player == player:
                                pieces[x][y].remove(piece)
                                jail[player_idx] += 1
                                chargeAction = True
                                return jail, chargeAction, copRegen, journalistRegen
                
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
                                                    chargeAction = True
                                                    return jail, chargeAction, copRegen, journalistRegen

                                        elif destiny >= 0 and destiny < .7:
                                            print("HEADLINE: Cops arrest gangster for attempted murder")
                                            for piece in pieces[x][y]:
                                                if piece.player == player:
                                                    pieces[x][y].remove(piece)
                                                    jail[player_idx] += 1
                                                    chargeAction = True
                                                    return jail, chargeAction, copRegen, journalistRegen


                
                else:
                    drawBoard(board, pieces)
                    pieceWarningRect = pygame.Rect(mousex, mousey, pieceWarningRect[2],pieceWarningRect[3])
                    DISPLAYSURF.blit(pieceWarning, pieceWarningRect)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()
                    time.sleep(1)
                    wait_for_input = False
                    return jail, chargeAction, copRegen, journalistRegen

def job(player, board, pieces):

    pieceWarning = BIGFONT.render('Choose a space with your piece', True, WHITE, BLACK)
    pieceWarningRect = pieceWarning.get_rect()
    destiny = random.random()
    chargeAction = False

    wait_for_move = True
    drawBoard(board, pieces)
    MAINCLOCK.tick(FPS)
    pygame.display.update()
    while wait_for_move == True:
        try:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    x,y = getSpaceClicked(mousex, mousey)
                    copFlag = copCheck(x,y, pieces)
                    for piece in pieces[x][y]:
                        if piece.player == player:
                            if copFlag == True:
                                if destiny >= .7:
                                    
                                    if board[x][y] == SPEAK_EASY and piece.player == player:
                                        player_bank[players.index(player)] += 4

                                    elif board[x][y] == LOAN_SHARK and piece.player == player:

                                        player_bank[players.index(player)] += 3
                                
                                    elif board[x][y] == PAWN_SHOP and piece.player == player:
                                        player_bank[players.index(player)] += 2

                                    elif board[x][y] == MOM_POP and piece.player == player:
                                        player_bank[players.index(player)] += 1

                                    elif board[x][y] == BANK and piece.player == player:
                                        player_bank[players.index(player)] += 8

                                    elif board[x][y] ==FINANCIAL_DISTRICT and piece.player == player:
                                        player_bank[players.index(player)] += 7

                                    elif board[x][y] == DISTILLERY and piece.player == player:
                                        player_bank[players.index(player)] += 6

                                    elif board[x][y] == RACE_TRACK and piece.player == player:
                                        player_bank[players.index(player)] += 5
                                    #successBanner = BIGFONT.render(str(player) + "robbed a " + str(board[x][y]), True, WHITE, BLACK)
                                    #successBannerRect = successBanner.get_rect()
                                    #successBannerRect = pygame.Rect(WINDOWWIDTH/3, WINDOWHEIGHT/2, successBannerRect[2],successBannerRect[3])
                                    #DISPLAYSURF.blit(successBanner, successBannerRect)
                                    chargeAction = True
                                    #time.sleep(3)
                                    return jail, chargeAction
                                elif destiny < .7:
                                    print("HEADLINE: Cops catch criminal in the act")
                                    pieces[x][y].remove(piece)
                                    jail[players.index(player)] += 1
                                    drawBoard(board, pieces)
                                    MAINCLOCK.tick(FPS)
                                    pygame.display.update()
                                    #successBanner = BIGFONT.render("Cops catch " +str(player) + "robbing a " + str(board[x][y]), True, WHITE, BLACK)
                                    #successBannerRect = successBanner.get_rect()
                                    #successBannerRect = pygame.Rect(WINDOWWIDTH/3, WINDOWHEIGHT/2, successBannerRect[2],successBannerRect[3])
                                    #DISPLAYSURF.blit(successBanner, successBannerRect)
                                    #time.sleep(3)
                                    chargeAction = True
                                    return jail, chargeAction
                            elif copFlag == False:
                                
                                if board[x][y] == SPEAK_EASY and piece.player == player:
                                    player_bank[players.index(player)] += 4

                                elif board[x][y] == LOAN_SHARK and piece.player == player:

                                    player_bank[players.index(player)] += 3
                            
                                elif board[x][y] == PAWN_SHOP and piece.player == player:
                                    player_bank[players.index(player)] += 2

                                elif board[x][y] == MOM_POP and piece.player == player:
                                    player_bank[players.index(player)] += 1

                                elif board[x][y] == BANK and piece.player == player:
                                    player_bank[players.index(player)] += 8

                                elif board[x][y] ==FINANCIAL_DISTRICT and piece.player == player:
                                    player_bank[players.index(player)] += 7

                                elif board[x][y] == DISTILLERY and piece.player == player:
                                    player_bank[players.index(player)] += 6

                                elif board[x][y] == RACE_TRACK and piece.player == player:
                                    player_bank[players.index(player)] += 5
                                #successBanner = BIGFONT.render(str(player) + "robbed a " + str(board[x][y]), True, WHITE, BLACK)
                                #successBannerRect = successBanner.get_rect()
                                #successBannerRect = pygame.Rect(WINDOWWIDTH/3, WINDOWHEIGHT/2, successBannerRect[2],successBannerRect[3])
                                #DISPLAYSURF.blit(successBanner, successBannerRect)
                                #time.sleep(3)
                                chargeAction = True
                                return jail, chargeAction

                        else:
                            drawBoard(board, pieces)
                            pieceWarningRect = pygame.Rect(mousex, mousey, pieceWarningRect[2],pieceWarningRect[3])
                            DISPLAYSURF.blit(pieceWarning, pieceWarningRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()
        except TypeError:
            continue

    if copFlag == True:
        if destiny >= .7:
            for piece in pieces[x][y]:
                if board[x][y] == SPEAK_EASY and piece.player == player:
                    player_bank[players.index(player)] += 4

                elif board[x][y] == LOAN_SHARK and piece.player == player:

                    player_bank[players.index(player)] += 3
            
                elif board[x][y] == PAWN_SHOP and piece.player == player:
                    player_bank[players.index(player)] += 2

                elif board[x][y] == MOM_POP and piece.player == player:
                    player_bank[players.index(player)] += 1

                elif board[x][y] == BANK and piece.player == player:
                    player_bank[players.index(player)] += 8

                elif board[x][y] ==FINANCIAL_DISTRICT and piece.player == player:
                    player_bank[players.index(player)] += 7

                elif board[x][y] == DISTILLERY and piece.player == player:
                    player_bank[players.index(player)] += 6

                elif board[x][y] == RACE_TRACK and piece.player == player:
                    player_bank[players.index(player)] += 5
                chargeAction = True
                print("Successful job")
                return jail, chargeAction
        elif destiny < .7:
            print("HEADLINE: Cops catch criminal in the act")
            for piece in pieces[x][y]:
                if piece.player == player:
                    pieces[x][y].remove(piece)
                    jail[players.index(player)] += 1
                    drawBoard(board, pieces)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()
                    chargeAction = True
                    return jail, chargeAction

    if copFlag == False:
        for piece in pieces[x][y]:
            print("successfull job")
            if board[x][y] == SPEAK_EASY and piece.player == player:
                player_bank[players.index(player)] += 4

            elif board[x][y] == LOAN_SHARK and piece.player == player:

                player_bank[players.index(player)] += 3
        
            elif board[x][y] == PAWN_SHOP and piece.player == player:
                player_bank[players.index(player)] += 2

            elif board[x][y] == MOM_POP and piece.player == player:
                player_bank[players.index(player)] += 1

            elif board[x][y] == BANK and piece.player == player:
                player_bank[players.index(player)] += 8

            elif board[x][y] ==FINANCIAL_DISTRICT and piece.player == player:
                player_bank[players.index(player)] += 7

            elif board[x][y] == DISTILLERY and piece.player == player:
                player_bank[players.index(player)] += 6

            elif board[x][y] == RACE_TRACK and piece.player == player:
                player_bank[players.index(player)] += 5
            chargeAction = True
            return jail, chargeAction

def bail(turn,pieces):
    rat1 = madeMan(BLACK,players[0])
    rat1.rat = True
    rat2 = madeMan(BRIGHTBLUE,players[1])
    rat2.rat = True
    #rat3 = madeMan(BLACK,players[2])
    #rat3.rat = True
    #rat4 = madeMan(BLACK,players[3])
    #rat4.rat = True
    destiny = random.random()
    if destiny <.5:
        if turn == "player1":
            pieces[0][0].append(rat1)
        elif turn == "player2":
            pieces[4][0].append(rat2)
        #elif turn == "player3":
            #pieces[0][4].append(rat3)
        #elif turn == "player4":
            #pieces[4][4].append(rat4)
    elif destiny >=.5:
        if turn == "player1":
            pieces[0][0].append(player11)
        elif turn == "player2":
            pieces[4][0].append(player21)
       #elif turn == "player3":
            #pieces[0][4].append(player31)
        #elif turn == "player4":
            #pieces[4][4].append(player41)
    






def copMove(board,pieces):
    
    delta_x = 200
    delta_y = 200
    copcount = 0

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            for piece in pieces[x][y]:
                if (piece.player == "cop" or piece.player == "journalist") and copcount <= 2:
                    try:
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
                    except (ValueError, IndexError) as error:
                        pieces[x][y]
                        print(error)
                        break
                #Traceback (most recent call last):
  #File "GangCity.py", line 1903, in <module>
    #main()
  #File "GangCity.py", line 173, in main
    #if runGame() == False:
  #File "GangCity.py", line 388, in runGame
    #copMove(mainBoard,pieces)
 # File "GangCity.py", line 1787, in copMove
    #pieces[x][y].remove(piece)
#ValueError: list.remove(x): x not in list

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
    if total_j <= 20:
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
