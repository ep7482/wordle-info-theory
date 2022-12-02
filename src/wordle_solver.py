import collections
import time
import itertools
import numpy as np

with open('data/guess_wordlelist.txt') as file:
    guess_words = file.readlines()
    guess_words = [item.rstrip().upper() for item in guess_words[1:]]

with open('data/wordlist.txt') as file:
    wordle_words = file.readlines()
    wordle_words = [item.rstrip().upper() for item in wordle_words]

color_points = [0, 1, 2]
combination_list = list(itertools.product(color_points, repeat = 5))

def word_space(guess, guess_pattern, guess_words):
    output_word_space = []
    guess_zeros = [guess[loc] for loc, val in enumerate(list(guess_pattern)) if val == 0]
    guess_ones = [guess[loc] for loc in range(len(guess_pattern)) if guess_pattern[loc]  == 1]
    guess_ones_loc = [loc for loc in range(len(guess_pattern)) if guess_pattern[loc]  == 1]
    guess_twos_list = [(guess[loc], loc) for loc, val in enumerate(list(guess_pattern)) if val == 2]

    guess_words = [word for word in guess_words if all(substring not in word for substring in guess_zeros)]
    if guess_pattern == (0,0,0,0,0):
        return guess_words
    guess_words.sort()
    next_word_space = []
    for word in guess_words:
        twos = 0
        for value in guess_twos_list:
            letter, loc= value[0], value[1]
            if word[loc] == letter:
                twos += 1
        if twos == len(guess_twos_list):
            next_word_space.append(word)

    for word in next_word_space:
        ones = 0
        if all(substring in word for substring in guess_ones):
            for char in guess_ones:
                if word.index(char) != guess.index(char):
                    ones += 1
        if (ones == len(guess_ones) and 0 not in[ord(word[j]) - ord(guess[j]) for j in guess_ones_loc]):
            output_word_space.append(word)

    output_word_space.sort()
    return output_word_space


def comp_help(countmap, guess, i, val):
    countmap[guess[i]] -= 1
    return countmap, val

def comparison(guess, true):
    assert len(guess) == 5 and len(true) == 5, "Words must have length of 5"
    countmap = collections.Counter(list(true))
    int_list = [comp_help(countmap, guess, i, 2)[1] if (ord(true[i]) - ord(guess[i]) == 0) else 0 for i in range(5)]
    for i in range(len(int_list)):
        if guess[i] in true and guess[i] != true[i] and countmap[guess[i]] != 0:
            int_list[i] = comp_help(countmap, guess, i, 1)[1]
    return tuple(int_list)

# t0 = time.time()
# comparison('HELLO', 'ABYSS')
# t1 = time.time()
# print(t1-t0)

def init_matrix(guess_words, wordle_words):
    output_array = []
    for x in range(len(wordle_words)):
        # inner_array = []
        t1 = time.time()
        for y in range(len(guess_words)):
            pattern = comparison(guess_words[y], wordle_words[x])
            # inner_array.append(len(word_space(guess_words[y], pattern, guess_words)))
            print(f'Inner Percent: {100 * (y / len(guess_words))}', end='\r')
        t2 = time.time()
        print(t2 - t1)
    return output_array


# init_matrix(guess_words, wordle_words)


matrix = np.zeros((len(wordle_words), len(guess_words)), dtype=np.uint8)
for i in range(len(guess_words)):
    for j in range(len(guess_words)):
        comparison(guess_words[i], guess_words[j])
    print(f'Inner Percent: {100 * (i / len(guess_words))}', end='\r')
print(matrix)


print('test')