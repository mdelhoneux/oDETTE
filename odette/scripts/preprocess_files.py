import os
import config
from src.treebank_transformer import TreebankTransformer
from src.UD_treebank import UDtreebank

def prepare_files(treebank_name, outdir=None, trainfile=None, testfile=None,
                  ambig_type=None, dep_style='ud', pos_style='ud'):
    if not outdir: outdir= config.exp + treebank_name
    if not os.path.exists(outdir): os.mkdir(outdir)
    if not trainfile and not testfile :
        tb = UDtreebank(treebank_name)
        trainfile = tb.trainfile
        devfile = tb.devfile
        testfile = tb.testfile
    TM = TreebankTransformer(treebank_name=treebank_name, dep_style=dep_style,
                             pos_style=pos_style)

    TM.transform(trainfile, TM.trainfile, 'to_conllx')
    TM.transform(devfile, TM.devfile, 'to_conllx')
    TM.transform(testfile, TM.testfile, 'to_conllx')

    #experiments about ambiguity
    if ambig_type:
        TM.transform(TM.trainfile, TM.trainfile, ambig_type)
        TM.transform(TM.testfile, TM.testfile, ambig_type)


if __name__=="__main__":
    """
    usage: python preprocess_files.py treebank_name trainfile testfile (ambig
    dep_style pos_style)
    """
    import sys
    treebank_name = sys.argv[1]
    train = sys.argv[2]
    test = sys.argv[3]
    ambig = None
    dep_style ="ud"
    pos_style ="ud"
    if len(sys.argv) > 4:
        ambig = sys.argv[4]
        dep_style = sys.argv[5]
        pos_style = sys.argv[6]
    prepare_files(treebank_name,trainfile=train,testfile=test, ambig_type=ambig,
                  dep_style=dep_style, pos_style=pos_style)
