#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#description	:Plot accuracy of a dependency relation (punct in main) in directory of treebanks
#usage			:python scripts/figure_5.py
#Python version :2.7.6
#==============================================================================

import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from math import sqrt

import config
from src.malteval import Malteval

def plot_dep_scores(indir, treebank_number, dep, fig=None, outfile='Figures/figure.png'):
    gold = indir + 'test_gold.conll'
    baseline = indir + 'dev_parsed_baseline.conll'
    transf = indir + 'dev_parsed.ud.conll'

    malteval = Malteval()
    mb = malteval.deprel_matrix(gold,baseline)
    mt = malteval.deprel_matrix(gold,transf)

    """The matplotlib thing"""
    x = np.array([malt[6].strip("\n") for malt in mb])
    p1 = np.array([float(malt[0]) if malt[0] is not "-" else 0. for malt in mb]) #sorry
    p2 = np.array([float(malt[0]) if malt[0] is not "-" else 0. for malt in mt]) #not sorry
    r1 = np.array([float(malt[1]) if malt[1] is not "-" else 0. for malt in mb])
    r2 = np.array([float(malt[1]) if malt[1] is not "-" else 0. for malt in mt])
    f1 = np.array([(2*p*r/(p+r)) if 0. not in (p,r) else 0. for p,r in zip(p1,r1)])
    f2 = np.array([(2*p*r/(p+r)) if 0. not in (p,r) else 0. for p,r in zip(p2,r2)])
    n1 = np.array([int(malt[2]) if malt[2] is not "-" else 0 for malt in mb])
    n2 = np.array([int(malt[2]) if malt[2] is not "-" else 0 for malt in mt])

    me1 = np.array([0.98/sqrt(n) if n != 0 else 0. for n in n1])
    me2 = np.array([0.98/sqrt(n) if n!= 0 else 0. for n in n2])

    allinfo = [(xi,fi1,fi2,mei1,mei2) for (xi,fi1,fi2,mei1,mei2) in zip(x,f1,f2,me1,me2) if xi == dep]
    x = [tup[0] for tup in allinfo]
    f1 = [tup[1] for tup in allinfo]
    f2 = [tup[2] for tup in allinfo]
    me1 = [tup[3] for tup in allinfo]
    me2 = [tup[4] for tup in allinfo]


    if fig == None:
        fig, ax = plt.subplots()
    else:
        ax = fig.add_subplot(1,1,1)

    if len(x) == 0:
        return fig, ax

    bar_width = 0.45
    last_index = treebank_number*3*bar_width
    index = last_index + np.arange(len(x))
    opacity = 0.4
    error_config = {'ecolor': '0.3'}


    ax.bar(index,f1, bar_width,
            alpha=opacity,
            color='b',
            error_kw=error_config,
            yerr=me1,
            label = 'baseline' if treebank_number == 0 else "",
            )

    ax.bar(index + bar_width ,f2, bar_width,
            alpha=opacity,
            color='r',
            error_kw=error_config,
            yerr=me2,
            label = 'transformed' if treebank_number == 0 else "",
            )

    if treebank_number == 0:
        plt.xlabel('%s deprel'%dep)
        plt.ylabel('Attachment score')

    plt.legend(bbox_to_anchor=(1.1, 1.05))
    plt.subplots_adjust(hspace=0.5)
    return (fig, ax)

if __name__=="__main__":
    dep = "punct"
    exp = config.exp
    ln = 0 #language counter
    outf = "Figures/punct.png"
    prev_fig = None
    l_considered = [line.strip("\n") for line in open("include", "r")]
    for language in l_considered:
        ldir = exp + "/" + language + "/"
        (fig, ax) = plot_dep_scores(ldir, ln, dep, prev_fig, outfile=outf)
        prev_fig = fig
        if ln == len(l_considered)-1:
            labels = [l.split("UD_")[1].strip("/") for l in l_considered]
            label_places = [i * 1.35 + 0.45 for i in range(len(labels))]
            ax.set_xticks(label_places)
            ax.set_xticklabels(labels, rotation='vertical')
        ln+=1
    fig.savefig(outf, bbox_inches='tight')
