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
        if parser == "malt":
            self._parser = MaltParser(name=treebank_name)
        elif parser == "maltOpt":
            self._parser = MaltOptimizer(name=treebank_name)
        elif parser == "udpipe":
            self._parser = UDPipeParser(path="%s/udpipe-parser"%outdir)
        else:
            raise Exception, "Invalid parser"

        if tagger == "udpipe":
            self._tagger = UDPipeTagger(path="%s/udpipe-tagger"%outdir)
            #TODO: change to that after I made sure maltopt works
            #self._tagger = UDPipeTagger(name=treebank_name)
        else:
            raise Exception, "Invalid tagger"
        self.treebank_name = treebank_name
        self._file_handler = file_handler
        #TODO: ouch this is ugly
        self.trainfile = "%s/train.conll"%outdir
        self.devfile = "%s/dev_tagged.conllu"%outdir
        self.testfile = "%s/test_tagged.conllu"%outdir
        self.dev_gold = "%s/dev_gold.conllx"%outdir
        self.test_gold = "%s/test_gold.conllx"%outdir
        self.dev_parsed = "%s/dev_parsed.conllu"%outdir
        self.dev_parsed_x = "%s/dev_parsed.conllx"%outdir

    def train_tagger(self):
        self._tagger.train(self.treebank.trainfile)

    def train_parser(self):
        #TODO: problem: depends on parser which to use: conllu or conllx
        self._parser.train(self.trainfile)

    def tag_test_files(self):
        self._tagger.tag(self.treebank.devfile, self.devfile)
        self._tagger.tag(self.treebank.testfile, self.testfile)

    def test_parser(self):
        self._parser.parse(self.devfile, self.dev_parsed)
