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

from collate import MODEL_BYTES, SUMMARY_DIRECTORY, read_collation

logger = logging.getLogger(__name__)

SIZEPLOTS_DIRECTORY = os.path.join(SUMMARY_DIRECTORY, 'sizeplots')
os.makedirs(SIZEPLOTS_DIRECTORY, exist_ok=True)


def main():
    """Collate all HPO results in a single table."""
    df = read_collation()
    # ratio displots are a bit of a mess
    # make_ratio_distplots(df, header=MODEL_BYTES, log=True)
    # make_ratio_distplots(df, header='training_time', log=False)
    # make_ratio_distplots(df, header='evaluation_time', log=False)
    make_sizeplots(df, header=MODEL_BYTES)
    make_sizeplots(df, header='training_time')
    make_skylines(df, header=MODEL_BYTES)
    make_skylines(df, header='training_time')


def make_ratio_distplots(df: pd.DataFrame, header: str = MODEL_BYTES, log: bool = False):
    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc=f'making ratio distplots for {header}',
    )

    min_bytes = df[header].min()
    max_bytes = df[header].max()

    if log:
        min_bytes = np.log10(min_bytes)
        max_bytes = np.log10(max_bytes)
        df[f'adj_{header}'] = (np.log10(df[header]) - min_bytes) / (max_bytes - min_bytes)
    else:
        df[f'adj_{header}'] = (df[header] - min_bytes) / (max_bytes - min_bytes)

    df['ratio'] = np.log10((0.0001 + df['hits@10']) / (0.0001 + df[f'adj_{header}']))

    for (dataset, optimizer), sdf in it:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.distplot(sdf['ratio'], ax=ax)
        ax.set_xlabel(f'$\log \\frac{{hits@10}}{{adj {header}}}$')
        ax.set_title(f'{dataset} - {optimizer} - {header} ({len(sdf.index)} experiments)')
        plt.tight_layout()
        plt.savefig(os.path.join(SIZEPLOTS_DIRECTORY, f'{header}_{dataset}_{optimizer}_rdist.pdf'.lower()), dpi=300)
        plt.close(fig)


def make_skylines(df: pd.DataFrame, header: str = MODEL_BYTES):
    """Make skyline plots for each dataset/optimizer combination."""
    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc=f'making skylines for {header}',
    )
    min_bytes = df[header].min()
    max_bytes = df[header].max()
    for (dataset, optimizer), sdf in it:
        dfs = []
        for model, ssdf in sdf.groupby('model'):
            try:
                skyline_df = get_skyline_df(ssdf, columns=[header, 'hits@10'], smaller_is_better=(True, False))
            except scipy.spatial.qhull.QhullError:
                logger.warning('could not make skyline df for %s %s %s', dataset, optimizer, model)
                # it's probably because there are too few points, but in that case we don't
                # need to worry about making a hull anyway, so just use the full df
                skyline_df = ssdf
            dfs.append(skyline_df)

        fig, ax = plt.subplots(figsize=(8, 5))
        g = sns.lineplot(
            x=header,
            y='hits@10',
            data=pd.concat(dfs),
            estimator=None,
            markers=True,
            hue='model',
            ax=ax
        )
        ax.set_xlim([min_bytes, max_bytes])
        ax.set_ylim([0.0, 1.0])
        # g.set(xscale="log", yscale='log')
        g.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
        ax.set_title(f'{dataset} - {optimizer} - {header} ({len(sdf.index)} experiments)')
        plt.tight_layout()
        plt.savefig(os.path.join(SIZEPLOTS_DIRECTORY, f'skyline_{header}_{dataset}_{optimizer}.pdf'.lower()), dpi=300)
        plt.close(fig)


def make_sizeplots(df: pd.DataFrame, header: str = MODEL_BYTES):
    for optimizer, sdf in tqdm(df.groupby('optimizer'), desc=f'making super-optimizer plots for {header}'):
        g = sns.FacetGrid(
            data=sdf,
            hue='model',
            hue_order=sorted(df['model'].unique()),
            col='dataset',
            col_wrap=2,
            legend_out=True
        )
        (
            g.map(sns.scatterplot, header, 'hits@10', alpha=0.5)
                .set(xscale="log")
                # .add_legend(loc='right', bbox_to_anchor=(2.25, 0.5), ncol=1)
        )
        # plt.title(f'{optimizer} - {header}  ({len(sdf.index)} experiments)')
        # plt.tight_layout()
        plt.savefig(os.path.join(SIZEPLOTS_DIRECTORY, f'trellis_scatter_{header}_{optimizer}.pdf'.lower()), dpi=300)
        plt.close(plt.gcf())

    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc=f'making sizeplots for {header}'
    )
    min_bytes = df[header].min()
    max_bytes = df[header].max()

    for (dataset, optimizer), sdf in it:
        fig, ax = plt.subplots(figsize=(8, 5))
        g = sns.scatterplot(
            x=header,
            y='hits@10',
            data=sdf,
            alpha=0.75,
            hue='model',
            hue_order=sorted(df['model'].unique()),
            ax=ax,
        )
        ax.set_xlim([min_bytes, max_bytes])
        ax.set_ylim([0.0, 1.0])
        g.set(xscale="log")
        g.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
        ax.set_title(f'{dataset} - {optimizer} - {header}  ({len(sdf.index)} experiments)')
        plt.tight_layout()
        plt.savefig(os.path.join(SIZEPLOTS_DIRECTORY, f'scatter_{header}_{dataset}_{optimizer}.pdf'.lower()), dpi=300)
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
