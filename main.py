import pygame
import random

class wordle_game:
    
    def __init__(self):
        pygame.font.init()
        self.running = True
        self.square_num = 30
        self.display_pixel_num = 600
        self.box_dim = 50
        self.spacing = 6
        self.margin = int((550 - (50 * self.spacing + self.spacing * 4)) / 2)
        self.letters = [chr(i) for i in range(65, 91)]
        self.box_font = pygame.font.SysFont('arial', 24)
        self.key_font = pygame.font.SysFont('Verdana', 24)
        self.letter_locs = []
        self.word_matrix = [['' for i in range(self.square_num//6)] for j in range(self.square_num//5)]
        self.word = []
        self.word_row = 0
        self.wordlist_matrix = []
        self.wordlist = []
        self.tile_matrix = [[((58, 58, 60), 2) for i in range(self.square_num//6)] for j in range(self.square_num//5)]

        
        
    def init_wordlist_matrix(self):
        with open('wordlist.txt') as file:
            self.wordlist_matrix = file.readlines()
            self.wordlist = [item.rstrip().upper() for item in self.wordlist_matrix]
            self.wordlist_matrix = [list(item.rstrip().upper()) for item in self.wordlist_matrix]

    def init_letter_locs(self):
        for i in range(self.square_num//5):
            temp = []
            for j in range(self.square_num//6):
                temp.append((self.box_dim//2 + self.margin + self.box_dim * (j + 1) + self.spacing * j,
                             self.box_dim//2 + self.box_dim * (i + 1) + self.spacing* i))
            self.letter_locs.append(temp)

    def add_letter(self, letter, location):
        text1 = self.box_font.render(letter, True, (255, 255, 255))
        textRect1 = text1.get_rect()
        textRect1.center = location
        self.screen.blit(text1, textRect1)

    def update_display(self):
        for x in range(len(self.word_matrix)):
            for y in range(len(self.word_matrix[x])):
                loc = self.letter_locs[x][y]
                self.add_letter(self.word_matrix[x][y], loc)

    def current_screen(self):
        for i in range(self.square_num//5):
                for j in range(self.square_num//6):
                    pygame.draw.rect(self.screen, self.tile_matrix[i][j][0], (self.margin + self.box_dim * (j + 1) + self.spacing * j, 
                                                              self.box_dim * (i + 1) + self.spacing * i, self.box_dim, self.box_dim), self.tile_matrix[i][j][1])  

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.display_pixel_num, self.display_pixel_num))
        
        self.init_wordlist_matrix()
        self.init_letter_locs()
        self.word_of_day = list(random.choice(self.wordlist))

        print(self.tile_matrix)
        print(self.word_of_day)

        while self.running:
            self.screen.fill((0, 0, 0))
            self.current_screen()

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
                            if self.word[l] == self.word_of_day[l]:
                                self.tile_matrix[self.word_row][l] = ((77, 149, 70), 0)
                            elif self.word[l] in self.word_of_day and self.word[l] != self.word_of_day[l]:
                                self.tile_matrix[self.word_row][l] = ((181, 159, 59), 0)
                            elif self.word[l] not in self.word_of_day and self.word[l] != self.word_of_day[l]:
                                self.tile_matrix[self.word_row][l] = ((58, 58, 60), 0)
                        self.word = []
                        self.word_row += 1

                    if event.key == pygame.K_BACKSPACE:
                        self.word = self.word[:-1]
                        self.word_matrix[self.word_row] = self.word

                    # print(event.unicode.upper(), self.word, self.word_matrix)
            
            self.update_display()
            pygame.display.flip()



    def close(self):
        pygame.quit()
        quit()



if __name__ == '__main__':
    game = wordle_game()
    game.run()