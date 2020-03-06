# -*- coding: utf-8 -*-

import json
import os
import pathlib

import pandas as pd

from pykeen.utils import flatten_dictionary

HERE = os.path.abspath(os.path.dirname(__file__))

SKIP = {'model', 'replicate', 'dataset'}


def get_df() -> pd.DataFrame:
    root = pathlib.Path(HERE) / 'results'
    data = []
    for run_label in root.iterdir():
        if run_label.name in {'.DS_Store'}:
            continue
        _date, _reference, model, dataset = run_label.name.split('_')
        for replicate in (run_label / 'replicates').iterdir():
            with (replicate / 'results.json').open() as rf:
                result = flatten_dictionary(json.load(rf))
            result.update(dict(
                # reference=reference,
                model=model,
                dataset=dataset,
                replicate=int(replicate.name.split('-')[1]),
            ))
            del result['losses']
            data.append(result)

    df = pd.DataFrame(data=data)
    df = df.set_index(['dataset', 'model', 'replicate']).reset_index()
    return df
