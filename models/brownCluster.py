import math
import operator
from os import path

class BrownCluster:
    def __init__(self):
        token_file_path = path.join(path.dirname(__file__), "../data/training/tokens.txt")
        f = open(token_file_path)

        content   = f.read()
        f.close
        self.text = content.split()

        # count tokens
        token_counts = {}
        for word in self.text:
            if word not in token_counts:
                token_counts[word] = 1.0
            else:
                token_counts[word] += 1.0

        # create a cluster for each word
        # where cluster 1 contains the most frquent word 
        # and cluster n the least frequent word
        sorted_words         = sorted(token_counts.iteritems(), key=operator.itemgetter(1), reverse=True)
        self.cluster_of_word = {}
        self.clusters        = {}

        for i, word in enumerate(sorted_words):
            self.cluster_of_word[word[0]] = i 
            self.clusters[i]              = [word[0]]

        self.number_of_tokens   = len(token_counts)
        self.number_of_clusters = self.number_of_tokens
        self.calc_cluster_propabilities()

    def calc_cluster_propabilities(self):
        self.cluster_bigramm_propabilities = {}
        self.pre_cluster_propabilities     = {}
        self.cluster_propabilities         = {}

        # count words in clusters and cluster bigrams
        pre_word = None
        for word in self.text:
            if pre_word != None:
                pre_cluster = self.cluster_of_word[pre_word]
                cluster     = self.cluster_of_word[word]

                if pre_cluster in self.pre_cluster_propabilities:
                    self.pre_cluster_propabilities[pre_cluster] += 1.0
                else:
                    self.pre_cluster_propabilities[pre_cluster] = 1.0

                if cluster in self.cluster_propabilities:
                    self.cluster_propabilities[cluster] += 1.0
                else:
                    self.cluster_propabilities[cluster] = 1.0

                cluster_bigramm_name = str(pre_cluster) + '#' + str(cluster)
                if cluster_bigramm_name in self.cluster_bigramm_propabilities:
                    self.cluster_bigramm_propabilities[cluster_bigramm_name] += 1.0
                else:
                    self.cluster_bigramm_propabilities[cluster_bigramm_name] = 1.0

            pre_word = word

        # normalize counts by text length
        # for cluster_index in self.pre_cluster_propabilities:
        #     self.pre_cluster_propabilities[cluster_index] /= self.number_of_clusters
        # for cluster_index in self.cluster_propabilities:
        #     self.cluster_propabilities[cluster_index] /= self.number_of_clusters
        # for cluster_bigramm_name in self.cluster_bigramm_propabilities:
        #     self.cluster_bigramm_propabilities[cluster_bigramm_name] /= self.number_of_clusters

    def calculate_quality(self, clusters_to_check):
        quality = 0.0

        # does only consider most frequent words
        for cluster in range(0, clusters_to_check):
            for other_cluster in range(0, clusters_to_check):
                if (cluster != other_cluster # dont try to merge cluster with itself :-)
                and cluster       in self.pre_cluster_propabilities 
                and other_cluster in self.cluster_propabilities):
                    cluster_bigramm_name = str(cluster) + '#' + str(other_cluster)

                    if cluster_bigramm_name in self.cluster_bigramm_propabilities:
                        a = self.cluster_bigramm_propabilities[cluster_bigramm_name]
                        b = self.pre_cluster_propabilities[cluster] * self.cluster_propabilities[other_cluster]
                        quality += a * math.log(a / b)

        return quality

    def merge(self, c1, c2, permanent=False):
        words_in_c2                   = self.clusters[c2]
        c2_pre_propability            = None
        c2_propability                = None
        cluster_preceding_c2_counts   = {}
        cluster_succsessing_c2_counts = {}

        if permanent:
            self.clusters[c1].extend(words_in_c2)

        for word in words_in_c2:
            self.cluster_of_word[word] = c1

        if c2 in self.pre_cluster_propabilities:
            c2_pre_propability = self.pre_cluster_propabilities.pop(c2)
            
            if c1 in self.pre_cluster_propabilities:
                self.pre_cluster_propabilities[c1] += c2_pre_propability
            else:
                self.pre_cluster_propabilities[c1] = c2_pre_propability

        if c2 in self.cluster_propabilities:
            c2_propability = self.cluster_propabilities.pop(c2)

            if c1 in self.cluster_propabilities:
                self.cluster_propabilities[c1] += c2_propability
            else:
                self.cluster_propabilities[c1] = c2_propability

        for cluster in self.clusters:
            cluster_bigramm_name1 = str(cluster) + '#' + str(c2)
            if cluster_bigramm_name1 in self.cluster_bigramm_propabilities:
                cluster_preceding_c2_counts[cluster] = self.cluster_bigramm_propabilities.pop(cluster_bigramm_name1)

                cluster_bigramm_name2 = str(cluster) + '#' + str(c1)
                if cluster_bigramm_name2 in self.cluster_bigramm_propabilities:
                    self.cluster_bigramm_propabilities[cluster_bigramm_name2] += cluster_preceding_c2_counts[cluster]
                else:
                    self.cluster_bigramm_propabilities[cluster_bigramm_name2] = cluster_preceding_c2_counts[cluster]

        for cluster in self.clusters:
            cluster_bigramm_name1 = str(c2) + '#' + str(cluster)
            if cluster_bigramm_name1 in self.cluster_bigramm_propabilities:
                cluster_succsessing_c2_counts[cluster] = self.cluster_bigramm_propabilities.pop(cluster_bigramm_name1)

                cluster_bigramm_name2 = str(c1) + '#' + str(cluster)
                if cluster_bigramm_name2 in self.cluster_bigramm_propabilities:
                    self.cluster_bigramm_propabilities[cluster_bigramm_name2] += cluster_succsessing_c2_counts[cluster]
                else:
                    self.cluster_bigramm_propabilities[cluster_bigramm_name2] = cluster_succsessing_c2_counts[cluster]

        if permanent:
            del self.clusters[c2]
        return words_in_c2, c2_pre_propability, c2_propability, cluster_preceding_c2_counts, cluster_succsessing_c2_counts

    def tmp_break(self, c1, c2, tmp):
        words_in_c2                   = tmp[0]
        c2_pre_propability            = tmp[1]
        c2_propability                = tmp[2]
        cluster_preceding_c2_counts   = tmp[3]
        cluster_succsessing_c2_counts = tmp[4]

        for word in words_in_c2:
            self.cluster_of_word[word] = c2

        if c2_pre_propability != None:
            self.pre_cluster_propabilities[c1] -= c2_pre_propability
            if self.pre_cluster_propabilities[c1] == 0:
                del self.pre_cluster_propabilities[c1]

            self.pre_cluster_propabilities[c2] = c2_pre_propability

        if c2_propability != None:
            self.cluster_propabilities[c1] -= c2_propability
            if self.cluster_propabilities[c1] == 0: # ? !=
                del self.cluster_propabilities[c1]

            self.cluster_propabilities[c2] = c2_propability

        for cluster in self.clusters:
            cluster_bigramm_name1 = str(cluster) + '#' + str(c2)
            if cluster_bigramm_name1 in self.cluster_bigramm_propabilities:
                self.cluster_bigramm_propabilities[cluster_bigramm_name1] = cluster_preceding_c2_counts[cluster]

                cluster_bigramm_name2 = str(cluster) + '#' + str(c1)
                self.cluster_bigramm_propabilities[cluster_bigramm_name2] -= cluster_preceding_c2_counts[cluster]
                if self.cluster_bigramm_propabilities[cluster_bigramm_name2] == 0:
                    del self.cluster_bigramm_propabilities[cluster_bigramm_name2]

        for cluster in self.clusters:
            cluster_bigramm_name1 = str(c2) + '#' + str(cluster)
            if cluster_bigramm_name1 in self.cluster_bigramm_propabilities:
                self.cluster_bigramm_propabilities[cluster_bigramm_name1] = cluster_succsessing_c2_counts[cluster]

                cluster_bigramm_name2 = str(c1) + '#' + str(cluster)
                self.cluster_bigramm_propabilities[cluster_bigramm_name2] -= cluster_succsessing_c2_counts[i]
                if self.cluster_bigramm_propabilities[cluster_bigramm_name2] == 0:
                    del self.cluster_bigramm_propabilities[cluster_bigramm_name2]

    def cluster_words(self, desired_number_of_clusters=1000, m=1000):
        iterations = 0
        while self.number_of_clusters > desired_number_of_clusters:
            iterations += 1
            print '\nNow there are', self.number_of_clusters, 'clusters'
            maximum_quality   = -1e5
            cluster_to_merge1 = 0
            cluster_to_merge2 = 0

            clusters_to_check = min(m + iterations, self.number_of_tokens)
            for cluster in range(0, clusters_to_check):
                for other_cluster in range(0, clusters_to_check):
                    if cluster != other_cluster and cluster in self.clusters and other_cluster in self.clusters:
                        tmp = self.merge(cluster, other_cluster)
                        self.calc_cluster_propabilities()

                        quality = self.calculate_quality(clusters_to_check)
                        self.tmp_break(cluster, other_cluster, tmp)
                        print cluster, other_cluster, quality

                        if quality > maximum_quality:
                            cluster_to_merge1 = cluster
                            cluster_to_merge2 = other_cluster
                            maximum_quality   = quality

            self.merge(cluster_to_merge1, cluster_to_merge2, permanent=True)
            print '\n', cluster_to_merge1, cluster_to_merge2, self.clusters[cluster_to_merge1]
            self.number_of_clusters -= 1

BC = BrownCluster()
BC.cluster_words(desired_number_of_clusters=20, m=500)