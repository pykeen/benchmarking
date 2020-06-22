# -*- coding: utf-8 -*-

"""Make interpretation tables

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
from typing import Iterable, Optional, Union

import click
import pandas as pd
from tabulate import tabulate
from typing.io import TextIO

from collate import SUMMARY_DIRECTORY, read_collation


@click.command()
def main():
    """Make interpretation at top 5, 10, and 15 best."""
    df = read_collation()
    target = 'hits@10'
    do_gold(df=df, target=target)
    do_top(df=df, target=target)


def do_gold(*, df, target):
    """Get the best configuration for each dataset/model.

    Columns returned: dataset, model, loss, training approach, inverse
    """
    output = os.path.join(SUMMARY_DIRECTORY, 'top_tables')
    os.makedirs(output, exist_ok=True)
    columns = ['loss', 'training_approach', 'inverse_relations', target]
    for dataset, dataset_df in df.groupby('dataset'):
        rows = []
        for model, model_df in dataset_df.groupby('model'):
            top_df = model_df.sort_values(target, ascending=False)
            r = top_df.iloc[0]
            rows.append((
                model,
                *[r[c] for c in columns]
            ))
        rdf = pd.DataFrame(
            rows,
            columns=['model', 'loss', 'training_approach', 'inverse_relations', target],
        ).sort_values('model')
        rdf.to_csv(os.path.join(output, f'{dataset.lower()}.tsv'), index=False, sep='\t')

        rdf.columns = [c.replace('_', ' ').title() for c in rdf.columns]
        s = rdf.to_latex(index=False)
        with open(os.path.join(output, f'{dataset.lower()}.tex'), 'w') as file:
            print(s, file=file)


def do_top(*, df, target):
    for top in (5, 10, 50):
        with open(os.path.join(SUMMARY_DIRECTORY, f'winners_at_top_{top:02}.md'), 'w') as file:
            configurations = [
                'model', 'loss', 'training_approach', 'inverse_relations',
                ('model', 'loss'), ('model', 'training_approach'), ('loss', 'training_approach'),
                ('model', 'loss', 'training_approach'),
            ]
            print(f'# Investigation of Top {top} Results\n', file=file)
            print(f'''This document gives insight into which models, loss functions, etc. are consistently
appearing in the top {top} experiments rated by {target} for **all** datasets. The ones that appear in the top {top}
experiments for every dataset are shown in **bold** in the index of each table. Note that not all tables
show that there are consistent best performers.
''', file=file)
            for config in configurations:
                print_top_winners(df=df, top=top, target=target, file=file, config=config)


def get_top_winners_df(
    *,
    df: pd.DataFrame,
    top: int,
    target: str,
    config: Union[str, Iterable[str]],
) -> pd.DataFrame:
    if isinstance(config, str):
        config = [config]
    d = {}
    for dataset, sub_df in df.groupby('dataset'):
        top_df = sub_df.sort_values(target, ascending=False).head(top)

        d[dataset] = Counter(make_index(r) for r in zip(*(top_df[t] for t in config)))
    return pd.DataFrame.from_dict(d).fillna(0).astype(int)


def make_index(r):
    if len(r) > 2:
        return ', '.join(r[:-1]) + f', and {r[-1]}'
    if len(r) == 1:
        return r[0]
    if len(r) == 2:
        return ' and '.join(r)
    else:
        raise ValueError


def print_top_winners(
    *,
    df: pd.DataFrame,
    top: int,
    target: str,
    config: Union[str, Iterable[str]],
    file: Optional[TextIO] = None,
) -> None:
    r = get_top_winners_df(df=df, top=top, config=config, target=target)

    r_transpose = r.transpose()
    winners = {
        column
        for column in r_transpose.columns
        if r_transpose[column].all()
    }

    title = f'`{config}`' if isinstance(config, str) else make_index([f'`{c}`' for c in config])
    print(f'## Investigation of {title}\n', file=file)

    # Add bold to winners
    r.index = [
        (
            f'**{i}**'
            if i in winners
            else i
        )
        for i in r.index
    ]

    print(tabulate(r, headers=r.columns, tablefmt='github'), file=file)
    print(file=file)
    print('', file=file)


if __name__ == '__main__':
    main()
