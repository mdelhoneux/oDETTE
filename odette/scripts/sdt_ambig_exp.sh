python odette/scripts/preprocess_files.py SDT ~/Data/SDT-2006-05-17/slovene_sdt_train.conll ~/Data/SDT-2006-05-17/slovene_sdt_test.conll disambig pdt sdt
python odette/scripts/baseline.py SDT
python odette/scripts/experiment.py SDT pdt sdt disambig
python odette/scripts/preprocess_files.py SDT ~/Data/SDT-2006-05-17/slovene_sdt_train.conll ~/Data/SDT-2006-05-17/slovene_sdt_test.conll ambig pdt sdt
python odette/scripts/baseline.py SDT
python odette/scripts/experiment.py SDT pdt sdt ambig
python odette/scripts/preprocess_files.py SDT ~/Data/SDT-2006-05-17/slovene_sdt_train.conll ~/Data/SDT-2006-05-17/slovene_sdt_test.conll
python odette/scripts/baseline.py SDT
python odette/scripts/experiment.py SDT pdt sdt orig
