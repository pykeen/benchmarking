# -*- coding: utf-8 -*-

import os

import pandas as pd

from utils import SKIP, get_df

HERE = os.path.abspath(os.path.dirname(__file__))
SUMMARIES = os.path.join(HERE, 'summaries')
os.makedirs(SUMMARIES, exist_ok=True)


def main():
    df = get_df()

    for dataset, dataset_df in df.groupby('dataset'):
        rows = []
        for model, model_df in dataset_df.groupby('model'):
            for column in model_df.columns:
                if column in SKIP:
                    continue
                mean = model_df[column].mean()
                std = model_df[column].std()
                if '.mean_rank.' in column or column.startswith('times'):
                    fmt = '5.2f'
                    factor = 1
                else:
                    fmt = '.2f'
                    factor = 100

                _, column = column.split('.', 1)
                t = f'{factor * mean:{fmt}} ± {factor * std:{fmt}}'
                rows.append((model, column, t))

        x = pd.DataFrame(rows, columns=['model', 'columns', 'values'])
        x = x.set_index(['model', 'columns']).unstack(level=-1).reset_index()
        new_columns = ['model'] + list(x.columns.get_level_values(1))[1:]
        x.columns = new_columns

        x.to_csv(os.path.join(SUMMARIES, f'{dataset}.tsv'), sep='\t', index=False)
        with open(os.path.join(SUMMARIES, f'{dataset}.latex'), 'w') as file:
            print(x.to_latex(index=False), file=file)


if __name__ == '__main__':
    main()
