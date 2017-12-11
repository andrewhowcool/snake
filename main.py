import pygame
import sys
import random
import time


# check for initializing errors
check_errors = pygame.init() # (success, errors)
if check_errors[1] > 0: # if there are errors more than 0
    print("Had {0} errors".format(check_errors[1]))
    sys.exit(-1) # give out error code
else:
    print("Successfully initialized")


# Play surface
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Snake game!')


# colors
red = pygame.Color(255, 0, 0) # gameover
green = pygame.Color(0, 255, 0) # snake
black = pygame.Color(0, 0, 0) # score
white = pygame.Color(255, 255, 255) # background
brown = pygame.Color(165, 42, 42) # food


# FPS controller
fpsController = pygame.time.Clock()


# important varibles
snakePos = [100, 50] # snake position
snakeBody = [[100, 50], [90, 50], [80, 50], [70, 50], [60, 50], [50, 50]]

foodPos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10] # food position
foodSpawn = True

direction = 'RIGHT'
changeTo = direction

score  = 0


# game over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Gameover', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360, 15)
    playSurface.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()

    # time.sleep(4)
    pygame.time.set_timer(pygame.USEREVENT, 4000)
    should_quit = False
    while not should_quit:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                should_quit = True

    pygame.quit() # pygame exit
    sys.exit() # console exit


# show score
def showScore(choice = 1):
    scoreFont = pygame.font.SysFont('monaco', 24)
    Ssurf = scoreFont.render('Score : {0}'.format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (360, 120)
    playSurface.blit(Ssurf, Srect)


# main logic of the game
while True:
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            pygame.quit() # pygame exit
            sys.exit() # console exit

        # keydown
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeTo = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeTo = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeTo = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeTo = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))


    # validation of direction
    if changeTo == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeTo == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeTo == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeTo == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'


    # update snake porition [x, y]
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10


    # snake body mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()


    # food spawn
    if foodSpawn == False:
        foodPos = [random.randrange(1, 72)*10, random.randrange(1, 46)*10]
    foodSpawn = True


    # background
    playSurface.fill(white)


    # draw snake
    for pos in snakeBody:
        snakeRect = pygame.Rect(pos[0], pos[1], 10, 10)
        pygame.draw.rect(playSurface, green, snakeRect)

    # draw food
    foodRect = pygame.Rect(foodPos[0], foodPos[1], 10, 10)
    pygame.draw.rect(playSurface, brown, foodRect)


    # boundaries
    if snakePos[0] > 710 or snakePos[0] < 0:
        gameOver()
    if snakePos[1] > 450 or snakePos[1] < 0:
        gameOver()

    # self hit
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()


    # update frame
    showScore()
    pygame.display.flip()
    fpsController.tick(15)
