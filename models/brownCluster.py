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
        self.cluster_transition_propabilities = defaultdict(lambda: defaultdict(float))
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
                self.cluster_transition_propabilities[pre_cluster_name][cluster_name] += 1
            
            pre_word = word

        # normalize counts by text length
        for cluster_index in self.cluster_propabilities:
            self.cluster_propabilities[cluster_index] /= self.text_length
        for cluster_index1 in self.cluster_transition_propabilities:
            for cluster_index2 in self.cluster_transition_propabilities[cluster_index1]:
                self.cluster_transition_propabilities[cluster_index1][cluster_index2] /= self.text_length

    def build_graph(self):
        for cluster in self.clusters:
            for other_cluster in self.clusters:
                edge_weight = self.calc_edge_weight(cluster.name, other_cluster.name)
                if edge_weight != 0:
                    cluster.edges[other_cluster.name] = edge_weight

        for cluster in self.clusters:
            cluster.calc_node_weight()

    def calc_edge_weight(self, cluster_name, other_cluster_name):
        a = self.cluster_propabilities[cluster_name] * self.cluster_propabilities[other_cluster_name]
        b = self.cluster_transition_propabilities[cluster_name][other_cluster_name] / a

        d = 0
        if b != 0:
            d = self.cluster_transition_propabilities[cluster_name][other_cluster_name] * math.log(b)

        if (cluster_name == other_cluster_name):
            return d 
        else:
            c = self.cluster_transition_propabilities[other_cluster_name][cluster_name] / a
            e = 0
            if c != 0:
                e = self.cluster_transition_propabilities[other_cluster_name][cluster_name] * math.log(c)
            return d + e

    def calc_potential_loss(self):
        for cluster in self.clusters:
            for other_cluster in self.clusters:
                merged_node_weight = self.calc_merged_node_weight(cluster, other_cluster)
                loss = cluster.node_weight + other_cluster.node_weight - cluster.edges[other_cluster.name] - merged_node_weight

    def calc_merged_node_weight(self, clusterA, clusterB):
        adjacent_clusters = set(clusterA.edges.keys() + clusterB.edges.keys())
        merged_node_weight = 0

        for other_cluster in adjacent_clusters:
            transition_propability_other_to_merged = self.cluster_transition_propabilities[other_cluster][clusterA.name] \
                                                     + self.cluster_transition_propabilities[other_cluster][clusterB.name]
            transition_propability_merged_to_other = self.cluster_transition_propabilities[clusterA.name][other_cluster] \
                                                     + self.cluster_transition_propabilities[clusterB.name][other_cluster]
            other_propabilities = self.cluster_propabilities[other_cluster] \
                                  * (self.cluster_propabilities[clusterA.name] + self.cluster_propabilities[clusterB.name])

            quality_other_to_merged = transition_propability_other_to_merged \
                                      * math.log(transition_propability_other_to_merged / other_propabilities)
            quality_merged_to_other = transition_propability_merged_to_other \
                                      * math.log(transition_propability_merged_to_other / other_propabilities)
            merged_node_weight += quality_other_to_merged + quality_merged_to_other

        return merged_node_weight

class Cluster():
    def __init__(self, name, words):
        self.name        = name
        self.words       = words
        self.edges       = {} # cluster : weight
        self.node_weight = 0

    def calc_node_weight(self):
        for edge_weight in self.edges.itervalues():
            self.node_weight += edge_weight

BrownCluster()