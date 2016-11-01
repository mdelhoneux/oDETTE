#!/usr/bin/env python
#==============================================================================
#author         :Miryam de Lhoneux
#email          :miryam.de_lhoneux@lingfil.uu.se
#date           :2015/12/30
#version        :1.0
#description    :Run a baseline parser
#usage          :python baseline.py treebank_name trainfile testfile
#Python version :2.7.6
#==============================================================================

import sys, os
import config
from src.malteval import Malteval, pos_tagging_accuracy
from src.parsers import MaltParser
from src.treebank_transformer import TreebankTransformer
from src.treebank_manager import TreebankManager
from src.UD_treebank import UDtreebank
from joblib import Parallel, delayed
import multiprocessing
from copy import deepcopy

malteval = Malteval()

def run_baseline_with_tagger(treebank_name,outdir=None,metric='LAS', parser="udpipe"):
    if not outdir: outdir= config.exp + treebank_name + "/"
    TM = TreebankManager(treebank_name,outdir=outdir, parser=parser)
    #TODO: I might want to retrain it even if it's trained - then I should
    #name it differently like with params or something
    #TODO: make using a devfile an option
    if not TM._tagger.is_trained():
        #TM.train_tagger(devfile=TM.treebank.devfile)
        TM.train_tagger()
    if not TM._parser.is_trained():
        #TM.train_parser(devfile=TM.devfile)
        TM.train_parser()
    TM.tag_test_file()
    TM.test_parser()
    uas, las= malteval.accuracy(TM.test_gold,TM.test_parsed)
    upos, xpos = pos_tagging_accuracy(TM.test_gold,TM.test_parsed)
    output = "%s;%s;%s;%s;%s\n"%(treebank_name,las,uas, upos,xpos)
    return output

def error_analysis(treebank_name, outdir=None,parser="udpipe"):
    #TODO: rename
    TM = TreebankManager(treebank_name, outdir=outdir,parser=parser)
    #do it only if file empty?
    TM.tag_test_file()
    TM.test_parser()
    import numpy as np
    lengths = [str(i) for i in np.arange(5,50,5)]
    lass = []
    for length in lengths:
        uas, las= malteval.accuracy(TM.test_gold,TM.test_parsed,maxSenLen=length)
        if las:
            lass.append(las)
    #get no lim
    uas, las= malteval.accuracy(TM.test_gold,TM.test_parsed)
    lass.append(las)
    output = treebank_name +";" + ";".join(lass) + "\n"
    return output


def learning_curve(treebank_name,outdir=None,metric='LAS',parser='udpipe', split_sizes=None):
    #NOTE: not sure what happens if I send main in parallel and this again
    if not outdir: outdir= config.exp + treebank_name + "/"
    TM = TreebankManager(treebank_name,outdir=outdir, parser=parser)
    if not TM._tagger.is_trained():
        TM.train_tagger(devfile=TM.treebank.devfile)
    TM.tag_test_file()
    TM.split_training()
    tot_splits = len(TM.splits)
    parser_name = deepcopy(TM._parser.name)
    num_cores = multiprocessing.cpu_count()
    tms = Parallel(n_jobs=num_cores)(delayed(_run_for_a_split)(i, deepcopy(TM), parser_name) for i in range(tot_splits))
    lass = []
    for tm in tms:
        uas, las= malteval.accuracy(tm.test_gold,tm.test_parsed)
        lass.append(las)
    output = treebank_name +";" + ";".join(lass) + "\n"
    return output

def optimize_udpipe(treebank_name,outdir=None,metric='LAS',parser='udpipe', n_runs=100):
    if not outdir: outdir= config.exp + treebank_name + "/"
    TM = TreebankManager(treebank_name,outdir=outdir, parser=parser)
    if not TM._tagger.is_trained():
        TM.train_tagger(devfile=TM.treebank.devfile)
    TM.tag_test_file()
    num_cores = min(multiprocessing.cpu_count(), n_runs)
    parser_name = deepcopy(TM._parser.name)
    tms = Parallel(n_jobs=num_cores)(delayed(_one_run)(i, deepcopy(TM), parser_name) for i in range(n_runs))
    lass = []
    for tm in tms:
        uas, las= malteval.accuracy(tm.test_gold,tm.test_parsed)
        lass.append(las)
    output = treebank_name +";" + ";".join(lass) + "\n"
    return output

def _one_run(i, TM, parser_name):
    TM.parser_name = parser_name + "_run_number_" + str(i)
    TM._parser.name = TM.parser_name
    TM._parser.run = i
    if not TM._parser.is_trained():
        TM._parser.train(TM.trainfile)
        TM.test_parser()
    return TM

def _run_for_a_split(i, TM, parser_name):
    TM.parser_name = parser_name + str(TM.split_sizes[i])
    TM._parser.name = TM.parser_name
    if not TM._parser.is_trained():
        TM._parser.train(TM.splits[i],devfile = TM.devfile)
    TM.test_parser()
    return TM


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
