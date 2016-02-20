#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:0.1
#Python version :2.7.6
#==============================================================================

"""FUNCTIONS"""
def dict_count_to_freq(d):
    """Turns dictionary of counts to dictionary of frequencies"""
    tot_d = sum(d.values())
    for val in d:
        d[val] /= float(tot_d)
    return d

"""OTHER"""
#ISO codes of different versions
v1_1 = {
     'UD_German': 'de',
     'UD_English': 'en',
     'UD_Basque': 'eu',
     'UD_Croatian': 'hr',
     'UD_Finnish': 'fi',
     'UD_Persian': 'fa',
     'UD_Danish': 'da',
     'UD_Hebrew': 'he',
     'UD_Indonesian': 'id',
     'UD_Greek': 'el',
     'UD_Swedish': 'sv',
     'UD_Finnish-FTB': 'fi_ftb',
     'UD_Irish': 'ga',
     'UD_Czech': 'cs',
     'UD_Spanish': 'es',
     'UD_French': 'fr',
     'UD_Bulgarian': 'bg',
     'UD_Italian': 'it',
     'UD_Hungarian': 'hu'
    }

extra = {
     'UD_Hindi': 'hi',
     'UD_Norwegian': 'no',
     'UD_Latin-ITT': 'la_itt',
     'UD_Latin-PROIEL': 'la_proiel',
     'UD_Dutch': 'nl',
     'UD_Romanian': 'ro',
     'UD_Slovenian': 'sl',
     'UD_Latin': 'la',
     'UD_Gothic': 'got',
     'UD_Arabic': 'ar',
     'UD_Estonian': 'et',
     'UD_Ancient_Greek': 'grc',
     'UD_Old_Church_Slavonic': 'cu',
     'UD_Ancient_Greek-PROIEL': 'grc_proiel',
     'UD_Tamil': 'ta',
     'UD_Japanese-KTC': 'ja_ktc',
     'UD_Portuguese': 'pt',
     'UD_Polish': 'pl'
    }

v1_2 = dict(v1_1.items() + extra.items())

pos_disambig = {
    #TODO: maybe these are not the best choices
    'ud':
    {
        'main_verb':'VERB',
        'auxiliary':'AUX'
    },
    'sdt':
    {
        'main_verb':'Verb-main',
        'auxiliary':'Verb-copula'
    },
    'pdt':
    {
        'main_verb':'Vp',
        'auxiliary':'Vc'
    }
}
