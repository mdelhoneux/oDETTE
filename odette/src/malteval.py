#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#description	:Wrapper around MaltEval to facilitate writing to tables
#usage			:python malteval.py gold test [tag: for pos tagging accuracy - parsing accuracy by default"
#Python version :2.7.6
#==============================================================================


import config
import os
import sys
import numpy as np

class Malteval(object):
    #TODO: there's a lot of removal potential here!! Lot of repetitions
    def __init__(self, location=config.malteval):
        self._location = location

    def accuracy(self,gold,test, exclude_punct=True, maxSenLen=None, minSenLen=None):
        """UAS and LAS of test on gold"""
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --row-header 0 --tab 1 --header-info 0 --Metric 'LAS;UAS'"%(self._location,gold,test)
        if exclude_punct:
            cmd += " --ExcludeUnicodePunc 1"
        if maxSenLen:
            cmd += " --MaxSentenceLength " + str(maxSenLen)
        if minSenLen:
            cmd += " --MinSentenceLength " + str(minSenLen)
        res = os.popen(cmd)
        accuracies = [line for line in res][2].strip("\n")
        #import ipdb;ipdb.set_trace()
        UAS, LAS= accuracies.split("\t")[:2]
        try:
            UAS, LAS = str(100*float(UAS)), str(100*float(LAS))
        #TODO: better fix this is hacky
        except ValueError:
            return None, None
        return UAS, LAS

    def significance(self,gold,baseline,test):
        """output: ** for p<.01 * for p<.05 and empty string otherwise"""
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s %s --row-header 0 --tab 1 --header-info 0 --stat 1 --GroupBy Token:accuracy"%(self._location,gold,baseline, test)
        res = [line for line in os.popen(cmd)]
        p_0_1 = int(res[20].split("\t")[1])
        p_0_5 = int(res[24].split("\t")[1])
        if p_0_1: return "**"
        elif p_0_5: return "*"
        else: return ""

    def significance_uas(self,gold,baseline,test):
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s %s --row-header 0 --tab 1 --header-info 0 --stat 1 --GroupBy Token:accuracy --Metric 'UAS'"%(self._location,gold,baseline, test)
        res = [line for line in os.popen(cmd)]
        p_0_1 = int(res[20].split("\t")[1])
        p_0_5 = int(res[24].split("\t")[1])
        if p_0_1: return "p_0_1"
        elif p_0_5: return "p_0_5"
        else: return False


    def non_projectivity(self,gold,test):
        """Percentage of non-projective structures in gold and test set"""
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --GroupBy ArcProjectivity:all  --row-header 0 --tab 1 --header-info 0"%(self._location,gold,test)
        res = os.popen(cmd)
        matrix =  [[value for value in line.split("\t")] for line in res][2:]
        if len(matrix) == 1: return (0.,0.) #0 non-projectivity
        non_proj_gold = float(matrix[0][3])
        proj_gold = float(matrix[1][3])
        gold_proj_percentage = non_proj_gold/(non_proj_gold + proj_gold)
        non_proj_test = float(matrix[0][2])
        proj_test = float(matrix[1][2])
        test_proj_percentage = non_proj_test/(non_proj_test + proj_test)
        return gold_proj_percentage,test_proj_percentage

    def deprel_matrix(self,gold,test):
        """Matrix of accuracy of dependency relations"""
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --GroupBy Deprel:all --tab 1 --header-info 0"%(self._location,gold,test)
        res = os.popen(cmd)
        return [[value for value in line.split("\t")] for line in res][2:]

    def pos_matrix(self,gold,test):
        """Matrix of accuracy of dependency relations"""
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --GroupBy Cpostag:all --tab 1 --header-info 0 "%(self._location,gold,test)
        res = os.popen(cmd)
        return [[value for value in line.split("\t")] for line in res][2:]

    def relation_length(self,gold,test):
        #cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --GroupBy RelationLength --tab 1 --header-info 0"%(self._location,gold,test)
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --GroupBy GroupedRelationLength --tab 1 --header-info 0"%(self._location,gold,test)
        res = os.popen(cmd)
        return [[value for value in line.strip("\n").split("\t")] for line in res][2:]

    def distance_to_root(self,gold,test):
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --GroupBy ArcDepth --tab 1 --header-info 0"%(self._location,gold,test)
        res = os.popen(cmd)
        return [[value for value in line.strip("\n").split("\t")] for line in res][2:]

    def projectivity(self,gold,test):
        #cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --GroupBy ArcProjectivity --tab 1 --header-info 0"%(self._location,gold,test)
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --GroupBy ArcProjectivity:all --tab 1 --header-info 0"%(self._location,gold,test)
        res = os.popen(cmd)
        return [[value for value in line.split("\t")] for line in res][2:]
        #return [[value for value in line.strip("\n").split("\t")] for line in res][2:]

    def sentence_length(self,gold,test):
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --GroupBy SentenceLength --tab 1 --header-info 0"%(self._location,gold,test)
        res = os.popen(cmd)
        return [[value for value in line.strip("\n").split("\t")] for line in res][2:]

    def binned_sentence_length(self,gold,test):
        bins = [i for i in range(0,60,10)]
        accuracies = []
        for i in range(len(bins)-1):
            minLen = bins[i]
            maxLen = bins[i+1]
            UAS, LAS = self.accuracy(gold, test, maxSenLen=maxLen, minSenLen=minLen)
            accuracies.append(LAS)
        UAS, LAS = self.accuracy(gold,test,minSenLen=51)
        accuracies.append(LAS)
        bins.append("50+")
        return zip(accuracies, bins[1:])


#--------------
def pos_tagging_accuracy(gold,test):
    """POS TAGGING ACCURACY"""
    #TODO: currently assumes perfect tokenization!!
    from src.conllu import ConllFileHandler
    conll_reader = ConllFileHandler()
    gold_graphs = conll_reader.file_to_dg_list(gold)
    test_graphs = conll_reader.file_to_dg_list(test)
    correct_u = 0
    correct_x = 0
    tot = 0
    for ggraph, tgraph in zip(gold_graphs,test_graphs):
        for gdep, tdep in zip(ggraph, tgraph):
            tot += 1
            if gdep.cpostag == tdep.cpostag:
                correct_u += 1
            if gdep.postag == tdep.postag:
                correct_x += 1
    return (correct_u/float(tot))*100, (correct_x/float(tot))*100

if __name__=="__main__":
    #usage: python malteval.py gold test [tag: for pos tagging accuracy - parsing accuracy by default"
    malteval = Malteval()
    gold = sys.argv[1]
    test = sys.argv[2]
    if len(sys.argv)>3 and sys.argv[3] == "tag":
        print pos_tagging_accuracy(gold,test)
    else:
        print malteval.accuracy(gold,test)
        #res = malteval.relation_length(gold,test)
