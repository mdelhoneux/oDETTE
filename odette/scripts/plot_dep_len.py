import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from math import sqrt

import config
from src.malteval import Malteval

def dir_to_plot(indir, outfile='Figures/deprel.png'):
        #TODO: rename and make option
        gold = indir + '/dev_gold.conll'
        #for conv (erm) baseline = malt, transf = udpipe
        baseline = indir + '/dev_parsed_maltOpt.conll'
        transf = indir + '/dev_parsed_udpipe.conll'
    
        malteval = Malteval()
        mb = malteval.relation_length(gold,baseline)
        mt = malteval.relation_length(gold,transf)

        #move the to_root to left of figure
        mb.insert(0,mb.pop(-1))
        mt.insert(0,mt.pop(-1))
        
    
        """The matplotlib thing"""
        #Note: I am taking the parser accuracy and the parsercounter
        #TODO: discard if 0
    
        #import ipdb; ipdb.set_trace()
        x = np.array([malt[2].strip("\n") for malt in mb])
        p1 = np.array([float(malt[0]) if malt[0] is not "-" else 0. for malt in mb])
        p2 = np.array([float(malt[0]) if malt[0] is not "-" else 0. for malt in mt])
        r1 = np.array([float(malt[1]) if malt[1] is not "-" else 0. for malt in mb])
        r2 = np.array([float(malt[1]) if malt[1] is not "-" else 0. for malt in mt])
        f1 = np.array([(2*p*r/(p+r)) if 0. not in (p,r) else 0. for p,r in zip(p1,r1)])
        f2 = np.array([(2*p*r/(p+r)) if 0. not in (p,r) else 0. for p,r in zip(p2,r2)])
        #they can have a different length somehow let's just cut the end

        max_dep_len = min(30,len(f1),len(f2))
        f1 = [i*100 for i in f1[:max_dep_len]]
        f2 = [i*100 for i in f2[:max_dep_len]]
        x = x[:max_dep_len]
    
        index = np.arange(len(x))
        plt.plot(index, f2, label="udpipe", color='#3399ff')
        plt.plot(index, f1, label="maltparser", color='#000034')

        plt.xlabel('Relation Length')
        plt.ylabel('Attachment score')
        plt.xticks(index, x, rotation='vertical')
        #plt.legend(bbox_to_anchor=(1.1, 1.05))
        plt.legend(loc=4)
        axes = plt.gca()
        axes.set_ylim([1,100])
        #plt.title(indir.split("UD_")[1].strip("/"))
        #if indir.split("UD_")[1].strip("/") == "Kazakh":
            #import ipdb;ipdb.set_trace()
        plt.tight_layout()
        #plt.show()
        plt.savefig(outfile)
        plt.clf()
    
if __name__=="__main__":
    #indir = sys.argv[1]
    #dir_to_plot(indir)
    exp = config.exp
    for language in os.listdir(exp):
        ldir = exp + "/" + language
        outf = "./Figures/group_dep_len_%s"%language
        #outf = "./Figures/dep_len_%s"%language
        dir_to_plot(ldir, outfile=outf)
