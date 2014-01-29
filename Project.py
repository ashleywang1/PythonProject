import pygame, sys, random

##TODO
""" 1) get jungle/ocean backgrounds and have those as options - will the transparency still work?
2) get animal characters
3) bombs would become bad food for them
4) coins would become good food
5) main menu - set difficulty / screen size / keep a high score sheet
6) add levels of difficulty - making the items drop faster, more bad items
/ changing background
7) more animation for getting good and bad things
8) SOUND ANIMATION
9) not just bombs, instant death ones - also point decreasing ones
10) pause feature - maybe? nevermind"""


black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue  = (0, 0, 255)

types = [green, red]
personSize = 50

def new_game(size):
    pygame.init()

    window_size = [size, size]
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Items and Person")
    
    board = Board(screen.get_size())

    #main menu
    startScreen = Board(screen.get_size())
    settings = main_menu(screen, startScreen)
    #the game
    main_loop(screen, board, settings)
    

def main_menu(screen, startScreen):
    board = startScreen
    
    background = pygame.Surface(screen.get_size())
    background.fill(white)
    screen.blit(background, (0, 0))
    
    settings = []


    #Ask for the character the user wants

    #draw the menu
    board.Choices.draw(screen)
    pygame.display.flip()

    #Set up the choices
    choices = [board.girl, board.boy, board.lion, board.ghost]
    areas = [(chara.rect.x, chara.rect.y) for chara in choices]

    #Wait for user input
    while True:
        event = pygame.event.wait()
        size = screen.get_size()
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            click = pygame.mouse.get_pos()

            for i in range (len(choices)):
                #check x
                if click[0] > areas[i][0] and click[0] < areas[i][0]+50:
                    #check y
                    if click[1] > areas[i][1] and click[1] < areas[i][1] + 50:
                        settings.append( choices[i] )
                        print i
                    else:
                        continue
                else:
                    continue
                
            print click
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONUP and len(settings) > 0:
                break
            else:
                continue
            
    #Ask for the difficulty

    #List the choices
    font = pygame.font.Font(None, 50)
    easy = font.render("Easy", True, blue)
    medium = font.render("Medium", True, blue)
    hard = font.render("Hard", True, blue)
    extreme = font.render("Extreme", True, blue)
    choices = [easy, medium, hard, extreme]

    #Draw the menu
    background.fill(white)
    screen.blit(background, (0, 0))
    lvl = []
    
    for i in range(len(choices)):
        text = choices[i]
        textRect = text.get_rect()
        textRect.centerx = screen.get_size()[0]/2
        print textRect.centerx
        print "x"
        textRect.centery = i*screen.get_size()[0]/len(choices) + 50
        print textRect.centery
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
            if event.type == pygame.MOUSEBUTTONUP and len(settings) > 0:
                break
            else:
                continue

    print settings[0]
    print settings[1]
    
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

def level_up(screen, level):
    font = pygame.font.Font(None, 60)
    text = font.render("Level up!", True, blue)
    textRect = text.get_rect()
    textX = screen.get_size()[0] / 2
    textY = screen.get_size()[1] / 2
    textRect.centerx = textX
    textRect.centery = textY
    screen.blit(text, textRect)

def game_over(screen, message):
    textSize = 90
    font = pygame.font.Font(None, 90)
    text = font.render(message, True, red)
    textX = screen.get_size()[0] / 2
    textY = screen.get_size()[1] / 2
    textRect = text.get_rect()
    textRect.centerx = textX
    textRect.centery = textY
    screen.blit(text, textRect)
    
def main_loop(screen, board, settings):
    background = pygame.Surface(screen.get_size())
    background.fill(white)
    screen.blit(background, (0, 0))

    board.personalize(settings)
        
    
    board.theHero.draw(screen)
    lvl = board.person.level
    update_text(screen, "Coins: " + str(board.person.points), "Lives: " + str(board.person.lives), "Level " + str(lvl))
    pygame.display.flip()
    
    items = board.items

    s = 0
    prevpts = 0
    currpts = 0

    while board.person.lives > 0:
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
        
        update_text(screen, "Coins: " + str(board.person.points), "Lives: " + str(board.person.lives), "Level " + str(lvl))
        currpts = board.person.points
        if currpts - prevpts > 19:
            prevpts = currpts
            board.person.level += 1
            lvl += 1
            level_up(screen, lvl)
            pygame.display.flip()
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(100)
        s += 1

    game_over(screen, "GAME OVER")
    pygame.display.flip()
    pygame.time.delay(5000)
    pygame.quit()

    

class Board:
    def __init__(self, size):

        self.size = size
        self.width = size[0]
        self.height = size[1]

        self.items = pygame.sprite.RenderPlain()

        #The choices
        self.Choices = pygame.sprite.RenderPlain()
        self.girl = Person(self, self.width/4, self.height/3, 50)
        self.girl.image =  pygame.image.load("girlCharacter.png").convert_alpha()
        self.boy = Person(self, 2*self.width/4, self.height/3, 50)
        self.boy.image = pygame.image.load("50x50guy.jpg").convert()
        self.lion = Person(self, 3*self.width/4, self.height/3, 50)
        self.lion.image = pygame.image.load("lion.jpg").convert()
        self.ghost = Person(self, self.width/4, 2*self.height/3, 50)
        self.ghost.image = pygame.image.load("halloweenGhost.jpg").convert()
            
        self.Choices.add(self.girl, self.boy, self.lion, self.ghost)
        
        #The player
        self.person = Person(self, self.width/2, self.height-personSize, personSize)
        self.theHero = pygame.sprite.RenderPlain()
        self.theHero.add(self.person)

    def makeItems(self, level):
            t = green
            if random.random() < 0.05 * level + 0.05:
                t = red
            i = Item(t, random.randint(0, self.size[0] - 28), random.randint(0 + level, 6 + level))
            self.items.add(i)

    def checkHits(self):
        hits = pygame.sprite.spritecollide(self.person, self.items, True)
        pts = 0
        lives = 0
        for i in hits:
            if i.color == green:
                pts += 1
            else:
                lives +=1
        self.person.add_points(pts)
        self.person.remove_lives(lives)

    def personalize(self, settings):
        #The first index of settings is the animal character
        character = settings[0]
        lvl = settings[1]

        self.person.image = character.image
        self.person.image.set_colorkey(white)
        self.person.level = lvl

class Item(pygame.sprite.Sprite):
    def __init__(self, color, x, speed):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([28, 28])
        self.image.fill(color)
        
        self.color = color    #green is good, red is bad
        self.x = x
        self.speed = speed
        self.pos = self.image.get_rect().move(x, 0)
        self.rect = self.pos

        self.set_pic()

    def move(self):
        self.pos = self.pos.move(0, self.speed)
        self.rect = self.pos

    def set_pic(self):
        if self.color == green:
            self.image = pygame.image.load("goldcoin.png").convert()
            self.image.set_colorkey(black)
        else:
            self.image = pygame.image.load("bomb.png").convert()
            self.image.set_colorkey(white)

class Person (pygame.sprite.Sprite):
    def __init__(self, board, col, row, size):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.board = board
        #this needs to be changed
        self.rect = pygame.Rect(col, row, size, size)
        
        self.points = 0
        self.lives = 5

        self.image = pygame.image.load("40x40girl.jpg").convert()


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

    def add_points(self, pts):
        self.points += pts

    def remove_lives(self, lives):
        self.lives -= lives


if __name__ == "__main__":
    new_game(400)
