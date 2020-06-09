# -*- coding: utf-8 -*-

import logging
import os
import random
from collections import Counter
from typing import Any, Mapping, Optional

import click
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from collate import COLLATION_PATH, SUMMARY_DIRECTORY, collate, read_collation

logger = logging.getLogger(__name__)

sns.set(font_scale=2, style='whitegrid')


def make_plots(*, target_header: str):
    df = read_collation()
    slice_dir = os.path.join(SUMMARY_DIRECTORY, 'paper')
    os.makedirs(slice_dir, exist_ok=True)

    loss_loops = set(map(tuple, df[['loss', 'training_loop']].values))
    loss_loops_counter = Counter(loss for loss, _ in loss_loops)
    loss_mult = {loss for loss, count in loss_loops_counter.items() if count > 1}

    df['loss_assumption'] = [
        (
            f'{loss} ({training_loop})'
            if loss in loss_mult
            else loss
        )
        for loss, training_loop in df[['loss', 'training_loop']].values
    ]

    it = tqdm(df.groupby(['dataset', 'optimizer']), desc='Making dataset/optimizer figures')
    for (dataset, optimizer), sub_df in it:
        plot_dataset_optimizer(
            df=sub_df,
            dataset=dataset,
            optimizer=optimizer,
            y='loss',
            hue='training_loop',
            col='model',
            target_header=target_header,
            slice_dir=slice_dir,
        )
        _write_dataset_optimizer_summaries(
            df=sub_df,
            dataset=dataset,
            optimizer=optimizer,
            target_header=target_header,
            model_dir=slice_dir,
        )

        # 2-way plots
        for y, hue in [
            ('loss_assumption', 'create_inverse_triples'),
            ('loss_assumption', 'training_loop'),
            ('training_loop', 'create_inverse_triples'),
        ]:
            _make_2way_plot(
                df=sub_df,
                target_header=target_header,
                y=y,
                hue=hue,
                slice_dir=slice_dir,
                dataset=dataset,
                optimizer=optimizer,
            )

        # Loss / Model / (Training Loop Chart | Inverse)
        for hue in ('training_loop', 'create_inverse_triples'):
            _make_loss_plots(
                df=sub_df,
                target_header=target_header,
                hue=hue,
                slice_dir=slice_dir,
                dataset=dataset,
                optimizer=optimizer,
            )

    it = tqdm(df.groupby('dataset'), desc=f'Making 1D slice plots for dataset')
    for dataset, sub_df in it:
        _make_summary_chart(
            df=sub_df,
            target_header=target_header,
            slice_dir=slice_dir,
            dataset=dataset,
        )


def plot_dataset_optimizer(*, df, y, col, hue, dataset, optimizer, target_header, slice_dir):
    g = sns.catplot(
        kind='bar',
        estimator=np.median,
        data=df,
        x=target_header,
        y=y,
        height=6,
        hue=hue,
        col=col,
        col_wrap=4,
        legend=True,
        legend_out=False,
        ci=None,
    )
    g.set_titles(template='{col_name}')
    g.set_ylabels('')
    g.set(xlim=[0.0, 1.0])
    plt.tight_layout()
    g.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_{y}_{col}_{hue}.png'.lower()), dpi=300)
    g.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_{y}_{col}_{hue}.pdf'.lower()))
    plt.close(g.fig)


def _make_loss_plots(*, df, target_header, hue, slice_dir, dataset, optimizer: Optional[str] = None):
    sns.set(font_scale=1.5, style='whitegrid')
    g = sns.catplot(
        kind='bar',
        estimator=np.median,
        data=df,
        x=target_header,
        y='model',
        height=6,
        hue=hue,
        col='loss',
        col_wrap=2,
        legend=True,
        legend_out=False,
        ci=None,
    )
    g.set_titles(template='{col_name}')
    g.set_ylabels('')
    g.set(xlim=[0.0, 1.0])
    plt.tight_layout()
    if optimizer is None:
        g.savefig(os.path.join(slice_dir, f'{dataset}_model_loss_{hue}.png'.lower()), dpi=300)
        g.savefig(os.path.join(slice_dir, f'{dataset}_model_loss_{hue}.pdf'.lower()))
    else:
        g.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_model_loss_{hue}.png'.lower()), dpi=300)
        g.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_model_loss_{hue}.pdf'.lower()))
    plt.close(g.fig)


def _make_2way_plot(*, df, target_header, y, hue, slice_dir, dataset, optimizer: Optional[str] = None):
    sns.set(style='whitegrid')
    g = sns.boxplot(
        x=target_header,
        y=y,
        hue=hue,
        data=df,
    )
    g.set(xlim=[0, 1.0], ylabel='')
    plt.tight_layout()
    if optimizer is not None:
        plt.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_loss_{hue}.png'.lower()), dpi=300)
        plt.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_loss_{hue}.pdf'.lower()))
    else:
        plt.savefig(os.path.join(slice_dir, f'{dataset}_loss_{hue}.png'.lower()), dpi=300)
        plt.savefig(os.path.join(slice_dir, f'{dataset}_loss_{hue}.pdf'.lower()))
    plt.close(plt.gcf())


def _make_summary_chart(*, df, target_header, slice_dir, dataset, ncols=2, nrows=2):
    if df['optimizer'].nunique() == 1:  # Don't bother with optimizer plot
        ablation_headers = ['model', 'loss_assumption', 'create_inverse_triples']
        figsize = (7 * ncols, 5 * nrows)
        fig = plt.figure(figsize=figsize)

        width = 2
        shape = (nrows, width * ncols)
        axes = []
        for i in range(nrows - 1):
            for j in range(ncols):
                axes.append(plt.subplot2grid(shape=shape, loc=(i, j * width), colspan=width))

        extra_rows = 1
        offset = width * (ncols - extra_rows) // 2
        # last row
        for j in range(extra_rows):
            axes.append(plt.subplot2grid(shape=shape, loc=(nrows - 1, offset + j * width), colspan=width))
    else:
        ablation_headers = ['model', 'loss_assumption', 'optimizer', 'create_inverse_triples']
        figsize = (7 * ncols, 5 * nrows)
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        axes = axes.ravel()

    for ablation_header, ax in zip(ablation_headers, axes):
        sns.boxplot(data=df, x=ablation_header, y=target_header, ax=ax)
        ax.set_title(ablation_header.replace('_', ' ').title(), fontdict={'fontsize': 22}, pad=10)
        ax.set_xlabel('')
        ax.set_ylabel(
            target_header,
            fontdict={'fontsize': 16},
        )
        for label in ax.get_xticklabels():
            label.set_ha("center")
            label.set_rotation(55)
            label.set_fontsize(15)
        ax.set_ylim([0.0, 1.0])

    fig.tight_layout()
    fig.savefig(os.path.join(slice_dir, f'{dataset}.png'.lower()), dpi=300)
    fig.savefig(os.path.join(slice_dir, f'{dataset}.pdf'.lower()))
    plt.close(fig)


def _write_dataset_optimizer_summaries(*, dataset, optimizer, df, target_header, model_dir):
    """Write model summaries, but trellis it on model."""
    data = pd.DataFrame([
        {
            'model': row['model'],
            'configuration': make_config_index(row),
            'replicate': row['replicate'],
            target_header: row[target_header],
        }
        for _, row in df.iterrows()
    ])
    logger.debug('%d replicates mapped for %s/%s', len(data.index), dataset, optimizer)

    means = data.groupby('configuration')[target_header].mean().sort_values()
    logger.debug('%d means mapped for %s/%s', len(means.index), dataset, optimizer)

    g = sns.catplot(
        kind='bar',
        estimator=np.median,
        data=data,
        x=target_header,
        y='configuration',
        col='model',
        col_wrap=4,
        ci=None,
        # capsize=.2, # restore if you want CIs
        order=means.index,
        palette="GnBu_d",
    )
    g.set_titles(template='{col_name}')
    g.set_ylabels('')
    g.set(xlim=[0.0, 1.0])

    sns.despine()
    g.fig.tight_layout()
    g.savefig(os.path.join(model_dir, f'{dataset}_{optimizer}.png'.lower()), dpi=300)
    g.savefig(os.path.join(model_dir, f'{dataset}_{optimizer}.pdf'.lower()))
    plt.close(g.fig)


def make_config_index(row: Mapping[str, Any]) -> str:
    return ' / '.join([
        'Inv.' if row['create_inverse_triples'] == 'True' else 'No Inv.',
        row["loss"],
        row["training_loop"].upper(),
    ])


@click.command()
def main():
    key = 'hits@10'
    if not os.path.exists(COLLATION_PATH):
        collate(key)
    # Plotting should be deterministic
    np.random.seed(5)
    random.seed(5)
    make_plots(target_header=key)
    click.echo('done!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
