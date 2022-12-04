import numpy as np
import matplotlib.pyplot as plt
import collections
import itertools
import time
import os
import pickle
from scipy.stats import entropy
from ast import literal_eval


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


def entropy_calc(pattern_matrix, guess_space=guess_words, progress=False):
    entropy_dict = {}
    for guess in guess_space:
        prob_list = np.fromiter(word_distribution(pattern_matrix, guess, guess_space).values(), dtype=float) / len(pattern_matrix[0])
        entropy_dict[guess] = entropy(prob_list, base=2)
        if progress: print(f'Percent: {100 * (guess_space.index(guess) / len(guess_space))}', end='\r')
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

def new_pattern_matrix(guess, true, pattern_matrix, mode, guess_space=guess_words):
    word_space_indices = word_space(guess, true, pattern_matrix, guess_space)[1]
    if mode == "HARD":
        output_matrix = pattern_matrix[:,word_space_indices][word_space_indices]
    elif mode == "EASY":
        output_matrix = pattern_matrix[:,word_space_indices]
    else:
        print("Choose mode: HARD or EASY")
    return output_matrix, word_space_indices


def backtrack_indices(index_list):
    val = 0
    for indices in reversed(index_list):
        val = indices[val]
    return guess_words[val]


def sim(mode, num_sims=len(wordle_words)):
    wordle_dist = []
    for true in wordle_words[:num_sims]:
        next_guess = "TARES"
        new_matrix = init_matrix()
        guess_space = guess_words
        indices_list = []
        counter = 1
        
        while next_guess != true:
            if mode == "HARD":
                newest_matrix = new_pattern_matrix(next_guess, true, new_matrix, mode, guess_space)[0]
                guess_space = word_space(next_guess, true, new_matrix, guess_space)[0]
                entropy_dict = entropy_calc(newest_matrix, guess_space)
            elif mode == "EASY":
                newest_matrix, ind = new_pattern_matrix(next_guess, true, new_matrix, mode, guess_words)
                indices_list.append(ind)
                entropy_dict = entropy_calc(newest_matrix)
                if backtrack_indices(indices_list) == true:
                    counter += 1
                    break
            else:
                print("Choose mode: HARD or EASY")
            next_guess = top_word_guess(entropy_dict, 1)[0][0]
            new_matrix = newest_matrix
            counter += 1
        wordle_dist.append(counter)
        print(wordle_words.index(true))
        # print(f'Percent: {100 * (wordle_words.index(true) / len(wordle_words))}', end='\r')

    return wordle_dist


def sim_hist(mode):
    text_file = open(f"data/{mode}mode_sim_results.txt", "r")
    sim_vals = literal_eval(text_file.read())
    plt.figure(figsize=(10, 8))
    plt.hist(sim_vals)
    plt.title(f"Wordle {mode} mode tries for 2315 games")
    plt.ylabel("Number of games played")
    plt.xlabel(f'Average number of tries - {sum(sim_vals) / len(sim_vals)}')
    plt.savefig(f'images/{mode}mode_hist.png')
    plt.show()


def sim_values(mode):
    if os.path.exists(f"data/{mode}mode_sim_results.txt") == False:
        sim_vals = sim(mode)   
        with open(f"data/{mode}mode_sim_results.txt", "w") as file:
            file.write(str(sim_vals))
    else:
        text_file = open(f"data/{mode}mode_sim_results.txt", "r")
        sim_vals = literal_eval(text_file.read())
    return sim_vals
    




    
