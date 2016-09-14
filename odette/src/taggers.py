#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2016/08/23
#version		:1.1
#description	:Wrapper around existing taggers
#usage			:python src/taggers.py trainfile testfile outfile
#Python version :2.7.6
#==============================================================================

import os

class Tagger(object):
    def train(self, trainfile):
        raise NotImplementedError
    def tag(self, testfile, outfile):
        raise NotImplementedError

class UDPipeTagger(Tagger):
    def __init__(self,path="./", name="udpipe_tagger"):
        self._path = path
        self.name = name

    def train(self,trainfile, devfile=None):
        if not devfile:
            cmd = "udpipe --train --parser=none --tokenizer=none %s%s %s"%(self._path,self.name, trainfile)
        else:
            cmd = "udpipe --train --heldout=%s --parser=none --tokenizer=none %s%s %s"%(devfile, self._path, self.name, trainfile)
            #TODO: need something different for Czech:
                #udpipe --train --parser=none --tokenizer=none --tagger guesser_suffix_rules=5 guesser_enrich_dictionary=3 EXP/UD_Czech/udpipe-tagger $UDCz/cs-ud-train.conllu 

        os.system(cmd)

    def tag(self,testfile,outfile):
        cmd = "udpipe --tag %s %s >%s"%(self._path,testfile,outfile)
        os.system(cmd)

    def is_trained(self):
        fullpath = self._path + self.name
        return os.path.exists(fullpath)

if __name__=="__main__":
    import sys
    trainfile = sys.argv[1]
    testfile = sys.argv[2]
    outfile = sys.argv[3]
    tagger = UDPipeTagger()
    tagger.train(trainfile)
    tagger.tag(testfile,outfile)
