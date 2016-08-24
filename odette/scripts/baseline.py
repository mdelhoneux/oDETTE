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
from src.malteval import Malteval
from src.parsers import MaltParser
from src.treebank_transformer import TreebankTransformer
from src.treebank_manager import TreebankManager
from src.UD_treebank import UDtreebank

malteval = Malteval()

#TODO: rename
def run_baseline_with_tagger(treebank_name,outdir=None,metric='LAS'):
    if not outdir: outdir= config.exp + treebank_name + "/"
    TM = TreebankManager(treebank_name,outdir)
    TT = TreebankTransformer(treebank_name=treebank_name)
    #TODO: ouch this is ugly
    TT.transform(TM.treebank.devfile, TM.dev_gold, "to_conllx")
    TM.train_tagger()
    TM.train_parser()
    TM.tag_test_files()
    TM.test_parser()
    TT.transform(TM.dev_parsed, TM.dev_parsed_x, "to_conllx")
    uas, las= malteval.accuracy(TM.dev_gold,TM.dev_parsed_x)
    output = "%s;%s;%s\n"%(treebank_name,las,uas)
    return output



#TODO: rename
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
