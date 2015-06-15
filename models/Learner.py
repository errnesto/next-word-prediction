# coding=utf-8
import codecs
import re
import math
from collections import defaultdict
from operator import itemgetter
from recordtype import recordtype

WordData    = recordtype('WordData', 'count group')
CountedWord = recordtype('PreWord', 'word count')

class Learner():
    """Parses text files to generate n-grams and cathegories

    detailed info here
    """
    INITAL_NUMBER_OF_GROUPS = 20

    vocabulary      = defaultdict(WordData)                 # word : WordData
    predecessors_of = defaultdict(set)                      # word : {word}
    successors_of   = defaultdict(lambda: defaultdict(int)) # word : {word : count}

    group_bigramm_counts = defaultdict(int) # group_bigramm_name : count
    group_counts         = defaultdict(int) # group_index : count

    predecessor_groups_of = defaultdict(set) # word : {pre_group}
    succsessor_groups_of  = defaultdict(set) # word : {succ_group}

    words_predecessing = defaultdict(lambda: defaultdict(int)) # group : {word : count}
    words_succsessing  = defaultdict(lambda: defaultdict(int)) # group : {word : count}

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

            if pre_word != None:
                # store predecessors
                self.predecessors_of[word].add(pre_word)

                # store succsessors with count
                self.successors_of[pre_word][word] += 1

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
            self.group_counts[wordData.group] += 1

            predecessors = self.predecessors_of[word]
            for pre_word in predecessors:
                pre_word_group     = self.vocabulary[pre_word].group
                bigram_count       = self.successors_of[pre_word][word]
                group_bigramm_name = str(pre_word_group) + '_' + str(wordData.group)

                # count group bigrams
                self.group_bigramm_counts[group_bigramm_name] += 1

                # store predecessor groups
                self.predecessor_groups_of[word].add(pre_word_group)

                # store words predecessing group of current word
                self.words_predecessing[wordData.group][pre_word] += 1

            successors = self.successors_of[word]
            for succ_word in successors:
                # store succsessor groups
                succ_word_group = self.vocabulary[succ_word].group
                self.succsessor_groups_of[word].add(succ_word_group)

                # store words succsessing group of current word
                self.words_succsessing[wordData.group][succ_word] += 1

        # calculate value needed for calculating perplexity
        for wordData in self.vocabulary.itervalues():
            self.wordEntropy += wordData.count * math.log(wordData.count)

    def update_help_counts(self, word):
        predecessors = self.predecessors_of[word]
        successors   = self.successors_of[word]

        for pre_word in predecessors:
            bigram_count   = self.successors_of[pre_word][word]
            pre_word_group = self.vocabulary[pre_word].group

            self.words_succsessing[pre_word_group][word] += bigram_count
            self.predecessor_groups_of[word].add(pre_word_group)

        for succ_word, count in successors.iteritems():
            succ_group = self.vocabulary[succ_word].group

            self.words_predecessing[succ_group][word] += count
            self.succsessor_groups_of[word].add(succ_group)

    def move_word(self, word, to_group):
        from_group = self.vocabulary[word].group
        self.vocabulary[word].group = to_group
        self.update_help_counts(word)

        # update counts

        #remove from group
        self.group_counts[from_group] -= self.vocabulary[word].count
        # add to group
        self.group_counts[to_group] += self.vocabulary[word].count

        for group in self.group_counts:
            if group != from_group:
                #remove from group
                group_bigramm_name1 = str(group) + "_" + str(from_group)
                group_bigramm_name2 = str(from_group) + "_" + str(group)
                self.group_bigramm_counts[group_bigramm_name1] -= self.words_succsessing[group][word]
                self.group_bigramm_counts[group_bigramm_name2] -= self.words_predecessing[group][word] 

                #add to group
                group_bigramm_name3 = str(group) + "_" + str(to_group)
                group_bigramm_name4 = str(to_group) + "_" + str(group)
                self.group_bigramm_counts[group_bigramm_name3] += self.words_succsessing[group][word]
                self.group_bigramm_counts[group_bigramm_name4] += self.words_predecessing[group][word]

        #remove from group
        self_bigramm_name = str(from_group) + "_" + str(from_group)
        self.group_bigramm_counts[self_bigramm_name] = self.group_bigramm_counts[self_bigramm_name] 
        - self.words_succsessing[from_group][word] 
        - self.words_predecessing[from_group][word]
        + self.successors_of[word][word]

        # add to groups
        self_bigramm_name = str(to_group) + "_" + str(to_group)
        self.group_bigramm_counts[self_bigramm_name] = self.group_bigramm_counts[self_bigramm_name] 
        + self.words_succsessing[to_group][word] 
        + self.words_predecessing[to_group][word]
        - self.successors_of[word][word]

        print self.group_bigramm_counts

        

    def calc_perplexity(self):
        sum1 = sum2 = 0
        for group_bigramm_count in self.group_bigramm_counts.itervalues():
            if group_bigramm_count > 0:
                sum1 += group_bigramm_count * math.log(group_bigramm_count)

        for group_count in self.group_counts.itervalues():
            if group_count > 0:
                sum2 += group_count * math.log(group_count)

        return sum1 - 2 * sum2 + self.wordEntropy

    def map_words_to_classes(self):
        self.setup_inital_data()
        perpelxity = self.calc_perplexity()

        print self.group_bigramm_counts

        did_update = True
        while did_update:
            did_update = False

            for word in self.vocabulary:
                min_perplexity       = self.calc_perplexity()
                old_group            = self.vocabulary[word].group
                min_perplexity_group = old_group

                for group in self.group_counts:                    
                    if group != old_group:
                        self.move_word(word, group)
                        temp_perpelxity = self.calc_perplexity()

                        if temp_perpelxity < min_perplexity:
                            min_perplexity       = temp_perpelxity
                            min_perplexity_group = group
                            did_update = True   
                        break

                # move word from its group to group which results in minimum perlexity
                perlexity = min_perplexity
                if min_perplexity_group != old_group:
                    print "move word " + word + " from group " + str(old_group) + " to group " + str(min_perplexity_group)
                    self.move_word(word, min_perplexity_group)
                break

            print "----"
            break

Learner()