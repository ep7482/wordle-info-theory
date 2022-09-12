import numpy as np
import itertools
import collections
import os.path


color_points = [0, 1, 2]
combination_list = list(itertools.product(color_points, repeat = 5))

def create_guess_file(entropy_dict, guess_words):
    entropy_dict = entropy_cal(guess_words)
    with open('first_guess_bit_list.txt', 'w') as file:
        for e in entropy_dict:
            file.write(str(e) + " " + str(entropy_dict[e]) + "\n")
    file.close()

def init_guess_file():
    return os.path.exists('first_guess_bit_list')

def information_bits(prob):
    if prob == 0:
        return 0
    return np.log2(1 / prob)

def probability(count, word_space_len):
    return count / word_space_len

def compare_words(word1, word2):
    temp_word = word2
    word1 = list(word1)
    word2 = list(word2)
    int_list = []
    countmap = collections.Counter(word2)
    for i in range(5):
        if word2[i] == word1[i] and countmap[word1[i]] != 0:
            int_list.append(2)
            countmap[word1[i]] -= 1
        elif word1[i] in word2 and word1[i] != word2[i] and countmap[word1[i]] != 0:
            int_list.append(1)
            countmap[word1[i]] -= 1
        else:
            int_list.append(0)
    return [temp_word, tuple(int_list)], tuple(int_list)


def top_word_guess(entropy_dict, num_display):
    return [(e, entropy_dict[e]) for e in entropy_dict][:num_display]

def entropy_progress(count, words):
    if count % int(len(words) / 100) == 0:
        print("Entropy Calculation Completion: ", round((100 * count) / (len(words))), "%", end='\r')

def word_space(guess, sol, guess_space):

    if len(guess_space) == 2 and guess in guess_space:
        guess_space.remove(guess)
        return guess_space

    guess_pattern = compare_words(guess, sol)[1]

    new_space = []
    ones = sum([1 for val in guess_pattern if val == 1])
    twos = sum([1 for val in guess_pattern if val == 2])

    for word in guess_space:
        word_pattern = compare_words(word, guess)[1]
        g_okay, y_okay, o_okay, gg_okay = 0, 0, 0, 0

        for g in range(len(guess)):
            for w in range(len(word)):
                if (guess_pattern[g] == 0 and guess[g] == word[w] and word_pattern[w] > 0):
                    g_okay += 1                    
                if (guess_pattern[g] == 1 and guess[g] == word[w] and word_pattern[w] > 0 and g != w):
                    y_okay += 1
                if (g == w and guess[g] == word[w] and guess_pattern[g] == 1):
                    o_okay += 1
                if (g == w and guess[g] == word[w] and guess_pattern[g] == 2):
                    gg_okay += 1
                   
        if g_okay == 0 and y_okay == ones and o_okay == 0 and gg_okay == twos:
            new_space.append(word)
    
    new_space.sort()
    return new_space

def entropy_cal(sol_words, guess_words):
    entropy_dict = {}
    sim_count = 0
    for sol in sol_words:

        total_list = [compare_words(sol, guess)[1] for guess in guess_words]
        count = collections.Counter(total_list)

        info_bits_list = [information_bits(probability(count[c], len(guess_words))) for c in count]
        prob_list = [probability(count[c], len(guess_words)) for c in count]
        
        entropy_dict[sol] = sum([prob_list[i]*info_bits_list[i] for i in range(len(count))])

        entropy_progress(sim_count, sol_words)
        sim_count += 1

    print('\n')
    entropy_dict = dict(sorted(entropy_dict.items(), key = lambda item : item[1], reverse =True))

    return entropy_dict