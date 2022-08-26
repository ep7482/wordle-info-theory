from gc import collect
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections
import os.path
# import tqdm
# import time


with open('data/wordlist.txt') as file:
    wordle_words = file.readlines()
    wordle_words = [item.rstrip().upper() for item in wordle_words]

with open('data/guess_wordlelist.txt') as file:
    guess_words = file.readlines()
    guess_words = [item.rstrip().upper() for item in guess_words[1:]]

color_points = [0, 1, 2]
combination_list = list(itertools.product(color_points, repeat = 5))

def information_bits(prob):
    if prob == 0:
        return 0
    return np.log2(1 / prob)

def probability(count):
    return count / len(guess_words)

def entropy(prob_list, info_bits_list):
    return sum([prob_list[i]*info_bits_list[i] for i in range(len(combination_list))])

def compare_words(guess, todays_word):
    temp_guess = guess
    guess = list(guess)
    todays_word = list(todays_word)
    int_list = []
    countmap = collections.Counter(todays_word)
    for i in range(len(todays_word)):
        if guess[i] == todays_word[i] and countmap[guess[i]] != 0:
            int_list.append(2)
            countmap[guess[i]] -= 1
        elif guess[i] in todays_word and guess[i] != todays_word[i] and countmap[guess[i]] != 0:
            int_list.append(1)
            countmap[guess[i]] -= 1
        else:
            int_list.append(0)
    word_dict = {}
    word_dict[temp_guess] = tuple(int_list)
    return word_dict, tuple(int_list)


def entropy_cal(wordle_words, single_guess=None):
    if single_guess != None:
        wordle_words = [single_guess]

    entropy_dict = {}
    sim_count = 0
    for i in wordle_words:
        guess = i
        total_list = []
        for sol in guess_words:
            word_dict, int_list = compare_words(guess, sol)
            total_list.append(int_list)


        count = collections.Counter(total_list)

        for combo in combination_list:
            if combo not in count.keys():
                count[combo] = 0

        count = dict(sorted(count.items(), key = lambda item : item[1], reverse =True))

        prob_list = []
        info_bits_list = []
        for c in count:
            count_num = count[c]
            info_bits = information_bits(probability(count_num))
            prob = probability(count_num)
            prob_list.append(prob)
            info_bits_list.append(info_bits)

        entropy_val = entropy(prob_list, info_bits_list)
        entropy_dict[guess] = entropy_val

        if sim_count % 100 == 0:
            print(sim_count)
        sim_count += 1
    entropy_dict = dict(sorted(entropy_dict.items(), key = lambda item : item[1], reverse =True))

    if single_guess != None:
        return count,prob_list, info_bits_list, entropy_dict

    return entropy_dict

entropy_dict = entropy_cal(guess_words, None)
counter = 0
for e in entropy_dict:
    if counter < 10:
        print(e, " ", entropy_dict[e])
    counter += 1

if os.path.exists('first_guess_bit_list') == False:
    with open('first_guess_bit_list.txt', 'w') as file:
        for e in entropy_dict:
            file.write(str(e) + " " + str(entropy_dict[e]) + "\n")
    file.close()


# plt.bar(range(len(prob_list)), prob_list)
# plt.show()

# count, probs, infos, entropie = entropy_cal(guess_words, "SLATE")
# print(entropie)
# print(max(probs))
# print(count)


# print("Count: ",count_)
# print("Prob: ", prob)
# print("Info Bits: ", info_bits)   
# plt.bar(range(len(count.values())), count.values())
# plt.show()
# plt.bar(range(len(prob_list)), prob_list)
# plt.show()