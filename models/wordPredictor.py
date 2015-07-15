# coding=utf-8
import os, sys
import operator
import unicodedata
import codecs
from collections import defaultdict

MAX_PREDICTED_WORDS = 30

class WordPredictor():
    def __init__(self):
        self.src_file_path = os.path.join(os.path.dirname(__file__), "../data/categories/")
        self.exclude       = ["<S/>", "<number>", "<abbrevation>", "<unkown>"]

        self.most_frequent                          = []
        self.class_of_words                         = {}
        self.class_to_word_transition_probabilities = defaultdict(float)

        self.build_categories()

    def getWordList(self, prev_word=None):
        if prev_word == None:
            prev_word = "<S/>"

        word_list = []
        if prev_word in self.class_of_words:
            word_probs = self.calc_probabilities(prev_word)
            word_list  = sorted(word_probs, key=word_probs.get, reverse=True)
            # dont predict internal symbols
            word_list  = filter(lambda word: word not in self.exclude, word_list)
            word_list  = word_list[:MAX_PREDICTED_WORDS]

        if len(word_list) < 5:
            # in case of unkown word just show most frequent
            word_list += self.most_frequent

        return word_list

    def calc_probabilities(self, prev_word):
        prev_word_class = self.class_of_words[prev_word]

        probabilities = {}
        for word in self.class_of_words:

            prob = self.class_to_word_transition_probabilities[(prev_word_class, word)]
            if prob > 0:
                probabilities[word] = prob

        return probabilities

    def go_to_categorie(self, category):
        self.most_frequent                          = []
        self.class_of_words                         = {}
        self.class_to_word_transition_probabilities = defaultdict(float)

        self.build_languge_model_from_dir(category)

    def build_categories(self):
        categories      = os.listdir(self.src_file_path)
        categories      = filter(lambda word: word != ".DS_Store", categories)
        encoding        = sys.getfilesystemencoding()
        categories      = map(lambda word: unicodedata.normalize("NFC", word.decode(encoding)), categories)
        self.categories = categories

    def build_languge_model_from_dir(self, directory):
        pathname                   = os.path.join(self.src_file_path, directory)
        total_word_counts          = defaultdict(int)

        classes_file = os.path.join(pathname, "paths")
        for line in codecs.open(classes_file, encoding="utf-8"):
            data = line.split()

            class_id   = data[0]
            word       = data[1]
            word_count = int(data[2])

            self.class_of_words[word] = class_id
            total_word_counts[word]   = word_count

        # store most frequnt words as fallback
        most_frequent = sorted(total_word_counts, key=total_word_counts.get, reverse=True)
        most_frequent = filter(lambda word: word not in self.exclude, most_frequent)
        self.most_frequent = most_frequent[:MAX_PREDICTED_WORDS]

        collocs_file = os.path.join(pathname, "collocs")
        for line in codecs.open(collocs_file, encoding="utf-8"):
            data = line.split()

            transition_prob = float(data[0])
            word1           = data[1]
            word2           = data[2]

            word_class1 = self.class_of_words[word1]

            self.class_to_word_transition_probabilities[(word_class1, word2)] += transition_prob
