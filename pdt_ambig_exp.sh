#PDT
python odette/scripts/preprocess_files.py PDT ~/Data/PDT/training.gs.conll ~/Data/PDT/devtest.hmm.conll disambig pdt pdt
python odette/scripts/baseline.py PDT
python odette/scripts/experiment.py PDT pdt pdt disambig
python odette/scripts/preprocess_files.py PDT ~/Data/PDT/training.gs.conll ~/Data/PDT/devtest.hmm.conll ambig pdt pdt
python odette/scripts/baseline.py PDT
python odette/scripts/experiment.py PDT pdt pdt ambig
python odette/scripts/preprocess_files.py PDT ~/Data/PDT/training.gs.conll ~/Data/PDT/devtest.hmm.conll
python odette/scripts/baseline.py PDT
python odette/scripts/experiment.py PDT pdt pdt orig
