# oDETTE (DEpendency Treebank Transformation and Evaluation)
A python package that is first aimed to serve as a platform for experiments on UD treebanks but can also be used with other dependency treebanks. It can be used to test parsers on all UD languages. Currently only MaltParser can be used. The package is first aimed at performing tree transformations. Currently only the verb group transformation has been implemented. Experiments are run in parallel to ensure fast results. 
 The verb group transformation and back transformation algorithms are described at length in

```bibtex
@inproceedings{delhoneuxMLCL2016,
    title={{Should Have, Would Have, Could Have. Investigating Verb Group Representations for Parsing with Universal Dependencies}},
    author={de Lhoneux, Miryam and Nivre, Joakim},
    booktitle={{Proceedings of the Workshop on Multilingual and Crosslingual Methods in NLP}},
    year = {2016}}
}

```
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
Most experiments on UD are run with main.py   
Run the following to find out more about the different options.
```bash
python odette/main.py --help
```
####All subparts can also be run individually:
```bash
$python odette/scripts/baseline.py treebank_name (e.g: UD_English) (trainfile testfile) #to run an individual baseline
$python odette/scripts/experiment.py treebank_name (dependency style (ud or pdt), POS-style (ud, pdt or sdt) ambig/orig/disambig) #to run a single transformation experiment (see paper to make sense of optional arguments)
$python odette/scripts/collect_stats.py treebank_name trainfile testfile (dependency style) #to collect stats of a single language
$python odette/scripts/transform_file.py infile outfile [transform|detransform|to_conllx] #to apply the change to a file
$python odette/src/parsers.py trainfile testfile outfile #to train Maltparser on a file and parse another
$python odette/src/malteval.py goldfile testfile #to print LAS UAS of a parsed file
```

###Release 1.0
The release corresponds to the experiments run in the paper cited above. All the commands corresponding to the tables are collected in paper\_commands.sh. The file gives comprehensive instructions for reproducing results. The experiments on SDT require the version of SDT available at http://nl.ijs.si/sdt/data/SDT-2006-05-17.zip and the PDT can be obtained through the LDC.

###TODO
* Write proper error messages
* Break the code if external code breaks (error messages coming from MaltParser can be confusing if something is done wrong)
