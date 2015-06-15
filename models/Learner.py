# coding=utf-8
import codecs
import re
import math
from operator import itemgetter
from recordtype import recordtype

WordData    = recordtype('WordData', 'count group')
CountedWord = recordtype('PreWord', 'word count')

class Learner():
    """Parses text files to generate n-grams and cathegories

    detailed info here
    """
    INITAL_NUMBER_OF_GROUPS = 20

    # comments in the form key : value

    vocabulary      = {} # word : WordData
    predecessors_of = {} # word : {word}
    successors_of   = {} # word : {word : count}

    group_bigramm_counts = {} # group_bigramm_name : count
    group_counts         = {} # group_index : count

    predecessor_groups_of = {} # word : {pre_group}
    succsessor_groups_of  = {} # word : {succ_group}

    words_predecessing = {} # group : {word : count}
    words_succsessing  = {} # group : {word : count}

    wordEntropy = 0

    def __init__(self):
        self.map_words_to_classes()

    def parse_file(self, file_path):
        """takes a path to a file in "Document Format" and returns a array of words

        see http://medialab.di.unipi.it/wiki/Document_Format for information about the "Document Format"
        """

        f = codecs.open(file_path, mode="r", encoding="utf-8")
        content = f.read()

        # strip xml <doc> tags
        content = re.sub(r"<doc.*>|<\/doc>", "", content)

        # strip special characters. Note that "." is not removed yet
        content = re.sub(u'[\]\[!"“„#$%&\\\'()*+,\/:;<=>?@\^_`{|}~-]', "", content)

        # find boundaries of sentences
        content = re.sub(ur"([a-z])\.\s([A-Z0-9])", r"\1 <S/> \2", content)
        content = re.sub(ur"\.$|^\b", " <S/> ", content, flags=re.MULTILINE)

        # TO DO:
        # maybe add a list of common abbrevations to remove spaces from them here

        words = content.split()

        return words

    def build_vocabulary(self):
        """ built vocabulary with word-counts and store predecessors and successors of a word

        The following lists are set up by this method:
        - vocabulary
        - predecessors_of (word)
        - successors_of (word)
        """
        words = self.parse_file("wiki_00")

        pre_word = None
        for word in words:
            # add to vocabulary with count and class 0
            wordData = self.vocabulary.get(word, WordData(0, 0)) # default is -> count: 0, group: 0
            wordData.count += 1
            self.vocabulary[word] = wordData

            # store predecessors
            if pre_word != None:
                old_predecessors = self.predecessors_of.get(word, {pre_word})
                self.predecessors_of[word] = old_predecessors.add(pre_word)

                # store succsessors with count
                old_successors       = self.successors_of.get(pre_word, {})
                old_successors_count = old_successors.get(word, 0)

                self.successors_of[pre_word]       = old_successors
                self.successors_of[pre_word][word] = old_successors_count + 1

            pre_word = word        

    def setup_inital_data(self):
        """ assign words to innital groups and build lists needed for group mapping

        The following lists or values are set up by this method:
        - group_counts
        - group_bigramm_counts
        - predecessor_groups_of (word)
        - succsessor_groups_of (word)
        - words_predecessing (group)
        - words_succsessing (group)
        - wordEntropy
        """
        self.build_vocabulary()
        sorted_vocabulary   = sorted(self.vocabulary.items(), key=lambda x: x[1].count, reverse=True)
        most_freguent_words = sorted_vocabulary[:self.INITAL_NUMBER_OF_GROUPS - 1]

        # assign a gruop to each of the most frequent words
        for group, wordTuple in enumerate(most_freguent_words):
            word = wordTuple[0]
            self.vocabulary[word].group = group + 1 # all other words are in group 0 so we start with group 1

        for word, wordData in self.vocabulary.iteritems():
            #count groups
            old_group_count = self.group_counts.get(wordData.group, 0)
            self.group_counts[wordData.group] = old_group_count + 1

            predecessors = self.predecessors_of[word]
            for pre_word in predecessors:
                pre_word_group     = self.vocabulary[pre_word].group
                bigram_count       = self.successors_of[pre_word][word]
                group_bigramm_name = str(pre_word_group) + '_' + str(wordData.group)

                # count group bigrams
                old_bigram_count = self.group_bigramm_counts.get(group_bigramm_name, 0)
                self.group_bigramm_counts[group_bigramm_name] = old_bigram_count + 1

                # store predecessor groups
                old_predecessor_groups = self.predecessor_groups_of.get(word, set())
                self.predecessor_groups_of[word] = predecessor_groups.add(pre_word_group)

                # store words predecessing group of current word
                old_pre_words_of_group = self.words_predecessing.get(wordData.group, {})
                old_pre_words_count    = old_pre_words_of_group.get(pre_word, 0)

                self.words_predecessing[wordData.group]           = old_pre_words_of_group
                self.words_predecessing[wordData.group][pre_word] = old_pre_words_count + 1

            successors = self.successors_of[word]
            for succ_word in successors:
                # store succsessor groups
                succ_word_group = self.vocabulary[succ_word].group
                old_word_set    = self.succsessor_groups_of.get(word, set())

                self.succsessor_groups_of[word] = old_word_set.add(succ_word_group)

                # store words succsessing group of current word
                old_succ_words_of_group = self.words_succsessing.get(wordData.group, {})
                old_succ_word_count     = old_succ_words_of_group.get(succ_word, 0)

                self.words_succsessing[wordData.group]            = old_succ_words_of_group
                self.words_succsessing[wordData.group][succ_word] = old_succ_word_count + 1


        # calculate value needed for calculating perplexity
        for wordData in self.vocabulary.itervalues():
            self.wordEntropy += wordData.count * math.log(wordData.count)

    def update_help_counts(self, word):
        predecessors = self.predecessors_of[word]
        successors   = self.successors_of[word]

        for pre_word in predecessors:
            bigram_count   = self.successors_of[pre_word][word]
            pre_word_group = vocabulary[pre_word].group

            self.words_succsessing[pre_word_group][word] += bigram_count
            self.predecessor_groups_of[word].add(pre_word_group)

        for succ_word, count in successors:
            succ_group = vocabulary[succ_word].group

            self.words_predecessing[succ_group][word] += count
            self.succsessor_groups_of[word].add(succ_group)

    def calc_perplexity(self):
        sum1 = sum2 = 0
        for group_bigramm_count in self.group_bigramm_counts.itervalues():
            sum1 += group_bigramm_count * math.log(group_bigramm_count)

        for group_count in self.group_counts.itervalues():
            sum2 += group_count * math.log(group_count)

        return sum1 - 2 * sum2 + self.wordEntropy

    def map_words_to_classes(self):
        self.setup_inital_data()
        perpelxity = self.calc_perplexity()

        i = 0
        while i < 1:
            i += 1

            for word in self.vocabulary:
                print word
                min_perplexity       = perpelxity
                min_perplexity_group = self.vocabulary[word].group

                for group in self.group_counts:
                    # move word to other group
                    if group != self.vocabulary[word].group:
                        self.vocabulary[word].group = group

                    temp_perpelxity = self.calc_perplexity()
                    if temp_perpelxity < min_perplexity:
                        min_perplexity       = temp_perpelxity
                        min_perplexity_group = group

                # move word from its group to group which results in minimum perlexity
                perlexity                   = min_perplexity
                self.vocabulary[word].group = min_perplexity_group

Learner()