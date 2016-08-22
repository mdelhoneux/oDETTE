#!/usr/bin/env python
#==============================================================================
#author			:Miryam de Lhoneux
#email			:miryam.de_lhoneux@lingfil.uu.se
#date			:2015/12/30
#version		:1.0
#Python version :2.7.6
#==============================================================================

"""FUNCTIONS"""
def dict_count_to_freq(d):
    """Turns dictionary of counts to dictionary of frequencies"""
    tot_d = sum(d.values())
    for val in d:
        d[val] /= float(tot_d)
    return d


iso_code ={
 'UD_Ancient_Greek': 'grc',
 'UD_Ancient_Greek-PROIEL': 'grc_proiel',
 'UD_Arabic': 'ar',
 'UD_Basque': 'eu',
 'UD_Bulgarian': 'bg',
 'UD_Catalan': 'ca',
 'UD_Chinese': 'zh',
 'UD_Croatian': 'hr',
 'UD_Czech': 'cs',
 'UD_Czech-CAC': 'cs_cac',
 'UD_Czech-CLTT': 'cs_cltt',
 'UD_Danish': 'da',
 'UD_Dutch': 'nl',
 'UD_Dutch-LassySmall': 'nl_lassysmall',
 'UD_English': 'en',
 'UD_English-ESL': 'en_esl',
 'UD_English-LinES': 'en_lines',
 'UD_Estonian': 'et',
 'UD_Finnish': 'fi',
 'UD_Finnish-FTB': 'fi_ftb',
 'UD_French': 'fr',
 'UD_Galician': 'gl',
 'UD_German': 'de',
 'UD_Gothic': 'got',
 'UD_Greek': 'el',
 'UD_Hebrew': 'he',
 'UD_Hindi': 'hi',
 'UD_Hungarian': 'hu',
 'UD_Indonesian': 'id',
 'UD_Irish': 'ga',
 'UD_Italian': 'it',
 'UD_Japanese-KTC': 'ja_ktc',
 'UD_Kazakh': 'kk',
 'UD_Latin': 'la',
 'UD_Latin-ITTB': 'la_ittb',
 'UD_Latin-PROIEL': 'la_proiel',
 'UD_Latvian': 'lv',
 'UD_Norwegian': 'no',
 'UD_Old_Church_Slavonic': 'cu',
 'UD_Persian': 'fa',
 'UD_Polish': 'pl',
 'UD_Portuguese': 'pt',
 'UD_Portuguese-BR': 'pt_br',
 'UD_Romanian': 'ro',
 'UD_Russian': 'ru',
 'UD_Russian-SynTagRus': 'ru_syntagrus',
 'UD_Slovenian': 'sl',
 'UD_Slovenian-SST': 'sl_sst',
 'UD_Spanish': 'es',
 'UD_Spanish-AnCora': 'es_ancora',
 'UD_Swedish': 'sv',
'UD_Swedish-LinES': 'sv_lines',
'UD_Tamil': 'ta',
'UD_Turkish': 'tr'
}

pos_disambig = {
    'ud':
    {
        'main_verb':'VERB',
        'auxiliary':'AUX'
    },
    'sdt':
    {
        'main_verb':'Verb-main',
        #'auxiliary':'Verb-copula'
        'auxiliary':'aux'
    },
    'pdt':
    {
        'main_verb':'Vp',
        #'auxiliary':'Vc'
        'auxiliary':'aux'
    }
}
