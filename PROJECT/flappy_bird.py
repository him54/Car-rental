import random #it generates random numbers
import sys # for exiting game
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables
FPS = 32
screenwidth = 289
screenheight = 511
screen = pygame.display.set_mode((screenwidth, screenheight))
GROUNDY = screenheight * 0.8
gameimages = {}
gamesound = {}
bird = 'gallery/images/bird.png'
background = 'gallery/images/background.png'
PIPE = 'gallery/images/pipe.png'

"""
   for welcome screen
"""
def welcomescreen():

    birdx = int(screenwidth/5)
    birdy = int((screenheight - gameimages['bird'].get_height())/2)
    messagex = int((screenwidth - gameimages['message'].get_width())/2)
    messagey = int(screenheight*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #close game if close or esc button pressed
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # start game if up or spacebar key pressed
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(gameimages['background'], (0, 0))    
                screen.blit(gameimages['bird'], (birdx, birdy))    
                screen.blit(gameimages['message'], (messagex,messagey ))    
                screen.blit(gameimages['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

#Main game started from here
def mainGame():
    score = 0
    birdx = int(screenwidth/5)
    birdy = int(screenwidth/2)
    basex = 0

    # Create 2 pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #List of upper pipes
    upperPipes = [
        {'x': screenwidth+200, 'y':newPipe1[0]['y']},
        {'x': screenwidth+200+(screenwidth/2), 'y':newPipe2[0]['y']},
    ]
    #List of lower pipes
    lowerPipes = [
        {'x': screenwidth+200, 'y':newPipe1[1]['y']},
        {'x': screenwidth+200+(screenwidth/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    birdVelY = -9
    birdMaxVelY = 10
    birdMinVelY = -8
    birdAccY = 1

    birdFlapAccv = -8 # velocity while flapping
    birdFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if birdy > 0:
                    birdVelY = birdFlapAccv
                    birdFlapped = True
                    gamesound['wing'].play()


        crashTest = isCollide(birdx, birdy, upperPipes, lowerPipes) # This function will return true if the bird is crashed
        if crashTest:
            return     

        #score Display
        birdMidPos = birdx + gameimages['bird'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + gameimages['pipe'][0].get_width()/2
            if pipeMidPos<= birdMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                gamesound['point'].play()


        if birdVelY <birdMaxVelY and not birdFlapped:
            birdVelY += birdAccY

        if birdFlapped:
            birdFlapped = False            
        birdHeight = gameimages['bird'].get_height()
        birdy = birdy + min(birdVelY, GROUNDY - birdy - birdHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -gameimages['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our images now
        screen.blit(gameimages['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(gameimages['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(gameimages['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(gameimages['base'], (basex, GROUNDY))
        screen.blit(gameimages['bird'], (birdx, birdy))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += gameimages['numbers'][digit].get_width()
        Xoffset = (screenwidth - width)/2

        for digit in myDigits:
            screen.blit(gameimages['numbers'][digit], (Xoffset, screenheight*0.12))
            Xoffset += gameimages['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(birdx, birdy, upperPipes, lowerPipes):
    if birdy> GROUNDY - 25  or birdy<0:
        gamesound['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = gameimages['pipe'][0].get_height()
        if(birdy < pipeHeight + pipe['y'] and abs(birdx - pipe['x']) < gameimages['pipe'][0].get_width()):
            gamesound['hit'].play()
            return True

    for pipe in lowerPipes:
        if (birdy + gameimages['bird'].get_height() > pipe['y']) and abs(birdx - pipe['x']) < gameimages['pipe'][0].get_width():
            gamesound['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = gameimages['pipe'][0].get_height()
    offset = screenheight/3
    y2 = offset + random.randrange(0, int(screenheight - gameimages['base'].get_height()  - 1.2 *offset))
    pipeX = screenwidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    gameimages['numbers'] = ( 
        pygame.image.load('gallery/images/0.png').convert_alpha(),
        pygame.image.load('gallery/images/1.png').convert_alpha(),
        pygame.image.load('gallery/images/2.png').convert_alpha(),
        pygame.image.load('gallery/images/3.png').convert_alpha(),
        pygame.image.load('gallery/images/4.png').convert_alpha(),
        pygame.image.load('gallery/images/5.png').convert_alpha(),
        pygame.image.load('gallery/images/6.png').convert_alpha(),
        pygame.image.load('gallery/images/7.png').convert_alpha(),
        pygame.image.load('gallery/images/8.png').convert_alpha(),
        pygame.image.load('gallery/images/9.png').convert_alpha(),
    )

    gameimages['message'] =pygame.image.load('gallery/images/mainscreen.png').convert_alpha()
    gameimages['base'] =pygame.image.load('gallery/images/base.png').convert_alpha()
    gameimages['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    gamesound['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    gamesound['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    gamesound['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    gamesound['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    gamesound['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    gameimages['background'] = pygame.image.load(background).convert()
    gameimages['bird'] = pygame.image.load(bird).convert_alpha()

    while True:
        welcomescreen() # Shows welcome screen to the user until he presses a button
        mainGame() # main game function 