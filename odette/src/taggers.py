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
    def __init__(self,path="./udpipe_tagger"):
        self._path = path

    def train(self,trainfile, devfile=None):
        if not devfile:
            cmd = "udpipe --train --parser=none --tokenizer=none %s %s"%(self._path,trainfile)
        else:
            cmd = "udpipe --train --heldout=%s --parser=none --tokenizer=none %s %s"%(devfile, self._path,trainfile)
        os.system(cmd)

    def tag(self,testfile,outfile):
        cmd = "udpipe --tag %s %s >%s"%(self._path,testfile,outfile)
        os.system(cmd)

if __name__=="__main__":
    import sys
    trainfile = sys.argv[1]
    testfile = sys.argv[2]
    outfile = sys.argv[3]
    tagger = UDPipeTagger()
    tagger.train(trainfile)
    tagger.tag(testfile,outfile)
