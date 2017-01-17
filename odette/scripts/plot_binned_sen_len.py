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
        mb = malteval.binned_sentence_length(gold,baseline)
        mt = malteval.binned_sentence_length(gold,transf)

        """The matplotlib thing"""
        #Note: I am taking the parser accuracy and the parsercounter
        #TODO: discard if 0
    
        x = np.array([malt[1] for malt in mb])
        #import ipdb; ipdb.set_trace()
        f1 = np.array([float(malt[0]) if malt[0] is not None else 0. for malt in mb])
        f2 = np.array([float(malt[0]) if malt[0] is not None else 0. for malt in mt])
        if np.any(f1==0):
            #find first 0 value
            maxLen = np.where(f1 == 0.)[0][0]
        else:
            maxLen = len(f1)

        #max_dep_len = min(30,len(f1),len(f2))
        #f1 = [i*100 for i in f1]
        #f2 = [i*100 for i in f2]
        x = x[:maxLen]
        f1 = f1[:maxLen]
        f2 = f2[:maxLen]
    
        index = np.arange(len(x))
        plt.plot(index, f2, label="udpipe", color='#3399ff')
        plt.plot(index, f1, label="maltparser", color='#000034')

        plt.xlabel('Sentence Length')
        plt.ylabel('Attachment score')
        plt.xticks(index, x, rotation='vertical')
        #plt.legend(bbox_to_anchor=(1.1, 1.05))
        plt.legend(loc=4)
        axes = plt.gca()
        axes.set_ylim([1,100])
        #plt.title(indir.split("UD_")[1].strip("/"))
        plt.tight_layout()
        plt.savefig(outfile)
        plt.clf()
    
if __name__=="__main__":
    #indir = sys.argv[1]
    #dir_to_plot(indir)
    exp = config.exp
    for language in os.listdir(exp):
        ldir = exp + "/" + language
        outf = "./Figures/binned_sen_len_%s"%language
        dir_to_plot(ldir, outfile=outf)