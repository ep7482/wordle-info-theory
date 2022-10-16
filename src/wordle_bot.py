from re import I, L
from wsgiref.util import guess_scheme
import numpy as np
import itertools
import collections
import os.path
from scipy.stats import entropy
import scipy.sparse as sps
import matplotlib.pyplot as plt
import time
import csv
import sys


color_points = [0, 1, 2]
combination_list = list(itertools.product(color_points, repeat = 5))

with open('data/guess_wordlelist.txt') as file:
    guess_words = file.readlines()
    guess_words = [item.rstrip().upper() for item in guess_words[1:]]

with open('data/wordlist.txt') as file:
    wordle_words = file.readlines()
    wordle_words = [item.rstrip().upper() for item in wordle_words]

def create_guess_file(entropy_dict, guess_words):
    entropy_dict = entropy_cal(guess_words)
    with open('first_guess_bit_list.txt', 'w') as file:
        for e in entropy_dict:
            file.write(str(e) + " " + str(entropy_dict[e]) + "\n")
    file.close()

def init_guess_file():
    return os.path.exists('first_guess_bit_list')

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


def top_word_guess(entropy_dict, num_display):
    return [(e, entropy_dict[e]) for e in entropy_dict][:num_display]


def word_space(guess, guess_pattern, guess_words):
    output_word_space = []
    guess_zeros = [guess[loc] for loc, val in enumerate(list(guess_pattern)) if val == 0]
    guess_ones = [guess[loc] for loc in range(len(guess_pattern)) if guess_pattern[loc]  == 1]
    guess_ones_loc = [loc for loc in range(len(guess_pattern)) if guess_pattern[loc]  == 1]
    guess_twos_list = [(guess[loc], loc) for loc, val in enumerate(list(guess_pattern)) if val == 2]

    guess_words = [word for word in guess_words if all(substring not in word for substring in guess_zeros)]
    if guess_pattern == (0,0,0,0,0):
        return guess_words, len(guess_words)

    for word in guess_words:
        twos = 0
        ones = 0
        if all(substring in word for substring in guess_ones):
            for value in guess_twos_list:
                letter, loc= value[0], value[1]
                if word[loc] == letter:
                    twos += 1
            for char in guess_ones:
                if word.index(char) != guess.index(char):
                    ones += 1
        if (ones == len(guess_ones) and 0 not in[ord(word[j]) - ord(guess[j]) for j in guess_ones_loc]
            and twos == len(guess_twos_list)):
            output_word_space.append(word)

                
    output_word_space.sort()
    return output_word_space, len(output_word_space)


def information_bits(prob):
    if prob == 0:
        return 0
    return np.log2(1 / prob)

def probability(count, word_space_len):
    return count / word_space_len


def entropy_calc(guess_words, guess_space):
    # if len(guess_space) == 2:
    #     return {guess_space[0]: 1.0, guess_space[1]: 1.0}

    entropy_dict = {}
    for guess in guess_words:
        count = dict.fromkeys(combination_list, 0)
        for word in  guess_space:
            pattern = comparison(guess, word)
            count[pattern] += 1


        info_bits_list = [information_bits(probability(count[c], len(guess_space))) for c in count]
        prob_list = [probability(count[c], len(guess_space)) for c in count]
        entropy_dict[guess] = sum([prob_list[i]*info_bits_list[i] for i in range(len(count))])

        print(f'Percent: {100 * (guess_words.index(guess) / len(guess_words))}', end='\r')

    print('\n')
    entropy_dict = dict(sorted(entropy_dict.items(), key = lambda item : item[1], reverse =True))

    return entropy_dict


# guess_spaceOne, guess_spaceOneLen = word_space("SLATE", (1,0,1,0,0), guess_words)
# e = entropy_calc(guess_words, guess_spaceOne)
# for val in top_word_guess(e, 10):
#     print(val)
# print('\n')

# guess_spaceTwo, guess_spaceTwoLen = word_space("RAINS", (0,1,0,0,2), guess_spaceOne)
# e = entropy_calc(guess_words, guess_spaceTwo)
# for val in top_word_guess(e, 10):
#     print(val)
# print('\n')

# guess_spaceThree, guess_spaceThreeLen = word_space("KOMBU", (0,0,0,1,0), guess_spaceTwo)

# e = entropy_calc(guess_words, guess_spaceThree)
# for val in top_word_guess(e, 10):
#     print(val)

def match_matrix(guess_words):
    # output_mat = sps.dok_matrix((len(guess_words), len(combination_list)), dtype=np.uint8)
    # for x in range(len(guess_words[:100])):
    #     for y in range(len(guess_words)):
    #         pattern = comparison(guess_words[x], guess_words[y])
    #         output_mat[x, combination_list.index(pattern)] += 1
    #     print(f'Percent: {100 * (x / len(guess_words[:100]))}', end='\r')
    # print('\n')
    output_mat = collections.defaultdict(dict)
    for x in range(len(guess_words[:100])):
        for y in range(len(guess_words)):
            pattern = comparison(guess_words[x], guess_words[y])
            if len(output_mat[x][combination_list.index(pattern)]) == 0:
                output_mat[x][combination_list.index(pattern)] = 0
            else:
                output_mat[x][combination_list.index(pattern)] += 1
        print(f'Percent: {100 * (x / len(guess_words))}', end='\r')
    print('\n')

    fields = ["Guess"] + combination_list
    with open("match_dict.csv", "w", newline='') as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        count = 0
        for k in output_mat:
            w.writerow({field: output_mat[k].get(field) or k for field in fields})
            count += 1
            print(count)

    return output_mat

t0 = time.time()
test_mat = match_matrix(guess_words)
print(test_mat)
t1 = time.time()
print(t1-t0)





# def matches_matrix(guess_words):
#     output_mat = np.zeros((len(guess_words), len(combination_list)), dtype=np.uint8)
#     for x in range(100):
#         for y in range(len(guess_words)):
#             pattern = comparison(guess_words[x], guess_words[y])
#             output_mat[x][combination_list.index(pattern)] += 1
#         print(f'Percent: {100 * (x / len(guess_words[:100]))}', end='\r')
#     print('\n')
#     return output_mat


# t0 = time.time()
# test_mat = matches_matrix(guess_words)[0]
# t1 = time.time()
# print(t1-t0)
# avg = 0
# for i in range(1000):
#     avg += (100 * (sum([1 for k in test_mat[i] if k == 0]) / len(test_mat[i])))
# print("Percent of zeros in matrix: ", avg / 1000)
# print("Num of zeros: ", 243 * (avg/1000))
# test_mat.sort()
# plt.bar(range(len(test_mat)), test_mat[::-1])
# plt.show()



'''             FOR TESTING PURPOSES, TOO SLOW
def calculate_entropy_1(guess_space, other_space):
    entropy_dict = {}
    for guess in guess_space:
        prob_list = []
        for pattern in combination_list:
            num_pos_matches = word_space(guess, pattern, other_space)[1]
            prob = num_pos_matches / len(guess_space)
            prob_list.append(prob)
        entropy_dict[guess] = entropy(prob_list, base=2)
        print(f'Percent: {100 * (guess_space.index(guess) / len(guess_space))}', end='\r')


    entropy_dict = dict(sorted(entropy_dict.items(), key = lambda item : item[1], reverse =True))
    return entropy_dict

def word_space2(guess, guess_space, guess_pattern):
    new_space = []
    ones = sum([1 for val in guess_pattern if val == 1])
    twos = sum([1 for val in guess_pattern if val == 2])

    guess_dict = {0:{}, 1:{}, 2:{}}
    for i in range(len(guess_pattern)):
        pattern_val = guess_pattern[i]
        guess_dict[pattern_val][guess[i]] = i

    

    for word in guess_space:
        word_pattern = comparison(word, guess)
        g_okay, y_okay, o_okay, gg_okay = 0, 0, 0, 0

        for g in range(len(guess)):
            if (guess[g] == word[g] and guess_pattern[g] == 2):
                gg_okay += 1
            for w in range(len(word)):
                # if (guess_pattern[g] == 0 and guess[g] == word[w] and word_pattern[w] > 0):
                #     g_okay += 1                    
                if (guess_pattern[g] == 1 and guess[g] == word[w] and word_pattern[w] > 0 and g != w):
                    y_okay += 1
                if (g == w and guess[g] == word[w] and guess_pattern[g] == 1):
                    o_okay += 1
                
                   
        if y_okay == ones and o_okay == 0 and gg_okay == twos and all(substring not in word for substring in guess_dict[0].keys()):
            new_space.append(word)
    
    new_space.sort()
    return new_space, len(new_space)
'''



