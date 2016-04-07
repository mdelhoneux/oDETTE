DATA=$DATA #should contain PDT SDT-2006-05-17 and ud-treebanks-v1.2
#Some commands specify the output file, some don't, but hopefully all will make sense.
#(only table 2 and 3 are created with a single command)
#All results are produced as csv files that are created in the current directory
#NOTE: some commands need the config file to be changed so running this whole file will not produce the exact same results as in the paper
# instructions are in the file

#preprocessing
#UD
cat $DATA/ud-treebanks-v1.2/UD_Czech/cs-ud-train-* >cs-ud-train.conllu #concatenate PDT training files
python odette/main.py --exp_type prep --include include.txt
#SDT
python odette/scripts/preprocess_files.py SDT $DATA/SDT-2006-05-17/slovene_sdt_train.conll $DATA/SDT-2006-05-17/slovene_sdt_test.conll orig pdt sdt
#PDT
mkdir EXP/PDT
python odette/src/conllu.py $DATA/PDT/training.gs.tab EXP/PDT/train.conll
python odette/src/conllu.py $DATA/PDT/devtest.hmm.tab EXP/PDT/test_gold.conll

##TABLES
#overview table (table 1)
python odette/main.py --include include.txt --exp_type stats --outfile stats.csv
python odette/scripts/collect_stats.py SDT EXP/SDT/train.conll EXP/SDT/test_gold.conll pdt
python odette/scripts/collect_stats.py PDT EXP/PDT/train.conll EXP/PDT/test_gold.conll pdt
#main results table (table 2)
python odette/main.py --include include.txt  --outfile baselines.csv
python odette/main.py --include include.txt  --exp_type exp --outfile table2.csv
#Results on MS (table 3)
python odette/main.py --exp_type ms_gold --include include.txt --outfile table3.csv


#ambiguous experiment on PDT and SDT (table 5)
#---turn off USE_CPOSTAG in config
#SDT
#disambig
python odette/scripts/preprocess_files.py SDT $DATA/SDT-2006-05-17/training.gs.conll $DATA/SDT-2006-05-17/devtest.hmm.conll disambig pdt sdt
python odette/scripts/baseline.py SDT
python odette/scripts/experiment.py SDT pdt pdt disambig
#ambig
python odette/scripts/preprocess_files.py SDT $DATA/SDT-2006-05-17/training.gs.conll $DATA/SDT-2006-05-17/devtest.hmm.conll ambig pdt sdt
python odette/scripts/baseline.py SDT
python odette/scripts/experiment.py SDT pdt sdt ambig

#PDT
#disambig
python odette/scripts/preprocess_files.py PDT $DATA/PDT/training.gs.conll $DATA/PDT/devtest.hmm.conll disambig pdt pdt
python odette/scripts/baseline.py PDT
python odette/scripts/experiment.py PDT pdt pdt disambig
#ambig
python odette/scripts/preprocess_files.py PDT $DATA/PDT/training.gs.conll $DATA/PDT/devtest.hmm.conll ambig pdt pdt
python odette/scripts/baseline.py PDT
python odette/scripts/experiment.py PDT pdt pdt ambig
#----

#ambiguous experiment on UD (table 6)
python odette/scripts/preprocess_files UD_Slovenian $DATA/ud-treebanks-v1.2/UD_Slovenian/sl-ud-train.conllu  $DATA/ud-treebanks-v1.2/UD_Slovenian/sl-ud-dev.conllu ambig ud ud
python odette/scripts/baseline.py UD_Slovenian
python odette/scripts/experiment.py UD_Slovenian 
python odette/scripts/preprocess_files UD_Czech $DATA/ud-treebanks-v1.2/UD_Czech/cs-ud-train.conllu  $DATA/ud-treebanks-v1.2/UD_Czech/cs-ud-dev.conllu ambig ud ud
python odette/scripts/baseline.py UD_Czech
python odette/scripts/experiment.py UD_Czech 
#For the bottom of the table, turn off KEEP_COP in config and rerun all commands above

#Figure
python odette/scripts/plot_deprel.py
