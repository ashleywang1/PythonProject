import pygame, sys, random

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

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
    background = pygame.Surface(screen.get_size())
    background.fill(white)
    screen.blit(background, (0, 0))

    startScreen.Choices.draw(screen)
    
    pygame.display.flip()

    choice = None

    while True:
        event = pygame.event.wait()
        size = screen.get_size()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = pygame.mouse.get_pos()
            if click[0] > size[0]/2:
                #the guy was chosen
                choice = "guy"
            else:
                #the girl was chosen
                choice = "girl"
                
            print click
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONUP:
                break

    return choice
    
def main_loop(screen, board, settings):
    background = pygame.Surface(screen.get_size())
    background.fill(white)
    screen.blit(background, (0, 0))

    board.personalize(settings)
        
    
    board.theHero.draw(screen)
    pygame.display.flip()
    
    items = board.items

    s = 0

    while s < 180:
        #Erase previous images
        screen.blit(background, (0, 0))

        #Draw the items
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        board.checkHits()
        if s % 3 == 0:
            board.makeItems(5)
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
        
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(100)
        s += 1
    
    pygame.quit()

    

class Board:
    def __init__(self, size):

        self.size = size
        self.width = size[0]
        self.height = size[1]

        self.items = pygame.sprite.RenderPlain()

        #The choices
        self.Choices = pygame.sprite.RenderPlain()
        self.girl = Person(self, self.width/3, self.height/2, 50)
        self.girl.image =  pygame.image.load("girlCharacter.png").convert()
        self.boy = Person(self, 2*self.width/3, self.height/2, 50)
        self.boy.image = pygame.image.load("50x50guy.jpg").convert_alpha()
        self.Choices.add(self.girl, self.boy)
        
        #The player
        self.person = Person(self, self.width/2, self.height-personSize, personSize)
        self.theHero = pygame.sprite.RenderPlain()
        self.theHero.add(self.person)

    def makeItems(self, prob):
            t = green
            if random.randint(0, prob) == prob:
                t = red
            i = Item(t, random.randint(0, self.size[0] - 28), 5)
            self.items.add(i)

    def checkHits(self):
        pygame.sprite.groupcollide(self.items, self.theHero, True, False)

    def personalize(self, settings):
        if settings == "girl":
            self.person.image = self.girl.image
        elif settings == "guy":
            self.person.image = self.boy.image

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

class Person (pygame.sprite.Sprite):
    def __init__(self, board, col, row, size):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.board = board
        #this needs to be changed
        self.rect = pygame.Rect(col, row, size, size)
        print col, row
        
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

 

if __name__ == "__main__":
    new_game(400)

    pass
