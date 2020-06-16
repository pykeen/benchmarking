# PyKEEN Experimental Results

This repository contains two main experiments:

## Reproducibility Study

In this study, we use the KGEMs reimplemented in PyKEEN and the authors' best
reported hyperparameters to make reproductions of past experiments.

## Ablation Study

In this study, we conduct a large number of hyper-parameter optimizations to
investigate the effects of certain aspects of models (training assumption,
loss function, regularizer, optimizer, negative sampling strategy, HPO
methodology, training strategy). There are two folders:

1. [`config`](/ablation/config) - The ablation study configuration JSON files
   used in the experiments
2. [`results`](/ablation/config) - The results from the ablation studies based
   on the configuration files

A summary of the results can be found [here](/ablation/results/_results/README.md)

## Regeneration of Charts

```sh
git clone https://github.com/mali-git/pykeen_experimental_results.git
cd pykeen_experimental_results
pip install -e .
# ABLATION
python ablation/collate.py
python ablation/paper_plots.py
python ablation/plot.py
# REPRODUCTIONS
python reproducibility/generate_summary_table.py
python reproducibility/plot.py
```
