import pygame, sys
import tests as T
from random import randrange

### Global Variables
WIDTH = 75  # this is the width of an individual square
HEIGHT = 75 # this is the height of an individual square

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

def get_row_top_loc(rowNum, height = HEIGHT):
    """
    Returns the location of the top pixel in a square in
    row rowNum, given the row height.
    """
    return rowNum*HEIGHT + 10

def get_col_left_loc(colNum, width = WIDTH):
    """
    Returns the location of the leftmost pixel in a square in
    column colNum, given the column width.
    """
    return colNum*WIDTH + 10

def update_text(screen, message, size = 10):
    """
    Used to display the text on the right-hand part of the screen.
    You don't need to code anything, but you may want to read and
    understand this part.
    """
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 0 + textSize
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.centerx = (size + 1) * WIDTH + 10
    textRect.centery = textY
    screen.blit(text, textRect)

def new_game(size = 10):
    """
    Sets up all necessary components to start a new game
    of Langton's Ant.
    """
    pygame.init() # initialize all imported pygame modules

    window_size = [size * WIDTH + 200, size * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    pygame.display.set_caption("Gravity") # caption sets title of Window 

    board = Board(size)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(screen, board, moveCount, clock, False, False)

def draw_grid(screen, size):
    """
    Draw the border grid on the screen.
    """
    horizontal = size*WIDTH + 2*size
    vertical = size*HEIGHT + 2*size
    pygame.draw.line(screen, blue, (0,0), (horizontal, 0), 20)
    pygame.draw.line(screen, blue, (0,0), (0, vertical), 20)
    pygame.draw.line(screen, blue, (horizontal,vertical), (0, vertical), 20)
    pygame.draw.line(screen, blue, (horizontal,vertical), (horizontal, 0), 20)
    for i in range(size):
        pygame.draw.line(screen, blue, (0,i*HEIGHT + 10), (horizontal, i*HEIGHT + 10), 1)
        pygame.draw.line(screen, blue, (i*WIDTH+10,0), (i*WIDTH+10, vertical), 1)
    
# Main program Loop: (called by new_game)
def main_loop(screen, board, moveCount, clock, stop, pause):
    #board.squares.draw(screen) # draw Sprites (Squares)    draw_grid(screen, board.size)
    #board.theAnt.draw(screen) # draw ant Sprite
    pygame.display.flip() # update screen
    
    if stop == True:
        again = raw_input("Would you like to run the simulation again? If yes, type 'yes'\n")
        if again == 'yes':
            new_game()
    while stop == False:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user clicks close
                stop = True
                pygame.quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if pause:
                        pause = False
                    else:
                        pause = True

        if stop == False and pause == False: 
            #game here

            board.squares.draw(screen)
            
            pygame.display.flip() # update screen
            clock.tick(5)
            
            moveCount += 1
            # ------------------------

    pygame.quit() # closes things, keeps idle from freezing




class Board:
    def __init__(self, size):

        self.size = size
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = []
        
        #---Populate boardSquares with Squares---#
        
        new = []
        for i in range (0, size):
            for j in range (0, size):
                s = Square(i, j, white)
                new.append(s)
                self.squares.add(s)
            self.boardSquares.append(new)
            new = []
        
        
    def get_square(self, x, y):
        """
        Given an (x, y) pair, return the Square at that location
        """
        return self.boardSquares[y][x]



class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect() # gets a rect object with width and height specified above
                                            # a rect is a pygame object for handling rectangles
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        self.color = white   

    def get_rect_from_square(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect

    def flip_color(self):
        """
        Flips the color of the square (white -> black or 
        black -> white)
        """
        a = self.color
        if a==black:
            self.color = white
            self.image.fill(self.color)
        elif a ==white:
            self.color = black
            self.image.fill(self.color)

new_game(3)
