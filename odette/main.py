#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#description	:Work with UD treebanks
#usage			:python main.py --help  #to find out about options
#Python version :2.7.6
#==============================================================================


import argparse
import os
from joblib import Parallel, delayed
import multiprocessing

import config
import src.utils
from scripts.preprocess_files import prepare_files
from scripts.baseline import run_baseline, run_baseline_with_tagger
from scripts.experiment import run_experiment, evaluate_on_transformed_gold, check_non_projectivity,evaluate_back_transformation_accuracy
from scripts.collect_stats import run_stats

def run(language, exp_type, metric, parser):
    language_dir = config.exp + language
    if not os.path.exists(language_dir):
        os.mkdir(language_dir)
    language_dir += "/"
    if exp_type == "baseline":
        return run_baseline(language,outdir=language_dir)
    elif exp_type == "tag_parse":
        return run_baseline_with_tagger(language, outdir=language_dir, parser=parser)
    elif exp_type == "prep":
        prepare_files(language,outdir=language_dir)
        return None
    elif exp_type =="exp":
        return run_experiment(language,outdir=language_dir, metric=metric)
    elif exp_type == "stats":
        return run_stats(language,outdir=language_dir)
    elif exp_type == "ms_gold":
        return evaluate_on_transformed_gold(language,outdir=language_dir)
    elif exp_type == "non_proj":
        return check_non_projectivity(language,outdir=language_dir)
    elif exp_type == "backtransf":
        return evaluate_back_transformation_accuracy(language,outdir=language_dir)
    else:
        raise Exception, "Invalid exp_type"

def table_headers(exp_type, metric):
    if exp_type == "prep":
        return ""
    if exp_type == "baseline":
        return "language;LAS;UAS\n"
    if exp_type == "tag_parse":
        return "language;LAS;UAS;POS\n"
    elif exp_type =="exp":
        return "language;baseline %s; transformed %s\n"%(metric,metric)
    elif exp_type =="stats":
        return "language;n sentences; n tokens; aux freq \n"
    elif exp_type == "ms_gold":
        return "language; LAS ; baseline LAS\n"
    elif exp_type == "non_proj":
        return "language; gold nproj; ms nproj; backtransformation nproj \n"
    elif exp_type == "backtransf":
        return "language;backtransformation accuracy\n"

def parse_list_arg(l):
    """Return a list of line values if it's a file or a list of values if it
    is a string"""
    if os.path.isfile(l):
        f = open(l, 'r')
        return [line.strip("\n") for line in f]
    else:
        return [el for el in l.split(" ")]

if __name__=="__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--outfile', default = './results.csv', help='A file name, it will contain the results: Default: results.csv in current directory')
    #TODO: note my preprocess could become obsolete with new treebank manager
    # would need to update treebank_transformer I guess
    arg_parser.add_argument('--exp_type', default = 'baseline', help='Type of  \
                            experiment to carry. Default: run all baselines.  {prep: preprocess files \
                                                                               stats: count sentences, tokens and auxiliaries \
                                                                               exp: run experiment \
                                                                               ms_gold: evaluate on transformed rep (warning: experiment must have been run before).  \
                                                                               non_proj: counts non-projectivity in gold, transformed and backtransformed training data.  \
                                                                               backtransf: test the accuracy of the backtransformation on the training files \
                                                                              }')
    arg_parser.add_argument('--include', default = 'all', help="The languages to be run, all by default")
    arg_parser.add_argument('--exclude', default = None, help="languages not to be run, default is none (warning: will exclude anything added in include)")
    arg_parser.add_argument('--parallel', default = 1, help="[1|0] Run everything in parallel. Default = 1.")
    arg_parser.add_argument('--metric', default = 'LAS', help="[LAS|UAS] Default = LAS.")
    arg_parser.add_argument('--parser', default = "udpipe", help="[malt|maltOpt|udpipe]")

    args = arg_parser.parse_args()
    args = vars(args)

    resfile = open(args['outfile'], "w")
    exp_type = args['exp_type']
    metric = args['metric']
    parser = args['parser']
    parallel = bool(int(args['parallel']))
    #just in case
    if parser == "maltOpt":
        parallel = 0


    langs = src.utils.iso_code
    if args['include'] == "all":
        l_considered = [language for language in langs]
    else:
        l_considered = parse_list_arg(args['include'])
    if args['exclude']:
        l_excluded = parse_list_arg(args['exclude'])
        for l in l_excluded:
            l_considered.remove(l)

    #write headers
    headers = table_headers(exp_type, metric)
    resfile.write(headers)

    #run everything
    if parallel:
        num_cores = multiprocessing.cpu_count()
        results = Parallel(n_jobs=num_cores)(delayed(run)(language,exp_type,metric, parser) for language in l_considered)
        for result in results:
            if result: #accounting for None returned in prep
                resfile.write(result)
    else:
        #results = [run(language,exp_type) for language in l_considered]
        for i, language in enumerate(l_considered):
            print "working on " + language + " (%s/%s)"%(i,len(l_considered))
            lres = run(language,exp_type,metric,parser)
            if lres:
                resfile.write(lres)
                resfile.flush()
