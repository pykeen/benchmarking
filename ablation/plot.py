import itertools as itt
import logging
import os
import random
import time
from typing import Any, Mapping

import click
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from collate import (
    ABLATION_HEADERS, BINARY_ABLATION_HEADERS, COLLATION_PATH, HERE, REGULARIZER, SUMMARY_DIRECTORY,
    collate, read_collation,
)

logger = logging.getLogger(__name__)


def make_plots(*, target_header: str):
    """Collate all HPO results in a single table."""
    df = read_collation()

    for k in ['searcher', 'evaluator']:
        if k in df.columns:
            del df[k]

    sns.set_style("darkgrid")
    _write_dataset_optimizer_summaries(
        df=df, target_header=target_header,
    )
    _write_dataset_optimizer_model_summaries(
        df=df, target_header=target_header,
    )
    _write_1d_sliced_summaries_stratified(
        df=df, target_header=target_header,
    )
    sns.set_style("white")
    _write_1d_sliced_summaries(
        df=df, target_header=target_header,
    )
    _write_2d_summaries(
        df=df, target_header=target_header,
    )


def make_config_index(row: Mapping[str, Any]) -> str:
    create_inverse_triples = row['create_inverse_triples']

    negative_sampler = row.get('negative_sampler')
    if pd.isna(negative_sampler):
        negative_sampler = 'No Samp.'

    regularizer = row["regularizer"]
    if pd.isna(regularizer):
        regularizer = 'No Reg.'
    else:
        regularizer = REGULARIZER.get(regularizer, regularizer)

    if create_inverse_triples == 'True':
        inv_text = 'Inv.'
    else:
        inv_text = 'No Inv.'

    return ' / '.join([
        inv_text,
        row["loss"],
        # regularizer,  # mehdi says we don't need this for now
        row["training_loop"].upper(),
        # negative_sampler,
    ])


def _write_2d_summaries(*, df: pd.DataFrame, target_header):
    for k in ['create_inverse_triples', 'loss', 'optimizer', 'training_loop']:
        values = df[k].unique()

        if len(values) == 2:
            _write_2d_sliced_summaries(df, target_header, 'dataset', 'model', k)
        else:
            for value in values:
                _write_2d_sliced_summaries(df, target_header, 'dataset', 'model', k, value)
                _write_2d_sliced_summaries(df, target_header, 'model', 'dataset', k, value)


def _write_dataset_optimizer_model_summaries(df: pd.DataFrame, target_header: str) -> None:
    model_dir = os.path.join(SUMMARY_DIRECTORY, 'dataset_optimizer_model_summary')
    os.makedirs(model_dir, exist_ok=True)

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
        plt.savefig(os.path.join(model_dir, f'{dataset}_{model}_{optimizer}.pdf'), dpi=300)
        plt.close(fig)


def _write_dataset_optimizer_summaries(df, target_header):
    """Write model summaries, but trellis it on model."""
    model_dir = os.path.join(SUMMARY_DIRECTORY, 'dataset_optimizer_summary')
    os.makedirs(model_dir, exist_ok=True)

    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc='writing dataset/optimizer summaries',
    )
    for (dataset, optimizer), dataset_model_df in it:
        it.write(f'{len(dataset_model_df.index)} rows for {dataset}/{optimizer}')
        data = pd.DataFrame([
            {
                'model': row['model'],
                'configuration': make_config_index(row),
                'replicate': row['replicate'],
                target_header: row[target_header],
            }
            for _, row in dataset_model_df.iterrows()
        ])
        logger.debug('%d replicates mapped for %s/%s', len(data.index), dataset, optimizer)

        means = data.groupby('configuration')[target_header].mean().sort_values()
        logger.debug('%d means mapped for %s/%s', len(means.index), dataset, optimizer)

        fig, ax = plt.subplots(figsize=(14, 7))
        sns.catplot(
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

        sns.despine()
        plt.tight_layout()
        plt.savefig(os.path.join(model_dir, f'{dataset}_{optimizer}.png'), dpi=300)
        plt.savefig(os.path.join(model_dir, f'{dataset}_{optimizer}.pdf'))
        plt.close(fig)


def _write_2d_sliced_summaries(
    df, target_header, slice_1='model', slice_2='dataset', slice_3='loss', val=None,
    n_cols=3,
):
    """The goal is to have for a given loss function the comparison of each dataset to all others"""
    slice_dir = os.path.join(SUMMARY_DIRECTORY, '2D-slices')
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
            sns.violinplot(
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

    plt.savefig(os.path.join(slice_dir, fig_name), dpi=300)
    plt.savefig(os.path.join(slice_dir, fig_name_pdf))
    plt.close(fig)


def _write_1d_sliced_summaries(*, df: pd.DataFrame, target_header: str):
    slice_dir = os.path.join(SUMMARY_DIRECTORY, '1D-slices')
    os.makedirs(slice_dir, exist_ok=True)

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
                ablation_headers = [ah for ah in ablation_headers if ah != 'training_loop']

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

            # Calculate the number of rows based on the preset number of columns
            # and a little extra logic for when there should be an empty space
            extra_rows = len(ablation_headers) % ncols
            if not extra_rows:
                nrows = len(ablation_headers) // ncols
            else:
                nrows = 1 + len(ablation_headers) // ncols

            fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 10))

            # Axes starts as a grid - ravel makes it possible to iterate as a list
            axes = axes.ravel()

            # Remove the spines on axes that won't be filled
            if extra_rows:
                for i in range(extra_rows):
                    axes[-i - 1].set_axis_off()

            # Make several plots in the grid. Each axis knows where it's supposed to plot
            for ablation_header, ax in zip(ablation_headers, axes):
                # Aggregate the dataset by maximum for this header
                # idx = sub_df.groupby([ablation_header])[target_header].transform(max) == sub_df[target_header]
                # sub_df_agg = sub_df[idx]
                # sub_df_agg.index = sub_df_agg[ablation_header]
                # sub_df_agg = sub_df_agg.sort_values(target_header, ascending=False)
                sns.boxplot(
                    data=sub_df, x=ablation_header, y=target_header, ax=ax,
                    # order=sub_df_agg.index,
                )
                # sns.swarmplot(
                #     data=sub_df, x=ablation_header, y=target_header, ax=ax,
                #     # order=sub_df_agg.index,
                #     linewidth=1.0,
                # )

                ax.set_title(ablation_header.replace('_', ' ').title())
                ax.set_xlabel('')
                ax.set_ylim([0.0, 1.0])

                for tick in ax.get_xticklabels():
                    tick.set_rotation(45)

            title_text = k.replace('_', ' ').title()
            if skip_text is not None:  # skip_text was calculated earlier
                plt.suptitle(f"1D Sliced Summary with\n{title_text}={v} (constants: {skip_text})", fontsize=20)
            else:
                plt.suptitle(f"1D Sliced Summary with\n{title_text}={v}", fontsize=20)

            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig(os.path.join(slice_dir, f'{k}_{v}.png'), dpi=300)
            plt.savefig(os.path.join(slice_dir, f'{k}_{v}.pdf'))
            plt.close(fig)

    with open(os.path.join(slice_dir, 'README.md'), 'w') as file:
        print(f'# Ablation Results\n', file=file)
        print(f'Output at {time.asctime()}', file=file)
        for ablation_header in ABLATION_HEADERS:
            print(f'\n## {ablation_header.replace("_", " ").title()}\n', file=file)
            for v in sorted(df[ablation_header].unique()):
                print(f'<img src="{ablation_header}_{v}.png" alt="{v}"/>\n', file=file)

    with open(os.path.join(HERE, 'README.md'), 'w') as file:
        print(f'# Ablation Results\n', file=file)
        print(f'Output at {time.asctime()}\n', file=file)
        for v in sorted(df['dataset'].unique()):
            print(f'<img src="summary/1D-slices/dataset_{v}.png" alt="{v}"/>\n', file=file)


def _write_1d_sliced_summaries_stratified(*, df: pd.DataFrame, target_header: str):
    slice_dir = os.path.join(SUMMARY_DIRECTORY, 'dataset_optimizer_1d_slices')
    os.makedirs(slice_dir, exist_ok=True)
    slice2d_dir = os.path.join(SUMMARY_DIRECTORY, 'dataset_optimizer_2d_slices')
    os.makedirs(slice2d_dir, exist_ok=True)
    slice3d_dir = os.path.join(SUMMARY_DIRECTORY, 'dataset_optimizer_3d_slices')
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
                    col_wrap=3,
                    legend_out=True,
                    ci=None,
                )
                plt.subplots_adjust(top=0.9)
                g.fig.suptitle(f'{optimizer}-{dataset}-{binary_ablation_header}-{ah1}-{ah2}', fontsize=20)
                # plt.tight_layout()
                plt.savefig(
                    os.path.join(
                        slice3d_dir,
                        f'{optimizer}-{dataset}-{binary_ablation_header}-{ah1}-{ah2}.png',
                    ),
                    dpi=300,
                )
                plt.savefig(
                    os.path.join(
                        slice3d_dir,
                        f'{optimizer}-{dataset}-{binary_ablation_header}-{ah1}-{ah2}.pdf',
                    ),
                )
                plt.close()

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
                )
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
            plt.savefig(os.path.join(slice2d_dir, f'{dataset}_{optimizer}_{ah1}_{ah2}.png'), dpi=300)
            plt.savefig(os.path.join(slice2d_dir, f'{dataset}_{optimizer}_{ah1}_{ah2}.pdf'))
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
                            data=sub_df, y=ablation_header, x=target_header, ax=ax,
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
                plt.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_{k}_{v}.png'), dpi=300)
                plt.savefig(os.path.join(slice_dir, f'{dataset}_{optimizer}_{k}_{v}.pdf'))
                plt.close(fig)


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
