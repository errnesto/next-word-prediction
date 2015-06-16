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

    predecessor_word_count_of_group = defaultdict(int) # group : word_count
    succsessor_word_count_of_group  = defaultdict(int) # group : word_count

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
            self.group_counts[wordData.group] += wordData.count

            predecessors = self.predecessors_of[word]
            for pre_word in predecessors:
                pre_word_group     = self.vocabulary[pre_word].group
                bigram_count       = self.successors_of[pre_word][word]
                group_bigramm_name = str(pre_word_group) + '_' + str(wordData.group)

                # count group bigrams
                self.group_bigramm_counts[group_bigramm_name] += bigram_count

                # store predecessor groups
                self.predecessor_groups_of[word].add(pre_word_group)

            successors = self.successors_of[word]
            for succ_word in successors:
                # store succsessor groups
                succ_word_group = self.vocabulary[succ_word].group
                self.succsessor_groups_of[word].add(succ_word_group)

        # calculate value needed for calculating perplexity
        for wordData in self.vocabulary.itervalues():
            self.wordEntropy += wordData.count * math.log(wordData.count)

    def update_help_counts(self, word):
        self.predecessor_word_count_of_group = defaultdict(int)
        self.succsessor_word_count_of_group  = defaultdict(int)
        self.predecessor_groups_of[word]     = set()
        self.succsessor_groups_of[word]      = set()

        predecessors = self.predecessors_of[word]
        successors   = self.successors_of[word]

        group = self.vocabulary[word].group
        for pre_word in predecessors:
            bigram_count   = self.successors_of[pre_word][word]
            pre_word_group = self.vocabulary[pre_word].group

            self.succsessor_word_count_of_group[pre_word_group] += bigram_count
            self.predecessor_groups_of[word].add(pre_word_group)

        for succ_word, count in successors.iteritems():
            succ_word_group = self.vocabulary[succ_word].group

            self.predecessor_word_count_of_group[succ_word_group] += count
            self.succsessor_groups_of[word].add(succ_word_group)
        
    def move_word(self, word, new_group):
        old_group = self.vocabulary[word].group
        self.vocabulary[word].group = new_group

        for group in self.predecessor_groups_of[word]:
            if group != old_group:
                group_bigramm_name = str(group) + "_" + str(old_group)
                self.group_bigramm_counts[group_bigramm_name] -= self.succsessor_word_count_of_group[group]

            if group != new_group:
                group_bigramm_name = str(group) + "_" + str(new_group)
                self.group_bigramm_counts[group_bigramm_name] += self.succsessor_word_count_of_group[group]

        for group in self.succsessor_groups_of[word]:
            if group != old_group: 
                group_bigramm_name = str(old_group) + "_" + str(group)
                self.group_bigramm_counts[group_bigramm_name] -= self.predecessor_word_count_of_group[group]

            if group != new_group:
                group_bigramm_name = str(new_group) + "_" + str(group)
                self.group_bigramm_counts[group_bigramm_name] += self.predecessor_word_count_of_group[group]

        self.group_counts[old_group] -= self.vocabulary[word].count
        self.group_counts[new_group] += self.vocabulary[word].count

        self_bigramm_name = str(old_group) + "_" + str(old_group)
        self.group_bigramm_counts[self_bigramm_name] = (self.group_bigramm_counts[self_bigramm_name] 
                                                        - self.succsessor_word_count_of_group[old_group]
                                                        - self.predecessor_word_count_of_group[old_group]
                                                        + self.successors_of[word][word])

        self_bigramm_name = str(new_group) + "_" + str(new_group)
        self.group_bigramm_counts[self_bigramm_name] = (self.group_bigramm_counts[self_bigramm_name] 
                                                        + self.succsessor_word_count_of_group[new_group]
                                                        + self.predecessor_word_count_of_group[new_group]
                                                        - self.successors_of[word][word])

        self.predecessor_word_count_of_group[old_group] -= self.successors_of[word][word]
        self.succsessor_word_count_of_group[old_group]  -= self.successors_of[word][word]
        self.predecessor_word_count_of_group[new_group] += self.successors_of[word][word]
        self.succsessor_word_count_of_group[new_group]  += self.successors_of[word][word]


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

        did_update = True
        while did_update:
            did_update = False
            print self.group_bigramm_counts

            for word in self.vocabulary:
                min_perplexity       = perpelxity
                old_group            = self.vocabulary[word].group
                min_perplexity_group = old_group
                
                self.update_help_counts(word)

                for group in self.group_counts:                    
                    if group != old_group:
                        self.move_word(word, group)
                        temp_perpelxity = self.calc_perplexity()

                        if temp_perpelxity < min_perplexity:
                            min_perplexity       = temp_perpelxity
                            min_perplexity_group = group   

                # move word from its group to group which results in minimum perpelxity
                perpelxity = min_perplexity
                
                self.move_word(word, min_perplexity_group)
                if min_perplexity_group != old_group:
                    print "move " + word + " from group " + str(old_group) + " to group " + str(min_perplexity_group)
                    did_update = True
            print ("---", perpelxity)
            print self.group_bigramm_counts
            break

    def print_gropus(self):
        groups = defaultdict(list)

        for word, wordData in self.vocabulary.iteritems():
            groups[wordData.group].append(word)

        for group in groups:
            print (group, groups[group])

    def stupid_test(self):
        self.setup_inital_data()

        print self.group_bigramm_counts
        print ("3:", self.group_counts[3], "2")
        print ("0:", self.group_counts[0], "13")
        print ("0_0:", self.group_bigramm_counts["0_0"], "5")
        print ("0_3:", self.group_bigramm_counts["0_3"], "2")
        print ("3_17:", self.group_bigramm_counts["3_17"], "1")
        print ("0_17:", self.group_bigramm_counts["0_17"], "0")
        print ("0_1:", self.group_bigramm_counts["0_1"], "1")

        print "---- Altweibersommer from 3 to 0"
        self.update_help_counts("Altweibersommer")
        self.move_word("Altweibersommer", 0)
        print ("3:", self.group_counts[3], "0")
        print ("0:", self.group_counts[0], "15")
        print ("0_0:", self.group_bigramm_counts["0_0"], "7")
        print ("3_17:", self.group_bigramm_counts["3_17"], "0")
        print ("0_17:", self.group_bigramm_counts["0_17"], "1")
        print ("0_1:", self.group_bigramm_counts["0_1"], "2")
        print ("0_2:", self.group_bigramm_counts["0_2"], "1")
        

        print "---- Altweibersommer from 0 to 2"
        self.move_word("Altweibersommer", 2)
        print self.succsessor_word_count_of_group[0]
        print ("0:", self.group_counts[0], "13")
        print ("2:", self.group_counts[2], "4")
        print ("0_2:", self.group_bigramm_counts["0_2"], "3")
        print ("3_17:", self.group_bigramm_counts["3_17"], "0")
        print ("2_17:", self.group_bigramm_counts["2_17"], "1")
        print ("2_1:", self.group_bigramm_counts["2_1"], "1")

        print "---- Altweibersommer from 2 to 1"
        self.move_word("Altweibersommer", 1)
        print "----"
        print self.group_bigramm_counts
        print ("2:", self.group_counts[2], "2")
        print ("1:", self.group_counts[1], "6")
        print ("0_3:", self.group_bigramm_counts["0_3"], "0")
        print ("3_17:", self.group_bigramm_counts["3_17"], "0")
        print ("0_1:", self.group_bigramm_counts["0_1"], "3")
        print ("1_17:", self.group_bigramm_counts["1_17"], "1")


Learner()