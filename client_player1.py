import socket
import threading

direction = 'none'
direction2 = 'none'

def start(s):
    import pygame
    import sys
    import random
    import time

    # check for initializing errors
    check_errors = pygame.init()  # (success, errors)
    if check_errors[1] > 0:  # if there are errors more than 0
        print("Had {0} errors".format(check_errors[1]))
        sys.exit(-1)  # give out error code
    else:
        print("Successfully initialized")

    # Play surface
    playSurface = pygame.display.set_mode((720, 460))
    pygame.display.set_caption('Snake game! Player1')

    # colors
    red = pygame.Color(255, 0, 0)  # gameover
    green = pygame.Color(0, 255, 0)  # snake1
    blue = pygame.Color(30, 144, 255)  # snake2
    black = pygame.Color(0, 0, 0)  # score
    white = pygame.Color(255, 255, 255)  # background
    brown = pygame.Color(165, 42, 42)  # food

    # FPS controller
    fpsController = pygame.time.Clock()

    # important varibles
    snakePos = [100, 50]  # snake1 position
    snakePos2 = [100, 80]
    snakeBody = [[100, 50], [90, 50], [80, 50], [70, 50], [60, 50], [50, 50]]
    snakeBody2 = [[100, 80], [90, 80], [80, 80], [70, 80], [60, 80], [50, 80]]

    foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]  # food position
    s.send(str.encode('x:'+str(foodPos[0])))
    time.sleep(0.1)
    s.send(str.encode('y:' + str(foodPos[1])))
    time.sleep(0.1)
    s.send(str.encode('start'))
    foodSpawn = True


    global direction
    global direction2
    changeTo = direction


    score = 0
    score2 = 0

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

        pygame.quit()  # pygame exit
        sys.exit()  # console exit

    # show score
    def showScore(choice=1):
        scoreFont = pygame.font.SysFont('monaco', 24)
        Ssurf = scoreFont.render('Player1 Score : {0}     Player2 Score : {1}'.format(score, score2), True, black)
        Srect = Ssurf.get_rect()
        if choice == 1:
            Srect.midtop = (200, 10)
        else:
            Srect.midtop = (360, 120)
        playSurface.blit(Ssurf, Srect)

    # main logic of the game
    while True:
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                pygame.quit()  # pygame exit
                sys.exit()  # console exit

            # keydown
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    changeTo = 'RIGHT'
                    s.send(str.encode(changeTo))
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    changeTo = 'LEFT'
                    s.send(str.encode(changeTo))
                if event.key == pygame.K_UP or event.key == ord('w'):
                    changeTo = 'UP'
                    s.send(str.encode(changeTo))
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    changeTo = 'DOWN'
                    s.send(str.encode(changeTo))
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

        # update snake position [x, y]
        if direction == 'RIGHT':
            snakePos[0] += 10
        if direction == 'LEFT':
            snakePos[0] -= 10
        if direction == 'UP':
            snakePos[1] -= 10
        if direction == 'DOWN':
            snakePos[1] += 10

        if direction2 == 'RIGHT':
            snakePos2[0] += 10
        if direction2 == 'LEFT':
            snakePos2[0] -= 10
        if direction2 == 'UP':
            snakePos2[1] -= 10
        if direction2 == 'DOWN':
            snakePos2[1] += 10

        # snake body mechanism
        snakeBody.insert(0, list(snakePos))
        if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
            score += 1
            time.sleep(0.3)
            foodSpawn = False
        else:
            snakeBody.pop()

        snakeBody2.insert(0, list(snakePos2))
        if snakePos2[0] == foodPos[0] and snakePos2[1] == foodPos[1]:
            score2 += 1
            time.sleep(0.3)
            foodSpawn = False
        else:
            snakeBody2.pop()

        # food spawn
        if foodSpawn == False:
            foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
            s.send(str.encode('x:' + str(foodPos[0])))
            time.sleep(0.1)
            s.send(str.encode('y:' + str(foodPos[1])))
        foodSpawn = True

        # background
        playSurface.fill(white)

        # draw snake
        for pos in snakeBody:
            snakeRect = pygame.Rect(pos[0], pos[1], 10, 10)
            pygame.draw.rect(playSurface, green, snakeRect)

        for pos2 in snakeBody2:
            snakeRect = pygame.Rect(pos2[0], pos2[1], 10, 10)
            pygame.draw.rect(playSurface, blue, snakeRect)

        # draw food
        foodRect = pygame.Rect(foodPos[0], foodPos[1], 10, 10)
        pygame.draw.rect(playSurface, brown, foodRect)

        # boundaries
        if snakePos[0] > 710 or snakePos[0] < 0:
            gameOver()
        if snakePos[1] > 450 or snakePos[1] < 0:
            gameOver()

        if snakePos2[0] > 710 or snakePos2[0] < 0:
            gameOver()
        if snakePos2[1] > 450 or snakePos2[1] < 0:
            gameOver()

        # self hit
        if direction != 'none':
            for block in snakeBody[1:]:
                if snakePos[0] == block[0] and snakePos[1] == block[1]:
                    gameOver()

        if direction2 != 'none':
            for block2 in snakeBody2[1:]:
                if snakePos2[0] == block2[0] and snakePos2[1] == block2[1]:
                    gameOver()

        # update frame
        showScore()
        pygame.display.flip()
        fpsController.tick(15)

def recv_message(clientsocket):
    global direction2

    while True:
        try:
            message = clientsocket.recv(1024)
            # if message.decode('utf-8') == 'brian: start':
                # start()
                # threading.Thread(target=start).start()

            if message.decode('utf-8') == 'andrew: RIGHT':
                direction2 = 'RIGHT'

            if message.decode('utf-8') == 'andrew: LEFT':
                direction2 = 'LEFT'

            if message.decode('utf-8') == 'andrew: UP':
                direction2 = 'UP'

            if message.decode('utf-8') == 'andrew: DOWN':
                direction2 = 'DOWN'

        except:
            break

        if message == b'':
            break

        print()
        print(message.decode('utf-8'))
    print('連線中斷')


def main():
    nickname = input('請輸入您的暱稱：')

    # ready = input('輸入ready')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 23012))

    s.send(str.encode(nickname))

    # threading.Thread(target=start).start()
    threading.Thread(target=recv_message, args=(s,)).start()
    # begin = input('輸入start')
    # if begin == 'start':
        # s.send(str.encode(begin))
        # start(s)
        # s.send(str.encode(begin))
    start(s)

    recv_message(s)


    # while True:
    #     message = input()
    #
    #     if message == 'quit':
    #         break
    #     s.send(str.encode(message))
    #
    # s.shutdown(socket.SHUT_RDWR)
    # s.close()






    # if message.decode('utf-8') == 'brian: start':
    #     import pygame
    #     import sys
    #     import random
    #     import time
    #
    #     # check for initializing errors
    #     check_errors = pygame.init()  # (success, errors)
    #     if check_errors[1] > 0:  # if there are errors more than 0
    #         print("Had {0} errors".format(check_errors[1]))
    #         sys.exit(-1)  # give out error code
    #     else:
    #         print("Successfully initialized")
    #
    #     # Play surface
    #     playSurface = pygame.display.set_mode((720, 460))
    #     pygame.display.set_caption('Snake game!')
    #
    #     # colors
    #     red = pygame.Color(255, 0, 0)  # gameover
    #     green = pygame.Color(0, 255, 0)  # snake
    #     black = pygame.Color(0, 0, 0)  # score
    #     white = pygame.Color(255, 255, 255)  # background
    #     brown = pygame.Color(165, 42, 42)  # food
    #
    #     # FPS controller
    #     fpsController = pygame.time.Clock()
    #
    #     # important varibles
    #     snakePos = [100, 50]  # snake position
    #     snakeBody = [[100, 50], [90, 50], [80, 50], [70, 50], [60, 50], [50, 50]]
    #
    #     foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]  # food position
    #     foodSpawn = True
    #
    #     direction = 'RIGHT'
    #     changeTo = direction
    #
    #     score = 0
    #
    #     # game over function
    #     def gameOver():
    #         myFont = pygame.font.SysFont('monaco', 72)
    #         GOsurf = myFont.render('Gameover', True, red)
    #         GOrect = GOsurf.get_rect()
    #         GOrect.midtop = (360, 15)
    #         playSurface.blit(GOsurf, GOrect)
    #         showScore(0)
    #         pygame.display.flip()
    #
    #         # time.sleep(4)
    #         pygame.time.set_timer(pygame.USEREVENT, 4000)
    #         should_quit = False
    #         while not should_quit:
    #             for event in pygame.event.get():
    #                 if event.type == pygame.USEREVENT:
    #                     should_quit = True
    #
    #         pygame.quit()  # pygame exit
    #         sys.exit()  # console exit
    #
    #     # show score
    #     def showScore(choice=1):
    #         scoreFont = pygame.font.SysFont('monaco', 24)
    #         Ssurf = scoreFont.render('Score : {0}'.format(score), True, black)
    #         Srect = Ssurf.get_rect()
    #         if choice == 1:
    #             Srect.midtop = (80, 10)
    #         else:
    #             Srect.midtop = (360, 120)
    #         playSurface.blit(Ssurf, Srect)
    #
    #     # main logic of the game
    #     while True:
    #         for event in pygame.event.get():
    #             # quit
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()  # pygame exit
    #                 sys.exit()  # console exit
    #
    #             # keydown
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_RIGHT or event.key == ord('d'):
    #                     changeTo = 'RIGHT'
    #                 if event.key == pygame.K_LEFT or event.key == ord('a'):
    #                     changeTo = 'LEFT'
    #                 if event.key == pygame.K_UP or event.key == ord('w'):
    #                     changeTo = 'UP'
    #                 if event.key == pygame.K_DOWN or event.key == ord('s'):
    #                     changeTo = 'DOWN'
    #                 if event.key == pygame.K_ESCAPE:
    #                     pygame.event.post(pygame.event.Event(pygame.QUIT))
    #
    #         # validation of direction
    #         if changeTo == 'RIGHT' and not direction == 'LEFT':
    #             direction = 'RIGHT'
    #         if changeTo == 'LEFT' and not direction == 'RIGHT':
    #             direction = 'LEFT'
    #         if changeTo == 'UP' and not direction == 'DOWN':
    #             direction = 'UP'
    #         if changeTo == 'DOWN' and not direction == 'UP':
    #             direction = 'DOWN'
    #
    #         # update snake position [x, y]
    #         if direction == 'RIGHT':
    #             snakePos[0] += 10
    #         if direction == 'LEFT':
    #             snakePos[0] -= 10
    #         if direction == 'UP':
    #             snakePos[1] -= 10
    #         if direction == 'DOWN':
    #             snakePos[1] += 10
    #
    #         # snake body mechanism
    #         snakeBody.insert(0, list(snakePos))
    #         if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
    #             score += 1
    #             foodSpawn = False
    #         else:
    #             snakeBody.pop()
    #
    #         # food spawn
    #         if foodSpawn == False:
    #             foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    #         foodSpawn = True
    #
    #         # background
    #         playSurface.fill(white)
    #
    #         # draw snake
    #         for pos in snakeBody:
    #             snakeRect = pygame.Rect(pos[0], pos[1], 10, 10)
    #             pygame.draw.rect(playSurface, green, snakeRect)
    #
    #         # draw food
    #         foodRect = pygame.Rect(foodPos[0], foodPos[1], 10, 10)
    #         pygame.draw.rect(playSurface, brown, foodRect)
    #
    #         # boundaries
    #         if snakePos[0] > 710 or snakePos[0] < 0:
    #             gameOver()
    #         if snakePos[1] > 450 or snakePos[1] < 0:
    #             gameOver()
    #
    #         # self hit
    #         for block in snakeBody[1:]:
    #             if snakePos[0] == block[0] and snakePos[1] == block[1]:
    #                 gameOver()
    #
    #         # update frame
    #         showScore()
    #         pygame.display.flip()
    #         fpsController.tick(15)




if __name__ == '__main__':
    main()