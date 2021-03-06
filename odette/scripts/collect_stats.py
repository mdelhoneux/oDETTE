#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#description	:Collect stats on treebanks (n of sentences, tokens and aux frequency)
#usage			:python scripts/collect_stats.py treebank_name trainfile testfile
#Python version :2.7.6
#==============================================================================


import sys
from src.treebank_transformer import TreebankTransformer
import config

#TODO: a function that just counts tokens and sentences might be useful
def run_stats(treebank_name,outdir=None,trainfile=None, testfile=None,dep_style="ud"):
    if not outdir: outdir= config.exp + treebank_name
    TM = TreebankTransformer(treebank_name=treebank_name, dep_style=dep_style)
    #replace train and test files if they are given as arg
    if trainfile: TM.trainfile = trainfile
    if testfile: TM.testfile = testfile
    aux_train, tot_train, s_train = TM.count_aux(TM.trainfile)
    aux_test, tot_test, s_test = TM.count_aux(TM.testfile)
    tot_s = s_train + s_test
    tot_aux = aux_train + aux_test
    tot_tokens = tot_train + tot_test
    aux_freq = (tot_aux/float(tot_tokens))*100
    output = "%s;%s;%s;%s\n"%(treebank_name, tot_s, tot_tokens, aux_freq)
    return output

def run_stats_cop(treebank_name,outdir=None,trainfile=None, testfile=None,dep_style="ud"):
    if not outdir: outdir= config.exp + treebank_name
    TM = TreebankTransformer(treebank_name=treebank_name, dep_style=dep_style)
    #replace train and test files if they are given as arg
    if trainfile: TM.trainfile = trainfile
    if testfile: TM.testfile = testfile
    cop_train, tot_train= TM.count_cop(TM.trainfile)
    cop_test, tot_test= TM.count_cop(TM.testfile)
    tot_cop = cop_train + cop_test
    tot_s = tot_train + tot_test
    cop_freq = (tot_cop/float(tot_s))*100
    output = "%s;%s;%s\n"%(treebank_name, tot_s, cop_freq)
    return output

if __name__=="__main__":
    treebank_name = sys.argv[1]
    train = sys.argv[2]
    test = sys.argv[3]
    dep_style = "ud"
    if len(sys.argv) > 4:
        dep_style = sys.argv[4]
    res = open('stats_%s.csv'%(treebank_name), "w")
    res.write("treebank_name;n sentences;n tokens; aux frequency\n")
    output=run_stats(treebank_name,res,trainfile=train,testfile=test,
                     dep_style=dep_style)
    res.write(output)
