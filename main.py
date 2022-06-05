import pygame

class wordle_game:
    
    def __init__(self):
        self.running = True
        self.square_num = 30
        self.display_pixel_num = 600
        self.box_dim = 50
        self.margin = int((500 - (50 * 5 + 5 * 4)) / 2)

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.display_pixel_num, self.display_pixel_num))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.close()
            
            self.screen.fill((255, 255, 255))
            
            for i in range(self.square_num//6):
                for j in range(self.square_num//5):
                    pygame.draw.rect(self.screen, (0, 0, 0), (self.margin + self.box_dim * (i + 1) + 5 * i, self.box_dim * (j + 1) + 5 * j, self.box_dim, self.box_dim), width = 2)



            pygame.display.flip()


    def close(self):
        pygame.quit()
        quit()



if __name__ == '__main__':
    game = wordle_game()
    game.run()