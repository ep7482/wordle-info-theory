import pygame

class wordle_game:
    
    def __init__(self):
        self.running = True
        self.square_num = 30
        self.display_pixel_num = 600
        self.box_dim = 50
        self.margin = int((500 - (50 * 5 + 5 * 4)) / 2)
        self.letters = [chr(i) for i in range(65, 91)]

        pygame.font.init()
        self.box_font = pygame.font.SysFont('arial', 20)
        self.key_font = pygame.font.SysFont('Verdana', 20)

        self.letter_locs = []
        for i in range(self.square_num//5):
            temp = []
            for j in range(self.square_num//6):
                temp.append((self.box_dim//2 + self.margin + self.box_dim * (j + 1) + 5 * j, self.box_dim//2 + self.box_dim * (i + 1) + 5 * i))
            self.letter_locs.append(temp)

        self.word_matrix = [['' for i in range(self.square_num//6)] for j in range(self.square_num//5)]

    def add_letter(self, letter, location):
        text1 = self.box_font.render(letter, True, (0, 0, 0))
        textRect1 = text1.get_rect()
        textRect1.center = location
        self.screen.blit(text1, textRect1)

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.display_pixel_num, self.display_pixel_num))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.close()
                if event.type == pygame.KEYDOWN:
                    print(event.unicode.upper())
            
            self.screen.fill((255, 255, 255))

            for i in range(self.square_num//5):
                for j in range(self.square_num//6):
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.margin + self.box_dim * (j + 1) + 5 * j, 
                                                              self.box_dim * (i + 1) + 5 * i, self.box_dim, self.box_dim), width = 2)
                    
            pygame.display.flip()



    def close(self):
        pygame.quit()
        quit()



if __name__ == '__main__':
    game = wordle_game()
    game.run()