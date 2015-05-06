import string
import random

class WordPredictor():

  def getWordList(self):
    word_list       = []
    number_of_words = random.randint(5, 30)

    for i in range(number_of_words):
      word_length = random.randint(4, 15)
      word_list.append(''.join(random.choice(string.letters) for i in range(word_length)))

    return word_list