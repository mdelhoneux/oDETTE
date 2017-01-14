import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from math import sqrt

import config
from src.malteval import Malteval


if __name__=="__main__":
    results = [line.strip("\n").split(";") for line in open("RES/las.csv", 'r')][1:]
    #TODO: sort by size (res[1])
    x = [res[0] for res in results]
    f1 = [float(res[3]) for res in results]
    f2 = [float(res[2]) for res in results]
    f3 = [float(res[4]) for res in results]

    plt.figure()
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
            color='#004C99',
            #color='white',
            label = 'SyntaxNet',
           )

    plt.ylabel('LAS')
    axes = plt.gca()
    axes.set_ylim([0,100])
    plt.xticks(index + bar_width, x)
    plt.legend(bbox_to_anchor=(0.45, 1.05), loc=2, borderaxespad=0.)
    plt.autoscale(axis='x')
    plt.tight_layout()
    plt.show()
    plt.savefig("Figures/las.png")
