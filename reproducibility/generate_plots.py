# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import seaborn as sns

from utils import get_df

HERE = os.path.abspath(os.path.dirname(__file__))


def make_plots():
    df = get_df()
    for dataset, dataset_df in df.groupby('dataset'):
        for column in dataset_df.columns:
            if column in {'model', 'replicate', 'dataset'}:
                continue
            metric_df = dataset_df[['model', 'replicate', column]]

            fig, ax = plt.subplots(1, figsize=(7, 6))

            sns.violinplot(data=metric_df, x='model', y=column, ax=ax)

            if metric_df[column].max() < 1.0:
                ax.set_ylim([0, 1.0])
            metric_type, metric_name = column.split('.', 1)
            ax.set_ylabel(metric_name)
            ax.set_xlabel('')
            ax.set_title(f'{dataset} - {metric_type} - {metric_name}')
            plt.xticks(
                rotation=45,
                horizontalalignment='right',
                fontweight='light',
                fontsize='x-large'
            )
            plt.tight_layout()
            dataset_dir = os.path.join(HERE, 'plots', dataset)
            os.makedirs(dataset_dir, exist_ok=True)
            plt.savefig(os.path.join(dataset_dir, f'{column}.png'))
            plt.close(fig)


if __name__ == '__main__':
    make_plots()
