import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import *

#global variables for the game 
FPS = 32 #frames per second, it means that they will create 32 frames per second if we would make them less then game is gonna feel slow and laggy
ScreenWidth = 289
ScreenHeight = 511
SCREEN = pygame.display.set_mode((ScreenWidth,ScreenHeight)) #creates a display screen made up of height and width
GROUNDY = ScreenHeight * 0.8   #height ka 0.8% dy rhy hain hum base wali image ko 
GAME_SPRITES = {}
GAME_SOUNDS = {}  
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
def welcomeScreen():
    #shows the welcome screen
    playerx = int(ScreenWidth)
    playery = int((ScreenHeight - GAME_SPRITES['PLAYER'].get_height())/2)
    messagex = int((ScreenWidth - GAME_SPRITES['message'].get_width())/2)
    messagey = int(ScreenHeight * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #for event in pygame.event.get(): --> this function actaully is all about if user press or takes anyof the action from the key borad 
            #if user press cross button [x] to close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.type==K_ESCAPE):
                #event.type==KEYDOWN it means any key has been pressed
                #event.type==K_ESCAPE it means the gam has to escape
                pygame.quit()
                sys.exit()
            #if the user press SPACE KEY or UPWARD KEY so game must start
            elif event.type == KEYDOWN or (event.type==K_SPACE or event.type==KEYUP ):
               return 
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['PLAYER'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS) #run the game till this much fps not more or less thn these
    pass
def mainGame():
    score = 0
    playerx = int(ScreenWidth/5)
    playery = int(ScreenHeight/2)
    basex = 0

    #create two pipes for blitting on the screen 
    newPipe1 = getrandomPipe()
    newPipe2 = getrandomPipe()

    #my list of upper pipe 
    upperPipes = [
        {'x': ScreenWidth+200, 'y':newPipe1[0]['y']},
        {'x': ScreenWidth+200+(ScreenWidth/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': ScreenWidth+200, 'y':newPipe1[1]['y']},
        {'x': ScreenWidth+200+(ScreenWidth/2), 'y':newPipe2[1]['y']},
    ]
    pipeVal = -4
    playerVely = -9 #falling velocity 
    playerValMaxy = 10 #maximum 
    playerValMiny = -8 #minimum
    playerAccy = 1 # 

    playerflapAcc = -8 #velocity while flapping
    playerFlapped = False #it is true only when the bird is flapping 

#GAME LOOOP
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit
                sys.exit
            if event.type == KEYDOWN and( K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerflapAcc
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        #check for collosion
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return
        
        #check for score
        playerMidPos = playerx + GAME_SPRITES['PLAYER'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score+=1
                print(f"your score is: {score}")
                GAME_SOUNDS['point'].play()

        if playerVely < playerValMaxy and not playerFlapped:
            playerVely  += playerAccy
        
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['PLAYER'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)       



#zip is used as:- > explained through example!
        #  a = [1,2,3]
        # >>> b = [4,5,6]
        # >>> d = zip(a,b)
        # >>> list(d) 
        # [(1, 4), (2, 5), (3, 6)]

    #move pipes to the left ----->
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVal
            lowerPipe['x'] += pipeVal

    #add a new pipe when the fisrt pipe is about to get out of the screen 
        if 0<upperPipes[0]['x']<5:
            newpipe = getrandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

    #if the pipe is going out of the screen remove it 
        if  upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0] .get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
    #blit sprites now 
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['PLAYER'], (playerx,playery))   
        myDigits = [int(x) for x in (str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['number'][digit].get_width()
        Xoffset = (ScreenWidth - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['number'][digit], (Xoffset, ScreenHeight*0.12))
            Xoffset += (GAME_SPRITES['number'][digit].get_width())
        pygame.display.update()
        FPSCLOCK.tick(FPS)
   
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['die'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['PLAYER'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getrandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = ScreenHeight/3
    y2 = offset + random.randrange(0, int(ScreenHeight - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = ScreenWidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

        
if __name__ == "__main__": #control starts from here 
    pygame.init() #initializing pygame modules 
    FPSCLOCK = pygame.time.Clock() #used for controlling FPS means k FPS iss say zada nai chalay ga 
    pygame.display.set_caption("Flappy Bird by Wajiha") 
    #creating tupples of images in dictionary of 'numbers'
    #purpose of convert alpha is only that it can render image in screen faster, means image is optimized for the game only 
    GAME_SPRITES['number'] = (      
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()      
    )      
    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/New Project (1).png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE)
    #pygame.image.transform.rotate function rotates the image nd 2nd argument of 180 rotates the image at angle of 180
    )

    #GAME SOUNDS
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    
    #GAME BACKGROUND 
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    #GAME_PALYER
    GAME_SPRITES['PLAYER'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        #keeps on showing until user does'nt press any key from keyboard
        mainGame() 
         #This is the main game function 