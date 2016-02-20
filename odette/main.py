#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
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
from scripts.baseline import run_baseline
from scripts.experiment import run_experiment, evaluate_on_transformed_gold, check_non_projectivity,evaluate_back_transformation_accuracy
from scripts.collect_stats import run_stats

#TODO: prepare file does not need to write to any file
#right now I quite inelegantly write empty strings to files but should do
#something better
#TODO: Refactor this stuff it's so ugly it makes me cry

def run(language, exp_type, metric):
    language_dir = config.exp + language
    if not os.path.exists(language_dir):
        os.mkdir(language_dir)
    language_dir += "/"
    if exp_type == "baseline":
        return run_baseline(language,outdir=language_dir)
    elif exp_type == "prep":
        prepare_files(language,outdir=language_dir)
        return ""
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

def parse_list(l):
    #TODO: rename
    """Return a list of line values if it's a file or a list of values if it
    is a string"""
    if os.path.isfile(l):
        f = open(l, 'r')
        return [line.strip("\n") for line in f]
    else:
        return [el for el in l.split(" ")]

if __name__=="__main__":
    #TODO: add stdout messages and maybe nohup the parsing stuff out
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--outfile', default = './results.csv', help='A file name, it will contain the results: Default: results.csv in current directory')
    arg_parser.add_argument('--exp_type', default = 'baseline', help='[prep|baseline|exp|stats|ms_gold|non_proj|backtransf] Type of experiment to carry. Default: run all baselines.  prep: preprocess files, stats: count sentences, tokens and auxiliaries. exp: run experiment.  ms_gold: evaluate on transformed rep (warning: experiment must have been run before).  non_proj: counts non-projectivity in gold, transformed and backtransformed training data.  backtransf: test the accuracy of the backtransformation on the training files')
    arg_parser.add_argument('--version', default = 'v1_2', help='[v1_1|v1_2] The version of UD.  Default = v1_2 which corresponds to v1.2. Note: The version needs to contain a iso dictionary in utils ')
    arg_parser.add_argument('--include', default = 'all', help="The languages to be run, all by default")
    arg_parser.add_argument('--exclude', default = None, help="languages not to be run, default is none (warning: will exclude anything added in included)")
    arg_parser.add_argument('--parallel', default = 1, help="[1 for True|0 for False] Run everything in parallel. Default = 1.")
    arg_parser.add_argument('--metric', default = 'LAS', help="[LAS|UAS] Default = LAS.")

    args = arg_parser.parse_args()
    args = vars(args) #converts the args namespace to a dict. Usage: args['arg']

    res = open(args['outfile'], "w")
    exp_type = args['exp_type']
    parallel = bool(int(args['parallel']))
    version = args['version']
    metric = args['metric']

    exec("langs = src.utils.%s"%version) #put iso_code in langs
    if args['include'] == "all":
        l_considered = [language for language in langs]
    else:
        l_considered = parse_list(args['include'])
    if args['exclude']:
        l_excluded = parse_list(args['exclude'])
        for l in l_excluded:
            l_considered.remove(l)

    headers = table_headers(exp_type, metric)
    res.write(headers)

    if parallel:
        #run everything in parallel
        num_cores = multiprocessing.cpu_count()
        results = Parallel(n_jobs=num_cores)(delayed(run)(language,exp_type,metric) for language in l_considered)
        for result in results:
            res.write(result)
    else:
        #results = [run(language,exp_type) for language in l_considered]
        for i, language in enumerate(l_considered):
            print "working on " + language + " (%s/%s)"%(i,len(l_considered))
            lres = run(language,exp_type,metric)
            res.write(lres)
            res.flush()
