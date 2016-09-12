#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#description	:Transform parse detransform experiment pipeline on a treebank
#usage			:python scripts/experiment.py treebank_name (POS-style)
#Python version :2.7.6
#==============================================================================


import sys
import config
from src.malteval import Malteval
from src.treebank_transformer import TreebankTransformer

malteval = Malteval()


def run_experiment(treebank_name,outdir=None,dep_style="ud", pos_style='ud',
                   metric='LAS'):
    #TODO: have options for what goes in table
    if not outdir: outdir= config.exp + treebank_name + "/"
    TM = TreebankTransformer(treebank_name=treebank_name, dep_style=dep_style, pos_style=pos_style)
    TM.transform_parse_detransform() #if you just want the eval you can just comment this out

    """FILES"""
    test_gold = TM.testfile
    parsed_baseline = outdir +  'dev_parsed_baseline.conll'
    parsed_ud = TM.parsed_ud
    #if you just eval comment the one up and uncomment the one down
    #parsed_ud = outdir + 'dev_parsed.ud.conll'

    """RESULTS"""
    buas, blas= malteval.accuracy(test_gold,parsed_baseline)
    uas, las = malteval.accuracy(test_gold,parsed_ud)
    output = ""
    if metric =="LAS":
        las = str(float(las)*100)
        blas = str(float(blas)*100)
        #significance of las
        sig = malteval.significance(test_gold, parsed_baseline, parsed_ud)
        las += sig
        output = "%s;%s;%s\n"%(treebank_name, blas, las)
    else:
        uas = str(float(uas)*100)
        buas = str(float(buas)*100)
        sig = malteval.significance_uas(test_gold, parsed_baseline, parsed_ud)
        uas += sig
        output = "%s;%s;%s\n"%(treebank_name, buas, uas)
    return output

def evaluate_back_transformation_accuracy(treebank_name,outdir=None):
    if not outdir: outdir= config.exp + treebank_name + "/"
    TM = TreebankTransformer(treebank_name=treebank_name)
    TM.transform_detransform_trainfile()
    train_gold = TM.trainfile
    train_backtransf = TM.back_transf
    accuracy_of_back_transf = malteval.accuracy(train_gold,train_backtransf)[0]
    accuracy_of_back_transf = str(float(accuracy_of_back_transf)*100)
    output = "%s;%s\n"%(treebank_name,accuracy_of_back_transf)
    return output

def evaluate_on_transformed_gold(treebank_name,outdir=None):
    """Evaluate on the transformed representation as gold standard"""
    if not outdir: outdir= config.exp + treebank_name + "/"
    TM = TreebankTransformer(treebank_name=treebank_name)
    dev_gold_ms = "%sdev_gold.ms.conll"%outdir
    parsed_ms = "%sdev_parsed.ms.conll"%outdir
    parsed_baseline = outdir +  'dev_parsed_baseline.conll'
    baseline_ms = outdir + 'dev_parsed_baseline.ms.conll'
    TM.transform(TM.testfile, dev_gold_ms, "transform")
    TM.transform(parsed_baseline, baseline_ms, "transform")
    uas, las = malteval.accuracy(dev_gold_ms,parsed_ms)
    buas, blas = malteval.accuracy(dev_gold_ms,baseline_ms)
    las = str(float(las)*100)
    blas = str(float(blas)*100)
    output = "%s;%s;%s\n"%(treebank_name, las, blas)
    return output

def check_non_projectivity(treebank_name,outdir=None):
    if not outdir: outdir= config.exp + treebank_name
    """FILES"""
    train_gold = outdir + '/train.conll'
    train_ms = outdir + '/train_ms.conll'
    train_backtransf = outdir + '/train_backtransf.conll'

    """RESULTS"""
    gold_proj, ms_proj= malteval.non_projectivity(train_gold,train_ms)
    gold_proj, back_transf_proj = malteval.non_projectivity(train_gold,train_backtransf)

    out = "%s;%s;%s;%s\n"%(treebank_name, gold_proj,ms_proj,back_transf_proj)
    return out

if __name__=="__main__":
    #usage: python experiment.py treebank_name (dep_stype, pos_style, ambig)
    treebank_name = sys.argv[1]
    dep_style = "ud"
    pos_style = 'ud'
    ambig = None
    if len(sys.argv) > 2:
        dep_style = sys.argv[2]
        pos_style = sys.argv[3]
        ambig = sys.argv[4]
    res = open('exp_results_%s_%s.csv'%(treebank_name, ambig), "w")
    res.write("treebank_name;baseline LAS; transformed LAS\n")
    output = run_experiment(treebank_name,dep_style=dep_style, pos_style=pos_style)
    #output = evaluate_back_transformation_accuracy(treebank_name)
    res.write(output)
