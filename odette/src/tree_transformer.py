#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#description	:Class to transform representations in dependency graphs
#               :Currently only verb group transformation is implemented
#Python version :2.7.6
#==============================================================================


from src.dependency_graph import DependencyGraph
from src.verbgroup import VerbGroup, VerbGroupMS

class TreeTransformer(object):
    def __init__(self,tree, dep_style="ud", pos_style='ud', *args,**kwargs):
        self.dg = tree
        self._dep_style = dep_style #to determine what is an auxiliary dependency
        self._pos_style = pos_style
        super(TreeTransformer,self).__init__(*args,**kwargs)

    def transform(self):
        raise NotImplementedError

    def detransform(self):
        raise NotImplementedError

    def invert_dep(self,a,b):
        """
        there is a dependency between a and b
        b is the head of a and c is in turn the head of b
        a becomes the head of b and c becomes the head of a
        the deprel between b and c becomes the deprel between a and c
        """
        a_ID, a_deprel = a.ID, a.deprel
        b_head, b_deprel = b.head, b.deprel

        a.head = b_head
        a.deprel = b_deprel
        b.head = a_ID
        b.deprel = a_deprel

    def move_dependents(self,a,b):
        """move dependents from a to b"""
        a_deps = self.dg.get_dependents(a)
        for ad in a_deps:
            ad.head = b.ID

class VGtransformer(TreeTransformer):
    """
    A class to transform verb groups in dependency trees
    """
    def __init__(self, *args, **kwargs):
        self.n_double_aux = 0
        self.n_right_aux = 0
        self.tot_aux = 0
        super(VGtransformer, self).__init__(*args, **kwargs)

    def add_vg_pos_information(self, aux_pos, main_verbs_pos):
        """Update a dictionary adding counts of aux and main verb pos tags"""
        VGs = self.find_vgs_in_ud()
        for vg in VGs:
            if vg.main_verb.postag not in main_verbs_pos:
                main_verbs_pos[vg.main_verb.postag] = 0
            main_verbs_pos[vg.main_verb.postag] += 1
            for aux_id in vg.aux_ids:
                aux = self.dg[aux_id - 1].postag
                if aux not in aux_pos:
                    aux_pos[aux] = 0
                aux_pos[aux] += 1

    def disambiguate_vg_postags(self):
        from src.utils import pos_disambig
        VGs = self.find_vgs_in_ud()
        for vg in VGs:
            vg.main_verb.postag = pos_disambig[self._pos_style]['main_verb']
            for i in vg.aux_ids:
                self.dg[i-1].postag = pos_disambig[self._pos_style]['auxiliary']

    def transform(self):
        """
        The function first looks for verb groups in the sentence. A verb group has a main verb
        and at least one auxiliary.
        When there's just one auxiliary, it changes the dependency direction between
        the auxiliary and main verb and the head of the main verb becomes the head
        of the auxiliary
        When there are several auxiliaries, it attaches the closest one to the verb
        and the head of the main verb becomes the head of the outermost one
        It then deals with the dependents of the main verb to keep projecivity:
        dependents to the left of the leftmost verb get attached to the leftmost verb
        dependents to the right of the rightmost verb get attached to the rightmost verb
        remaining dependents get attached to the auxiliary that is closest to the verb
        """
        VGs = self.find_vgs_in_ud()
        for vg in VGs:
            if len(vg.aux_ids) == 1:
                self.invert_dep(vg.closest_aux, vg.main_verb)
            else:
                #if len(vg.aux_ids) >2:
                #self.dg.to_latex() #how I found the strange Danish example
                self.vg_to_chain(vg)
            self.projectivize(vg)

    def detransform(self):
        """Attach auxiliaries and their dependents to the main verb"""
        VGs = self.find_vgs_in_ms()
        for vg in VGs:
            self.invert_dep(vg.main_verb, vg.outermost_aux)
            for aux in vg.aux_ids:
                #other auxiliaries are dependent of an aux
                #and get moved at the same time as other dependents
                self.move_dependents(self.dg[aux-1],vg.main_verb)

    def is_aux_dependency(self,dep):
        if self._dep_style == "ud":
            return self.is_aux_dependency_in_ud(dep)
        elif self._dep_style == "pdt":
            return self.is_aux_dependency_in_pdt(dep)

    def is_aux_dependency_in_ud(self,dep):
        """Only auxiliary dependencies between verbal forms (aux or verb) are considered"""
        aux_tags = ["AUX", "VERB"]
        return ((dep.deprel == "aux") and (dep.cpostag in aux_tags) and (self.dg[dep.head-1].cpostag in aux_tags))

    def is_aux_dependency_in_pdt(self,dep):
        #TODO: I might want to also consider pos tags and keep only the verb ones
        return (dep.deprel == "AuxV")

    def is_head_of_aux_dependency(self,dependency):
        """return the ID of the dependency relation if it is"""
        deps = self.dg.get_dependents(dependency)
        for dep in deps:
            if self.is_aux_dependency(dep):
                return dep.ID
        return None

    def find_vgs_in_ud(self):
        """
        Pass sentence left to right collecting auxiliares,
        their main verbs and the other auxiliaries of the main verb
        Input: dependency graph
        output: list of verb group objects
        """
        #TODO: I might want to rename that since I use it for PDT
        VGs = []
        main_verbs = []
        vg = VerbGroup()
        i = -1
        while i < (len(self.dg) -1):
            i += 1
            if self.is_aux_dependency(self.dg[i]):
                self.tot_aux += 1
                aux = self.dg[i]
                if aux.head not in main_verbs: #new verb group
                    self.save_vg(vg,VGs) #save previous vg
                    main_verbs.append(aux.head)
                    vg = VerbGroup()
                    vg.aux_ids.append(aux.ID)
                    vg.main_verb = self.dg[aux.head - 1]
                else:
                    vg.aux_ids.append(aux.ID)
        self.save_vg(vg,VGs) #save last vg
        return VGs

    def find_vgs_in_ms(self):
        VGs = []
        vg = VerbGroupMS()
        i = -1
        all_aux = []
        while i < (len(self.dg) -1):
            i += 1
            if self.is_aux_dependency(self.dg[i]):
                aux = self.dg[i].head
                if aux not in all_aux:
                    vg.aux_ids.append(aux)
                    all_aux.append(aux)
                    self.recurse_aux_chain(vg,i,all_aux)
                    outermost_aux_id = self.dg.furthest_to(vg.aux_ids,vg.main_verb.ID)
                    vg.outermost_aux = self.dg[outermost_aux_id -1]
                    VGs.append(vg)
                    vg = VerbGroupMS()
        return VGs

    def recurse_aux_chain(self,vg,i,all_aux):
        """
        Recurse the chain of auxiliary dependency relations
        If the main verb is to the left, the recursion follows the heads of
        auxiliary dependency relations
        If the main verb is to the right, the recursion follows the dependents
        of auxiliary dependency relations until it finds the main verb
        """
        if self.dg.head_is_to_the_right(self.dg[i]):
            vg.main_verb = self.dg[i]
            self.recurse_aux_chain_via_head(vg,self.dg[i].head-1,all_aux)
        else:
            self.recurse_aux_chain_via_dependent(vg,i,all_aux)

    def recurse_aux_chain_via_head(self,vg,i,all_aux):
        #the head is itself the head of an aux dependency relation
        head = self.dg[self.dg[i].head -1]
        if self.is_aux_dependency(self.dg[i]):
            vg.aux_ids.append(head.ID)
            all_aux.append(head.ID)
            self.recurse_aux_chain_via_head(vg,head.ID -1,all_aux)

    def recurse_aux_chain_via_dependent(self,vg,i,all_aux):
        i_next = self.is_head_of_aux_dependency(self.dg[i])
        #the dependent is itself the head of an aux dependency relation
        if i_next:
            vg.aux_ids.append(self.dg[i].ID)
            all_aux.append(self.dg[i].ID)
            self.recurse_aux_chain_via_dependent(vg,i_next-1,all_aux)
        else:
            vg.main_verb = self.dg[i]

    def save_vg(self,vg,VGs):
        if len(vg.aux_ids) > 0:
            vg.aux_ids.sort()
            vg.rightmost_verb = self.dg[max(vg.aux_ids[-1],vg.main_verb.ID) - 1]
            vg.leftmost_verb = self.dg[min(vg.aux_ids[0],vg.main_verb.ID) - 1]
            closest_aux_id = self.dg.closest_to(vg.aux_ids, vg.main_verb.ID)
            vg.closest_aux = self.dg[closest_aux_id - 1]
            outermost_aux = self.dg.furthest_to(vg.aux_ids,vg.main_verb.ID)
            vg.outermost_aux = self.dg[outermost_aux -1]
            VGs.append(vg)

    def vg_to_chain(self,vg):
        mv_head,mv_deprel = vg.main_verb.head, vg.main_verb.deprel
        #change direction of dependency relation between main verb and closest aux
        vg.main_verb.head = vg.closest_aux.ID
        vg.main_verb.deprel = vg.closest_aux.deprel
        #head of main verb becomes head of outermost aux
        vg.outermost_aux.head = mv_head
        vg.outermost_aux.deprel = mv_deprel
        #remaining aux: a chain from the outermost to the main verb
        #main verb is to the right
        if vg.outermost_aux.ID < vg.main_verb.ID:
            for aux in vg.aux_ids[1:]:
                self.dg[aux-1].head = vg.aux_ids[vg.aux_ids.index(aux)-1]
        #main verb to the left
        else:
            for aux in vg.aux_ids[-2::-1]:
                self.dg[aux-1].head = vg.aux_ids[vg.aux_ids.index(aux)+1]

    def projectivize(self,vg):
        deps = self.dg.get_dependents(vg.main_verb)
        for dep in deps:
            if dep.is_to_the_left_of(vg.leftmost_verb):
                dep.head = vg.leftmost_verb.ID
            elif dep.is_to_the_right_of(vg.rightmost_verb):
                dep.head = vg.rightmost_verb.ID
            else:
                dep.head = vg.closest_aux.ID
