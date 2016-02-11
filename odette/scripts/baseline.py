#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#description	:Run a baseline parser
#usage			:python baseline.py treebank_name trainfile testfile
#Python version :2.7.6
#==============================================================================


import sys, os
import config
from odette.src.malteval import Malteval
from odette.src.parsers import MaltParser
from odette.src.treebank_transformer import TreebankTransformer
from odette.src.UD_treebank import UDtreebank

def run_baseline(treebank_name, use_cpostag=False,outdir=None, trainfile=None,
                 testfile=None, ambig="orig", pos_style="ud"):
    if not outdir: outdir= config.exp + treebank_name
    if not os.path.exists(outdir): os.mkdir(outdir)
    malteval = Malteval()
    if not trainfile and not testfile :
        tb = UDtreebank(treebank_name)
        trainfile = tb.trainfile
        testfile = tb.devfile
    TM = TreebankTransformer(treebank_name=treebank_name, use_cpostag=use_cpostag)
    TM.transform(trainfile, TM.trainfile, 'to_conllx')
    TM.transform(testfile, TM.testfile, 'to_conllx')

    #experiments about ambiguity
    if ambig == "disambig":
        TM.transform(trainfile, TM.trainfile, 'disambig')
        TM.transform(testfile, TM.testfile, 'disambig')
    if ambig == "ambig":
        TM.transform(trainfile, TM.trainfile, 'ambig')
        TM.transform(testfile, TM.testfile, 'ambig')

    """Train and parse"""
    train_gold = TM.trainfile
    test_gold = TM.testfile

    TM._parser.train(train_gold)
    parsed_baseline = outdir + '/dev_parsed_baseline.conll'
    TM._parser.parse(test_gold, parsed_baseline)

    """RESULTS"""
    uas, las= malteval.accuracy(test_gold,parsed_baseline)
    #res.write("%s;%s;%s\n"%(treebank_name,las,uas))
    output = "%s;%s;%s\n"%(treebank_name,las,uas)
    return output

if __name__=="__main__":
    """usqge: python baseline.py treebank_name trainfile testfile (ambig pos_style)"""
    treebank_name = sys.argv[1]
    train = sys.argv[2]
    test = sys.argv[3]
    ambig = "orig"
    pos_style = "ud"
    if len(sys.argv) > 4:
        ambig = sys.argv[4]
        pos_style = sys.argv[5]
    res = open('baseline_results_%s_%s.csv'%(treebank_name,ambig), "w")
    res.write("treebank_name;LAS;UAS\n")
    output = run_baseline(treebank_name,trainfile=train,testfile=test,ambig=ambig,pos_style=pos_style,
                 use_cpostag=True)
    res.write(output)
