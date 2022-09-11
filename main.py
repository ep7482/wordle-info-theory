import wordle_game
import wordle_bot as bot


with open('data/wordlist.txt') as file:
    wordle_words = file.readlines()
    wordle_words = [item.rstrip().upper() for item in wordle_words]

with open('data/guess_wordlelist.txt') as file:
    guess_words = file.readlines()
    guess_words = [item.rstrip().upper() for item in guess_words[1:]]

if __name__ == '__main__':

    #Create and run game
    game = wordle_game.wordle_game()
    game.run()

    # words = bot.word_space("SLATE","ABYSS", guess_words)
    # entropy = bot.entropy_cal(guess_words, words)
    # for top in bot.top_word_guess(entropy, 10):
    #     print(top)

    # new_words = bot.word_space("RAINS", "ABYSS", words)
    # entropy = bot.entropy_cal(guess_words, new_words)
    # for top in bot.top_word_guess(entropy, 10):
    #     print(top)

    # newer_words = bot.word_space("KOMBU", "ABYSS", new_words)
    # entropy = bot.entropy_cal(guess_words, newer_words)
    # for top in bot.top_word_guess(entropy, 10):
    #     print(top)

    # print(newer_words)