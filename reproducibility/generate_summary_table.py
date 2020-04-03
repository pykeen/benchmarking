# -*- coding: utf-8 -*-

import os
from collections import defaultdict

import pandas as pd
from jinja2 import Environment, FileSystemLoader

from utils import get_df, SKIP

HERE = os.path.abspath(os.path.dirname(__file__))
SUMMARIES = os.path.join(HERE, 'summaries')
os.makedirs(SUMMARIES, exist_ok=True)


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
                    fmt = '5.2f'
                    std_fmt = '.2f'
                    factor = 1.0
                else:
                    std_fmt = fmt = '.2f'
                    factor = 100.0

                _, column = column.split('.', 1)
                t = f'{(factor * mean):{fmt}} ± {(factor * std):{std_fmt}}'
                rows.append((model, column, t))

        x = pd.DataFrame(rows, columns=['model', 'columns', 'values'])
        x = x.set_index(['model', 'columns']).unstack(level=-1).reset_index().set_index('model')
        x.columns = x.columns.get_level_values(1)
        x = x[[col for col in list(x.columns) if col not in {'training', 'evaluation'}]]
        x.columns = get_renamed_columns(x)
        x = get_reordered_df(x)

        # Save as TSV
        x.to_csv(os.path.join(SUMMARIES, f'{dataset}.tsv'), sep='\t', index=True)

        # Save as Latex table
        table_latex = x.to_latex(
            index=True,
            escape=False,
            column_format='l' + ('r' * len(x.columns)),
            bold_rows=True,
        )
        table_latex = table_latex.replace('±', '$\\pm$')
        with open(os.path.join(SUMMARIES, f'{dataset}_table.tex'), 'w') as file:
            print(table_latex, file=file)

        all_tables.append((dataset, x))

    write_pdfs(all_tables)


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

            hits_df = sub_df[['hits@1', 'hits@3', 'hits@5', 'hits@10']]
            if measurement == 'avg':
                ranked_df = sub_df[['MR', 'MRR', 'AMR']]
            else:
                ranked_df = sub_df[['MR', 'MRR']]

            tables[measurement, 'hits'] = get_latex(hits_df)
            tables[measurement, 'rank'] = get_latex(ranked_df)

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
    return table_latex.replace('±', '$\\pm$')


def get_renamed_columns(df: pd.DataFrame):
    rv = []
    for column in df.columns:
        column = column.replace('_', ' ').replace('.', ' ')

        if column.startswith('hits at k'):
            column_split = list(column.split(' '))
            column = f'hits@{column_split[-1]}'
            t = column_split[-2]
        elif column.startswith('mean reciprocal rank'):
            t = column.split(' ')[-1]
            column = 'MRR'
        elif column.startswith('mean rank'):
            t = column.split(' ')[-1]
            column = 'MR'
        elif column.startswith('adjusted mean rank'):
            column = 'AMR'
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

    reordered = []
    for x in ['', 'avg', 'best', 'worst']:
        for y in r[x]:
            reordered.append((x, y))
    return df[reordered]


if __name__ == '__main__':
    main()
