import pytest
import os, sys
from collections import defaultdict

# get path to import Lerner module
lib_path = os.path.abspath(os.path.join('..', 'next-word-predictor'))
sys.path.append(lib_path)
from models.Learner import Learner

@pytest.fixture
def learner():
    script_dir       = os.path.dirname(__file__)
    test_corpus_path = os.path.join(script_dir, "test_corpus")

    learner = Learner(corpus=[test_corpus_path])
    return learner

@pytest.fixture
def word_counts():
    return {u'im': 1, u'in': 2, u'Neuenglandstaaten': 1, u'Altweibersommer': 2, u'wird': 1, u'genannt': 1, u'Nordamerika': 1, u'<S/>': 4, u'hat': 1, u'\xe4hnlich': 1, u'den': 1, u'diese': 2, u'Zeit': 1, u'Der': 1, u'verschiedenen': 1, u'Niederschlag': 1, u'gefunden': 1, u'man': 1, u'nennt': 1, u'insbesondere': 1, u'Deutschen': 1, u'und': 1, u'Russland': 1, u'In': 2, u'Bauernregeln': 1}

@pytest.fixture
def group_bigramm_counts():
    return defaultdict(int, {'12_0': 1, '6_8': 1, '1_6': 2, '3_19': 1, '13_14': 1, '1_0': 1, '0_7': 1, '0_4': 2, '4_17': 1, '0_3': 1, '0_0': 5, '0_1': 1, '6_16': 1, '3_0': 1, '0_5': 1, '16_0': 1, '2_2': 1, '17_3': 1, '11_2': 1, '15_1': 1, '5_0': 1, '8_9': 1, '4_1': 1, '19_13': 1, '9_0': 1, '10_12': 1, '14_5': 1, '7_0': 1, '2_15': 1, '5_11': 1, '0_18': 1, '18_10': 1})

@pytest.fixture
def group_counts():
    return {0: 12, 1: 4, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1}

def check_all(group_bigramm_counts, group_counts, test_group_bigramm_counts, test_group_counts):
    for group in group_counts:
        assert group_counts[group] is test_group_counts[group]
    for bigram in group_bigramm_counts:
        assert group_bigramm_counts[bigram] is test_group_bigramm_counts[bigram]

# Tests:
# ----------------------------------------------------------------

def test_if_words_are_counted_correctly(learner, word_counts):
    for word in word_counts:
        assert learner.vocabulary[word].count is word_counts[word]

def test_initial_group_bigramm_counts(learner, group_bigramm_counts):
    for bigram in group_bigramm_counts:
        assert group_bigramm_counts[bigram] is learner.group_bigramm_counts[bigram]
    
def test_remove_Altweibersommer_from_group_4(learner, group_bigramm_counts, group_counts):
    learner.update_help_counts("Altweibersommer")
    assert learner.vocabulary["Altweibersommer"].count is 2

    learner.remove_word_from_its_group("Altweibersommer")
    group_counts[4]              -= 2
    group_bigramm_counts["4_1"]  -= 1
    group_bigramm_counts["4_17"] -= 1
    group_bigramm_counts["0_4"]  -= 2

    check_all(group_bigramm_counts, group_counts, learner.group_bigramm_counts, learner.group_counts)

def test_remove_Zeit_from_group_0(learner, group_bigramm_counts, group_counts):
    learner.update_help_counts("Zeit")
    assert learner.vocabulary["Zeit"].count is 1

    learner.remove_word_from_its_group("Zeit")
    group_counts[0]              -= 1
    group_bigramm_counts["5_0"]  -= 1
    group_bigramm_counts["0_18"] -= 1

    check_all(group_bigramm_counts, group_counts, learner.group_bigramm_counts, learner.group_counts)

def test_remove_Bauernregeln_from_group_0(learner, group_bigramm_counts, group_counts):
    learner.update_help_counts("Bauernregeln")
    assert learner.vocabulary["Bauernregeln"].count is 1

    learner.remove_word_from_its_group("Bauernregeln")
    group_counts[0]             -= 1
    group_bigramm_counts["0_0"] -= 1
    group_bigramm_counts["0_7"] -= 1

    check_all(group_bigramm_counts, group_counts, learner.group_bigramm_counts, learner.group_counts)

def test_remove_Indian_from_group_2(learner, group_bigramm_counts, group_counts):
    learner.update_help_counts("Indian")
    assert learner.vocabulary["Indian"].count is 2

    learner.remove_word_from_its_group("Indian")
    group_counts[2]              -= 2
    group_bigramm_counts["2_2"]  -= 1
    group_bigramm_counts["11_2"] -= 1
    group_bigramm_counts["2_15"] -= 1

    check_all(group_bigramm_counts, group_counts, learner.group_bigramm_counts, learner.group_counts)

def test_move_Altweibersommer_to_gruop_0_then_19(learner, group_bigramm_counts, group_counts):
    learner.update_help_counts("Altweibersommer")

    # move to group 0
    (temp_group_bigramm_counts, temp_group_counts) = learner.move_word_to_group("Altweibersommer", 0)
    group_bigramm_counts_0 = group_bigramm_counts.copy()
    group_counts_0         = group_counts.copy()

    group_counts_0[0]              += 2
    group_bigramm_counts_0["0_1"]  += 1
    group_bigramm_counts_0["0_17"] += 1
    group_bigramm_counts_0["0_0"]  += 2

    check_all(group_bigramm_counts_0, group_counts_0, temp_group_bigramm_counts, temp_group_counts)

    # move to group 19
    (temp_group_bigramm_counts, temp_group_counts) = learner.move_word_to_group("Altweibersommer", 19)
    group_bigramm_counts_19 = group_bigramm_counts.copy()
    group_counts_19         = group_counts.copy()

    group_counts_19[19]              += 2
    group_bigramm_counts_19["19_1"]  += 1
    group_bigramm_counts_19["19_17"] += 1
    group_bigramm_counts_19["0_19"]  += 2

    check_all(group_bigramm_counts_19, group_counts_19, temp_group_bigramm_counts, temp_group_counts)
