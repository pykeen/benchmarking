# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import seaborn as sns

from utils import get_df

HERE = os.path.abspath(os.path.dirname(__file__))


def make_dataset_plots():
    df = get_df()
    for dataset, dataset_df in df.groupby('dataset'):
        if len(dataset_df['model'].unique()) < 2:
            continue

        columns = [column for column in dataset_df.columns if column not in {'model', 'replicate', 'dataset'}]

        for column in columns:
            metric_df = dataset_df[['model', column]]

            fig, ax = plt.subplots(1, figsize=(7, 6))

            sns.boxplot(data=metric_df, y='model', x=column, ax=ax)

            # if metric_df[column].max() < 1.0:
            #     ax.set_xlim([0, 1.0])
            metric_type, metric_name = column.split('.', 1)
            # ax.set_ylabel(metric_name)
            # ax.set_xlabel('')
            ax.set_title(f'{dataset} - {metric_type} - {metric_name}')
            plt.tight_layout()
            dataset_dir = os.path.join(HERE, 'plots', dataset)
            os.makedirs(dataset_dir, exist_ok=True)
            path = os.path.join(dataset_dir, f'{column}.png')
            plt.savefig(path)
            plt.close(fig)


if __name__ == '__main__':
    make_dataset_plots()
