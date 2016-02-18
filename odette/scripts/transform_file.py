#!/usr/bin/env python
#==============================================================================
#author         :Miryam de Lhoneux
#email          :miryam.de_lhoneux@lingfil.uu.se
#date           :2015/12/30
#version        :0.1
#description    :Perform a transformation on a file
#usage          :python transform_file.py infile outfile [transform|detransform|to_conllx]
#Python version :2.7.6
#==============================================================================


import sys
from src.treebank_transformer import TreebankTransformer

if __name__=="__main__":
    infile = sys.argv[1]
    out = sys.argv[2]
    change = sys.argv[3]
    #TODO: make this an option
    dep_style = 'pdt'
    TM = TreebankTransformer(dep_style=dep_style)
    TM.transform(infile,out,change)
