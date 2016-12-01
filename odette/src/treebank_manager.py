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
    def __init__(self,treebank_name=None,file_handler=ConllFileHandler(), parser="maltOpt", outdir=None, tagger="udpipe", devfile=None):
        if not outdir: outdir= config.exp + treebank_name
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
            self._parser = UDPipeParser(path="%s"%outdir, name="udpipe-parser")
        else:
            raise Exception, "Invalid parser"

        if tagger == "udpipe":
            self._tagger = UDPipeTagger(path="%s"%outdir, name="udpipe-tagger")
        else:
            raise Exception, "Invalid tagger"
        self.treebank_name = treebank_name
        self._file_handler = file_handler

        #TODO: all of this is VERY confusing -->either clean or remove need to
        #use conllx at all

        self.test_tagged = "%stest_tagged.conllu"%outdir
        self.dev_tagged = "%sdev_tagged.conllu"%outdir
        self.testfile = self.treebank.testfile
        #TODO: name the outfile according to parsing model
        self.test_gold = "%stest_gold.conllx"%outdir
        self.TT.transform(self.testfile, self.test_gold, "to_conllx")

        #need conllx for maltopt and malteval
        if self.conllx:
            self.trainfile = "%strain.conll"%outdir
            self.TT.transform(self.treebank.trainfile,self.trainfile,"to_conllx")
            self.devfile = "%sdevfile.conll"%outdir
            self.TT.transform(self.treebank.devfile,self.devfile,"to_conllx")
        else:
            self.trainfile = self.treebank.trainfile
            self.devfile = self.treebank.devfile

        self.dev_gold = "%sdev_gold.conllx"%outdir
        self.TT.transform(self.devfile, self.dev_gold, "to_conllx")

    def train_tagger(self, devfile=None):
        #TODO: this is actually pretty useless
        self._tagger.train(self.trainfile, devfile)

    def train_parser(self, devfile=None):
        #TODO: this is actually pretty useless
        self._parser.train(self.trainfile, devfile)

    def tag_test_file(self):
        self._tagger.tag(self.testfile, self.test_tagged)
        self._tagger.tag(self.devfile, self.dev_tagged)
        if self.conllx:
            #test
            self.test_tagged_x = "%stest_tagged.conllx"%self.outdir
            self.TT.transform(self.test_tagged,self.test_tagged_x,"to_conllx")
            self.test_tagged = self.test_tagged_x
            #dev
            self.dev_tagged_x = "%sdev_tagged.conllx"%self.outdir
            self.TT.transform(self.dev_tagged,self.dev_tagged_x,"to_conllx")
            self.dev_tagged = self.dev_tagged_x

    def test_parser(self):
        self.test_parsed = "%stest_parsed_%s.conll"%(self.outdir, self.parser_name)
        self.dev_parsed = "%sdev_parsed_%s.conll"%(self.outdir, self.parser_name)
        #TODO: move this somewhere else? 
        #check if file has already been parsed
        #if os.stat(self.test_parsed).st_size == 0:
        self._parser.parse(self.test_tagged, self.test_parsed)
        self._parser.parse(self.dev_tagged, self.dev_parsed)
        if not self.conllx: #TODO: this is hacky, means if conllx has not been used so far
            self.test_parsed_x = "%stest_parsed_%s.conllx"%(self.outdir, self.parser_name)
            #same thing: hacky and ugly
            #if os.stat(self.test_parsed_x).st_size == 0:
            self.TT.transform(self.test_parsed, self.test_parsed_x, "to_conllx")
            self.test_parsed = self.test_parsed_x
            #dev
            self.dev_parsed_x = "%sdev_parsed_%s.conllx"%(self.outdir, self.parser_name)
            self.TT.transform(self.dev_parsed, self.dev_parsed_x, "to_conllx")
            self.dev_parsed = self.dev_parsed_x

    def split_training(self):
        training_dgs = self._file_handler.file_to_dg_list(self.trainfile)
        from random import shuffle
        shuffle(training_dgs)
        self.split_sizes = config.split_sizes
        self.splits = []
        # do not consider split sizes below tot n
        tot_tokens = sum([len(dg) for dg in training_dgs])
        self.split_sizes = [i for i in self.split_sizes if i<tot_tokens]

        n_tokens = 0
        sentence_number = 0
        for split_size in self.split_sizes:
            next_split = False
            while not next_split:
                n_tokens += len(training_dgs[sentence_number])
                if n_tokens/float(split_size) >=1:
                    split_filename = "%ssplit_%s"%(self.outdir,split_size)
                    self.splits.append(split_filename)
                    split_dgs = training_dgs[:sentence_number + 1]
                    self._file_handler.dep_graphs_to_file(split_filename,split_dgs)
                    next_split = True
                else:
                    sentence_number +=1
