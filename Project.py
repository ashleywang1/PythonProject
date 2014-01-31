import pygame, sys, random, inputbox

##TODO
"""
5) main menu - set difficulty / screen size / keep a high score sheet
8) SOUND ANIMATION
"""

#Color wheel initialization
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue  = (0, 0, 255)

#Sound clip initialization
pygame.mixer.init()
good_sd = pygame.mixer.Sound("good.wav")
bad_sd = pygame.mixer.Sound("bad.wav")

#Game constants initialization
personSize = 50
PERSON_SIZE = 50

def new_game(size):

    #Start up the display
    pygame.init()
    window_size = [size, size]
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Keep on Swimming")

    #Initialize the board
    board = Board(screen.get_size())

    #main menu
    startScreen = Board(screen.get_size())
    settings = main_menu(screen, startScreen)
    #the game
    main_loop(screen, board, settings)
    

def main_menu(screen, startScreen):
    board = startScreen

    #Draw a white background
    background = pygame.Surface(screen.get_size())
    background.fill(white)
    screen.blit(background, (0, 0))

    #Initialize the settings
    settings = []

    """The first setting - what kind of character to play"""

    #draw the menu
    board.Choices.draw(screen)
    font = pygame.font.Font(None, 30)
    ask = font.render("Click the character you would like to play!", True, blue)
    askRect = ask.get_rect()
    askRect.centerx = screen.get_size()[0]/2
    askRect.centery = screen.get_size()[0]/3
    screen.blit(ask, askRect)
    
    pygame.display.flip()

    #Set up the choices
    choices = [board.seal, board.shark, board.penguin]
    areas = [(chara.rect.x, chara.rect.y) for chara in choices]

    #Wait for user input
    while True:
        event = pygame.event.wait()
        size = screen.get_size()
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            click = pygame.mouse.get_pos()

            for i in range (len(choices)):
                #check x
                if click[0] > areas[i][0] and click[0] < areas[i][0]+50:
                    #check y
                    if click[1] > areas[i][1] and click[1] < areas[i][1] + 50:
                        settings.append( choices[i] )
                        
                    else:
                        continue
                else:
                    continue
            
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONUP and len(settings) > 0:
                break
            else:
                continue

    """The second setting - what difficulty to begin with"""

    #Draw the menu
    background.fill(white)
    screen.blit(background, (0, 0))
    lvl = []

    #List the choices
    font = pygame.font.Font(None, 40)
    difficulty = font.render("Difficulty?", True, black)
    easy = font.render("Easy", True, blue)
    medium = font.render("Medium", True, blue)
    hard = font.render("Hard", True, blue)
    extreme = font.render("Extreme", True, blue)
    choices = [difficulty, easy, medium, hard, extreme]

    #Wait for user input
    for i in range(len(choices)):
        text = choices[i]
        textRect = text.get_rect()
        textRect.centerx = screen.get_size()[0]/2
        textRect.centery = i*screen.get_size()[0]/len(choices) + 50
        lvl.append(textRect.centery)
        screen.blit(text, textRect)
    pygame.display.flip()
    
    while True:
        event = pygame.event.wait()
        size = screen.get_size()
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            click = pygame.mouse.get_pos()

            for i in range (len(choices)):
                #check x
                if click[1] > lvl[i]-10 and click[1] < lvl[i]+10:
                    settings.append(i * 5 + 1)
                else:
                    continue
                
            print click
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONUP and len(settings) > 1:
                break
            else:
                continue

    
    return settings

def update_text(screen, message1, message2, message3):
    font = pygame.font.Font(None, 20)
    text1 = font.render(message1, True, black)
    textRect1 = text1.get_rect()
    textRect1.x = 10
    textRect1.y = 5
    screen.blit(text1, textRect1)

    text2 = font.render(message2, True, black)
    textRect2 = text2.get_rect()
    textRect2.x = screen.get_size()[0] - 80
    textRect2.y = 5
    screen.blit(text2, textRect2)

    text3 = font.render(message3, True, black)
    textRect3 = text3.get_rect()
    textRect3.centerx = screen.get_size()[0] / 2
    textRect3.centery = 10
    screen.blit(text3, textRect3)

    text4 = font.render("P to pause", True, black)
    textRect4 = text4.get_rect()
    textRect4.centerx = screen.get_size()[0] / 2
    textRect4.centery = 35
    screen.blit(text4, textRect4)

def level_up(screen, level):
    font = pygame.font.Font(None, 60)
    text = font.render("Level up!", True, blue)
    textRect = text.get_rect()
    textX = screen.get_size()[0] / 2
    textY = screen.get_size()[1] / 2
    textRect.centerx = textX
    textRect.centery = textY
    screen.blit(text, textRect)

def game_over(screen):
    font = pygame.font.Font(None, 90)
    text = font.render("GAME OVER", True, red)
    textX = screen.get_size()[0] / 2
    textY = screen.get_size()[1] / 2
    textRect = text.get_rect()
    textRect.centerx = textX
    textRect.centery = textY
    screen.blit(text, textRect)

    font2 = pygame.font.Font(None, 40)
    text2 = font2.render("New game?", True, black)
    textX2 = screen.get_size()[0] / 2
    textY2 = screen.get_size()[1] / 2 + 80
    textRect2 = text2.get_rect()
    textRect2.centerx = textX2
    textRect2.centery = textY2
    screen.blit(text2, textRect2)

    return textRect2


def update_high_score(points):
    
    name = inputbox.main()
    print name
    high_scores = open("highscores.txt", "a")
    high_scores.write(name)
    high_scores.write(" : ")
    high_scores.write(str (points ))
    high_scores.write(" \n")
    high_scores.close()

def main_loop(screen, board, settings):
    #Initialize background
    background = pygame.Surface(screen.get_size())
    background.fill(white)
    background = pygame.image.load("ocean.png").convert()
    screen.blit(background, (0, 0))

    #Peronalize board based on user inputs from startScreen
    board.personalize(settings)

    #Draw the hero and initialize his level
    board.theHero.draw(screen)
    lvl = board.person.level
    update_text(screen, "Points: " + str(board.person.points), "Lives: " + str(board.person.lives), "Level " + str(lvl))
    pygame.display.flip()

    #Initialize the item drops on the board
    items = board.items
    n = 0
    s = 0
    prevpts = 0
    currpts = 0

    #Initialize the game progress booleans
    stop = False
    pause = False

    while stop == False:
        while board.person.lives > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if pause == True:
                            pause = False
                        else:
                            pause = True
            if pause == False:
                #Erase previous images
                screen.blit(background, (0, 0))

                #Draw the items
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                
                board.checkHits()
                if s % 3 == 0:
                    board.makeItems(lvl)
                for i in items:
                    screen.blit(background, i.pos, i.pos)
                for i in items:
                    i.move()
                    screen.blit(i.image, i.pos)


                #Draw the person
                board.theHero.draw(screen)

                #Sense mouse position
                mouse = pygame.mouse.get_pos()
                x = mouse[0]
                y = mouse[1]

                hero = board.person
                heroPosition = hero.rect

                if x > heroPosition.x+25:
                    #"person moving to the right"
                    hero.move_right(x, board.width)
            
                elif x < heroPosition.x+25:
                    #board.person.move_left(x)
                    hero.move_left(x, board.width)
                else:
                    print "person stopped"
           
                update_text(screen, "Points: " + str(board.person.points), "Lives: " + str(board.person.lives), "Level " + str(lvl))
                currpts = board.person.points
                if currpts - prevpts > 9:
                    prevpts = currpts
                    board.person.level += 1
                    lvl += 1
                    n += 1
                if n % 4 != 0:
                    level_up(screen, lvl)
                    n += 1
                pygame.display.flip()
                pygame.display.update()
                pygame.display.flip()
                pygame.time.delay(100)
                s += 1

        restart = game_over(screen)
        pygame.display.flip()
        
        stop = False
        while not stop:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                stop = True
                update_high_score(board.person.points)
                pygame.quit()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pos()
                if click[0] > restart.x and click[0] < restart.x + 100:
                    if click[1] > restart.y and click[1] < restart.y + 40:
                        new_game(screen.get_size()[0])
    

class Board:
    def __init__(self, size):

        self.size = size
        self.width = size[0]
        self.height = size[1]

        self.items = pygame.sprite.RenderPlain()

        #Right and left
        self.left = pygame.image.load("shark_left.png").convert()
        self.right = pygame.image.load("shark_right.png").convert()

        #The choices
        self.Choices = pygame.sprite.RenderPlain()
        
        self.seal = Person(self, self.width/4-20, 2*self.height/3, 50)
        self.seal.left = pygame.image.load("seal_left.png").convert()
        self.seal.right = pygame.image.load("seal_right.png").convert()
        self.seal.image = self.seal.right
        
        self.shark = Person(self, 2*self.width/4-20, 2*self.height/3, 50)
        self.shark.left = pygame.image.load("shark_left.png").convert()
        self.shark.right = pygame.image.load("shark_right.png").convert()
        self.shark.image = self.shark.right

        self.penguin = Person(self, 3*self.width/4-20, 2*self.height/3, 50)
        self.penguin.image = pygame.image.load("penguin.jpg").convert()
        self.penguin.right = self.penguin.image
        self.penguin.left = self.penguin.image
        
        self.Choices.add(self.seal, self.shark, self.penguin)
        
        
        #The player
        self.person = Person(self, self.width/2, self.height-personSize, personSize)
        self.theHero = pygame.sprite.RenderPlain()
        self.theHero.add(self.person)

    def makeItems(self, level):
            t = "good"
            r = random.random()
            cutoff = 0.04 * level + 0.04
            if r < cutoff:
                if r > cutoff * level / (level + 1):
                    t = "bad"
                else:
                    t = "kill"
            i = Item(t, random.randint(0, self.size[0] - 32), random.randint(0 + level, 6 + level))
            self.items.add(i)
            if self.person.lives < 3:
                if random.random() < 0.05:
                    i = Item("better", random.randint(0, self.size[0] - 32), random.randint(0 + level, 6 + level))
                    self.items.add(i)

    def checkHits(self):
        hits = pygame.sprite.spritecollide(self.person, self.items, True)
        pts = 0
        lives = 0
        for i in hits:
            if i.category == "good":
                pts += 1
                good_sd.play()
            elif i.category == "better":
                lives += 1
            elif i.category == "bad":
                pts -= 1
                bad_sd.play(1)
            else:
                lives -= 1
        self.person.change_points(pts)
        self.person.change_lives(lives)

    def personalize(self, settings):
        #The first index of settings is the animal character
        character = settings[0]
        lvl = settings[1]

        self.person.image = character.image
        self.person.image.set_colorkey(white)
        self.person.level = lvl

        self.left = character.left
        self.right = character.right

class Item(pygame.sprite.Sprite):
    def __init__(self, category, x, speed):
        pygame.sprite.Sprite.__init__(self)
        
        self.category = category
        self.set_pic()
        self.x = x
        self.speed = speed
        self.pos = self.image.get_rect().move(x, 0)
        self.rect = self.pos

    def move(self):
        self.pos = self.pos.move(0, self.speed)
        self.rect = self.pos

    def set_pic(self):
        if self.category == "good":
            if random.random() < 0.5:
                self.image = pygame.image.load("orangefish.png").convert()
            else:
                self.image = pygame.image.load("greenfish.png").convert()
        elif self.category == "better":
            self.image = pygame.image.load("bubble.png").convert()
        elif self.category == "bad":
            self.image = pygame.image.load("plastic.png").convert()
        else:
            self.image = pygame.image.load("net.png").convert()
        self.image.set_colorkey(white)

class Person (pygame.sprite.Sprite):
    def __init__(self, board, col, row, size):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.board = board
        self.rect = pygame.Rect(col, row, size, size)
        
        self.points = 0
        self.lives = 5

        self.image = pygame.image.load("40x40girl.jpg").convert()
        self.right = board.right
        self.left = board.left


    def move_right(self, destination, size):
        """Move the person to the right"""
        WIDTH = 50
        HEIGHT = 50
        if destination > WIDTH*size-WIDTH/2:
            velocity =0
        else:
            velocity = (destination - self.rect.x-WIDTH/2)/3
            
        x = self.rect.x + velocity
        y = self.rect.y
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)

        self.image = self.board.right
        
    def move_left(self, destination, size):
        """Move the person to the right"""
        WIDTH = 50
        HEIGHT = 50
        if destination < WIDTH/2:
            velocity = 0
        else:
            velocity = (self.rect.x+WIDTH/2 - destination)/3
        x = self.rect.x - velocity
        y = self.rect.y
        self.rect = pygame.Rect(x, y, 50, 50)

        self.image = self.board.left

    def change_points(self, pts):
        self.points += pts

    def change_lives(self, lives):
        self.lives += lives


if __name__ == "__main__":
    new_game(500)
