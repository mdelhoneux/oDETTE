# oDETTE (DEpendency Treebank Transformation and Evaluation)
A python package that is first aimed to serve as a platform for experiments on UD treebanks but can also be used with other dependency treebanks. It can be used to test parsers on all UD languages. Currently only MaltParser can be used. The package is first aimed at performing tree transformations. Currently only the verb group transformation has been implemented. Experiments are run in parallel to ensure fast results.
#Installation instructions
```bash
$git clone repository 
$pip install -r requirements.txt
$export PYTHONPATH=$PYTHONPATH:path/to/directory
$mkdir EXP #this will contain the files that the package will work with
```
###Requirements: 
python 2.7
####Maltparser
```bash
$wget http://maltparser.org/dist/maltparser-1.8.1.tar.gz
$tar -xvf maltparser-1.8.1.tar
```
####Malteval
```bash
$wget http://stp.lingfil.uu.se/~nivre/download/UD_Data+MaltEval.tar.gz
$tar -xvf UD_Data+MaltEval.tar.gz 
$mv Users/joani384/MaltEval/lib/MaltEval.jar /path/to/dir
$rm -r Users UD_Data
```
###Config file
Change variables data, code, maltparser and malteval to be the directories that you put them in. By default, it is assumed that the code is the current directory, that data, maltparser and malteval are directories in the current directory called ud-treebanks-v1.2, maltparser-1.8.1 and malteval respectively. 

#Usage
To reproduce experiments run the main file with the different options.
Run the following to find out more about the different options.
```bash
python odette/main.py --help
```
####All subparts can also be run individually:
```bash
$python odette/scripts/baseline.py treebank_name (e.g: UD_English) trainfile testfile #to run an individual baseline
$python odette/scripts/experiment.py treebank_name POS-style (ud or sdt) #to run a single transformation experiment
$python odette/scripts/collect_stats.py treebank_name trainfile testfile #to collect stats of a single language
$python odette/scripts/transform_file.py infile outfile [transform|detransform|to_conllx] #to apply the change to a file
$python odette/src/parsers.py trainfile testfile outfile #to train Maltparser on a file and parse another
$python odette/src/malteval.py goldfile testfile #to print LAS UAS of a parsed file
```
