# -*- coding: utf-8 -*-

import os
import pathlib

import pandas as pd

import pykeen_report.utils

HERE = os.path.abspath(os.path.dirname(__file__))
RESULTS = os.path.join(HERE, 'results.tsv')
SKIP = {'model', 'replicate', 'dataset', 'model_bytes'}


def read_experiment_collation() -> pd.DataFrame:
    if os.path.exists(RESULTS):
        return pd.read_csv(RESULTS, sep='\t')
    return collate_experiments()


def collate_experiments() -> pd.DataFrame:
    root = pathlib.Path(HERE) / 'results'
    return pykeen_report.utils.collate_experiments(root=root, output=RESULTS)


if __name__ == '__main__':
    collate_experiments()
