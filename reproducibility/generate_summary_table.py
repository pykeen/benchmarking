# -*- coding: utf-8 -*-

"""Generate a summary table for the reproduction."""

import logging
import os
from collections import defaultdict
from typing import Iterable, List, Mapping, Tuple

import humanize
import pandas as pd
from jinja2 import Environment, FileSystemLoader

import pykeen.datasets
import pykeen.models
from utils import SKIP, read_experiment_collation

logger = logging.getLogger(__name__)

HERE = os.path.abspath(os.path.dirname(__file__))
SUMMARIES = os.path.join(HERE, 'summaries')
os.makedirs(SUMMARIES, exist_ok=True)

# can be any one-character string that you're sure won't appear in the table
PHANTOM_PLACEHOLDER = '✠'


def generate_results_table():
    all_tables = []
    for dataset, dataset_df in read_experiment_collation().groupby('dataset'):
        if len(dataset_df['model'].unique()) < 2:
            continue

        tall_summary_df = get_tall_summary_df(dataset_df)
        tall_summary_df.to_csv(os.path.join(SUMMARIES, f'{dataset}.tsv'), sep='\t', index=False)

        wide_summary_df = reorganize_summary_df(tall_summary_df)

        # Save as Latex table
        table_latex = wide_summary_df.to_latex(
            index=True,
            escape=False,
            column_format='l' + ('r' * len(wide_summary_df.columns)),
            bold_rows=True,
        )
        table_latex = _process_tex(table_latex)
        with open(os.path.join(SUMMARIES, f'{dataset}_table.tex'), 'w') as file:
            print(table_latex, file=file)

        dataset = pykeen.datasets.datasets[dataset].__name__
        all_tables.append((dataset, wide_summary_df))

    return all_tables


def get_tall_summary_df(df: pd.DataFrame):
    rows = []
    for model, model_df in df.groupby('model'):
        for column in model_df.columns:
            if column in SKIP:
                continue
            mean = model_df[column].mean()
            std = model_df[column].std()
            if '.mean_rank.' in column or column.startswith('times'):
                pass
            else:
                mean *= 100.0
                std *= 100.0

            _, column = column.split('.', 1)

            rows.append((
                model, column, f'{mean:.2f}', f'{std:.2f}',
            ))
    return pd.DataFrame(rows, columns=['model', 'columns', 'mean', 'std'])


def reorganize_summary_df(df: pd.DataFrame) -> pd.DataFrame:
    _n = df.groupby(['columns']).aggregate(lambda q: max(map(len, q)))
    n = _n['std']
    _mean_n = _n['mean']

    df['values'] = [
        (_mean_n[column] - len(mean)) * PHANTOM_PLACEHOLDER + mean + ' ± ' + (
            n[column] - len(std)) * PHANTOM_PLACEHOLDER + std
        for column, mean, std in df[['columns', 'mean', 'std']].values
    ]
    rv = df[['model', 'columns', 'values']]
    rv = rv.set_index(['model', 'columns']).unstack(level=-1).reset_index().set_index('model')
    rv.columns = rv.columns.get_level_values(1)
    rv = rv[[col for col in list(rv.columns) if col not in {'training', 'evaluation'}]]
    rv.columns = get_renamed_columns(rv)
    rv = get_reordered_df(rv)
    return rv


def _process_tex(s: str) -> str:
    s = s.replace('±', '$\\pm$').replace(PHANTOM_PLACEHOLDER, '$\\phantom{5}$')
    # s = s.replace('\\begin{tabular}', '\\begin{tabular*}')
    # s = s.replace('\\end{tabular}', '\\end{tabular*}')
    return s


def write_pdfs(
    *,
    all_tables: Iterable[Tuple[str, pd.DataFrame]],
    size_table: pd.DataFrame,
) -> None:
    loader = FileSystemLoader(HERE)
    environment = Environment(
        autoescape=False,
        loader=loader,
        trim_blocks=False,
    )
    template = environment.get_template('table_template.tex')

    table_results = _make_table_results(all_tables)

    tex = template.render(
        table_results=table_results,
        size_table=size_table.to_latex(
            multirow=True,
            column_format='llrr',
            bold_rows=True,
        ),
    )
    with open(os.path.join(SUMMARIES, f'results.tex'), 'w') as file:
        print(tex, file=file)

    try:
        os.system(f"cd {SUMMARIES} && latexmk -pdf results")
        os.system(f"cd {SUMMARIES} && rm *.log && rm *.aux && rm *.fls && rm *.fdb_latexmk")
    except OSError:
        logger.warning('Was not able to build PDF.')


def _make_table_results(
    all_tables: Iterable[Tuple[str, pd.DataFrame]],
) -> List[Tuple[str, Mapping[str, pd.DataFrame]]]:
    table_results = []

    for dataset, df in all_tables:
        z = defaultdict(list)
        for measurement, y in df.columns:
            z[measurement].append((measurement, y))

        tables = {}
        for measurement, y in z.items():
            sub_df = df[y]
            sub_df.index.name = None
            sub_df.columns = list(sub_df.columns.get_level_values(1))

            if measurement == 'avg':
                cols = ['MR', 'MRR (\\%)', 'AMR (\\%)']
            else:
                cols = ['MR', 'MRR (\\%)']
            cols.extend(['Hits@1 (\\%)', 'Hits@3 (\\%)', 'Hits@5 (\\%)', 'Hits@10 (\\%)'])
            tables[measurement] = get_latex(sub_df[cols])

        table_results.append((dataset, tables))
    return table_results


def get_latex(df: pd.DataFrame) -> str:
    table_latex = df.to_latex(
        index=True,
        escape=False,
        column_format='l' + ('r' * len(df.columns)),
        bold_rows=True,
    )
    return _process_tex(table_latex)


def get_renamed_columns(df: pd.DataFrame):
    return pd.MultiIndex.from_tuples([
        _help_rename_column(column)
        for column in df.columns
    ])


def _help_rename_column(column: str) -> Tuple[str, str]:
    column = column.replace('_', ' ').replace('.', ' ')

    if column.startswith('hits at k'):
        column_split = list(column.split(' '))
        column = f'Hits@{column_split[-1]} (\\%)'
        t = column_split[-2]
    elif column.startswith('mean reciprocal rank'):
        t = column.split(' ')[-1]
        column = 'MRR (\\%)'
    elif column.startswith('mean rank'):
        t = column.split(' ')[-1]
        column = 'MR'
    elif column.startswith('adjusted mean rank'):
        column = 'AMR (\\%)'
        t = 'avg'
    elif column == 'model':
        t = ''
    else:
        t = 'time'
    return t, column


def get_reordered_df(df: pd.DataFrame) -> pd.DataFrame:
    r = defaultdict(list)
    for first_level_label, second_level_label in df.columns:
        r[first_level_label].append(second_level_label)

    columns = [
        (first_level_label, second_level_label)
        for first_level_label in ['', 'avg', 'best', 'worst']
        for second_level_label in r[first_level_label]
    ]
    return df[columns]


def generate_size_table():
    df = read_experiment_collation()
    rv = df[['dataset', 'model', 'model_bytes']].drop_duplicates()
    rv['dataset'] = rv['dataset'].map(lambda s: pykeen.datasets.datasets[s].__name__)
    rv['Bytes'] = rv['model_bytes'].map(humanize.naturalsize)
    rv = rv.pivot(index='model', columns='dataset', values='Bytes').fillna('-')
    rv = rv[sorted(rv.columns)]
    rv.to_csv(os.path.join(SUMMARIES, 'sizes.tsv'), sep='\t')
    with open(os.path.join(SUMMARIES, 'sizes.tex'), 'w') as file:
        print(rv.to_latex(multirow=True), file=file)
    return rv


def main():
    size_table = generate_size_table()
    all_tables = generate_results_table()
    write_pdfs(all_tables=all_tables, size_table=size_table)


if __name__ == '__main__':
    main()
