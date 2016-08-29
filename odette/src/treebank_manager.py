#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2016/08/23
#version		:1.1
#description	:A class to facilitate treebank managing
#               :It can also be used to run baselines
#Python version :2.7.6
#==============================================================================


from src.conllu import ConllFileHandler, MaltTabReader
from src.parsers import MaltParser, MaltOptimizer, UDPipeParser
from src.taggers import UDPipeTagger
import config
import os
from src.UD_treebank import UDtreebank
from src.treebank_transformer import TreebankTransformer

class TreebankManager():
    #TODO: change default parser back to maltparser
    def __init__(self,treebank_name=None,file_handler=ConllFileHandler(), parser="maltOpt", outdir=None, tagger="udpipe"):
        if not outdir: outdir= config.exp + treebank_name
        if not os.path.exists(outdir): os.mkdir(outdir)
        #if not trainfile and not testfile :
        self.treebank = UDtreebank(treebank_name)
        #self.trainfile = tb.trainfile
        #self.devfile = tb.devfile
        #self.testfile = tb.testfile
        self.conllx = False
        self.TT = TreebankTransformer(treebank_name=treebank_name)
        if parser == "malt":
            self._parser = MaltParser(name=treebank_name)
        elif parser == "maltOpt":
            self._parser = MaltOptimizer(name=treebank_name)
            self.conllx = True
        elif parser == "udpipe":
            self._parser = UDPipeParser(path="%s/udpipe-parser"%outdir)
        else:
            raise Exception, "Invalid parser"

        if tagger == "udpipe":
            self._tagger = UDPipeTagger(path="%s/udpipe-tagger"%outdir)
        else:
            raise Exception, "Invalid tagger"
        self.treebank_name = treebank_name
        self._file_handler = file_handler
        self.outdir = outdir

        #TODO: all of this is VERY confusing

        self.test_tagged = "%s/test_tagged.conllu"%outdir
        self.testfile = self.treebank.testfile
        self.test_parsed = "%s/test_parsed.conll"%outdir

        #need conllx for maltopt
        if self.conllx:
            self.trainfile = "%s/train.conll"%outdir
            self.TT.transform(self.treebank.trainfile,self.trainfile,"to_conllx")
            self.devfile = "%s/devfile.conll"%outdir
            self.TT.transform(self.treebank.devfile,self.devfile,"to_conllx")
            self.test_gold = "%s/test_gold.conllx"%outdir
            self.TT.transform(self.testfile, self.test_gold, "to_conllx")
        else:
            self.trainfile = self.treebank.trainfile
            self.devfile = self.treebank.devfile
            self.test_gold = self.treebank.testfile
        if parser == "malt":
            self.test_tagged = self.devfile
            self.test_gold = self.dev_gold
            self.testfile = self.treebank.devfile

    def train_tagger(self, devfile=None):
        self._tagger.train(self.trainfile, devfile)

    def train_parser(self, devfile=None):
        self._parser.train(self.trainfile, devfile)

    def tag_test_file(self):
        self._tagger.tag(self.testfile, self.test_tagged)
        if self.conllx:
            self.test_tagged_x = "%s/test_tagged.conllx"%self.outdir
            self.TT.transform(self.test_tagged,self.test_tagged_x,"to_conllx")
            self.test_tagged = self.test_tagged_x

    def test_parser(self):
        self._parser.parse(self.test_tagged, self.test_parsed)
