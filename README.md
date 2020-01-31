# PyKEEN Experimenal Results

This repository contains two main experiments:

## Reproducibility Study

In this study, we use the KGEMs reimplemented in PyKEEN and the authors' best
reported hyperparemeters to make reproductions of past experiments.

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
