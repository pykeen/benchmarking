# PyKEEN Benchmarking Results

This repository contains the results from the reproducibility and benchmarking studies
described in 

[**Bringing Light Into the Dark: A Large-scale Evaluation of Knowledge Graph Embedding Models Under a Unified Framework**](http://arxiv.org/abs/2006.13365).
<br /> Ali, M., Berrendorf, M., Hoyt, C. T., Vermue, L., Galkin, M., Sharifzadeh, S., Fischer, A., Tresp, V., & Lehmann, J. (2020).
<br /> *arXiv*, 2006.13365.

## Reproducibility Study

In this study, we use the KGEMs reimplemented in PyKEEN and the authors' best
reported hyper-parameters to make reproductions of past experiments.

## Benchmarking Study

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
git clone https://github.com/pykeen/benchmarking.git pykeen_benchmarking
cd pykeen_benchmarking
pip install -e .
# ABLATION
python ablation/collate.py
python ablation/paper_plots.py
python ablation/plot.py
# REPRODUCTIONS
python reproducibility/generate_summary_table.py
python reproducibility/plot.py
```
