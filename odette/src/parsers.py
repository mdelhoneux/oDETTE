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
        #cmd = "java -jar -Xmx8g %s -c %s -m learn -i %s -grl root"%(self._path_to_malt, self.name, trainfile)
        cmd = "java -jar -Xmx8g %s -F ./ud.xml -c %s -m learn -i %s -grl root -a stacklazy"%(self._path_to_malt, self.name, trainfile)
        #print cmd
        os.system(cmd)

    def parse(self, testfile, outfile):
        #TODO: I don't think I need to use ud.xml here
        cmd = "java -jar -Xmx8g %s -F ./ud.xml -c %s -m parse -i %s -o %s -grl root"%(self._path_to_malt,self.name, testfile, outfile)
        #cmd = "java -jar -Xmx8g %s -c %s -m parse -i %s -o %s -grl root"%(self._path_to_malt,self.name, testfile, outfile)
        #print cmd
        os.system(cmd)

    def is_trained(self):
        #return os.path.exists("%s%s"%(self._path_to_malt,self.name))
        return os.path.exists("%s.mco"%self.name)

class MaltOptimizer(Parser):
    #NOTE: does not support parallel training
    def __init__(self, name="parser", path_to_malt=config.maltparser, path_to_malt_opt=config.maltopt):
        self._path_to_malt = path_to_malt
        self._path_to_malt_opt = path_to_malt_opt
        self.name = name

    def train(self, trainfile, devfile=None):
        #TODO: this is so ugly it makes me cry
        owd = os.getcwd()
        os.chdir(self._path_to_malt_opt)

        treebank_dir = config.exp +  self.name
        #TODO: this is a hack
        if config.justFeatureModel:
            cmd01 = "mv %s/phase1_logFile.txt ./"%treebank_dir
            cmd02 = "mv %s/phase2_logFile.txt ./"%treebank_dir
            os.system(cmd01)
            os.system(cmd02)#getting uglier by the minute
            cmd = "java -jar -Xmx2g %sMaltOptimizer.jar -p 3 -m %s -c %s %s"%(self._path_to_malt_opt,self._path_to_malt,trainfile, devfile)
            os.system(cmd)

        else:
            for i in range(1,4):
                if i == 1 or not devfile:
                    v = ""
                else:
                    v = "-v " + devfile
                cmd = "java -jar -Xmx2g %sMaltOptimizer.jar -p %d -m %s -c %s %s"%(self._path_to_malt_opt, i,self._path_to_malt,trainfile, v)
                os.system(cmd)

        optfile = open("phase3_optFile.txt", "r")
        #take last line of file and take what's to the right of feat model option
        feature_model = [line for line in optfile][-1].split("feature_model (-F):")[1].strip("\n")

        cmd2 = "mv %s/finalOptionsFile.xml %s"%(self._path_to_malt_opt, treebank_dir)
        cmd3 = "mv %s.mco %s"%(self.name,owd)
        cmd4 = "cp %s %s"%(feature_model, treebank_dir)
        #TODO: AAAAAH nooooo  noonoononono 
        if justFeatureModel:
            cmd5 = "mv phase3_logFile.txt %s"%treebank_dir
            cmd6 = "mv phase3_optFile.txt %s"%treebank_dir
        else:
            cmd5 = 'for i in $(seq 1 3); do end="_optFile.txt"; mv phase$i$end %s;done'%treebank_dir
            cmd6 = 'for i in $(seq 1 3); do end="_logFile.txt"; mv phase$i$end %s;done'%treebank_dir
        os.system(cmd2)
        os.system(cmd3)
        os.system(cmd4)
        os.system(cmd5)
        os.system(cmd6)
        os.chdir(owd)
        #need more for czech -- sometimes
        cmd5 = "java -jar -Xmx2g %s -f %s/finalOptionsFile.xml -c %s_maltopt -F %s/%s"%(self._path_to_malt,treebank_dir, self.name, treebank_dir,feature_model)
        os.system(cmd5)

    def parse(self,testfile,outfile):
        #TODO: aaaah seriously Miryam
        cmd = "java -jar -Xmx8g %s -f %s%s/finalOptionsFile.xml -c %s_maltopt -m parse -i %s -o %s"%(self._path_to_malt,config.exp,self.name, self.name, testfile, outfile)
        os.system(cmd)

    def is_trained(self):
        #TODO: actually this checks if MaltParser is trained -- do something
        #about this
        return os.path.exists("%s_maltopt.mco"%self.name)

class UDPipeParser(Parser):
    def __init__(self,name="udpipe_parser",path="./", run=1):
        self._path = path
        self.name=name
        self.run = run

    def train(self,trainfile, devfile=None):
        if not devfile:
            cmd = "udpipe --train --tagger=none --tokenizer=none --parser run=%d %s%s %s"%(self.run, self._path, self.name, trainfile)
        else:
            cmd = "udpipe --train --heldout=%s --tagger=none --tokenizer=none --parser run=%d %s%s %s"%(devfile,self.run, self._path, self.name, trainfile)
        os.system(cmd)

    def parse(self,testfile,outfile):
        cmd = "udpipe --parse %s%s %s >%s"%(self._path, self.name,testfile,outfile)
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
