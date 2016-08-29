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
    def train(self, trainfile, devfile):
        raise NotImplementedError
    def parse(self, testfile, outfile):
        raise NotImplementedError

class MaltParser(Parser):
    #TODO: unpack more options
    def __init__(self, path_to_malt=config.maltparser, name='parser'):
        self._path_to_malt = path_to_malt
        self.name = name

    def train(self, trainfile, devfile=None):
        cmd = "java -jar -Xmx2g %s -c %s -m learn -i %s -grl root"%(self._path_to_malt, self.name, trainfile)
        os.system(cmd)

    def parse(self, testfile, outfile):
        cmd = "java -jar -Xmx2g %s -c %s -m parse -i %s -o %s -grl root"%(self._path_to_malt,self.name, testfile, outfile)
        os.system(cmd)

class MaltOptimizer(Parser):
    #NOTE: does not support parallel training
    def __init__(self, name="parser", path_to_malt=config.maltparser, path_to_malt_opt=config.maltopt):
        self._path_to_malt = path_to_malt
        self._path_to_malt_opt = path_to_malt_opt
        self._name = name

    def train(self, trainfile, devfile=None):
        #TODO: this is so ugly it makes me cry
        #TODO: move this to some bash script?
        owd = os.getcwd()
        os.chdir(self._path_to_malt_opt)
        if devfile:
            valid_command = "-v " + devfile
        else:
            valid_command = ""
        for i in range(1,4):
            #TODO: erm I'm sure I can do that more neatly
            if i == 1:
                v = ""
            else:
                v  = valid_command
            cmd = "java -jar %sMaltOptimizer.jar -p %d -m %s -c %s %s"%(self._path_to_malt_opt, i,self._path_to_malt,trainfile, v)
            print cmd
            os.system(cmd)
        cmd3 = "mv %sfinalOptionsFile.xml %s%s"%(self._path_to_malt_opt, config.exp,self._name)
        cmd4 = "mv %s.mco %s"%(self._name,owd)
        os.system(cmd3)
        os.system(cmd4)
        os.chdir(owd)
        cmd2 = "java -jar -Xmx2g %s -f %s%s/finalOptionsFile.xml -c %s -m learn -i %s -grl root"%(self._path_to_malt,config.exp,self._name, self._name, trainfile)
        os.system(cmd2)

    def parse(self,testfile,outfile):
        #TODO: aaaah seriously Miryam
        cmd = "java -jar -Xmx2g %s -f %s%s/finalOptionsFile.xml -c %s -m parse -i %s -o %s -grl root"%(self._path_to_malt,config.exp,self._name, self._name, testfile, outfile)
        os.system(cmd)

class UDPipeParser(Parser):
    def __init__(self,path="./udpipe_parser"):
        self._path = path

    def train(self,trainfile, devfile=None):
        if not devfile:
            cmd = "udpipe --train --tagger=none --tokenizer=none %s %s"%(self._path,trainfile)
        else:
            cmd = "udpipe --train --heldout=%s --tagger=none --tokenizer=none %s %s"%(devfile,self._path,trainfile)
        os.system(cmd)

    def parse(self,testfile,outfile):
        cmd = "udpipe --parse %s %s >%s"%(self._path,testfile,outfile)
        os.system(cmd)


if __name__=="__main__":
    maltparser = MaltParser()
    trainfile = sys.argv[1]
    testfile = sys.argv[2]
    outfile = sys.argv[3]
    maltparser.train(trainfile)
    maltparser.parse(testfile,outfile)
