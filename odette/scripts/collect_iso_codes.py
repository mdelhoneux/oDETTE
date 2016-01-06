#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#description	:collect iso codes in UD directories
#usage			:python scripts/collect_iso_codes.py
#Python version :2.7.6
#==============================================================================


import os
v1 = "/home/miryam/Data/ud-treebanks-v1.1/"
v2 = "/home/miryam/Data/ud-treebanks-v1.2/"
v1_1 = {}
v1_2 = {}
for language in os.listdir(v1):
    ldir = v1 + "/" + language
    for f in os.listdir(ldir):
        if len(f.split(".")) >1 and f.split(".")[1] == "conllu":
            iso_code = f.split("-")[0]
            v1_1[language] = iso_code

for language in os.listdir(v2):
    if language in v1_1:
        continue
    ldir = v2 + "/" + language
    for f in os.listdir(ldir):
        if len(f.split(".")) >1 and f.split(".")[1] == "conllu":
            iso_code = f.split("-")[0]
            v1_2[language] = iso_code
