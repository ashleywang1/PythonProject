import pygame, sys, random

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

types = [green, red]

def new_game(size):
    pygame.init()

    window_size = [size, size]
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Items")

    main_loop(screen)

def main_loop(screen):
    background = pygame.Surface(screen.get_size())
    background.fill(white)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    board = Board(screen.get_size())
    
    items = board.items

    s = 0

    while s < 80:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        board.makeItems()
        for i in items:
            screen.blit(background, i.pos, i.pos)
        for i in items:
            i.move()
            screen.blit(i.image, i.pos)

        pygame.display.update()
        pygame.time.delay(100)
        s += 1
    pygame.quit()

    

class Board:
    def __init__(self, size):

        self.size = size

        self.items = pygame.sprite.RenderPlain()

        """self.player = Player(self)
                          
        self.thePlayer = pygame.sprite.RenderPlain()
        self.thePlayer.add(self.player)"""

    def makeItems(self):
            i = Item(random.choice(types), random.randint(0, self.size[0] - 20), 5)
            self.items.add(i)
        

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

if __name__ == "__main__":
    new_game(400)

    pass
