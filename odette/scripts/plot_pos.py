from src.treebank_transformer import TreebankTransformer
from matplotlib import pyplot as plt
import sys

def plot_f_dict(d, filename):
    plt.figure()
    plt.bar(range(len(d)), d.values(), align="center")
    plt.xticks(range(len(d)), list(d.keys()))
    plt.savefig(filename)

if __name__=="__main__":
    treebank_name = sys.argv[1]
    pos_style = "ud"
    if len(sys.argv) > 2:
        pos_style = sys.argv[2]
    TT = TreebankTransformer(treebank_name, use_cpostag=True,pos_style=pos_style)
    main_verb_pos, aux_pos = TT.collect_vg_postags(TT.trainfile)
    plot_f_dict(main_verb_pos, "main_verb_%s.png"%treebank_name)
    plot_f_dict(aux_pos, "aux_pos_%s.png"%treebank_name)
