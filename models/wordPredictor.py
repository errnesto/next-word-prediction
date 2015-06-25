import string
import random
import operator
from os import path
from collections import defaultdict

class WordPredictor():
  def __init__(self):
    self.src_file_path                   = path.join(path.dirname(__file__), "../data/language/")
    self.class_of_words                  = {}
    self.probability_of_words_in_classes = defaultdict(float)
    self.class_transition_probabilities  = defaultdict(float)

  def getWordList(self, prev_word="<S/>"):
    prev_word_class = self.class_of_words[prev_word]

    predictions = {}
    for word in self.class_of_words:
      class_id        = self.class_of_words[word]
      transition_prob = self.class_transition_probabilities[(prev_word_class, class_id)]
      word_prob       = self.probability_of_words_in_classes[(word, class_id)]

      prob =  word_prob * transition_prob
      if prob > 0.0001:
        predictions[word] = prob

    word_list = sorted(predictions, key=predictions.get, reverse=True)

    return len(word_list)

  def build_languge_model_from_file(self, filename):
    classes = path.join(self.src_file_path, "paths")
    number_of_words_in_classes = defaultdict(int)
    for line in open(classes):
      data = line.split()

      class_id   = data[0]
      word       = data[1]
      word_count = int(data[2])

      self.class_of_words[word]                               = class_id
      self.probability_of_words_in_classes[(word, class_id)] += word_count
      number_of_words_in_classes[class_id]                   += word_count

    for word, class_id in self.probability_of_words_in_classes:
      self.probability_of_words_in_classes[(word, class_id)] /= number_of_words_in_classes[class_id]

    collocs = path.join(self.src_file_path, "collocs")
    for line in open(collocs):
      data = line.split()

      transition_prob = float(data[0])
      word1           = data[1]
      word2           = data[2]

      word_class1 = self.class_of_words[word1]
      word_class2 = self.class_of_words[word2]

      self.class_transition_probabilities[(word_class1, word_class2)] += transition_prob

# w = WordPredictor()
# w.build_languge_model_from_file("")
# w.getWordList()