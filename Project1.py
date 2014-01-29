import pygame, sys, random

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

    character = raw_input("Which character would you like to play? Girl? Boy?")
    board.setCharacter(screen)
    
    main_loop(screen, board)

def main_loop(screen, board):    
    
    background = pygame.Surface(screen.get_size())
    background.fill(white)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    
    difficulty = raw_input("Would you like to play on easy? medium? hard?")
    
    board.theHero.draw(screen)
    pygame.display.flip()
    
    items = board.items

    s = 0

    while True:
        #Erase previous images
        screen.blit(background, (0, 0))

        #Draw the items
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        board.makeItems()
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

        
        self.person = Person(self, self.width/2, self.height-personSize, 50)
        self.theHero = pygame.sprite.RenderPlain()
        self.theHero.add(self.person)

    def makeItems(self):
            i = Item(random.choice(types), random.randint(0, self.size[0] - 20), 5)
            self.items.add(i)

    def setCharacter(self, screen):
        #Set the image of the self.person...
        print "setting character"
        #self.person.image = pygame.image.load("50x50guy.jpg").convert_alpha()

        background = pygame.Surface(screen.get_size())
        background.fill(white)
        screen.blit(background, (0, 0))
        
        self.Choices = pygame.sprite.RenderPlain()
        girl = Person(self, self.width/3, self.height/2, 50)
        girl.image =  pygame.image.load("girlCharacter.png").convert()
        boy = Person(self, 2*self.width/3, self.height/2, 50)
        self.Choices.add(girl, boy)
        boy.image = pygame.image.load("50x50guy.jpg").convert_alpha()

        self.Choices.draw(screen)

        pygame.display.flip()
        
class Item(pygame.sprite.Sprite):
    def __init__(self, color, x, speed):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        
        self.color = color    #green is good, red is bad
        self.x = x
        self.speed = speed
        self.pos = self.image.get_rect().move(x, 0)

    def move(self):
        self.pos = self.pos.move(0, self.speed)
        if self.pos.top <= 400:
            return False

class Person (pygame.sprite.Sprite):
    def __init__(self, board, col, row, size):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.board = board
        #this needs to be changed
        self.rect = pygame.Rect(col, row, size, size)        
        self.image = pygame.image.load("girlCharacter.png").convert()


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
