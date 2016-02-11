#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#description	:dependency relation of a DependencyGraph object
#Python version :2.7.6
#==============================================================================

class Dependency(object):
    """
    Dependency relation in conllu format, i.e:
    ID form lemma cpostag postag feats head deprel deps misc
    """
    def is_to_the_left_of(self,other_dep):
        return self.ID < other_dep.ID

    def is_to_the_right_of(self,other_dep):
        return self.ID > other_dep.ID

    def __str__(self):
        """
        output: conllu format
        """
        conllu = [self.ID,self.form, self.lemma,self.cpostag,self.postag,self.feats,
                  self.head, self.deprel,self.deps, self.misc]
        depstr = "\t".join([str(el) for el in conllu])
        return depstr + "\n"
