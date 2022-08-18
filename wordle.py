import enum
from struct import Struct
import pygame
import random

class wordle_game:
    """
    A class to play the game wordle


    Attributes
    ----------
    square_num, display_pixel_num, box_dim, spacing, word_row, margin : int
        variables that are associated with the spacing and dimensions of the game display
    enter_key_loc, backspace_key_loc : tuple
        location of the enter and backspace key
    letters : array of chars
        letters of the alphabet 
    box_font, key_font, enter_size, del_size : pygame.font
        various fonts used for the different buttons and display of the game
    LIGHT_GRAY, GREEN, YELLOW, DARK_GRAY : tuple
        RGB tuple values for the standard wordle color scheme
    keyboard : double list
    standard keyboard list

    Methods
    -------
    init_keyboard()
        Initialize the keyboard display (Color, key location, key display dimension)
    init_wordlist_matrix()
        Read a list of words and creates an array of words
    init_letter_locs()
        Create a list of locations (x, y) for display purposes
    add_letter(letter, location)
        Add letter to screen at the appropriate location
    update_display()
        Update the UI display, specifically the letters of the keyboard and wordle grid
    current_screen()
        Draw wordle grid and keyboard, specifically the boxes of the wordle display
    run()
        Main wordle game function where the game runs and game logic is implemented
    """
    
    pygame.font.init()
    square_num = 30
    display_pixel_num = 600
    box_dim = 50
    spacing = 6
    word_row = 0
    margin = int((550 - (50 * spacing + spacing * 4)) / 2)

    enter_key_loc = (0, 0)
    backspace_key_loc = (0, 0)

    letters = [chr(i) for i in range(65, 91)]

    box_font = pygame.font.SysFont('arial', 24)
    key_font = pygame.font.SysFont('Helvetica', 48)
    enter_size = pygame.font.SysFont('arial', 20)
    del_size = pygame.font.SysFont('arial', 20)

    LIGHT_GRAY = (134, 136, 138)
    GREEN = (77, 149, 70)
    YELLOW = (181, 159, 59)
    DARK_GRAY = (58, 58, 60)

    keyboard = [['Q','W','E','R','T','Y','U','I','O','P'],
                    ['A','S','D','F','G','H','J','K','L'],
                    ['Z','X','C','V','B','N','M'],
                    ['ENTER'],['DELETE']]
    
    
    def __init__(self, Terminal = False):
        """
        Parameters
        ----------
        Terminal : bool
            A boolean to determine if the game should be played on the terminal or through pygame interface
        """
        self.running = True
        self.letter_locs = []
        self.word = []
        self.wordlist_matrix = []
        self.wordlist = []
        self.key_dict = {}
        self.guesses = []

        self.word_matrix = [['' for i in range(self.square_num//6)] for j in range(self.square_num//5)]
        self.tile_matrix = [[((58, 58, 60), 2) for i in range(self.square_num//6)] for j in range(self.square_num//5)]


    def init_keyboard(self):
        """
        Initializes the keyboard's color, location, and key box dimension for display purposes. 
        These attributes are stores in a nested hashmap with the key letter being the key and 
        the values being a hashmap of the color, location, and box dimension.
        example -> {Letter : {"Color" : color, "Loc" : location, "Rect" : box_dimension} ... }
        """
        start_key_y = 343 + self.box_dim
        for i in self.keyboard:
            for index, value in enumerate(i):
                
                self.key_dict[value] = {}
                self.key_dict[value]["Color"] = self.LIGHT_GRAY

                if self.keyboard.index(i) == 0:
                    self.key_dict[value]["Loc"] = (21 + 60 + 43 * index + self.spacing * index, 6 + start_key_y + self.box_dim//2)
                    self.key_dict[value]["Rect"] = (60 + 43 * index + self.spacing * index, start_key_y, 43, self.box_dim + 10)
                elif self.keyboard.index(i) == 1:
                    self.key_dict[value]["Loc"] = (21 + 83 + 43 * index + self.spacing * index, 
                    6 + self.box_dim//2 + start_key_y + self.spacing + self.box_dim + 12)
                    self.key_dict[value]["Rect"] = (83 + 43 * index + self.spacing * index, 
                    start_key_y + self.spacing + self.box_dim + 12, 43, self.box_dim + 10)
                elif self.keyboard.index(i) == 2:
                    self.key_dict[value]["Loc"] = (21 + 83 + 43 + self.spacing + 43 * index + self.spacing * index, 
                    6 + self.box_dim//2 + start_key_y + 2 * (self.spacing + self.box_dim + 12))
                    self.key_dict[value]["Rect"] = (83 + 43 + self.spacing + 43 * index + self.spacing * index, 
                    start_key_y + 2 * (self.spacing + self.box_dim + 12), 43, self.box_dim + 10)
                elif self.keyboard.index(i) == 3:
                    self.key_dict[value]["Loc"] = (93, start_key_y + 2 * (self.spacing + self.box_dim + 12) + 6 + self.box_dim//2)
                    self.key_dict[value]["Rect"] = (60, start_key_y + 2 * (self.spacing + self.box_dim + 12), 66, self.box_dim + 10)
                else:
                    self.key_dict[value]["Loc"] = (508, start_key_y + 2 * (self.spacing + self.box_dim + 12) + 4 + self.box_dim//2)
                    self.key_dict[value]["Rect"] = (475, start_key_y + 2 * (self.spacing + self.box_dim + 12), 66, self.box_dim + 10)
        
    def init_wordlist_matrix(self):
        """
        Opens text file with word list of possible solutions and acceptable words for gameplay.
        Reads text file and creates list of words. Creates two list. One list contains string values
        of the words. Another list contains lists of the char values of each word.
        examples -> ['ABACK', 'ABASE', 'ABATE', ...]
                    [['A', 'B', 'A', 'C', 'K'], ['A', 'B', 'A', 'S', 'E'], ['A', 'B', 'A', 'T', 'E'], ...]
        """
        with open('wordlist.txt') as file:
            self.wordlist_matrix = file.readlines()
            self.wordlist = [item.rstrip().upper() for item in self.wordlist_matrix]
            self.wordlist_matrix = [list(item.rstrip().upper()) for item in self.wordlist_matrix]

    def init_letter_locs(self):
        """
        Finds location values of the wordle grid where the letters would be displayed during gameplay. 
        """
        for i in range(self.square_num//5):
            temp = []
            for j in range(self.square_num//6):
                temp.append((self.box_dim//2 + self.margin + self.box_dim * (j + 1) + self.spacing * j,
                             self.box_dim//2 + self.box_dim * (i + 1) + self.spacing* i))
            self.letter_locs.append(temp)

    def add_letter(self, letter, location):
        """
        Adds letter to display using the location and letter char value.

        Attributes
        ----------
        letter : char
            The letter to be added to the display
        location : (int, int)
            The location where the letter will be displayed
        """
        if letter is self.keyboard[-2][0]:
            text1 = self.enter_size.render(letter, True, (255, 255, 255))
        elif letter is self.keyboard[-1][0]:
            text1 = self.del_size.render(letter, True, (255, 255, 255))
        else:
            text1 = self.box_font.render(letter, True, (255, 255, 255))
        textRect1 = text1.get_rect()
        textRect1.center = location
        self.screen.blit(text1, textRect1)

    def update_display(self):
        """
        Updates the wordle grid display and keyboard display. Any changes to the attributes (ex. color) of each
        grid will be updated as the game runs, including user input words. 
        """
        #Updating wordle grid
        for x in range(len(self.word_matrix)):
            for y in range(len(self.word_matrix[x])):
                loc = self.letter_locs[x][y]
                self.add_letter(self.word_matrix[x][y], loc)

        #Updating keyboard grid
        for key in self.key_dict.keys():
            loc = self.key_dict[key]["Loc"]
            self.add_letter(key, loc)



    def current_screen(self):
        """
        Draws the wordle game user interface with the letter attributes (ex. color, box dimensions) 
        as the game runs.
        """
        #Draw wordle grid
        for i in range(self.square_num//5):
                for j in range(self.square_num//6):
                    pygame.draw.rect(self.screen, self.tile_matrix[i][j][0], (self.margin + self.box_dim * (j + 1) + self.spacing * j, 
                    self.box_dim * (i + 1) + self.spacing * i, self.box_dim, self.box_dim), self.tile_matrix[i][j][1])  
        start_key_y =  343 + self.box_dim    

        #Draw keyboard keys
        for key in self.key_dict.keys():
            rect = self.key_dict[key].get("Rect")
            color = self.key_dict[key].get("Color")
            pygame.draw.rect(self.screen, color, rect, border_radius=4)


    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.display_pixel_num, self.display_pixel_num))
        
        self.init_wordlist_matrix()
        self.init_letter_locs()
        self.init_keyboard()
        self.word_of_day = list(random.choice(self.wordlist))

        print(self.word_of_day)

        while self.running:
            self.screen.fill((18, 18, 19))
            self.current_screen()

            
            wordle_image = pygame.image.load(r'wordleimage.png')
            w, h = wordle_image.get_size()
            wordle_image = pygame.transform.scale(wordle_image, (w//3, h//3))
            self.screen.blit(wordle_image, (220, 8))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.unicode.upper() in self.letters and len(self.word) < 5 and self.word_row < 6:
                        self.word.append(event.unicode.upper())
                        self.word_matrix[self.word_row] = self.word
                        
                    if len(self.word) == 5 and self.word in self.wordlist_matrix and event.key == pygame.K_RETURN:
                        for l in range(5):
                            #letter in same position
                            if self.word[l] == self.word_of_day[l]:
                                self.tile_matrix[self.word_row][l] = (self.GREEN, 0)
                                if self.word[l] in self.key_dict.keys():
                                    self.key_dict[self.word[l]]["Color"] = self.GREEN

                            #letter in word but different position
                            elif self.word[l] in self.word_of_day and self.word[l] != self.word_of_day[l]:
                                self.tile_matrix[self.word_row][l] = (self.YELLOW, 0)
                                if self.word[l] in self.key_dict.keys():
                                    self.key_dict[self.word[l]]["Color"] = self.YELLOW

                            #letter not in word
                            elif self.word[l] not in self.word_of_day and self.word[l] != self.word_of_day[l]:
                                self.tile_matrix[self.word_row][l] = (self.DARK_GRAY, 0)
                                if self.word[l] in self.key_dict.keys():
                                    self.key_dict[self.word[l]]["Color"] = self.DARK_GRAY
                        self.word = []
                        self.word_row += 1
                        
                    if event.key == pygame.K_BACKSPACE:
                        self.word = self.word[:-1]
                        self.word_matrix[self.word_row] = self.word
            
            self.update_display()
            pygame.display.flip()


    def close(self):
        pygame.quit()
        quit()

