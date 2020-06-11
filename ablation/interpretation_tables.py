# -*- coding: utf-8 -*-

"""Make interpretaion tables

1.) Which interaction model was always among the top 5/top 10-performing configurations for each dataset?
2.) Which loss function was always among the top 5/top 10-performing configuration for each dataset?
3.) Which training assumption was always among the top 5/top 10-performing configurations for each dataset?
4.) Which combination of interaction model and loss function was always among the top 5/top 10-performing configurations for each dataset?
5.) Which combination of interaction models and training assumption was always among the top 5/top 10-performing configurations for each dataset?
6.) Which combination of loss function and training assumption was always among the top 5/top 10-performing configurations for each dataset?
7.) Which combination interaction models, training assumption, loss function was always among the top 5/top 10-performing configurations for each dataset? Did these configurations use inverse triples?
8.) How many of the top 5/top 10 configurations for each dataset use inverse triples?
"""

import os
from collections import Counter

import click
import pandas as pd
from tabulate import tabulate

from collate import SUMMARY_DIRECTORY, read_collation


@click.command()
def main():
    """Make interpretation at top 5, 10, and 15 best."""
    df = read_collation()
    for top in (5, 10, 50):
        with open(os.path.join(SUMMARY_DIRECTORY, f'winners_at_top_{top}.txt'), 'w') as file:
            _1(df, top, file=file)
            _2(df, top, file=file)
            _3(df, top, file=file)


def _1(df, top, file):
    for key in ['model', 'loss', 'training_loop', 'create_inverse_triples']:
        d = {}
        for dataset, sub_df in df.groupby('dataset'):
            top_df = sub_df.sort_values('hits@10', ascending=False).head(top)
            d[dataset] = Counter(top_df[key])
        r = pd.DataFrame.from_dict(d).fillna(0).astype(int)
        print(f'TOP RESULTS FOR {key} (N={top})', file=file)
        print(tabulate(r, headers=r.columns), file=file)
        _print_winners(r, top, file=file)
        print('', file=file)


def _2(df, top, file):
    for a, b in [('model', 'loss'), ('model', 'training_loop'), ('loss', 'training_loop')]:
        d = {}
        for dataset, sub_df in df.groupby('dataset'):
            top_df = sub_df.sort_values('hits@10', ascending=False).head(top)
            d[dataset] = Counter(f'{x}_{y}' for x, y in zip(top_df[a], top_df[b]))
        r = pd.DataFrame.from_dict(d).fillna(0).astype(int)
        print(f'TOP RESULTS FOR {a}-{b} (N={top})', file=file)
        print(tabulate(r, headers=r.columns), file=file)
        _print_winners(r, top, file=file)
        print('', file=file)


def _3(df, top, file):
    for a, b, c in [('model', 'loss', 'training_loop')]:
        d = {}
        for dataset, sub_df in df.groupby('dataset'):
            top_df = sub_df.sort_values('hits@10', ascending=False).head(top)
            d[dataset] = Counter(f'{x}_{y}_{z}' for x, y, z in zip(top_df[a], top_df[b], top_df[c]))
        r = pd.DataFrame.from_dict(d).fillna(0).astype(int)
        print(f'TOP RESULTS FOR {a}-{b}-{c} (N={top})', file=file)
        print(tabulate(r, headers=r.columns), file=file)
        _print_winners(r, top, file=file)
        print('', file=file)


def _print_winners(r, top, file):
    r_transpose = r.transpose()
    for column in r_transpose.columns:
        if r_transpose[column].all():
            print(f'Winner at N={top}: {column}', file=file)


if __name__ == '__main__':
    main()
