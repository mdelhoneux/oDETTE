DATA=~/Data
#overview table
python main.py --include include.txt --exp_type stats --outfile stats.csv
python scripts/collect_stats.py SDT $DATA/SDT-2006-05-17/slovene_sdt_train.conll $DATA/SDT-2006-05-17/slovene_sdt_test.conll sdt
#main results table (table 2)
python main.py --include include.txt --use_cpostag 1 --outfile baselines.csv
python main.py --include include.txt --use_cpostag 1 --exp_type exp --outfile exp.csv
#Results on MS (Table 3)
python main.py --exp_type ms_gold --include include.txt --use_cpostag 1 --outfile results_on.ms.csv
#ambiguous experiments (remaining tables)
python scripts/baseline.py SDT $DATA/SDT-2006-05-17/slovene_sdt_train.conll $DATA/SDT-2006-05-17/slovene_sdt_test.conll disambig sdt
python scripts/baseline.py SDT $DATA/SDT-2006-05-17/slovene_sdt_train.conll $DATA/SDT-2006-05-17/slovene_sdt_test.conll ambig sdt
python scripts/baseline.py UD_Slovenian $DATA/ud-treebanks-v1.2/UD_Slovenian/sl-ud-train.conllu $DATA/ud-treebanks-v1.2/UD_Slovenian/sl-ud-dev.conllu disambig ud
python scripts/baseline.py UD_Slovenian $DATA/ud-treebanks-v1.2/UD_Slovenian/sl-ud-train.conllu $DATA/ud-treebanks-v1.2/UD_Slovenian/sl-ud-dev.conllu  ambig ud
