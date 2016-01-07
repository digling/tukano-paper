# Supplementary Material and Source Code accompanying "Improved Computational Models of Sound Change Shed Light on the History of the Tukano Languages"

## General remarks

This datasets contains the supplementary material and the source code to replicate the analyses underlying the paper "Improved computational models of sound change shed light on the history of the Tukano languages" by J.-M. List and T. Chacon. With the material offered in this repository, you should be able to replicate all analyses we describe in the paper, provided you

* have Python3 installed (our analyses were based on Python 3.4 and Python 3.5)
* have LingPy installed (http://lingpy.org, version 2.2 or higher, LingPy is only used for marginal tasks of filehandling, and one can easily write a workaround that functions without LingPy)
* have Networkx installed (http://networkx.org)

## Structure of the repository

This repository contains a lot of different files. In order to keep some order in the potential chaos, the files are all given a prefix in upper-case letters:

* C: major code files (all in Python)
* D: major data files (text or tsv-format)
* R: major result files (trees in newick-format, or other formats)
* L: major library files (the code that is the basic for the analysis which are carry out with help of the scripts)
* I: the input data for the major analysis in JSON-format
* T: template files
* E: two external tree files which we supply here: the tree by Chacon (2014), as mentioned in the paper, and the consensus tree which we suggest to reflect our current knowledge along with its limitations on the classification of the Tukano languages.

## Preparing the data

In order to run the code that prepares the data, simply type the following from the terminal (note that "python" refers to your actual python3-version, which may have a different name depending on your operating system): 

```shell

$ python C_compile_data.py
```

This should reproduce the file `I_data`.json, which is needed for the main analysis.

Alternatively, simply run the shell script:

```shell
$ sh MAKE.sh compile
```

## Carrying out the main analysis

For the main analysis (be careful, since it takes a long time if you want to check 500 000 trees for each model), simply type:

```shell
$ sh MAKE.sh analyse
```

## Creating the plots

In this repository, the plots are given as a simple zip-file. If you unpack this file on your computer and open the file BROWSE.html in your preferred webbrowser, you can navigate between the explicit results for each of the analyses. In order to replicate the creation of these plots, type:

```shell

$ sh MAKE.sh plot
```

This will create a folder called "html" which should contain the same files as the zip-file "html.zip".

## Testing the accurracy of reconstruction

In order to test how well a given family tree and a given model yields the same proto-forms as Chacon (2014), just type:

```shell
$ sh MAKE.sh proto
```

## Testing the degree of homoplasy

In order to test the degree of homoplasy, just type:

```shell
$ sh MAKE.sh homoplasy
```

## Results

Currently, we do not have any program that computes consensus trees automatically. So we did this with help of Dendroscope (http://dendroscope.org). The main analysis creates two different kinds of output data:

* `R_model_trees`: the file containing the most parsimonious trees for a given model
* `R_model.trees.log`: the file containing all trees which were tested during the analysis along with their parsimony scores
* `R_scf_model.gml`: A gml-file showing the graph of all directed changes inferred by the model. Use software like cytoscape (http://cytoscape.org) to browse and inspect this file.
* `R_sound-change-frequencies-model.tsv`: A tsv-file which shows the frequency of inferred sound-change processes and is thereby also essential to check for homoplastic characters.

In order to plot your model, you need to calculate the consensus using any program you find useful (we recommend Dendroscope, since it's easy to use) and then run the plot-code in Python, thereby specifying the name of your tree file:

```shell

$ python C_analyze.py plot matrix=yourmodel tree=yourconsensus
```

Don't forget to adjust "yourmodel" and "yourconsensus" accordingly!



