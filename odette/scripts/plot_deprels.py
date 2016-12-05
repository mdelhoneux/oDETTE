import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from math import sqrt

import config
from src.malteval import Malteval

def dir_to_plot(indir, outfile='Figures/deprel.png'):
        #TODO: rename
        gold = indir + '/dev_gold.conll'
        #for conv (erm) baseline = malt, transf = udpipe
        baseline = indir + '/dev_parsed_maltOpt.conll'
        transf = indir + '/dev_parsed_udpipe.conll'

        malteval = Malteval()
        mb = malteval.deprel_matrix(gold,baseline)
        mt = malteval.deprel_matrix(gold,transf)
    
        """The matplotlib thing"""
        #Note: I am taking the parser accuracy and the parsercounter
        #TODO: discard if 0
    
        #I was assuming x is always the same but somehow for tamil this is not the case
        x1 = np.array([malt[6].strip("\n") for malt in mb])
        x2= np.array([malt[6].strip("\n") for malt in mt])
        x = x1

        p1 = np.array([float(malt[0]) if malt[0] is not "-" else 0. for malt in mb])
        p2 = np.array([float(malt[0]) if malt[0] is not "-" else 0. for malt in mt])

        #import ipdb; #ipdb.set_trace()
        r1 = np.array([float(malt[1]) if malt[1] is not "-" else 0. for malt in mb])
        r2 = np.array([float(malt[1]) if malt[1] is not "-" else 0. for malt in mt])
        f1 = np.array([(2*p*r/(p+r)) if 0. not in (p,r) else 0. for p,r in zip(p1,r1)])
        f2 = np.array([(2*p*r/(p+r)) if 0. not in (p,r) else 0. for p,r in zip(p2,r2)])
        n1 = np.array([int(malt[2]) if malt[2] is not "-" else 0 for malt in mb])
        n2 = np.array([int(malt[2]) if malt[2] is not "-" else 0 for malt in mt])
        #TODO: is this correct now?? or should n be the treebank counter?
        st1 = np.array([sqrt(f*(1-f)/n) if f != 0 else 0. for f,n in zip(f1, n1)]) #oh python, the things you let me do
        st2 = np.array([sqrt(f*(1-f)/n) if f != 0 else 0. for f,n in zip(f2, n2)])
    
        #next = wikipedia
        me1 = np.array([0.98/sqrt(n) if n != 0 else 0. for n in n1])
        me2 = np.array([0.98/sqrt(n) if n!= 0 else 0. for n in n2])
    
        #filter out infrequent stuff 
        #n1 = np.array([i for i in n2 if i>10]) #does not seem to work
        inds = n1.argsort()[::-1] #index in inversed order
        #import ipdb; ipdb.set_trace()
        x = x[inds]
        #f1 = [i*100 for i in f1]
        #f2 = [i*100 for i in f2]

        f1 = f1[inds]
        #import ipdb; ipdb.set_trace()
        #fails on TAMIL not worth fixing for now
        try:
            f2 = f2[inds]
        except IndexError:
            return
        st1 = st1[inds]
        st2 = st2[inds]
        me1 = me1[inds]
        me2 = me2[inds]


    
        error_config = {'ecolor': '0.3'}
    
        plt.figure()
        bar_width = 0.35
        index = np.arange(len(x))
        plt.bar(index,f1, bar_width,
                            color='#000034',
                             error_kw=error_config,
                             #yerr=st1,
                             yerr=me1,
                             label = 'malt',
                             )
    
        plt.bar(index + bar_width ,f2, bar_width,
                            color='#3399ff',
                             error_kw=error_config,
                             #yerr=st2,
                             yerr=me2,
                             label = 'udpipe',
                             )
    
        plt.xlabel('Deprel')
        plt.ylabel('Attachment score')
        axes = plt.gca()
        axes.set_ylim([0,1])
        plt.xticks(index + bar_width, x, rotation='vertical')
        plt.legend(bbox_to_anchor=(1.1, 1.05))
        #plt.tight_layout()
        plt.title(indir.split("UD_")[1].strip("/"))
        plt.savefig(outfile)
        #plt.show()
        plt.clf()
    
if __name__=="__main__":
    exp = config.exp
    for language in os.listdir(exp):
        ldir = exp + "/" + language
        outf = "./Figures/deprels_%s"%language
        dir_to_plot(ldir, outfile=outf)
