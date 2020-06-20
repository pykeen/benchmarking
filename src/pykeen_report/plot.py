# -*- coding: utf-8 -*-

"""Tools for plotting PyKEEN experiments."""

import itertools as itt
import logging
import os
import time
from typing import Any, List, Mapping, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import scipy.spatial.qhull
import seaborn as sns
from matplotlib import gridspec
from scipy.spatial import ConvexHull
from tqdm import tqdm

from .constants import ABLATION_HEADERS, BINARY_ABLATION_HEADERS

logger = logging.getLogger(__name__)


def plot_3d_barplot(
    *,
    df, y, col, hue, dataset, optimizer, target_header, slice_dir,
    name: Optional[str] = None,
    make_pngs: bool = True,
    make_pdfs: bool = True,
) -> None:
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
    _clean_legend_title(g._legend)
    plt.tight_layout()
    if name is None:
        name = f'{dataset}_{optimizer}_{y}_{col}_{hue}'
    if make_pngs:
        g.savefig(os.path.join(slice_dir, f'{name}.png'.lower()), dpi=300)
    if make_pdfs:
        g.savefig(os.path.join(slice_dir, f'{name}.pdf'.lower()))
    plt.close(g.fig)


def write_1d_sliced_summaries_stratified(
    *,
    df: pd.DataFrame,
    target_header: str,
    output_directory: str,
    make_png: bool = True,
    make_pdf: bool = True,
) -> None:
    slice_dir = os.path.join(output_directory, 'dataset_optimizer_1d_slices')
    os.makedirs(slice_dir, exist_ok=True)
    slice2d_dir = os.path.join(output_directory, 'dataset_optimizer_2d_slices')
    os.makedirs(slice2d_dir, exist_ok=True)
    slice3d_dir = os.path.join(output_directory, 'dataset_optimizer_3d_slices')
    os.makedirs(slice3d_dir, exist_ok=True)

    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc='Making summaries stratified by dataset/optimizer',
    )
    for (dataset, optimizer), dataset_model_df in it:
        # 3D slices
        it_3d_slices = tqdm(
            BINARY_ABLATION_HEADERS,
            desc=f'Make 3D slice plots stratified by {dataset}/{optimizer}',
            leave=False,
        )
        for binary_ablation_header in it_3d_slices:
            other_ablation_headers = [
                ablation_header
                for ablation_header in ABLATION_HEADERS
                if (
                    ablation_header not in BINARY_ABLATION_HEADERS
                    and ablation_header not in {'dataset', 'optimizer'}
                )
            ]
            it_3d_slices_inner = tqdm(
                itt.product(other_ablation_headers, repeat=2),
                desc=f'Make 3D slice plots stratified by {dataset}/{optimizer} for {binary_ablation_header}',
                leave=False,
            )
            for ah1, ah2 in it_3d_slices_inner:
                if ah1 == ah2:
                    continue
                g = sns.catplot(
                    kind='bar',
                    estimator=np.median,
                    data=dataset_model_df,
                    x=target_header,
                    y=ah1,
                    height=6,
                    hue=binary_ablation_header,
                    col=ah2,
                    col_wrap=4,
                    legend_out=True,
                    ci=None,
                )
                g.set_titles(template='{col_name}', size=20)
                g.set_ylabels('')
                g.set_yticklabels(fontdict={'fontsize': 15})
                g.set(xlim=[0.0, 1.0])
                _clean_legend_title(g._legend)
                plt.tight_layout()
                if make_png:
                    plt.savefig(
                        os.path.join(
                            slice3d_dir,
                            f'{optimizer}-{dataset}-{binary_ablation_header}-{ah1}-{ah2}.png',
                        ),
                        dpi=300,
                    )
                if make_pdf:
                    plt.savefig(
                        os.path.join(
                            slice3d_dir,
                            f'{optimizer}-{dataset}-{binary_ablation_header}-{ah1}-{ah2}.pdf',
                        ),
                    )
                plt.close(g.fig)

        # 2D slices
        _2d_slice_ablation_headers = [
            ablation_header
            for ablation_header in ABLATION_HEADERS
            if ablation_header not in {'dataset', 'optimizer'}
        ]
        it_2d_slices = tqdm(
            itt.product(_2d_slice_ablation_headers, repeat=2),
            desc=f'Make 2d slice plots stratified by {dataset}/{optimizer}',
            total=len(_2d_slice_ablation_headers) ** 2,
            leave=False,
        )
        for ah1, ah2 in it_2d_slices:
            if ah1 == ah2:
                continue

            if 2 == len(dataset_model_df[ah2].unique()):
                g = sns.catplot(
                    data=dataset_model_df,
                    x=target_header,
                    kind='box',
                    y=ah1,
                    hue=ah2,
                    ci=None,
                    legend=True
                )
                _clean_legend_title(g.legend)
            else:
                g = sns.catplot(
                    data=dataset_model_df,
                    x=target_header,
                    kind='box',
                    y=ah1,
                    col=ah2,
                    col_wrap=4,
                    ci=None,
                )
            g.fig.suptitle(f'{dataset} - {optimizer} - {ah1} - {ah2}', fontsize=20)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            if make_png:
                plt.savefig(os.path.join(slice2d_dir, f'{dataset}_{optimizer}_{ah1}_{ah2}_2d.png'), dpi=300)
            if make_pdf:
                plt.savefig(os.path.join(slice2d_dir, f'{dataset}_{optimizer}_{ah1}_{ah2}_2d.pdf'))
            plt.close()

        outer_it = tqdm(
            ABLATION_HEADERS,
            desc=f'Making 1D slice plots stratified by {dataset}/{optimizer}',
            leave=False,
        )
        for k in outer_it:
            if k in {'dataset', 'optimizer'}:
                continue
            ablation_headers = [
                ablation_header
                for ablation_header in ABLATION_HEADERS
                if ablation_header not in {k, 'dataset', 'optimizer'}
            ]

            # 1D slices
            inner_it = tqdm(
                dataset_model_df.groupby(k),
                desc=f'Making 1D slice plots stratified by {dataset}/{optimizer} for {k}',
                leave=False,
            )
            for v, sub_df in inner_it:
                fig, axes = plt.subplots(ncols=3, figsize=(14, 5))
                for ablation_header, ax in zip(ablation_headers, axes.ravel()):
                    try:
                        sns.boxplot(
                            data=sub_df,
                            y=ablation_header,
                            x=target_header,
                            ax=ax,
                            # order=sub_df_agg.index,
                        )
                    except ValueError:
                        logger.exception('could not make box plot')
                        continue

                    ax.set_title(ablation_header.replace('_', ' ').title())
                    ax.set_ylabel('')
                    ax.set_xlim([0.0, 1.0])

                    # for tick in ax.get_yticklabels():
                    #    tick.set_rotation(45)

                plt.suptitle(
                    f"Stratified Summary for {dataset}-{optimizer}\n{k.replace('_', ' '.title())}: {v}",
                    fontsize=20,
                )
                plt.tight_layout(rect=[0, 0.03, 1, 0.90])
                if make_png:
                    plt.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_{k}_{v}_1d.png'), dpi=300)
                if make_pdf:
                    plt.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_{k}_{v}_1d.pdf'))
                plt.close(fig)


def write_2d_sliced_summaries(
    *,
    df,
    target_header,
    slice_1='model',
    slice_2='dataset',
    slice_3='loss',
    val=None,
    n_cols=3,
    output_directory: str,
    make_png: bool = True,
    make_pdf: bool = True,
):
    """The goal is to have for a given loss function the comparison of each dataset to all others"""
    slice_dir = os.path.join(output_directory, '2D-slices')
    os.makedirs(slice_dir, exist_ok=True)

    n_boxes = df[slice_1].nunique()
    if n_cols < n_boxes:
        n_rows = df[slice_1].nunique() // n_cols
    else:
        n_rows, n_cols = 1, n_boxes

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 4 * n_rows))

    slice_1_it = tqdm(
        df.groupby(slice_1),
        desc='Writing 2D slice summary',
    )
    for (slice_1_value, sdf), ax in zip(slice_1_it, axes.ravel()):
        if val is not None:
            sdf[val] = [val if x else f'Not {val}' for x in (sdf[slice_3] == val)]
            hue = val
        else:
            hue = slice_3

        try:
            g = sns.violinplot(
                data=sdf,
                x=slice_2,
                y=target_header,
                split=True,
                ax=ax,
                cut=0,
                hue=hue,
            )
        except ValueError:
            slice_1_it.write(f'could not make violin plot for {slice_1}-{slice_1_value}, {slice_2}, {hue}')
            continue
        else:
            _clean_legend_title(g._legend)

        ax.set_ylim([0.0, 1.0])
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
        ax.set_title(f'{slice_1} - {slice_1_value}')
        ax.set_xlabel('')
    plt.tight_layout()

    if val is not None:
        fig_name = f'{slice_1}-{slice_2}-{slice_3}-{val}.png'
        fig_name_pdf = f'{slice_1}-{slice_2}-{slice_3}-{val}.pdf'
    else:
        fig_name = f'{slice_1}-{slice_2}-{slice_3}.png'
        fig_name_pdf = f'{slice_1}-{slice_2}-{slice_3}.pdf'

    if make_png:
        plt.savefig(os.path.join(slice_dir, fig_name), dpi=300)
    if make_pdf:
        plt.savefig(os.path.join(slice_dir, fig_name_pdf))
    plt.close(fig)


def write_2d_summaries(
    *,
    df: pd.DataFrame, target_header, output_directory: str,
    make_png: bool = True,
    make_pdf: bool = True,
):
    for k in ['inverse_relations', 'loss', 'optimizer', 'training_approach']:
        values = df[k].unique()
        if len(values) == 2:
            write_2d_sliced_summaries(
                df=df, target_header=target_header,
                slice_1='dataset', slice_2='model', slice_3=k,
                output_directory=output_directory,
                make_png=make_png, make_pdf=make_pdf,
            )
        else:
            for value in values:
                write_2d_sliced_summaries(
                    df=df, target_header=target_header,
                    slice_1='dataset', slice_2='model', slice_3=k, val=value,
                    output_directory=output_directory,
                    make_png=make_png, make_pdf=make_pdf,
                )
                write_2d_sliced_summaries(
                    df=df, target_header=target_header,
                    slice_1='model', slice_2='dataset', slice_3=k, val=value,
                    output_directory=output_directory,
                    make_png=make_png, make_pdf=make_pdf,
                )


def write_dataset_optimizer_barplots(
    *,
    dataset: str,
    optimizer: str,
    df: pd.DataFrame,
    target_header: str,
    output_directory: str,
    name: Optional[str] = None,
    make_pngs: bool = True,
    make_pdfs: bool = True,
) -> None:
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
    if name is None:
        name = f'{dataset}_{optimizer}'
    if make_pngs:
        g.savefig(os.path.join(output_directory, f'{name}.png'.lower()), dpi=300)
    if make_pdfs:
        g.savefig(os.path.join(output_directory, f'{name}.pdf'.lower()))
    plt.close(g.fig)


def make_config_index(row: Mapping[str, Any]) -> str:
    return ' / '.join([
        'Inv.' if row['inverse_relations'] == 'True' else 'No Inv.',
        row["loss"],
        row["training_approach"],
    ])


def make_summary_chart(
    *,
    df,
    target_header,
    slice_dir,
    dataset,
    ncols=2,
    nrows=2,
    make_pngs: bool = True,
    make_pdfs: bool = True,
) -> None:
    if df['optimizer'].nunique() == 1:  # Don't bother with optimizer plot
        ablation_headers = ['model', 'loss_training_approach', 'inverse_relations']
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
        ablation_headers = ['model', 'loss_training_approach', 'optimizer', 'inverse_relations']
        figsize = (7 * ncols, 5 * nrows)
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        axes = axes.ravel()

    for ablation_header, ax in zip(ablation_headers, axes):
        sns.boxplot(data=df, x=ablation_header, y=target_header, ax=ax)

        if ablation_header == 'loss_training_approach':
            title = 'Loss / Training Approach'
        else:
            title = ablation_header.replace('_', ' ').title()
        ax.set_title(title, fontdict={'fontsize': 22}, pad=10)
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
    if make_pngs:
        fig.savefig(os.path.join(slice_dir, f'{dataset}.png'.lower()), dpi=300)
    if make_pdfs:
        fig.savefig(os.path.join(slice_dir, f'{dataset}.pdf'.lower()))
    plt.close(fig)


def make_2way_boxplot(
    *,
    df,
    target_header,
    y,
    hue,
    slice_dir,
    dataset,
    name: Optional[str] = None,
    make_pngs: bool = True,
    make_pdfs: bool = True,
) -> None:
    sns.set(style='whitegrid')
    g = sns.catplot(
        x=target_header,
        y=y,
        hue=hue,
        data=df,
        kind='box',
        legend_out=False,
    )
    g.set(xlim=[0, 1.0], ylabel='')
    _clean_legend_title(g._legend)
    plt.tight_layout()

    if name is None:
        name = f'{dataset}_loss_{hue}'
    if make_pngs:
        plt.savefig(os.path.join(slice_dir, f'{name}.png'.lower()), dpi=300)
    if make_pdfs:
        plt.savefig(os.path.join(slice_dir, f'{name}.pdf'.lower()))
    plt.close(plt.gcf())


def make_loss_plot_barplot(
    *,
    df: pd.DataFrame,
    target_header: str,
    hue: str,
    output_directory: str,
    dataset: str,
    name: Optional[str] = None,
    make_pngs: bool = True,
    make_pdfs: bool = True,
) -> None:
    sns.set(font_scale=1.5, style='whitegrid')

    dfs = [
        sdf
        for _, sdf in df.groupby(['model', 'loss'])
        if sdf[hue].nunique() == 2
    ]
    if not dfs:
        logger.warning('Could not make model/loss barplot for %s', hue)
        return

    plot_df = pd.concat(dfs)

    g = sns.catplot(
        kind='bar',
        estimator=np.median,
        data=plot_df,
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
    _clean_legend_title(g._legend)
    plt.tight_layout()

    if name is None:
        name = f'{dataset}_model_loss_{hue}'
    if make_pngs:
        g.savefig(os.path.join(output_directory, f'{name}.png'.lower()), dpi=300)
    if make_pdfs:
        g.savefig(os.path.join(output_directory, f'{name}.pdf'.lower()))
    plt.close(g.fig)


def _clean_legend_title(legend):
    title = legend.get_title()
    title.set_text(title.get_text().replace('_', ' ').title())


def write_dataset_optimizer_model_summaries(
    *,
    df: pd.DataFrame,
    target_header: str,
    output_directory: str,
    make_png: bool = True,
    make_pdf: bool = True,
) -> None:
    it = tqdm(
        df.groupby(['dataset', 'model', 'optimizer']),
        desc='writing dataset/model/optimizer summaries',
    )
    for (dataset, model, optimizer), dataset_model_df in it:
        data = pd.DataFrame([
            {
                'configuration': make_config_index(row),
                'replicate': row['replicate'],
                target_header: row[target_header],
            }
            for _, row in dataset_model_df.iterrows()
        ])

        means = data.groupby('configuration')[target_header].mean().sort_values()

        # data.to_csv(os.path.join(SUMMARY_DIRECTORY, f'{dataset}_{model}.tsv'), sep='\t', index=False)
        fig, ax = plt.subplots(1, figsize=(14, 7))
        sns.barplot(
            data=data,
            x=target_header,
            y='configuration',
            ax=ax,
            ci=None,
            # capsize=.2, # restore if you want CIs
            order=means.index,
            palette="GnBu_d",
            estimator=np.median,
        )
        ax.set_title(f'Stratified Summary for\n{dataset} - {model} - {optimizer}', fontsize=20)
        ax.set_ylabel('')
        ax.set_yticks([])

        # set individual bar lables using above list
        fontsize = 20
        for y, (label, patch) in enumerate(zip(means.index, ax.patches)):
            # get_x pulls left or right; get_height pushes up or down
            ax.text(
                0.005,
                y + 0.03,
                label,
                fontsize=fontsize,
                color='white',
                ha='left',
                va='center',
            )

        # ax.xaxis.grid(True)
        # sns.despine(trim=True, left=True)
        sns.despine()
        plt.tight_layout()
        if make_png:
            plt.savefig(os.path.join(output_directory, f'{dataset}_{model}_{optimizer}.png'), dpi=300)
        if make_pdf:
            plt.savefig(os.path.join(output_directory, f'{dataset}_{model}_{optimizer}.pdf'))
        plt.close(fig)


def write_1d_sliced_summaries(
    *,
    df: pd.DataFrame,
    target_header: str,
    output_directory: str,
    make_png: bool = True,
    make_pdf: bool = True,
) -> None:
    outer_it = tqdm(ABLATION_HEADERS, desc='Making 1D slice plots')
    for k in outer_it:
        ncols = 2

        inner_it = tqdm(df.groupby(k), desc=f'Making 1D slice plots for {k}', leave=False)
        for v, sub_df in inner_it:
            ablation_headers = [
                ablation_header
                for ablation_header in ABLATION_HEADERS
                if ablation_header != k
            ]

            # Mehdi rule - if we're doing dataset slices, don't show training loop
            if k == 'dataset':
                ablation_headers = [ah for ah in ablation_headers if ah != 'training_approach']

            # Identify any headers for which there is only one value after groupby primary header
            skip_headers = {}
            for ablation_header in ablation_headers:
                unique = list(sub_df[ablation_header].unique())
                if len(unique) == 1:
                    skip_headers[ablation_header] = unique[0]

            skip_text = None
            if skip_headers:
                skip_text = ', '.join(
                    f'{skip_key.replace("_", " ").title()}={skip_value}'
                    for skip_key, skip_value in sorted(skip_headers.items())
                )
                inner_it.write(f'Skipping: {skip_text} for {k}={v}')

            # Remove headers for which there is only one value. These will be reported
            # in the title of the chart.
            ablation_headers = [
                ablation_header
                for ablation_header in ablation_headers
                if ablation_header not in skip_headers
            ]

            vert_fig = plt.figure(figsize=(7, 5.5 * len(ablation_headers)))
            grid_spec = gridspec.GridSpec(
                len(ablation_headers), 1,
                figure=vert_fig,
                height_ratios=[
                    2 + sub_df[ablation_header].nunique()
                    for ablation_header in ablation_headers
                ],
            )
            vert_axes = [plt.subplot(x) for x in grid_spec]

            # Calculate the number of rows based on the preset number of columns
            # and a little extra logic for when there should be an empty space
            extra_rows = len(ablation_headers) % ncols
            if not extra_rows:
                nrows = len(ablation_headers) // ncols
                figsize = (7 * ncols, 5 * nrows)
                fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

                # Axes starts as a grid - ravel makes it possible to iterate as a list
                axes = axes.ravel()
            else:
                nrows = 1 + len(ablation_headers) // ncols
                figsize = (7 * ncols, 5 * nrows)
                fig = plt.figure(figsize=figsize)

                width = 2
                shape = (nrows, width * ncols)
                axes = []
                for i in range(nrows - 1):
                    for j in range(ncols):
                        axes.append(plt.subplot2grid(shape=shape, loc=(i, j * width), colspan=width))

                offset = width * (ncols - extra_rows) // 2
                # last row
                for j in range(extra_rows):
                    axes.append(plt.subplot2grid(shape=shape, loc=(nrows - 1, offset + j * width), colspan=width))

            # Make several plots in the grid. Each axis knows where it's supposed to plot
            for ablation_header, g_ax, vert_ax in zip(ablation_headers, axes, vert_axes):
                for ax in (g_ax, vert_ax):
                    # Aggregate the dataset by maximum for this header
                    # idx = sub_df.groupby([ablation_header])[target_header].transform(max) == sub_df[target_header]
                    # sub_df_agg = sub_df[idx]
                    # sub_df_agg.index = sub_df_agg[ablation_header]
                    # sub_df_agg = sub_df_agg.sort_values(target_header, ascending=False)
                    sns.boxplot(data=sub_df, x=ablation_header, y=target_header, ax=ax)
                    ax.set_title(ablation_header.replace('_', ' ').title(), fontdict={'fontsize': 22}, pad=10)
                    ax.set_xlabel('')
                    ax.set_ylabel(target_header, fontdict={'fontsize': 16})
                    for label in ax.get_xticklabels():
                        label.set_ha("center")
                        label.set_rotation(55)
                        label.set_fontsize(15)
                    ax.set_ylim([0.0, 1.0])

            # title_text = k.replace('_', ' ').title()
            # if skip_text is not None:  # skip_text was calculated earlier
            #     plt.suptitle(f"1D Sliced Summary with\n{title_text}={v} (constants: {skip_text})", fontsize=20)
            # else:
            #     plt.suptitle(f"1D Sliced Summary with\n{title_text}={v}", fontsize=20)
            # plt.tight_layout(rect=[0, 0.03, 1, 0.95])

            fig.tight_layout()
            if make_png:
                fig.savefig(os.path.join(output_directory, f'{k}_{v}.png'), dpi=300)
            if make_pdf:
                fig.savefig(os.path.join(output_directory, f'{k}_{v}.pdf'))
            plt.close(fig)

            vert_fig.tight_layout()
            if make_png:
                vert_fig.savefig(os.path.join(output_directory, f'VERT_{k}_{v}.png'), dpi=300)
            if make_pdf:
                vert_fig.savefig(os.path.join(output_directory, f'VERT_{k}_{v}.pdf'))
            plt.close(vert_fig)

    with open(os.path.join(output_directory, 'README.md'), 'w') as file:
        print(f'# Ablation Results\n', file=file)
        print(f'Output at {time.asctime()}', file=file)
        for ablation_header in ABLATION_HEADERS:
            print(f'\n## {ablation_header.replace("_", " ").title()}\n', file=file)
            for v in sorted(df[ablation_header].unique()):
                print(f'<img src="{ablation_header}_{v}.png" alt="{v}"/>\n', file=file)


def _skyline_plot(
    x: str,
    y: str,
    data: pd.DataFrame,
    **kwargs,
):
    order = [False, True]
    sizes = {
        False: 40,
        True: 100,
    }
    alpha = kwargs.pop('alpha', 1.0)
    alpha_non_skyline = max(alpha / 2, 0.1)
    # skyline
    sns.scatterplot(
        x=data.loc[data['skyline'], x],
        y=data.loc[data['skyline'], y],
        size=data['skyline'],
        size_order=order,
        sizes=sizes,
        alpha=alpha,
        marker='x',
        **kwargs,
    )
    sns.scatterplot(
        x=data.loc[~data['skyline'], x],
        y=data.loc[~data['skyline'], y],
        size=data['skyline'],
        size_order=order,
        sizes=sizes,
        alpha=alpha_non_skyline,
        marker='.',
        **kwargs,
    )


def make_sizeplots_trellised(
    *,
    df: pd.DataFrame,
    target_x_header: str,
    target_y_header: str,
    output_directory: str,
    make_png: bool = True,
    make_pdf: bool = True,
    name: Optional[str] = None,
) -> None:
    hue_order = sorted(df['model'].unique())
    sdf = df.copy()
    sdf['skyline'] = False
    for dataset, sub_df in df.groupby(by='dataset'):
        skyline_df = get_skyline_df(
            df=sub_df,
            columns=[target_x_header, target_y_header],
            smaller_is_better=(True, False),
        )
        sdf.loc[skyline_df.index, 'skyline'] = True

    skyline_models = sorted(set(sdf.loc[sdf.skyline, 'model']))

    g = sns.FacetGrid(
        data=sdf,
        hue='model',
        hue_order=hue_order,
        col='dataset',
        col_wrap=2,
        sharex=False,
        sharey=False,
        height=4,
        legend_out=True,
    )
    for ax, dataset in zip(g.axes, g.col_names):
        try:
            skyline_df = get_skyline_df(
                sdf[sdf['dataset'] == dataset],
                columns=[target_x_header, target_y_header],
                smaller_is_better=(True, False),
            )
        except scipy.spatial.qhull.QhullError:
            pass
        else:
            sns.lineplot(
                x=target_x_header,
                y=target_y_header,
                data=skyline_df,
                estimator=None,
                markers=True,
                legend=False,
                ax=ax,
                color='black',
                alpha=.2,
            )
    g.map_dataframe(
        _skyline_plot,
        target_x_header,
        target_y_header,
        alpha=1.0,
    )

    g.set(xlabel=target_x_header.replace('_', ' ').title(), xscale='log')
    g.set_titles(template='{col_name}', fontsize=20)

    with plt.rc_context({'axes.labelsize': 'large'}):
        g.add_legend(label_order=skyline_models, title='Model', loc='center right')

    # redundant
    g.axes[0].set_xlabel('')
    g.axes[1].set_xlabel('')

    if name is None:
        name = f'trellis_scatter_{target_x_header}'
    if make_png:
        g.savefig(os.path.join(output_directory, f'{name}.png'.lower()), dpi=300)
    if make_pdf:
        g.savefig(os.path.join(output_directory, f'{name}.pdf'.lower()))
    plt.close(g.fig)


def make_grouped_sizeplots(
    *,
    df: pd.DataFrame,
    target_x_header: str,
    target_y_header: str,
    output_directory: str,
    make_png: bool = True,
    make_pdf: bool = True,
) -> None:
    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc=f'making sizeplots for {target_x_header}'
    )
    min_bytes = df[target_x_header].min()
    max_bytes = df[target_x_header].max()

    for (dataset, optimizer), sdf in it:
        fig, ax = plt.subplots(figsize=(8, 5))

        g = sns.scatterplot(
            x=target_x_header,
            y=target_y_header,
            data=sdf,
            alpha=0.75,
            hue='model',
            hue_order=sorted(df['model'].unique()),
            ax=ax,
        )
        try:
            skyline_df = get_skyline_df(
                sdf[sdf['dataset'] == dataset],
                columns=[target_x_header, target_y_header],
                smaller_is_better=(True, False),
            )
        except scipy.spatial.qhull.QhullError:
            it.write(f'Not enough data points to make make hull for {dataset}/{optimizer}')
        else:
            sns.lineplot(
                x=target_x_header,
                y=target_y_header,
                data=skyline_df,
                estimator=None,
                markers=True,
                legend=False,
                ax=ax,
            )

        ax.set_xlim([min_bytes, max_bytes])
        ax.set_ylim([0.0, 1.0])
        ax.set_xlabel(target_x_header.replace('_', ' ').title())
        g.set(xscale='log')
        g.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), ncol=1)
        _clean_legend_title(g.legend)

        ax.set_title(f'{dataset} - {optimizer} - {target_x_header}  ({len(sdf.index)} experiments)')

        plt.tight_layout()
        if make_pdf:
            plt.savefig(os.path.join(output_directory, f'scatter_{target_x_header}_{dataset}_{optimizer}.pdf'.lower()))
        if make_png:
            plt.savefig(os.path.join(output_directory, f'scatter_{target_x_header}_{dataset}_{optimizer}.png'.lower()),
                        dpi=300)
        plt.close(fig)


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
