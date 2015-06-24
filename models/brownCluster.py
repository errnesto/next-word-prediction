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

        self.clusters                         = [] # list of clusters
        self.clusters_by_word                 = {}
        self.cluster_transition_propabilities = defaultdict(lambda: defaultdict(float))
        self.cluster_propabilities            = defaultdict(float)
        self.text_length                      = len(self.text)
        self.potential_deltas                 = {}

        self.main()

        for cluster in self.clusters:
            print cluster.words, cluster.name

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
            cluster.edges = defaultdict(float)
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

    def update_propabilities(self):
        self.cluster_transition_propabilities = defaultdict(lambda: defaultdict(float))
        self.cluster_propabilities            = defaultdict(float)
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

    def init_deltas(self):
        max_loss = 0
        for cluster in self.clusters:
            for other_cluster in self.clusters:
                if other_cluster > cluster: # loss(a_b) == loss(b_a) so dont calculate twice | loss(a_a) would be doing nothing
                   self.set_delta_for(cluster, other_cluster) 

    def set_delta_for(self, cluster, other_cluster):
        merged_node_weight = self.calc_merged_node_weight(cluster, other_cluster)

        loss = cluster.node_weight + other_cluster.node_weight - cluster.edges[other_cluster.name] - merged_node_weight
        self.potential_deltas[loss] = (cluster, other_cluster)

    def get_max_delta(self):
        losses  = sorted(self.potential_deltas.keys())
        max_key = losses[-1]

        return self.potential_deltas[max_key]

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
            quality_other_to_merged = 0
            if transition_propability_other_to_merged > 0:
                quality_other_to_merged = transition_propability_other_to_merged \
                                          * math.log(transition_propability_other_to_merged / other_propabilities)
            quality_merged_to_other = 0
            if transition_propability_merged_to_other > 0:
                quality_merged_to_other = transition_propability_merged_to_other \
                                          * math.log(transition_propability_merged_to_other / other_propabilities)
            merged_node_weight += quality_other_to_merged + quality_merged_to_other

        return merged_node_weight

    def main(self):
        self.set_up_counts()
        self.build_graph()
        self.init_deltas()

        i = 5
        while i > 2:
            c1, c2 = self.get_max_delta()

            merged_cluster = Cluster(name=len(self.clusters), words=c1.words + c2.words)
            for word in c1.words:
                self.clusters_by_word[word] = merged_cluster
            for word in c2.words:
                self.clusters_by_word[word] = merged_cluster

            self.clusters.remove(c1)
            self.clusters.remove(c2)
            self.clusters.append(merged_cluster)

            self.update_propabilities()
            for cluster in self.clusters:
                for other_cluster in self.clusters:
                    if other_cluster > cluster and cluster != c1 and cluster != c2:
                        print cluster.name, other_cluster.name
            i -= 1

class Cluster():
    def __init__(self, name, words):
        self.name        = name # int
        self.words       = words # list
        self.edges       = defaultdict(float) # cluster : weight
        self.node_weight = 0.0

    def calc_node_weight(self):
        for edge_weight in self.edges.itervalues():
            self.node_weight += edge_weight

BrownCluster()