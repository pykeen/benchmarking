# -*- coding: utf-8 -*-

import json
import os
import pathlib

import pandas as pd
from tqdm import tqdm

import pykeen.models
from pykeen.utils import flatten_dictionary
from src.utils import get_model_size

HERE = os.path.abspath(os.path.dirname(__file__))
RESULTS = os.path.join(HERE, 'results.tsv')
SKIP = {'model', 'replicate', 'dataset', 'model_bytes'}


def get_df() -> pd.DataFrame:
    if os.path.exists(RESULTS):
        return pd.read_csv(RESULTS, sep='\t')
    return collate()


def collate() -> pd.DataFrame:
    root = pathlib.Path(HERE) / 'results'
    data = []
    for run_label in tqdm(list(root.iterdir()), desc='Collating reproductions'):
        if run_label.name in {'.DS_Store'}:
            continue
        _date, _reference, model, dataset = run_label.name.split('_')

        # get size
        with (run_label / 'configuration_copied.json').open() as file:
            config = json.load(file)
        model_size = get_model_size(**config['pipeline'])

        for replicate in (run_label / 'replicates').iterdir():
            with (replicate / 'results.json').open() as rf:
                result = flatten_dictionary(json.load(rf))
            result.update(dict(
                # reference=reference,
                model=pykeen.models.get_model_cls(model).__name__,
                dataset=dataset,
                replicate=int(replicate.name.split('-')[1]),
                model_bytes=model_size,
            ))
            del result['losses']
            data.append(result)

    df = pd.DataFrame(data=data)
    df = df.set_index(['dataset', 'model', 'replicate']).reset_index()
    df.to_csv(RESULTS, sep='\t', index=False)
    return df


if __name__ == '__main__':
    collate()
