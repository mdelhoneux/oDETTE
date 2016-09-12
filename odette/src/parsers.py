#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#description	:Wrapper around existing parsers
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
    def is_trained(self):
        raise NotImplementedError

class MaltParser(Parser):
    #TODO: unpack more options: the best would be to read them from config files
    def __init__(self, path_to_malt=config.maltparser, name='parser'):
        self._path_to_malt = path_to_malt
        self.name = name

    def train(self, trainfile, devfile=None):
        cmd = "java -jar -Xmx8g %s -c %s -m learn -i %s -grl root"%(self._path_to_malt, self.name, trainfile)
        os.system(cmd)

    def parse(self, testfile, outfile):
        cmd = "java -jar -Xmx8g %s -c %s -m parse -i %s -o %s -grl root"%(self._path_to_malt,self.name, testfile, outfile)
        os.system(cmd)

    def is_trained(self):
        return os.path.exists("%s%s"%(self._path_to_malt,self.name))

class MaltOptimizer(Parser):
    #NOTE: does not support parallel training
    def __init__(self, name="parser", path_to_malt=config.maltparser, path_to_malt_opt=config.maltopt):
        self._path_to_malt = path_to_malt
        self._path_to_malt_opt = path_to_malt_opt
        self.name = name

    def train(self, trainfile, devfile=None):
        #TODO: (TODO REALLY LIKE REALLY TODO): WRONG use - correct that
        #TODO: this is so ugly it makes me cry
        #TODO: move this to some bash script?
        owd = os.getcwd()
        os.chdir(self._path_to_malt_opt)
        for i in range(1,4):
            if i == 1 or not devfile:
                v = ""
            else:
                v = "-v" + devfile
            cmd = "java -jar %sMaltOptimizer.jar -p %d -m %s -c %s %s"%(self._path_to_malt_opt, i,self._path_to_malt,trainfile, v)
            os.system(cmd)

        #TODO: this does not seem to work
        #cmd3 = "mv %s.*.xml %s%s"%(self._path_to_malt_opt, config.exp,self.name)
        #cmd4 = "mv %s.*.txt %s%s"%(self._path_to_malt_opt, config.exp,self.name)
        cmd3 = "mv %s/finalOptionsFile.xml %s%s"%(self._path_to_malt_opt, config.exp,self.name)
        cmd5 = "mv %s.mco %s"%(self.name,owd)
        #os.system(cmd3)
        #os.system(cmd4)
        os.system(cmd5)
        os.chdir(owd)
        #TODO: erm -grl option surely optimized --> should not be added here - 
        #need more for czech -- sometimes
        cmd2 = "java -jar -Xmx2g %s -f %s%s/finalOptionsFile.xml -c %s -m learn -i %s -grl root"%(self._path_to_malt,config.exp,self.name, self.name, trainfile)
        os.system(cmd2)

    def parse(self,testfile,outfile):
        #TODO: aaaah seriously Miryam
        cmd = "java -jar -Xmx2g %s -f %s%s/finalOptionsFile.xml -c %s -m parse -i %s -o %s -grl root"%(self._path_to_malt,config.exp,self.name, self.name, testfile, outfile)
        os.system(cmd)

    def is_trained(self):
        #TODO: actually this checks if MaltParser is trained -- do something
        #about this
        return os.path.exists("%s.mco"%self.name)

class UDPipeParser(Parser):
    def __init__(self,name="udpipe_parser",path="./"):
        self._path = path
        self.name=name

    def train(self,trainfile, devfile=None):
        if not devfile:
            cmd = "udpipe --train --tagger=none --tokenizer=none %s %s %s"%(self._path,self.name,trainfile)
        else:
            cmd = "udpipe --train --heldout=%s --tagger=none --tokenizer=none %s %s %s"%(devfile,self._path, self.name, trainfile)
        os.system(cmd)

    def parse(self,testfile,outfile):
        cmd = "udpipe --parse %s %s %s >%s"%(self._path, self.name,testfile,outfile)
        os.system(cmd)

    def is_trained(self):
        fullpath = self._path + self.name
        return os.path.exists(fullpath)


if __name__=="__main__":
    maltparser = MaltParser()
    trainfile = sys.argv[1]
    testfile = sys.argv[2]
    outfile = sys.argv[3]
    maltparser.train(trainfile)
    maltparser.parse(testfile,outfile)
