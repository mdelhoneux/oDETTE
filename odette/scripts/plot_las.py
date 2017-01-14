#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#description	:plot las of all languages
#usage			:python scripts/plot_las.py
#Python version :2.7.6
#==============================================================================

import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from math import sqrt

import config
from src.malteval import Malteval

def plot_las(indir, treebank_number, fig=None, outfile='Figures/figure.png'):
    gold = indir + '/dev_gold.conll'
    #for conv (erm) baseline = malt, transf = udpipe
    baseline = indir + '/dev_parsed_maltOpt.conll'
    transf = indir + '/dev_parsed_udpipe.conll'

    malteval = Malteval()
    #f=LAS
    #ughhh this is hacky and makes the code much more complicated than it should
    #be
    UAS, LAS1 = malteval.accuracy(gold,baseline)
    f1 = [LAS1]
    UAS, LAS2 = malteval.accuracy(gold,transf)
    f2 = [LAS2]
    #import ipdb; ipdb.set_trace()
    print indir
    print f1
    print f2


    if not fig:
        fig, ax = plt.subplots()
    ax = fig.add_subplot(1,1,1)

    bar_width = 0.45
    last_index = treebank_number*3*bar_width
    index = last_index + np.arange(len(f1))
    error_config = {'ecolor': '0.3'}
    ax.set_ylim([0,100])
    ax.get_xaxis().set_visible(False)


    ax.bar(index,f1, bar_width,
           color='#000034',
           error_kw=error_config,
           label = 'malt' if treebank_number == 0 else "",
          )

    ax.bar(index + bar_width ,f2, bar_width,
           color='#3399ff',
           error_kw=error_config,
           label = 'udpipe' if treebank_number == 0 else "",
          )

    if treebank_number == 0:
        #plt.xlabel('%s pos'%pos)
        plt.ylabel('Attachment score')

        plt.legend(bbox_to_anchor=(1.1, 1.05))
    return (fig, ax)

if __name__=="__main__":
    #pos = sys.argv[1]
    exp = config.exp
    outf = "Figures/las.png"
    prev_fig = None
    l_considered = [line.strip("\n") for line in open("selection.txt", "r")]
    #TODO: rank by size & add size
    for ln, language in enumerate(l_considered):
        ldir = exp + "/" + language + "/"
        (fig, ax) = plot_las(ldir, ln, prev_fig, outfile=outf)
        prev_fig = fig
        if ln == len(l_considered)-1:
            labels = [l.split("UD_")[1].strip("/") for l in l_considered]
            label_places = [i * 1.35 + 0.45 for i in range(len(labels))]
            ax.set_xticks(label_places)
            ax.get_xaxis().set_visible(True)
            ax.set_xticklabels(labels, rotation='vertical')
        else:
            ax.get_xaxis().set_visible(False)
    fig.savefig(outf, bbox_inches='tight')
