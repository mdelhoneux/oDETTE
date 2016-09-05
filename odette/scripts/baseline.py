#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#description	:Run a baseline parser
#usage			:python baseline.py treebank_name trainfile testfile
#Python version :2.7.6
#==============================================================================

import sys, os
import config
from src.malteval import Malteval, pos_tagging_accuracy
from src.parsers import MaltParser
from src.treebank_transformer import TreebankTransformer
from src.treebank_manager import TreebankManager
from src.UD_treebank import UDtreebank

malteval = Malteval()

def run_baseline_with_tagger(treebank_name,outdir=None,metric='LAS', parser="udpipe"):
    if not outdir: outdir= config.exp + treebank_name + "/"
    TM = TreebankManager(treebank_name,outdir, parser=parser)
    #TODO: I might want to retrained it even if it's trained - then I should
    #name it differently like with params or something
    if not TM._tagger.is_trained():
        TM.train_tagger(devfile=TM.treebank.devfile)
    if not TM._parser.is_trained():
        TM.train_parser(devfile=TM.devfile)
    TM.tag_test_file()
    TM.test_parser()
    uas, las= malteval.accuracy(TM.test_gold,TM.test_parsed)
    upos, xpos = pos_tagging_accuracy(TM.test_gold,TM.test_parsed)
    output = "%s;%s;%s;%s;%s\n"%(treebank_name,las,uas, upos,xpos)
    return output

def learning_curve(treebank_name,outdir=None,metric='LAS',parser='udpipe'):
    if not outdir: outdir= config.exp + treebank_name + "/"
    TM = TreebankManager(treebank_name,outdir, parser=parser)
    TM.split_training()
    TM.tag_test_file()
    lass = []
    for i in range(1,len(self.splits)):
        TM._parser.train(self.splits[i],devfile = TM.devfile)
        TM.test_parser()
        uas, las= malteval.accuracy(TM.test_gold,TM.test_parsed)
        lass.append(las)
    #TODO: plot training size number instead of split n
    from matplotlib import pyplot as plt
    plt.plot(lass)
    plt.savefig("./learning_curve.png")
    return lass


def run_baseline(treebank_name, outdir=None, trainfile=None, testfile=None):
    if not outdir: outdir= config.exp + treebank_name
    TM = TreebankTransformer(treebank_name=treebank_name)
    """Train and parse"""
    train_gold = TM.trainfile
    test_gold = TM.testfile

    TM._parser.train(train_gold)
    parsed_baseline = outdir + '/dev_parsed_baseline.conll'
    TM._parser.parse(test_gold, parsed_baseline)

    """RESULTS"""
    uas, las= malteval.accuracy(test_gold,parsed_baseline)
    output = "%s;%s;%s\n"%(treebank_name,las,uas)
    return output

if __name__=="__main__":
    """usage: python baseline.py treebank_name (trainfile testfile)"""
    treebank_name = sys.argv[1]
    train=None
    test=None
    if len(sys.argv) > 2:
        train = sys.argv[2]
        test = sys.argv[3]
    res = open('baseline_results_%s.csv'%(treebank_name), "w")
    res.write("treebank_name;LAS;UAS\n")
    output = run_baseline(treebank_name,trainfile=train,testfile=test)
    res.write(output)
