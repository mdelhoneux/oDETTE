#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#description	:Wrapper around existing parsers (only MaltParser for now)
#usage			:python src/parsers.py trainfile testfile outfile
#Python version :2.7.6
#==============================================================================


import config
import os
import sys

class Parser(object):
    def train(self, trainfile):
        raise NotImplementedError
    def parse(self, testfile, outfile):
        raise NotImplementedError

class MaltParser(Parser):
    #TODO: unpack more options
    def __init__(self, path_to_malt=config.maltparser, name='parser'):
        self._path_to_malt = path_to_malt
        self.name = name

    def train(self, trainfile):
        cmd = "java -jar -Xmx2g %s/maltparser-1.8.1.jar -c %s -m learn -i %s -grl root"%(self._path_to_malt, self.name, trainfile)
        os.system(cmd)

    def parse(self, testfile, outfile):
        cmd = "java -jar -Xmx2g %s/maltparser-1.8.1.jar -c %s -m parse -i %s -o %s -grl root"%(self._path_to_malt,self.name, testfile, outfile)
        os.system(cmd)

if __name__=="__main__":
    maltparser = MaltParser()
    trainfile = sys.argv[1]
    testfile = sys.argv[2]
    outfile = sys.argv[3]
    maltparser.train(trainfile)
    maltparser.parse(testfile,outfile)
