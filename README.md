# PyKEEN Benchmarking Results

This repository contains the results from the reproducibility and benchmarking studies
described in 

> [**Bringing Light Into the Dark: A Large-scale Evaluation of Knowledge Graph Embedding Models Under a Unified Framework**](http://arxiv.org/abs/2006.13365).
<br /> Ali, M., Berrendorf, M., Hoyt, C. T., Vermue, L., Galkin, M., Sharifzadeh, S., Fischer, A., Tresp, V., & Lehmann, J. (2020).
<br /> *arXiv*, 2006.13365.

This repository itself is archived on Zenodo at [![DOI](https://zenodo.org/badge/222931424.svg)](https://zenodo.org/badge/latestdoi/222931424).

## Reproducibility Study

In this study, we use the KGEMs reimplemented in PyKEEN and the authors' best
reported hyper-parameters to make reproductions of past experiments.
The experimental artifacts from the reproducibility study can be found [here](/reproducibility).

## Benchmarking (Ablation) Study

In this study, we conduct a large number of hyper-parameter optimizations to
investigate the effects of certain aspects of models (training assumption,
loss function, regularizer, optimizer, negative sampling strategy, HPO
methodology, training strategy). The experimental artifacts from the ablation study can be found [here](/ablation).

## Regeneration of Charts

All configuration for installation of relevant code, collation of results,
and generation of charts is included in the `tox.ini` configuration that
can be run with:

```shell
$ pip install tox
$ tox
```
