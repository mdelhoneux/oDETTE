#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#description	:A class to facilitate tree transformations on treebanks
#               :It can also be used to run baselines
#Python version :2.7.6
#==============================================================================


from src.conllu import ConllFileHandler
from src.tree_transformer import VGtransformer
from src.parsers import MaltParser
import config

class TreebankTransformer():
    def __init__(self,treebank_name=None,file_handler=ConllFileHandler(), transformer="vg",
                 parser="malt", outdir=None, pos_style="ud", use_cpostag=False):
        #TODO: ouch this is ugly
        if not outdir:
            if not treebank_name:
                self.outdir = config.exp
            else:
                self.outdir= config.exp + treebank_name + "/"
        else:
            self.outdir = outdir
        if parser == "malt":
            self._parser = MaltParser(name=treebank_name)
        else:
            raise Exception, "Invalid parser"
        self.treebank_name = treebank_name
        self._file_handler = file_handler
        self._transformer=transformer
        self.use_cpostag = use_cpostag
        self.trainfile = "%strain.conll"%self.outdir
        self.testfile = "%stest_gold.conll"%self.outdir
        self._pos_style = pos_style

    def init_files_for_transformation(self):
        self.parsed_ms = "%sdev_parsed.ms.conll"%self.outdir
        self.parsed_ud = "%sdev_parsed.ud.conll"%self.outdir
        self.transformed_train = "%strain.ms.conll"%self.outdir
        self.back_transf =  "%strain_backtransf.conll"%self.outdir

    def transform_parse_detransform(self):
        self.init_files_for_transformation()
        self.transform(self.trainfile, self.transformed_train, "transform")
        self._parser.train(self.transformed_train)
        self._parser.parse(self.testfile,self.parsed_ms)
        self.transform(self.parsed_ms, self.parsed_ud, "detransform")
        #TODO: somehow buggy with copula exp
        #self.transform(self.transformed_train, self.back_transf, "detransform")

    def count_aux(self, infile):
        """return n of aux n of tokens and n of sentences"""
        n_aux = 0
        n_tokens = 0
        dgs_in = self._file_handler.file_to_dg_list(infile)
        for dg in dgs_in:
            n_tokens += len(dg)
            transform = VGtransformer(dg, pos_style=self._pos_style)
            transform.transform()
            n_aux += transform.tot_aux
        return n_aux, n_tokens, len(dgs_in)

    def transform(self, infile, outfile, transformation):
        dgs_in = self._file_handler.file_to_dg_list(infile)
        dgs_out = []
        for dg in dgs_in:
            if self._transformer == "vg":
                transform = VGtransformer(dg, pos_style=self._pos_style)
            else:
                raise Exception, "Invalid transformation"
            if transformation == "transform":
                transform.transform()
            elif transformation == "detransform":
                transform.detransform()
            elif transformation == "disambig":
                transform.disambiguate_vg_postags()
            elif transformation == "ambig":
                dg.make_verbs_ambiguous()
            elif transformation == "to_conllx":
                dg.to_conllx(self.use_cpostag)
            else:
                raise Exception, "Invalid transformation"
            dgs_out.append(dg)
        self._file_handler.dep_graphs_to_file(outfile, dgs_out)
