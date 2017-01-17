import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from math import sqrt

import config
from src.malteval import Malteval


if __name__=="__main__":
    results = [line.strip("\n").split(";") for line in open("RES/las.csv", 'r')][1:]
    size = np.array([int(res[1].strip("K")) for res in results])
    inds = size.argsort()[::-1]
    x = np.array([res[0] +"\n" + res[1] for res in results])[inds]
    f1 = np.array([float(res[3]) for res in results])[inds]
    f2 = np.array([float(res[2]) for res in results])[inds]
    f3 = np.array([float(res[4]) for res in results])[inds]

    fig = plt.figure()
    bar_width = 0.25
    index = np.arange(len(x))
    plt.bar(index,f1, bar_width,
                        color='#000034',
                        edgecolor='none',
                         label = 'malt',
                         )

    plt.bar(index + bar_width ,f2, bar_width,
                        color='#3399ff',
                        edgecolor='none',
                         label = 'udpipe',
                         )

    plt.bar(index + 2*bar_width ,f3, bar_width,
            edgecolor='none',
            color='#97caef',
            #color='white',
            label = 'syntaxnet',
            #label = '', 
           )

    plt.ylabel('LAS')
    axes = plt.gca()
    axes.set_ylim([0,100])
    plt.xticks(index + 1.5*bar_width, x)
    #plt.legend(bbox_to_anchor=(0.45, 1.05), loc=2, borderaxespad=0., frameon=False)
    leg = plt.legend(loc=1, borderaxespad=0., frameon=False)
    # swap_and_right_align_legend 

    vp = leg._legend_box._children[-1]._children[0] 
    for c in vp._children: 
        c._children.reverse() 
        vp.align="right" 
    plt.autoscale(axis='x')
    plt.tight_layout()
    plt.show()
    #fig.savefig("Figures/las_nosyntaxnet.png")
    fig.savefig("Figures/las.png")
