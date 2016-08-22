#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#Python version :2.7.6
#==============================================================================

import config
import src.utils
class UDtreebank():
    def __init__(self,language,location = config.data):
        self._language = language
        self._location = location
        iso_dic = src.utils.iso_code
        files_prefix = self._location + language + "/" + iso_dic[self._language]
        self.trainfile = files_prefix + "-ud-train.conllu"
        self.devfile = files_prefix + "-ud-dev.conllu"
        self.testfile = files_prefix + "-ud-test.conllu"
