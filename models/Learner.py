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

    def __init__(self, corpus):
        self.vocabulary      = defaultdict(WordData)                 # word : WordData
        self.predecessors_of = defaultdict(set)                      # word : {word}
        self.successors_of   = defaultdict(lambda: defaultdict(int)) # word : {word : count}

        self.group_bigramm_counts = defaultdict(int) # group_bigramm_name : count
        self.group_counts         = defaultdict(int) # group_index : count

        self.predecessor_groups_of = defaultdict(set) # word : {pre_group}
        self.succsessor_groups_of  = defaultdict(set) # word : {succ_group}

        self.predecessor_word_count_of_group = defaultdict(int) # group : word_count
        self.succsessor_word_count_of_group  = defaultdict(int) # group : word_count

        self.wordEntropy = 0

        # set up 
        words = self.parse_file(corpus[0])
        self.build_vocabulary(words=words)
        self.setup_inital_data()

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

    def build_vocabulary(self, words):
        """ built vocabulary with word-counts and store predecessors and successors of a word

        The following lists are set up by this method:
        - vocabulary
        - predecessors_of (word)
        - successors_of (word)
        """

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
        - wordEntropy
        """
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
                bigramm_count       = self.successors_of[pre_word][word]
                group_bigramm_name = str(pre_word_group) + '_' + str(wordData.group)

                # count group bigrams
                self.group_bigramm_counts[group_bigramm_name] += bigramm_count

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

        predecessors = self.predecessors_of[word]
        successors   = self.successors_of[word]

        group = self.vocabulary[word].group
        for pre_word in predecessors:
            bigramm_count   = self.successors_of[pre_word][word]
            pre_word_group = self.vocabulary[pre_word].group

            self.succsessor_word_count_of_group[pre_word_group] += bigramm_count
            self.predecessor_groups_of[word].add(pre_word_group)

        for succ_word, count in successors.iteritems():
            succ_word_group = self.vocabulary[succ_word].group

            self.predecessor_word_count_of_group[succ_word_group] += count
            self.succsessor_groups_of[word].add(succ_word_group)

    def remove_word_from_its_group(self, word):
        old_group = self.vocabulary[word].group
        self.vocabulary[word].group = None

        for group in self.predecessor_groups_of[word]:
            if group != old_group:
                group_bigramm_name = str(group) + "_" + str(old_group)
                self.group_bigramm_counts[group_bigramm_name] -= self.succsessor_word_count_of_group[group]

        for group in self.succsessor_groups_of[word]:
            if group != old_group: 
                group_bigramm_name = str(old_group) + "_" + str(group)
                self.group_bigramm_counts[group_bigramm_name] -= self.predecessor_word_count_of_group[group]

        self.group_counts[old_group] -= self.vocabulary[word].count

        self_bigramm_name = str(old_group) + "_" + str(old_group)
        self.group_bigramm_counts[self_bigramm_name] = (self.group_bigramm_counts[self_bigramm_name] 
                                                        - self.succsessor_word_count_of_group[old_group]
                                                        - self.predecessor_word_count_of_group[old_group]
                                                        + self.successors_of[word][word])

        self.predecessor_word_count_of_group[old_group] -= self.successors_of[word][word]
        self.succsessor_word_count_of_group[old_group]  -= self.successors_of[word][word]
    
    def move_word_to_group(self, word, new_group):
        self.vocabulary[word].group = new_group

        group_bigramm_counts = defaultdict(int, {key: val for key, val in self.group_bigramm_counts.iteritems() if val != 0})
        group_counts         = defaultdict(int, {key: val for key, val in self.group_counts.iteritems() if val != 0})

        for group in self.predecessor_groups_of[word]:
            if group != new_group:
                group_bigramm_name = str(group) + "_" + str(new_group)
                group_bigramm_counts[group_bigramm_name] += self.succsessor_word_count_of_group[group]

        for group in self.succsessor_groups_of[word]:
            if group != new_group:
                group_bigramm_name = str(new_group) + "_" + str(group)
                group_bigramm_counts[group_bigramm_name] += self.predecessor_word_count_of_group[group]

        group_counts[new_group] += self.vocabulary[word].count

        self_bigramm_name = str(new_group) + "_" + str(new_group)
        group_bigramm_counts[self_bigramm_name] = (self.group_bigramm_counts[self_bigramm_name] 
                                                        + self.succsessor_word_count_of_group[new_group]
                                                        + self.predecessor_word_count_of_group[new_group]
                                                        - self.successors_of[word][word])

        return (group_bigramm_counts, group_counts)


    def calc_perplexity(self, group_bigramm_counts, group_counts):
        sum1 = sum2 = 0
        for group_bigramm_count in group_bigramm_counts.itervalues():
            if group_bigramm_count > 0:
                sum1 += group_bigramm_count * math.log(group_bigramm_count)

        for group_count in group_counts.itervalues():
            if group_count > 0:
                sum2 += group_count * math.log(group_count)

        return sum1 - 2 * sum2 + self.wordEntropy

    def map_words_to_classes(self):
        perpelxity = self.calc_perplexity(self.group_bigramm_counts, self.group_counts)

        did_update = True
        while did_update:
            did_update = False

            for word in self.vocabulary:
                min_perplexity       = perpelxity
                old_group            = self.vocabulary[word].group
                min_perplexity_group = old_group
                
                self.update_help_counts(word)
                self.remove_word_from_its_group(word)

                for group in self.group_counts:                    
                    if group != old_group:
                        # move word to group without side effects
                        (current_group_bigramm_counts, current_group_counts) = self.move_word_to_group(word, group)
                        temp_perpelxity = self.calc_perplexity(current_group_bigramm_counts, current_group_counts)

                        if temp_perpelxity < min_perplexity:
                            min_perplexity       = temp_perpelxity
                            min_perplexity_group = group

                # move word from its group to group which results in minimum perpelxity permanetly
                (self.group_bigramm_counts, self.group_counts) = self.move_word_to_group(word, min_perplexity_group)
                if min_perplexity_group != old_group:
                    print word + " " + str(old_group) + " -> " + str(min_perplexity_group)
                    perpelxity = min_perplexity
                    did_update = True

            print ("---", perpelxity)

    def print_groups(self):
        groups = defaultdict(list)

        for word, wordData in self.vocabulary.iteritems():
            groups[wordData.group].append(word)

        for group in groups:
            print (group, groups[group])

# Learner(corpus=["../_tests/units/test_corpus"])