
import pytest
import os, sys
import src.wordle_bot as bot



@pytest.fixture
def pattern_data():
    return {
        "SHARD":
        {
            "CRANE": (0,1,2,0,0),
            "SHTIK": (2,2,0,0,0),
            "SHARD": (2,2,2,2,2)
        },
        "BROWN":
        {
            "THREE": (0,0,1,0,0),
            "BLUES": (2,0,0,0,0),
            "WONKY": (1,1,1,0,0),
            "BROWN": (2,2,2,2,2)
        },
        "ABYSS":
        {
            "SLATE": (1,0,1,0,0),
            "RAINS": (0,1,0,0,2),
            "KOMBU": (0,0,0,1,0),
            "ABBAS": (2,2,0,0,2),
        },
        "CRANE":
        {
            "WEARY": (0,1,2,1,0)
        },
        "WEARY":
        {
            "MEETS": (0,2,0,0,0)
        },
        "GONER":
        {
            "ROWER": (0,2,0,2,2)
        }

    }

def test_compare_words(pattern_data):
    for true in pattern_data:
        for guess in pattern_data[true]:
            pattern = pattern_data[true][guess]
            # print(true, guess, pattern, bot.compare_words(guess, true)[1], pattern == bot.compare_words(guess, true)[1])
            # assert pattern == bot.compare_words(guess, true)[1]
            assert pattern == bot.comparison(guess, true)