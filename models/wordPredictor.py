# coding=utf-8
import os, sys
import operator
import unicodedata
from collections import defaultdict

MAX_PREDICTED_WORDS = 30

class WordPredictor():
  def __init__(self):
    self.src_file_path = os.path.join(os.path.dirname(__file__), "../data/categories/")
    self.exclude       = ["<S/>", "<number>", "<abbrevation>", "<unkown>"]

    self.most_frequent                   = []
    self.class_of_words                  = {}
    self.probability_of_words_in_classes = defaultdict(float)
    self.class_transition_probabilities  = defaultdict(float)

    self.build_categories()

  def getWordList(self, prev_word="<S/>"):
    if prev_word in self.class_of_words:
      word_probs = self.calc_probabilities(prev_word)
      word_list  = sorted(word_probs, key=word_probs.get, reverse=True)
      # dont predict internal symbols
      word_list  = filter(lambda word: word not in self.exclude, word_list)
      word_list  = word_list[:MAX_PREDICTED_WORDS]
    else:
      # in case of unkown word just show most frequent
      word_list = self.most_frequent

    return word_list

  def calc_probabilities(self, prev_word):
    prev_word_class = self.class_of_words[prev_word]

    probabilities = {}
    for word in self.class_of_words:
      class_id        = self.class_of_words[word]
      transition_prob = self.class_transition_probabilities[(prev_word_class, class_id)]
      word_prob       = self.probability_of_words_in_classes[(word, class_id)]

      prob =  word_prob * transition_prob
      if prob > 0:
        probabilities[word] = prob

    return probabilities

  def go_to_categorie(self, category):
    self.most_frequent                   = []
    self.class_of_words                  = {}
    self.probability_of_words_in_classes = defaultdict(float)
    self.class_transition_probabilities  = defaultdict(float)

    self.build_languge_model_from_dir(category)

  def build_categories(self):
    categories = os.listdir(self.src_file_path)
    categories = filter(lambda word: word != ".DS_Store", categories)
    print sys.getfilesystemencoding()
    categories = map(lambda word: unicodedata.normalize("NFC", word.decode("utf-8")), categories)
    self.categories = categories

  def build_languge_model_from_dir(self, directory):
    pathname                   = os.path.join(self.src_file_path, directory)
    number_of_words_in_classes = defaultdict(int)
    total_word_counts          = defaultdict(int)

    classes_file = os.path.join(pathname, "paths")
    for line in open(classes_file):
      data = line.split()

      class_id   = data[0]
      word       = data[1]
      word_count = int(data[2])

      self.class_of_words[word]                               = class_id
      self.probability_of_words_in_classes[(word, class_id)] += word_count
      number_of_words_in_classes[class_id]                   += word_count

      total_word_counts[word] += word_count

    # normalize counts
    for word, class_id in self.probability_of_words_in_classes:
      self.probability_of_words_in_classes[(word, class_id)] /= number_of_words_in_classes[class_id]

    # store most frequnt words as fallback
    most_frequent = sorted(total_word_counts, key=total_word_counts.get, reverse=True)
    most_frequent = filter(lambda word: word not in self.exclude, most_frequent)
    self.most_frequent = most_frequent[:MAX_PREDICTED_WORDS]

    collocs_file = os.path.join(pathname, "collocs")
    for line in open(collocs_file):
      data = line.split()

      transition_prob = float(data[0])
      word1           = data[1]
      word2           = data[2]

      word_class1 = self.class_of_words[word1]
      word_class2 = self.class_of_words[word2]

      self.class_transition_probabilities[(word_class1, word_class2)] += transition_prob