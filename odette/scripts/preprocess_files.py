import os
from src.treebank_transformer import TreebankTransformer
from src.UD_treebank import UDtreebank

def prepare_files(treebank_name, outdir=None, trainfile=None,
                  testfile=None, ambig_type=None):
    if not outdir: outdir= config.exp + treebank_name
    if not os.path.exists(outdir): os.mkdir(outdir)
    if not trainfile and not testfile :
        tb = UDtreebank(treebank_name)
        trainfile = tb.trainfile
        testfile = tb.devfile
    TM = TreebankTransformer(treebank_name=treebank_name)
    TM.transform(trainfile, TM.trainfile, 'to_conllx')
    TM.transform(testfile, TM.testfile, 'to_conllx')

    #experiments about ambiguity
    if ambig_type:
        TM.transform(trainfile, TM.trainfile, ambig_type)
        TM.transform(testfile, TM.testfile, ambig_type)

if __name__=="__main__":
    """usage: python preprocess_files.py treebank_name trainfile testfile (ambig)"""
    treebank_name = sys.argv[1]
    train = sys.argv[2]
    test = sys.argv[3]
    ambig = None
    if len(sys.argv) > 4:
        ambig = sys.argv[4]
    prepare_files(treebank_name,trainfile=train,testfile=test,dep_style=dep_style,
                  pos_style=pos_style, ambig_type=ambig)