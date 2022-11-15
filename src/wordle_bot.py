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
import json
from ast import literal_eval
from tqdm import tqdm 

color_points = [0, 1, 2]
combination_list = list(itertools.product(color_points, repeat = 5))

ZERO = np.uint(0)
ONE = np.uint(1)
TWO = np.uint(2)

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
    int_list = [comp_help(countmap, guess, i, TWO)[1] if (ord(true[i]) - ord(guess[i]) == 0) else ZERO for i in range(5)]
    for i in range(len(int_list)):
        if guess[i] in true and guess[i] != true[i] and countmap[guess[i]] != 0:
            int_list[i] = comp_help(countmap, guess, i, ONE)[1]
    return tuple(int_list)


def top_word_guess(entropy_dict, num_display):
    return [(e, entropy_dict[e]) for e in entropy_dict][:num_display]


def word_space(guess, guess_pattern, guess_words):
    output_word_space = []
    guess_zeros = [guess[loc] for loc, val in enumerate(list(guess_pattern)) if val == 0]
    guess_ones = [guess[loc] for loc in range(len(guess_pattern)) if guess_pattern[loc]  == 1]
    guess_ones_loc = [loc for loc in range(len(guess_pattern)) if guess_pattern[loc]  == 1]
    guess_twos_list = [(guess[loc], loc) for loc, val in enumerate(list(guess_pattern)) if val == 2]

    # print(guess_zeros)
    guess_words = [word for word in guess_words if all(substring not in word for substring in guess_zeros)]
    if guess_pattern == (0,0,0,0,0):
        return guess_words
    guess_words.sort()
    # print(guess_words)
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

    
    # print("HERE", output_word_space)
    output_word_space.sort()
    return output_word_space


def information_bits(prob):
    if prob == 0:
        return 0
    return np.log2(1 / prob)

def probability(count, word_space_len):
    return count / word_space_len

# def word_space(guess, guess_pattern, guess_space):
#     new_space = []
#     ones = sum([1 for val in guess_pattern if val == 1])
#     twos = sum([1 for val in guess_pattern if val == 2])

#     guess_dict = {0:{}, 1:{}, 2:{}}
#     for i in range(len(guess_pattern)):
#         pattern_val = guess_pattern[i]
#         guess_dict[pattern_val][guess[i]] = i

    

#     for word in guess_space:
#         word_pattern = comparison(word, guess)
#         g_okay, y_okay, o_okay, gg_okay = 0, 0, 0, 0

#         for g in range(len(guess)):
#             if (guess[g] == word[g] and guess_pattern[g] == 2):
#                 gg_okay += 1
#             for w in range(len(word)):
#                 # if (guess_pattern[g] == 0 and guess[g] == word[w] and word_pattern[w] > 0):
#                 #     g_okay += 1                    
#                 if (guess_pattern[g] == 1 and guess[g] == word[w] and word_pattern[w] > 0 and g != w):
#                     y_okay += 1
#                 if (g == w and guess[g] == word[w] and guess_pattern[g] == 1):
#                     o_okay += 1
                
                   
#         if y_okay == ones and o_okay == 0 and gg_okay == twos and all(substring not in word for substring in guess_dict[0].keys()):
#             new_space.append(word)
    
#     new_space.sort()
#     return new_space

# for x in guess_words:
#     for y in guess_words:
#         comparison(x,y)
#     print(f'Percent: {100 * (guess_words.index(x) / len(guess_words))}', end='\r')


# solution = "ABYSS"
# guess = "TARES"
# pattern = comparison(guess, solution)
# guess_space1 = word_space('TRACK', (0,0,0,0,0), guess_words)
# guess_space1 = word_space('TREES', (0,0,0,0,0), guess_space1)
# guess_space1 = word_space('YOUNG', (1,2,0,0,1), guess_space1)
# guess_space1 = word_space('DODGY', (0,2,0,2,2), guess_space1)

# print(len(guess_space1))
# e = entropy_calc(guess_words, guess_spaceOne)
# for val in top_word_guess(e, 10):
#     print(val)
# print('\n')

# guess2 = "ALAMO"
# pattern2 = comparison(guess2, solution)
# guess_space2 = word_space(guess2, pattern2, guess_words)
# print(pattern2, guess_space2)
# nextSpace = word_space("A")

# guess_spaceTwo = word_space("RAINS", (0,1,0,0,2), guess_spaceOne)
# e = entropy_calc(guess_words, guess_spaceTwo)
# for val in top_word_guess(e, 10):
#     print(val)
# print('\n')

# guess_spaceThree, guess_spaceThreeLen = word_space("KOMBU", (0,0,0,1,0), guess_spaceTwo)

# e = entropy_calc(guess_words, guess_spaceThree)
# for val in top_word_guess(e, 10):
#     print(val)

def init_match_matrix(guess_words, combination_list):
    if os.path.exists('test.txt'):
        out_dict = {}
        with open('test.txt') as file:
            for line in file:
                word = line[:5]
                word_array = literal_eval(line[6:])
                out_dict[word] = word_array
        return out_dict
    else:
        with open('test.txt', 'w') as file:
            for x in range(len(guess_words)):
                temp_list = [0 for i in range(243)]
                for y in range(len(guess_words)):
                    pattern = comparison(guess_words[x], guess_words[y])
                    index = combination_list.index(pattern)
                    temp_list[index] += 1
                print(f'Percent: {100 * (x / len(guess_words))}', end='\r')
                file.write(guess_words[x] + ' ' + json.dumps(temp_list))
                file.write('\n')
    return init_match_matrix(guess_words, combination_list)


# pattern_dict = collections.defaultdict(lambda : collections.defaultdict(set))
# for word in guess_words:
#     for word2 in guess_words:
#         pattern_index = combination_list.index(comparison(word, word2))
#         pattern_dict[word][pattern_index].add(word2)
#     print(f'Percent: {100 * (guess_words.index(word) / len(guess_words))}', end='\r')

# with open('precompute.txt', 'w') as file:
#     for x in range(len(guess_words)):
#         temp_list = {i : set() for i in range(len(combination_list))}
#         for y in range(len(guess_words)):
#             pattern = comparison(guess_words[x], guess_words[y])
#             index = np.uint8(combination_list.index(pattern))
#             word = np.uint8(guess_words.index(guess_words[y]))
#             temp_list[index].add(word)
#             print(y)
#             # temp_list.append(combination_list.index(pattern))
#             # file.write(guess_words[x] + ' ' + json.dumps(temp_list))
#             file.write(guess_words[x] + ' ' + str(temp_list))

#         file.write('\n')
#         print(f'Percent: {100 * (x / len(guess_words))}', end='\r')
        
# new_dic = np.array([])
# for x in range(len(guess_words)):
#     temp_list = np.array([])
#     for y in range(len(guess_words)):
#         pattern = comparison(guess_words[x], guess_words[y])
#         index = np.uint8(combination_list.index(pattern))
#         word = np.uint8(guess_words.index(guess_words[y]))
#         # temp_list[index].add(word

#         # file.write(guess_words[x] + ' ' + str(temp_list))
#     new_dic[guess_words[x]] = temp_list
#     print(f'Percent: {100 * (x / len(guess_words))}', end='\r')



def match_matrix(guess_space, guess_words, combination_list):
    out_dict = dict.fromkeys(guess_space, None)
    for x in range(len(guess_space)):
        temp_list = [0 for i in range(243)]
        for y in range(len(guess_space)):
            pattern = comparison(guess_space[x], guess_space[y])
            index = combination_list.index(pattern)
            temp_list[index] += 1
        out_dict[guess_space[x]] = temp_list
        print(f'Percent: {100 * (x / len(guess_space))}', end='\r')
    return out_dict

# guess_space1 = word_space('SLATE', (1,0,1,0,0), guess_words)
# print(len(guess_space1))
# t0 = time.time()
# test_mat = match_matrix(guess_space1, guess_words, combination_list)
# print(test_mat)
# t1 = time.time()
# print(t1-t0)

t0 = time.time()
temp_dict = {x : set() for x in range(len(guess_words))}
for word in guess_words:
    temp_set = set()
    for word2 in guess_words:
        temp_set.add(comparison(word, word2))
    temp_dict[guess_words.index(word)] = temp_set
    print(f'Percent: {100 * (guess_words.index(word) / len(guess_words))}', end='\r')
t1 = time.time()
print(t1 - t0)

def entropy_calc(guess_words, guess_space, match_mat):
    # if len(guess_space) == 2:
    #     return {guess_space[0]: 1.0, guess_space[1]: 1.0}

    entropy_dict = {}
    # if len(guess_space) == 12972:
    #     match_mat = init_match_matrix(guess_space, combination_list)
    # else:
    #     match_mat = match_matrix(guess_space, guess_words, combination_list)

    for guess in guess_space:
        count = dict.fromkeys(combination_list, 0)
        for word in  guess_words:
            pattern = comparison(guess, word)
            count[pattern] += 1
        prob_list = [count[c] / len(guess_space) for c in count]



        # prob_list = [count / len(guess_space) for count in match_mat[guess]]
        info_bits_list = [information_bits(prob) for prob in prob_list]
        entropy_dict[guess] = sum([prob_list[i]*info_bits_list[i] for i in range(len(prob_list))])

        print(f'Percent: {100 * (guess_space.index(guess) / len(guess_space))}', end='\r')

    print('\n')
    entropy_dict = dict(sorted(entropy_dict.items(), key = lambda item : item[1], reverse =True))

    return entropy_dict

# guess_space1 = word_space('SLATE', (1,0,1,0,0), guess_words)
# t0 = time.time()
# e =  entropy_calc(guess_space1, guess_space1, 0)
# t1 = time.time()
# print(t1-t0)
# for val in top_word_guess(e, 10):
#     print(val)
# print('\n')


def sim():
    mat_match = init_match_matrix(guess_words, combination_list)
    true_word = "ABYSS"
    guess = "TARES"
    pattern = comparison(guess, true_word)
    guess_space = word_space(guess, pattern, guess_words)
    for i in range(10):
        e = entropy_calc(guess_words, guess_space, mat_match)
        top_word = top_word_guess(e,1)[0][0]
        print(top_word)
        if top_word == true_word:
            print(f'WON IN {i + 2} GUESSES')
            break
        pattern = comparison(top_word, true_word)
        # guess_space = word_space(top_word, pattern, guess_space)
        # print(guess_space)


# sim()


# entropy_calc(guess_words, guess_words)
# true_word = "ABYSS"
# guess = "SLATE"
# pattern = comparison(guess, true_word)
# guess_space1 = word_space(guess, pattern, guess_words)
# t0 = time.time()
# e = entropy_calc(guess_words, guess_space1)
# t1 = time.time()
# print(t1-t0)
# for val in top_word_guess(e, 1):
#     print(val)
# print('\n')

# guess = 'RAINS'
# pattern = comparison(guess, true_word)
# guess_space2 = word_space(guess, pattern, guess_space1)
# t0 = time.time()
# e = entropy_calc(guess_words, guess_space2)
# t1 = time.time()
# print(t1-t0)
# for val in top_word_guess(e, 10):
#     print(val)
# print('\n')

# guess = 'AMBOS'
# pattern = comparison(guess, true_word)
# guess_space3 = word_space(guess, pattern, guess_space2)
# t0 = time.time()
# e = entropy_calc(guess_words, guess_space3)
# t1 = time.time()
# print(t1-t0)
# for val in top_word_guess(e, 10):
#     print(val)
# print('\n')

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

def entropy_calc(guess_words, guess_space):
    # if len(guess_space) == 2:
    #     return {guess_space[0]: 1.0, guess_space[1]: 1.0}

    entropy_dict = {}
    for guess in guess_words:
        count = dict.fromkeys(combination_list, 0)
        for word in  guess_space:
            pattern = comparison(guess, word)
            count[pattern] += 1

        prob_list = [count[c] / len(guess_space) for c in count]
        info_bits_list = [information_bits(prob) for prob in prob_list]
        entropy_dict[guess] = sum([prob_list[i]*info_bits_list[i] for i in range(len(count))])

        print(f'Percent: {100 * (guess_words.index(guess) / len(guess_words))}', end='\r')

    print('\n')
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



