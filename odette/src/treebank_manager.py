#!/usr/bin/env python
#==============================================================================
#author         :Miryam de Lhoneux
#email          :miryam.de_lhoneux@lingfil.uu.se
#date           :2016/08/23
#version        :1.1
#description    :A class to facilitate treebank managing
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
    def __init__(self,treebank_name=None,file_handler=ConllFileHandler(), parser="maltOpt", outdir=None, tagger="udpipe"):
        if not outdir: outdir= config.exp + treebank_name
        #import ipdb;ipdb.set_trace()
        #if not outdir: self.outdir= config.exp + treebank_name + "/"
        self.outdir = outdir
        if not os.path.exists(self.outdir): os.mkdir(self.outdir)
        self.treebank = UDtreebank(treebank_name)
        self.conllx = False
        self.TT = TreebankTransformer(treebank_name=treebank_name)
        self.parser_name = parser
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

        #TODO: all of this is VERY confusing -->either clean or remove need to
        #use conllx at all

        self.test_tagged = "%s/test_tagged.conllu"%outdir
        self.testfile = self.treebank.testfile
        self.test_parsed = "%s/test_parsed_%s.conll"%(outdir, self.parser_name)
        self.test_gold = "%s/test_gold.conllx"%outdir
        self.TT.transform(self.testfile, self.test_gold, "to_conllx")

        #need conllx for maltopt and malteval
        if self.conllx:
            self.trainfile = "%s/train.conll"%outdir
            self.TT.transform(self.treebank.trainfile,self.trainfile,"to_conllx")
            self.devfile = "%s/devfile.conll"%outdir
            self.TT.transform(self.treebank.devfile,self.devfile,"to_conllx")
        else:
            self.trainfile = self.treebank.trainfile
            self.devfile = self.treebank.devfile
        if parser == "malt": #test on development file
            self.TT.transform(self.treebank.devfile,self.devfile,"to_conllx")
            self.test_gold = self.devfile
            self.testfile = self.treebank.devfile

    def train_tagger(self, devfile=None):
        #TODO: this is actually pretty useless
        self._tagger.train(self.trainfile, devfile)

    def train_parser(self, devfile=None):
        #TODO: this is actually pretty useless
        self._parser.train(self.trainfile, devfile)

    def tag_test_file(self):
        self._tagger.tag(self.testfile, self.test_tagged)
        if self.conllx:
            self.test_tagged_x = "%s/test_tagged.conllx"%self.outdir
            self.TT.transform(self.test_tagged,self.test_tagged_x,"to_conllx")
            self.test_tagged = self.test_tagged_x

    def test_parser(self):
        self._parser.parse(self.test_tagged, self.test_parsed)
        if not self.conllx: #TODO: this is hacky, means if conllx has not been used so far
            self.test_parsed_x = "%s/test_parsed_%s.conllx"%(self.outdir, self.parser_name)
            self.TT.transform(self.test_parsed, self.test_parsed_x, "to_conllx")
            self.test_parsed = self.test_parsed_x

    def split_training(self):
        training_dgs = self._file_handler.file_to_dg_list(self.trainfile)
        import numpy as np
        self.split_sizes = np.arange(1000,15000,1000)
        self.splits = []
        for split_size in self.split_sizes:
            next_split = False
            for sentence_number, dg in enumerate(training_dgs):
                n_tokens = sum(len(dg) for dg in training_dgs[:sentence_number + 1])
                if n_tokens/float(split_size) >=1:
                    split_filename = "%ssplit_%s"%(self.outdir,split_size)
                    self.splits.append(split_filename)
                    split_dgs = training_dgs[:sentence_number + 1]
                    self._file_handler.dep_graphs_to_file(split_filename,split_dgs)
                    next_split = True
                    break
            if next_split:
                continue
