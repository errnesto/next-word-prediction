# coding=utf-8
import codecs
import re
import operator
from rcdtype import *

Vword = recordtype('Vword', 'count group')

class Learner():
    """Parses text files to generate n-grams and cathegories

    detailed info here
    """

    # comments in the form key : value

    vocabulary  = [] # word : Vword

    predecessors_of       = [] # word : [pre_words]
    successors_of         = [] # word : [(succ_word, count)]
    predecessor_groups_of = [] # word : [pre_group]
    succsessor_groups_of  = [] # word : [succ_group]

    words_predecessing    = [] # group : {word : count}
    words_succsessing     = [] # group : {word : count}

    def __init__(self):
        self.build_vocabulary()
        self.map_words_to_classes()

    def parse_file(self, file_path):
        """takes a path to a file in "Document Format" and returns a array of words

        see http://medialab.di.unipi.it/wiki/Document_Format for information about the "Document Format"
        """

        f = codecs.open(file_path, mode="r", encoding="utf-8")
        content = f.read()

        # strip xml <doc> tags
        content = re.sub(r"<doc.*>|<\/doc>", "", content)

        # strip special characters note "." is not removed yet
        content = re.sub(u'[\]\[!"“„#$%&\\\'()*+,\/:;<=>?@\^_`{|}~-]', "", content)

        # find boundaries of sentences
        content = re.sub(ur"([a-z])\.\s([A-Z0-9])", r"\1 <S/> \2", content)
        content = re.sub(ur"\.$|^\b", " <S/> ", content, flags=re.MULTILINE)

        # TO DO:
        # maybe add a list of common abbrevations to remove socres from them here

        words = content.split()

        return words

    def build_vocabulary(self):
        words = self.parse_file("wiki_00")

        for group, word in enumerate(words):
            if word in self.vocavulary:
                self.vocavulary[word].count += 1
            else:
                self.vocavulary[word] = Vword(1, group) #we use integers for group names

        

    def map_words_to_classes(self):
        INITAL_NUMBER_OF_GROUPS = 100
        sorted_vocabulary = sorted(self.vocavulary.items(), key=operator.itemgetter(1), reverse = True)
        rare_words        = map(lambda tup: tup[0], sorted_vocabulary[INITAL_NUMBER_OF_GROUPS - 1:])

        # put all rare words in the same group
        for word in rare_words:
            self.vocabulary[word].group = -1 # we are shure -1 is not used as a group name yet

        i = 0
        while i < 1:
            i += 1

            for word, word_count in self.vocabulary:
                for group in self.groups:
                    print(word, word_count)
                    # remove 'word' from its class
                    # add 'word' to 'class'
                    # claculate perplexity
                    # store exchange with min perplexity as 'min_perplexity_class'

                # move word from its class to 'min_perplexity_class'

    def calc_perplexity(self):
        # for every group bigramm
            # add the number of occurences x log the number of occurences
        # for every group
            # add the number of occurences x log the number of occurences
        # for everx word 
            # add the number of occurences x log the number of occurencess

    def generate_counts(self, word):
        predecessors = self.predecessors_of[word]
        successors   = self.successors_of[word]

        for pre_word in predecessors:
            bigrams   = filter(lambda s: s == word, self.successors_of[pre_word])
            pre_group = vocabulary[pre_word].group

            self.words_succsessing[pre_group][word] += len(bigrams)
            self.predecessor_groups_of[word].append(pre_group)

        for succ_word, count in successors:
            succ_group = vocabulary[succ_word].group

            self.words_predecessing[succ_group][word] += count
            self.succsessor_groups_of[word].append(succ_group)

Learner()