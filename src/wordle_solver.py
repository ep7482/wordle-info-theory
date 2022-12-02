print('test')
import numpy as np
import matplotlib.pyplot as plt
import collections
import itertools
import time
import os
import pickle
from scipy.stats import entropy

with open('data/guess_wordlelist.txt') as file:
    guess_words = file.readlines()
    guess_words = [item.rstrip().upper() for item in guess_words[1:]]


with open('data/wordlist.txt') as file:
    wordle_words = file.readlines()
    wordle_words = [item.rstrip().upper() for item in wordle_words]


color_points = [0, 1, 2]
combination_list = list(itertools.product(color_points, repeat = 5))
combination_dict = {combination_list[i] : i for i in range(len(combination_list))}


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


def init_matrix():
    if os.path.exists('data/init_matrix.pickle') == False:
        with open('data/init_matrix.pickle', 'wb') as handle:
            output_matrix = np.zeros((len(guess_words), len(guess_words)),dtype=np.uint8)
            for i in range(len(guess_words)):
                for j in range(len(guess_words)):
                    pattern = comparison(guess_words[i], guess_words[j])
                    output_matrix[i][j] = combination_dict[pattern]
                print(f'Percent: {100 * (i / len(guess_words))}', end='\r')
            pickle.dump(output_matrix, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open('data/init_matrix.pickle', 'rb') as handle:
            output_matrix = pickle.load(handle)
    return output_matrix


def top_word_guess(entropy_dict, num_display):
    return [(e, entropy_dict[e]) for e in entropy_dict][:num_display]


def information_bits(prob):
    if prob == 0:
        return 0
    return np.log2(1 / prob)


def probability(count, word_space_len):
    return count / word_space_len


def entropy_calc(pattern_matrix, guess_space=guess_words):
    entropy_dict = {}
    for guess in guess_space:
        prob_list = np.fromiter(word_distribution(pattern_matrix, guess, guess_space).values(), dtype=float) / len(pattern_matrix[0])
        entropy_dict[guess] = entropy(prob_list, base=2)
        print(f'Percent: {100 * (guess_space.index(guess) / len(guess_space))}', end='\r')
    print('\n')
    entropy_dict = dict(sorted(entropy_dict.items(), key = lambda item : item[1], reverse =True))
    return entropy_dict


def word_distribution(pattern_matrix, word, guess_space):
    index = guess_space.index(word)
    sorted_counter_by_val = collections.Counter(pattern_matrix[index])
    for i in range(243):
        if i not in sorted_counter_by_val.keys():
            sorted_counter_by_val[i] = 0   
    return sorted_counter_by_val


def plot_distribution(pattern_matrix, word):
    dist = dict(sorted(word_distribution(pattern_matrix, word).items(), key = lambda item: item[1], reverse=True))
    dist_vals = dist.values()
    plt.figure(figsize=(10, 8))
    plt.bar(range(243), dist_vals, width=1, edgecolor='black')
    plt.show()


def word_space(guess, true, pattern_matrix, guess_space):
    values = pattern_matrix[guess_space.index(guess)]
    pattern_index = combination_dict[comparison(guess, true)]
    indices = np.where(values == pattern_index)[0]
    new_word_space = [guess_space[i] for i in list(indices)]
    return new_word_space, indices

def new_pattern_matrix(guess, true, pattern_matrix, guess_space=guess_words):
    word_space_indices = word_space(guess, true, pattern_matrix, guess_space)[1]
    output_matrix = pattern_matrix[:,word_space_indices][word_space_indices]
    return output_matrix, word_space_indices

pattern_matrix = init_matrix()
# entropy_dict = entropy_calc(pattern_matrix)
# print(top_word_guess(entropy_dict, 10))


true = "ABYSS"
new_matrix, word_indices = new_pattern_matrix("SLATE", true, pattern_matrix)
guess_space = word_space("SLATE", true, pattern_matrix, guess_words)[0]

new_matrix, word_indices = new_pattern_matrix("RAINS", true, new_matrix)
guess_space = word_space("RAINS", true, new_matrix, guess_space)[0]

# new_matrix, word_indices = new_pattern_matrix("KOMBU", true, new_matrix)



t0 = time.time()
entropy_dict = entropy_calc(new_matrix, guess_space)
t1 = time.time()
print(top_word_guess(entropy_dict, 10))
print(t1-t0)


t0 = time.time()
print(word_space("SLATE", true, pattern_matrix))
t1 = time.time()
print(t1 - t0)



# sorted_counter_by_key = dict(sorted(counter.items(), key = lambda item: item[0]))
# for i in range(243):
#     if i not in sorted_counter_by_key.keys():
#         sorted_counter_by_key[i] = 0;


