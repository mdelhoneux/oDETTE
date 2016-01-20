#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#description	:Wrapper around MaltEval to facilitate writing to tables
#usage			:python src/malteval.py gold test
#Python version :2.7.6
#==============================================================================


import config
import os
import sys

class Malteval(object):
    def __init__(self, location=config.malteval):
        self._location = location

    def accuracy(self,gold,test):
        """UAS and LAS of test on gold"""
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s --row-header 0 --tab 1 --header-info 0 --Metric 'LAS;UAS'"%(self._location,gold,test)
        res = os.popen(cmd)
        accuracies = [line for line in res][2].strip("\n")
        UAS, LAS= accuracies.split("\t")[:2]
        return UAS, LAS

    def significance(self,gold,baseline,test):
        """output: ** for p<.01 * for p<.05 and empty string otherwise"""
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s %s --row-header 0 --tab 1 --header-info 0 --stat 1 --GroupBy Token:accuracy"%(self._location,gold,baseline, test)
        res = [line for line in os.popen(cmd)]
        #print "\n".join([str(n) + " " + line.strip("\n") for (n,line) in enumerate(res)])
        p_0_1 = int(res[20].split("\t")[1])
        p_0_5 = int(res[24].split("\t")[1])
        if p_0_1: return "**"
        elif p_0_5: return "*"
        else: return ""

    def significance_uas(self,gold,baseline,test):
        cmd = "java -jar -Xmx2g %s/MaltEval.jar -g %s -s %s %s --row-header 0 --tab 1 --header-info 0 --stat 1 --GroupBy Token:accuracy --Metric 'UAS'"%(self._location,gold,baseline, test)
        res = [line for line in os.popen(cmd)]
        #print "\n".join([str(n) + " " + line.strip("\n") for (n,line) in enumerate(res)])
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

if __name__=="__main__":
    malteval = Malteval()
    gold = sys.argv[1]
    test = sys.argv[2]
    print malteval.accuracy(gold,test)
