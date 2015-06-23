import math
import operator
from os import path
from collections import defaultdict

class BrownCluster:
    def __init__(self):
        token_file_path = path.join(path.dirname(__file__), "../data/training/tokens.txt")
        f = open(token_file_path)

        content   = f.read()
        f.close
        self.text = content.split()

        self.LCC                              = {} # merged_clusters_name : total graph weight change
        self.clusters                         = [] # list of clusters
        self.clusters_by_word                 = {}
        self.cluster_transition_propabilities = defaultdict(float)
        self.cluster_propabilities            = defaultdict(float)
        self.text_length                      = len(self.text)

        self.set_up_counts()
        self.build_graph()

        for cluster in self.clusters:
            print cluster.words[0], cluster.edges

    def set_up_counts(self):
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
        sorted_words = sorted(token_counts.iteritems(), key=operator.itemgetter(1), reverse=True)
        for i, word in enumerate(sorted_words):
            cluster = Cluster(name=i, words=[word[0]])
            self.clusters.append(cluster)
            self.clusters_by_word[word[0]] = cluster        

        # cluster propabilities
        pre_word = None
        for word in self.text:
            cluster_name = self.clusters_by_word[word].name
            self.cluster_propabilities[cluster_name] += 1

            if pre_word != None:
                pre_cluster_name = self.clusters_by_word[pre_word].name
                cluster_transiton_name = str(pre_cluster_name) + '_' + str(cluster_name)
                self.cluster_transition_propabilities[cluster_transiton_name] += 1
            
            pre_word = word

        # normalize counts by text length
        for cluster_index in self.cluster_propabilities:
            self.cluster_propabilities[cluster_index] /= self.text_length
        for cluster_transiton_name in self.cluster_transition_propabilities:
            self.cluster_transition_propabilities[cluster_transiton_name] /= self.text_length

    def build_graph(self):
        for cluster in self.clusters:
            for other_cluster in self.clusters:
                edge_weight = self.calc_edge_weight(cluster.name, other_cluster.name)
                if edge_weight != 0:
                    cluster.edges[other_cluster.name] = edge_weight

    def calc_edge_weight(self, cluster, other_cluster):
        cluster_transiton_name1 = str(cluster) + '_' + str(other_cluster)
        cluster_transiton_name2 = str(other_cluster) + '_' + str(cluster)

        a = self.cluster_propabilities[cluster] * self.cluster_propabilities[other_cluster]
        b = self.cluster_transition_propabilities[cluster_transiton_name1] / a

        d = 0
        if b != 0:
            d = self.cluster_transition_propabilities[cluster_transiton_name1] * math.log(b)

        if (cluster == other_cluster):
            return d 
        else:
            c = self.cluster_transition_propabilities[cluster_transiton_name2] / a
            e = 0
            if c != 0:
                e = self.cluster_transition_propabilities[cluster_transiton_name2] * math.log(c)
            return d + e


class Cluster():
    def __init__(self, name, words):
        self.name  = name
        self.words = words
        self.edges = {} # cluster : weight

BrownCluster()