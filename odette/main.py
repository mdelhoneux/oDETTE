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
from scripts.baseline import run_baseline
from scripts.experiment import run_experiment, evaluate_on_transformed_gold, check_non_projectivity
from scripts.collect_stats import run_stats

def run(language, exp_type, use_cpostag=False):
    language_dir = config.exp + language
    if not os.path.exists(language_dir):
        os.mkdir(language_dir)
    language_dir += "/"
    if exp_type == "baseline":
        return run_baseline(language,outdir=language_dir, use_cpostag=use_cpostag)
    elif exp_type =="exp":
        return run_experiment(language,outdir=language_dir, use_cpostag=use_cpostag)
    elif exp_type == "stats":
        return run_stats(language,outdir=language_dir)
    elif exp_type == "ms_gold":
        return evaluate_on_transformed_gold(language,outdir=language_dir)
    elif exp_type == "non_proj":
        return check_non_projectivity(language,outdir=language_dir)

def table_headers(exp_type):
    if exp_type == "baseline":
        return "language;LAS;UAS\n"
    elif exp_type =="exp":
        return "language;baseline LAS; transformed LAS\n"
    elif exp_type =="stats":
        return "language;n sentences; n tokens; aux freq \n"
    elif exp_type == "ms_gold":
        return "language; LAS ; basline LAS\n"
    elif exp_type == "non_proj":
        return "language; gold nproj; ms nproj; backtransformation nproj \n"

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
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--outfile', default = './results.csv', help='A file name, it will contain the results: Default: results.csv in current directory')
    arg_parser.add_argument('--exp_type', default = 'baseline', help='[baseline|exp|stats|ms_gold|non_proj] Type of experiment to carry. Default: run all baselines.  stats: count sentences, tokens and auxiliaries. exp: run experiment (warning: the baselines must have been run). ms_gold: evaluate on transformed rep (warning: experiment must have been run before).  non_proj: counts non-projectivity in gold, transformed and backtransformed training data')
    arg_parser.add_argument('--version', default = 'v1_2', help='[v1_1|v1_2] The version of UD.  Default = v1_2 which corresponds to v1.2. Note: The version needs to contain a iso dictionary in utils ')
    arg_parser.add_argument('--include', default = 'all', help="The languages to be run, all by default")
    arg_parser.add_argument('--exclude', default = None, help="languages not to be run, default is none (warning: will exclude anything added in included)")
    #TODO: default should be yes
    arg_parser.add_argument('--use_cpostag', default = 0, help="[1 for true|0 for False] Use the cpostag instead of the postag for parsing. Default = False")

    args = arg_parser.parse_args()
    args = vars(args) #converts the args namespace to a dict. Usage: args['arg']

    res = open(args['outfile'], "w")
    exp_type = args['exp_type']
    use_cpostag = bool(int(args['use_cpostag']))
    version = args['version']
    exec("langs = src.utils.%s"%version) #put iso_code in langs
    if args['include'] == "all":
        l_considered = [language for language in langs]
    else:
        l_considered = parse_list(args['include'])
    if args['exclude']:
        l_excluded = parse_list(args['exclude'])
        for l in l_excluded:
            l_considered.remove(l)

    headers = table_headers(exp_type)
    res.write(headers)

    #run everything in parallel
    num_cores = multiprocessing.cpu_count()
    results = Parallel(n_jobs=num_cores)(delayed(run)(language,exp_type,use_cpostag=use_cpostag) for language in l_considered)
    for result in results:
        res.write(result)
