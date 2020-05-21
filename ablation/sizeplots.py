import logging
import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import scipy.spatial.qhull
import seaborn as sns
from scipy.spatial import ConvexHull
from tqdm import tqdm

from collate import COLLATION_PATH, MODEL, SUMMARY_DIRECTORY

logger = logging.getLogger(__name__)

SIZEPLOTS_DIRECTORY = os.path.join(SUMMARY_DIRECTORY, 'sizeplots')
os.makedirs(SIZEPLOTS_DIRECTORY, exist_ok=True)


def main():
    """Collate all HPO results in a single table."""
    df = pd.read_csv(COLLATION_PATH, sep='\t')
    make_ratio_distplots(df)
    make_sizeplots(df)
    make_skylines(df)


def make_ratio_distplots(df: pd.DataFrame):
    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc='making ratio distplots'
    )
    min_bytes = np.log10(df['model_bytes'].min())
    max_bytes = np.log10(df['model_bytes'].max())
    df['adj_log_bytes'] = (np.log10(df['model_bytes']) - min_bytes) / (max_bytes - min_bytes)

    df['ratio'] = np.log10((0.0001 + df['hits@10']) / (0.0001 + df['adj_log_bytes']))
    for (dataset, optimizer), sdf in it:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.distplot(sdf['ratio'], ax=ax)
        ax.set_xlabel('$\log \\frac{hits@10}{adj \log size}$')
        ax.set_title(f'{dataset} - {optimizer} ({len(sdf.index)} experiments)')
        plt.tight_layout()
        plt.savefig(os.path.join(SIZEPLOTS_DIRECTORY, f'{dataset}_{optimizer}_rdist.png'), dpi=300)
        plt.close(fig)


def make_skylines(df: pd.DataFrame):
    """Make skyline plots for each dataset/optimizer combination."""
    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc='making skylines'
    )
    min_bytes = df['model_bytes'].min()
    max_bytes = df['model_bytes'].max()
    for (dataset, optimizer), sdf in it:
        dfs = []
        for model, ssdf in sdf.groupby('model'):
            try:
                skyline_df = get_skyline_df(ssdf, columns=['model_bytes', 'hits@10'], smaller_is_better=(True, False))
            except scipy.spatial.qhull.QhullError:
                logger.warning('could not make skyline df for %s %s %s', dataset, optimizer, model)
                # it's probably because there are too few points, but in that case we don't
                # need to worry about making a hull anyway, so just use the full df
                skyline_df = ssdf
            dfs.append(skyline_df)

        fig, ax = plt.subplots(figsize=(8, 5))
        g = sns.lineplot(
            x='model_bytes',
            y='hits@10',
            data=pd.concat(dfs),
            estimator=None,
            markers=True,
            hue='model',
            ax=ax
        )
        ax.set_xlim([min_bytes, max_bytes])
        ax.set_ylim([0.0, 1.0])
        g.set(xscale="log")
        g.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
        ax.set_title(f'{dataset} - {optimizer}  ({len(sdf.index)} experiments)')
        plt.tight_layout()
        plt.savefig(os.path.join(SIZEPLOTS_DIRECTORY, f'{dataset}_{optimizer}_skyline.png'), dpi=300)
        plt.close(fig)


def make_sizeplots(df: pd.DataFrame):
    df['model'] = df['model'].map(lambda s: MODEL.get(s, s))
    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc='making sizeplots'
    )
    min_bytes = df['model_bytes'].min()
    max_bytes = df['model_bytes'].max()

    for (dataset, optimizer), sdf in it:
        fig, ax = plt.subplots(figsize=(8, 5))
        g = sns.scatterplot(
            x='model_bytes', y='hits@10', data=sdf,
            alpha=0.75, hue='model', hue_order=sorted(df['model'].unique()),
            ax=ax,
        )
        ax.set_xlim([min_bytes, max_bytes])
        ax.set_ylim([0.0, 1.0])
        g.set(xscale="log")
        g.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
        ax.set_xlabel('Model Size (bytes)')
        ax.set_title(f'{dataset} - {optimizer}  ({len(sdf.index)} experiments)')
        plt.tight_layout()
        plt.savefig(os.path.join(SIZEPLOTS_DIRECTORY, f'{dataset}_{optimizer}_scatter.png'), dpi=300)
        plt.close(plt.gcf())


def get_skyline_df(
    df: pd.DataFrame,
    columns: List[str],
    smaller_is_better: Tuple[bool, ...],
):
    """Get the skyline which contains all entries which are not dominated by another entry.
​
    :param columns: name of columns to use for the skyline
    :param df: A dataframe of skyline candidates.
    :param smaller_is_better: Whether smaller or larger values are better. One value per column.
    :return: The skyline as sub-dataframe
    """
    x = df[columns].values

    # skyline candidates can only be found in the convex hull
    hull = ConvexHull(x)
    candidates = hull.vertices
    x = x[candidates].copy()

    # turn sign for values where smaller is better => larger is always better
    x[:, smaller_is_better] *= -1

    # x[i, :] is dominated by x[j, :] if stronger(x[i, k], x[j, k]).all()
    # the skyline consists of points which are **not** dominated
    selected_candidates, = (~(x[:, None, :] < x[None, :, :]).all(axis=-1).any(axis=1)).nonzero()
    return df.iloc[candidates[selected_candidates]]


if __name__ == '__main__':
    main()
