# coding=utf-8
import codecs
import re
import math
from operator import itemgetter
from recordtype import recordtype

WordData = recordtype('WordData', 'count group')
PreWord  = recordtype('PreWord', 'word count')

class Learner():
    """Parses text files to generate n-grams and cathegories

    detailed info here
    """

    # comments in the form key : value

    vocabulary      = {} # word : WordData
    predecessors_of = {} # word : PreWord

    group_bigramm_counts = {} # group_bigramm_name : count
    group_counts         = {} # group_index : count

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

        pre_word = None
        for word in words:
            # add to vocabulary with count and class 0
            if word in self.vocabulary:
                self.vocabulary[word].count += 1
            else:
                self.vocabulary[word] = WordData(1, 0) #we use integers for group names

            # store predecessors
            if word in self.predecessors_of:
                found = False
                for pre in self.predecessors_of[word]:
                    if pre.word == pre_word:
                        pre.count += 1
                        found = True
                        break

                if not found and pre_word != None:
                    self.predecessors_of[word].append(PreWord(pre_word, 1))
            elif pre_word != None:
                self.predecessors_of[word] = [PreWord(pre_word, 1)]

            pre_word = word
        

    def map_words_to_classes(self):
        INITAL_NUMBER_OF_GROUPS = 100
        sorted_vocabulary       = sorted(self.vocabulary.items(), key=lambda x: x[1].count, reverse=True)
        most_freguent_words     = sorted_vocabulary[:INITAL_NUMBER_OF_GROUPS - 1]

        # assign a gruop to each of the most frequent words
        for group, wordTuple in enumerate(most_freguent_words):
            word = wordTuple[0]
            self.vocabulary[word].group = group + 1 # all other words are in group 0 so we start with group 1

        i = 0
        while i < 1:
            i += 1

            for word in self.vocabulary:
                print word
                min_perplexity       = self.calc_perplexity()
                min_perplexity_group = self.vocabulary[word].group

                for group in self.group_counts:
                    # move word to other group
                    if group != self.vocabulary[word].group:
                        self.vocabulary[word].group = group

                    perpelxity = self.calc_perplexity()
                    if perpelxity < min_perplexity:
                        min_perplexity       = perpelxity
                        min_perplexity_group = group

                # move word from its group to group which results in minimum perlexity
                self.vocabulary[word].group = min_perplexity_group

    def calc_perplexity(self):
        self.count_groups()
        sum1 = sum2 = sum3 = 0
        for group_bigramm_count in self.group_bigramm_counts.itervalues():
            sum1 += group_bigramm_count * math.log(group_bigramm_count)

        for group_count in self.group_counts.itervalues():
            sum2 += group_count * math.log(group_count)

        # TO DO: this does not change
        for wordData in self.vocabulary.itervalues():
            sum2 += wordData.count * math.log(wordData.count)

        return sum1 - 2 * sum2 + sum3
        
    def count_groups(self):
        for word, wordData in self.vocabulary.iteritems():
            if wordData.group in self.group_counts:
                self.group_counts[wordData.group] += 1
            else:
                self.group_counts[wordData.group] = 1

            # count group bigrams
            predecessors = self.predecessors_of[word]
            for pre_word in predecessors:
                pre_group = self.vocabulary[pre_word.word].group
                group_bigramm_name = str(pre_group) + '_' + str(wordData.group)

                if group_bigramm_name in self.group_bigramm_counts:
                    self.group_bigramm_counts[group_bigramm_name] += pre_word.count
                else:
                    self.group_bigramm_counts[group_bigramm_name] = pre_word.count


Learner()