# -*- coding: utf-8 -*-

import os
from collections import defaultdict

import pandas as pd
from jinja2 import Environment, FileSystemLoader

import pykeen.datasets
import pykeen.models
from utils import SKIP, get_df

HERE = os.path.abspath(os.path.dirname(__file__))
SUMMARIES = os.path.join(HERE, 'summaries')
os.makedirs(SUMMARIES, exist_ok=True)

KEZ = '✠'


def main():
    all_tables = []
    for dataset, dataset_df in get_df().groupby('dataset'):
        if len(dataset_df['model'].unique()) < 2:
            continue
        rows = []
        for model, model_df in dataset_df.groupby('model'):
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

                rows.append((model, column, f'{mean:.2f}', f'{std:.2f}'))

        z = pd.DataFrame(rows, columns=['model', 'columns', 'mean', 'std'])
        z.to_csv(os.path.join(SUMMARIES, f'{dataset}.tsv'), sep='\t', index=False)

        _n = z.groupby(['columns']).aggregate(lambda q: max(map(len, q)))
        n = _n['std']
        _mean_n = _n['mean']

        z['values'] = [
            (_mean_n[column] - len(mean)) * KEZ + mean + ' ± ' + (n[column] - len(std)) * KEZ + std
            for column, mean, std in z[['columns', 'mean', 'std']].values
        ]
        x = z[['model', 'columns', 'values']]
        x = x.set_index(['model', 'columns']).unstack(level=-1).reset_index().set_index('model')
        x.columns = x.columns.get_level_values(1)
        x = x[[col for col in list(x.columns) if col not in {'training', 'evaluation'}]]
        x.columns = get_renamed_columns(x)
        x = get_reordered_df(x)

        # Save as Latex table
        table_latex = x.to_latex(
            index=True,
            escape=False,
            column_format='l' + ('r' * len(x.columns)),
            bold_rows=True,
        )
        table_latex = _process_tex(table_latex)
        with open(os.path.join(SUMMARIES, f'{dataset}_table.tex'), 'w') as file:
            print(table_latex, file=file)

        dataset = pykeen.datasets.datasets[dataset].__name__
        all_tables.append((dataset, x))

    write_pdfs(all_tables)


def _process_tex(s):
    s = s.replace('±', '$\\pm$').replace(KEZ, '$\\phantom{5}$')
    # s = s.replace('\\begin{tabular}', '\\begin{tabular*}')
    # s = s.replace('\\end{tabular}', '\\end{tabular*}')
    return s


def write_pdfs(all_tables) -> None:
    loader = FileSystemLoader(os.path.join(HERE, 'templates'))
    environment = Environment(
        autoescape=False,
        loader=loader,
        trim_blocks=False,
    )
    template = environment.get_template('table_template.tex')

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

    tex = template.render(table_results=table_results)
    with open(os.path.join(SUMMARIES, f'results.tex'), 'w') as file:
        print(tex, file=file)

    try:
        os.system(f"cd {SUMMARIES} && latexmk -pdf results")
        os.system(f"cd {SUMMARIES} && rm *.log && rm *.aux && rm *.fls && rm *.fdb_latexmk")
    except OSError:
        print('Was not able to build PDF.')


def get_latex(df: pd.DataFrame) -> str:
    table_latex = df.to_latex(
        index=True,
        escape=False,
        column_format='l' + ('r' * len(df.columns)),
        bold_rows=True,
    )
    return _process_tex(table_latex)


def get_renamed_columns(df: pd.DataFrame):
    rv = []
    for column in df.columns:
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
        rv.append((t, column))
    return pd.MultiIndex.from_tuples(rv)


def get_reordered_df(df: pd.DataFrame):
    r = defaultdict(list)
    for x, y in df.columns:
        r[x].append(y)

    reordered = [
        (x, y)
        for x in ['', 'avg', 'best', 'worst']
        for y in r[x]
    ]
    return df[reordered]


if __name__ == '__main__':
    main()
