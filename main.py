import src.wordle_game as wordle_game
import src.wordle_solver as bot


with open('data/wordlist.txt') as file:
    wordle_words = file.readlines()
    wordle_words = [item.rstrip().upper() for item in wordle_words]

with open('data/guess_wordlelist.txt') as file:
    guess_words = file.readlines()
    guess_words = [item.rstrip().upper() for item in guess_words[1:]]

if __name__ == '__main__':

    #Create and run game
    game = wordle_game.wordle_game(wordle_words=wordle_words, guess_words=guess_words)
    game.run()

print("test")