#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#description	:Read and write files in conll format using DependencyGraph objects
#Python version :2.7.6
#==============================================================================


from odette.src.dependency import Dependency
from odette.src.dependency_graph import DependencyGraph

conllu = ["ID", "form", "lemma", "cpostag", "postag", "feats", "head", "deprel",
          "deps", "misc"]

conllx = ["ID", "form", "lemma", "cpostag", "postag", "feats", "head", "deprel",
          "phead", "pdeprel"]

malttab = ["form", "postag", "head", "deprel"]

class ConllFileHandler():
    def __init__(self,conll=conllu,separator="\t"):
        """Input: list of index labels (conllu default)"""
        self.conll = dict(enumerate(conllu))
        self._separator = separator

    def file_to_dg_list(self,filename, separator=None):
        """
        Input: a file in conll format
        Output: a list of dependency graphs
        @param: column separator
        """
        if not separator: separator = self._separator
        dependency_graphs = []
        with open(filename,'r') as f:
            dg = DependencyGraph()#initialize the first dg
            for line in f:
                if line.startswith("#"):
                    continue
                if line in ('\n', '\r\n'):#blank lines are end of sentences
                    #TODO: remove or make it an option
                    #if not dg.has_cop_deprel(): #remove any dg that has a copula deprel
                    dependency_graphs.append(dg)#retrieve the dg 
                    dg = DependencyGraph()#reinitialize
                else:
                    line = line.strip("\n")
                    dep = self.line_to_dependency(line, separator)
                    dg.append(dep)
        return dependency_graphs

    def line_to_dependency(self,line,separator):
        #TODO: slightly hacky but really fastest way to do it instead of
        #checking both the head and the ID
        dep_dict = {}
        cols = line.split(separator)
        for n, value in enumerate(cols):
            dep_dict[self.conll[n]] = value
        dep = Dependency()
        for col in dep_dict:
            if (col is "ID") or (col is "head"):
                try:
                    setattr(dep, col, int(dep_dict[col]))
                    setattr(dep, 'split_word', False) #maybe I shouldnt do this but check if attribute exists instead
                #case of word split ex: au = a le
                #add a field to retrieve them
                except ValueError:
                    setattr(dep, col, dep_dict[col])
                    setattr(dep, 'split_word', True)
            else:
                    setattr(dep, col, dep_dict[col])
        return dep

    def dep_graphs_to_file(self,filename,dependency_graphs):
        f=open(filename,'w')
        for dg in dependency_graphs:
            for dep in dg:
                f.write(dep.__str__())
            f.write("\n")
        f.close()

class MaltTabReader(ConllFileHandler):
    def __init__(self, *args, **kwargs):
        super(MaltTabReader,self,*args,**kwargs).__init__()
        self.conll = malt

    def dep_graphs_to_file(self,filename, dependency_graphs):
        f=open(filename,'w')
        for dg in dependency_graphs:
            for i,dep in enumerate(dg):
                dep.ID = i
                for el in conllu:
                    if el not in dep:
                        setattr(dep,el, "-")
                f.write(dep.__str__())
            f.write("\n")
        f.close()


def test_read():
    import difflib
    #cn = ConllFileHandler()
    cn = MaltTabReader()
    infile = 'test.tab'
    dgs = cn.file_to_dg_list(infile)
    out = './sanitytest.conll'
    cn.dep_graphs_to_file(out, dgs)
    diff = difflib.ndiff(infile.readlines(), out.readlines())
    delta = ''.join(x[2:] for x in diff if x.startswith('- '))
    print delta

if __name__ =="__main__":
    test_read()
