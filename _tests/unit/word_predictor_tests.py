# coding=utf-8
import pytest, os, sys

lib_path = os.path.abspath(os.path.join("..", "next-word-predictor"))
sys.path.append(lib_path)

from models.wordPredictor import WordPredictor

# tokenized corpus
# </S> the dog 
# </S> the dog 
# </S> the dog 
# </S> the cat 
# </S> the cat 
# </S> the mouse </S>

@pytest.fixture
def word_predictor():
    word_predictor = WordPredictor()
    word_predictor.src_file_path = os.path.join(os.path.dirname(__file__), "data/")
    return word_predictor

def test_build_categories(word_predictor):
    word_predictor.build_categories()

    assert u"testlang" in word_predictor.categories
    assert u"täst&1" in word_predictor.categories
    assert u".DS_Store"  not in word_predictor.categories

def test_build_languge_model_from_dir(word_predictor):
    word_predictor.build_languge_model_from_dir("testlang")

    assert word_predictor.most_frequent           == ["the", "dog", "cat", "mouse", "rare"]
    assert word_predictor.class_of_words["<S/>"]  == "A"
    assert word_predictor.class_of_words["the"]   == "B"
    assert word_predictor.class_of_words["rare"]  == "B"
    assert word_predictor.class_of_words["dog"]   == "C"
    assert word_predictor.class_of_words["cat"]   == "C"
    assert word_predictor.class_of_words["mouse"] == "C"

def test_build_languge_model_from_dir_and_calc_class_transition_probs(word_predictor):
    word_predictor.build_languge_model_from_dir("testlang")

    # identical to word transition counts
    # beacuse A and B have only one word 
    assert abs(word_predictor.class_to_word_transition_probabilities[("A", "the")] - 0.3333) < 0.0001
    assert abs(word_predictor.class_to_word_transition_probabilities[("B", "mouse")] - 0.0555) < 0.0001
    # sum of all words in C to <S/>
    assert abs(word_predictor.class_to_word_transition_probabilities[("C", "<S/>")] - 0.3333) < 0.0001
    # some dont have transiotion probs
    assert word_predictor.class_to_word_transition_probabilities[("A", "rare")] == 0
    assert word_predictor.class_to_word_transition_probabilities[("B", "the")] == 0

def test_getWordList_first_word(word_predictor):
    word_predictor.go_to_categorie("testlang")

    # on short lists most frequent words are added
    assert word_predictor.getWordList() == ["the"] + word_predictor.most_frequent

def test_getWordList_cat(word_predictor):
    word_predictor.go_to_categorie("testlang")

    # on short lists most frequent words are added
    assert word_predictor.getWordList("cat") == word_predictor.most_frequent

def test_getWordList_rare(word_predictor):
    # even thogh rare_dog has a propability of 0
    # we predict dog as most likely because rare is in group B
    # and B_dog has a propabilty of 1666666667 
    word_predictor.go_to_categorie("testlang")

    # on short lists most frequent words are added
    assert word_predictor.getWordList("rare") == ["dog", "cat", "mouse"] + word_predictor.most_frequent