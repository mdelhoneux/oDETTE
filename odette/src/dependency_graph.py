#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#description	:class to facilitate work with dependency graphs
#Python version :2.7.6
#==============================================================================


import os
class DependencyGraph(list):
    """
    A dependency graph is a list of dependency relations in conll format
    i.e.: ID form lemma cpostag postag feats head deprel deps misc
    """
    def get_split_words(self):
        return [dep for dep in self if dep.split_word]

    def remove_split_words(self):
        self.split = self.get_split_words()
        for dep in self.split:
            self.remove(dep)

    def reinsert_split_words(self):
        if not self.split: raise Exception, "no splits known"
        for dep in self.split:#property added when calling get split words
            first_word_index = int(dep.ID.split("-")[0])
            self.insert(first_word_index, dep)

    def get_dependents(self,word):
        return [dep for dep in self if (dep.head == word.ID)]

    def get_left_dependents(self,word):
        return [dep for dep in self if (dep.ID < word.ID) and (dep.head == word.ID)]

    def get_right_dependents(self,word):
        return [dep for dep in self if (dep.ID > word.ID) and (dep.head == word.ID)]

    def head_is_to_the_right(self,dep):
        return dep.ID < dep.head

    def has_cop_deprel(self):
        for dep in self:
            if dep.deprel == "cop":
                return True
        return False

    def to_conllx(self, use_cpostag=False):
        """
        make sure last two columns are underscore and postag is not empty
        if it is replace it with cpostag
        @parameter: use_cpostag: to replace postag with cpostag for parsing
        """
        self.remove_split_words()
        for dep in self:
            dep.deps = "_"
            dep.misc = "_"
            if dep.postag == "_":
                dep.postag = dep.cpostag
            if use_cpostag:
                dep.postag = dep.cpostag

    def make_verbs_ambiguous(self, dep_style="ud"):
        for dep in self:
            if dep_style == "ud":
                if dep.cpostag == "AUX":
                    dep.cpostag = "VERB"
                dep.postag = dep.cpostag
            elif dep_style == "pdt":
                pos = dep.postag.split("-")
                if len(pos) >1:
                    if pos[0] == "Verb":
                        dep.postag = "Verb"

    def closest_to(self,wordlist,main_word):
        """Find the word in the wordlist that is closest to the main word"""
        diffs = [abs(main_word - word) for word in wordlist]
        closest = diffs.index(min(diffs))
        return wordlist[closest]

    def furthest_to(self,wordlist,main_word):
        """Find the word in the wordlist that is furthest away from to the main word"""
        diffs = [abs(main_word - word) for word in wordlist]
        furthest = diffs.index(max(diffs))
        return wordlist[furthest]

    def to_latex(self):
        """
        Writes a dependency graph to latex then convert to png then open the figure
        in google chrome
        """
        #DISCLAIMER: MIGHT NOT WORK
        #FIXME: warning this thing became more of a bash script with lots of hardcoded stuff
        #generalize it at some point or remove (the Danish group seems to have
        #done a python visualizer (cf TLT talk) so I should check their code
        #FIXME: doesnt' work for French because of weird characters - I should do something
        # about the encoding
        #TODO: option to not output it to a file
        out = open('figure.tex', "w")
        text = " \& ".join([dep.form for dep in self])
        text += "\\\\"
        deps = []
        for dep in self:
            if dep.head == 0:
                #root case
                deplatex = "\deproot{%d}{%s}"%(dep.ID, dep.deprel)
                deps.append(deplatex)
            else:
                deplatex = "\depedge{%d}{%d}{%s}"%(dep.head, dep.ID, dep.deprel)
                deps.append(deplatex)
        dependencies = "\n".join(deps)

        out.write(" \
                          \documentclass{standalone} \n "\
                        + "\usepackage{tikz} \n "\
                        + "\usepackage{tikz-dependency} \n "\
                        + "\\begin{document} \n" \
                        + "\\begin{dependency}[theme = simple] \n" \
                        + "\\begin{deptext} \n" \
                        + " %s \n "%text\
                        + " \end{deptext} \n "\
                        + " %s \n "%dependencies\
                        + " \end{dependency} \n" \
                        + " \n \end{document}" )

        out.close()
        os.system("sh ./odette/src/createfigure.sh")
