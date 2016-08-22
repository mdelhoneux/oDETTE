#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#description	:collect iso codes in UD directories
#usage			:python scripts/collect_iso_codes.py
#Python version :2.7.6
#==============================================================================


import os
import sys
import pprint

#generate a dictionary of iso_codes from ud treebank directory
codes = {}
ud_dir = sys.argv[1]
for language in os.listdir(ud_dir):
    ldir = ud_dir + "/" + language
    for f in os.listdir(ldir):
        if len(f.split(".")) >1 and f.split(".")[1] == "conllu":
            iso_code = f.split("-")[0]
            codes[language] = iso_code

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(codes)
