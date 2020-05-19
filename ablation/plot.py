import logging
import os
import time

import click
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from collate import ABLATION_HEADERS, COLLATION_PATH, HERE, SUMMARY_DIRECTORY, collate

logger = logging.getLogger(__name__)

sns.set_style("darkgrid")

MODEL = {
    'unstructuredmodel': 'um',
    'structuredembedding': 'se',
}

LOSS = {
    'marginranking': 'MR',
    'crossentropy': 'CE',
    'bceaftersigmoid': 'BCE',
    'softplus': 'SoftPlus',
}

_create_inverse_triples_map = {
    None: '?',
    True: '+',
    False: '-',
}


def make_config_index(row) -> str:
    create_inverse_triples = _create_inverse_triples_map.get(row.get('create_inverse_triples'))
    if create_inverse_triples is None:
        raise ValueError(f'Invalid create_inverse_triples value: {create_inverse_triples}')

    negative_sampler = row.get('negative_sampler')
    if pd.isna(negative_sampler):
        negative_sampler = 'No Samp.'

    regularizer = row["regularizer"]
    if regularizer == 'no':
        regularizer = 'No Reg.'

    return f'Inv. {create_inverse_triples} / {row["loss"]} / {regularizer} / {row["training_loop"].upper()} / {negative_sampler}'


def make_plots(*, target_header: str):
    """Collate all HPO results in a single table."""
    df = pd.read_csv(COLLATION_PATH, sep='\t')
    df['model'] = df['model'].map(lambda l: MODEL.get(l, l))
    df['loss'] = df['loss'].map(lambda l: LOSS.get(l, l))

    for k in ['searcher', 'evaluator']:
        if k in df.columns:
            del df[k]

    _write_model_summaries(
        df=df, target_header=target_header,
    )
    # _write_1d_sliced_summaries(
    #     df=df, target_header=target_header,
    # )
    # _write_2d_summaries(
    #     df=df, target_header=target_header,
    # )


def _write_2d_summaries(*, df: pd.DataFrame, target_header):
    for k in ['create_inverse_triples', 'loss', 'optimizer', 'training_loop']:
        values = df[k].unique()

        if len(values) == 2:
            _write_2d_sliced_summaries(df, target_header, 'dataset', 'model', k)
        else:
            for value in values:
                _write_2d_sliced_summaries(df, target_header, 'dataset', 'model', k, value)
                _write_2d_sliced_summaries(df, target_header, 'model', 'dataset', k, value)


def _write_model_summaries(df, target_header):
    model_dir = os.path.join(SUMMARY_DIRECTORY, 'modelsummary')
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

        config_order = data.groupby('configuration')[target_header].mean().sort_values()

        # data.to_csv(os.path.join(SUMMARY_DIRECTORY, f'{dataset}_{model}.tsv'), sep='\t', index=False)
        fig, ax = plt.subplots(1, figsize=(14, 7))
        sns.barplot(
            data=data, x=target_header, y='configuration', ax=ax, capsize=.2,
            order=config_order.index,
            palette="GnBu_d",
        )
        ax.set_title(f'{dataset} - {model} - {optimizer}')
        ax.set_ylabel('')
        ax.set_yticks([])

        # set individual bar lables using above list
        fontsize = 20
        for y, (label, patch) in enumerate(zip(config_order.index, ax.patches)):
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
        plt.savefig(os.path.join(model_dir, f'{dataset}_{model}_{optimizer}.png'))
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

    for (slice_1_value, sdf), ax in zip(df.groupby(slice_1), axes.ravel()):
        if val is not None:
            sdf[val] = [val if x else 'other' for x in (sdf[slice_3] == val)]
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
            logger.exception('could not make violin plot')
            continue
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
        ax.set_title(f'{slice_1} - {slice_1_value}')
        ax.set_xlabel('')
    plt.tight_layout()

    if val is not None:
        fig_name = f'{slice_1}-{slice_2}-{slice_3}-{val}.png'
    else:
        fig_name = f'{slice_1}-{slice_2}-{slice_3}.png'

    plt.savefig(os.path.join(slice_dir, fig_name))
    plt.close(fig)


def _write_1d_sliced_summaries(*, df: pd.DataFrame, target_header: str):
    slice_dir = os.path.join(SUMMARY_DIRECTORY, '1D-slices')
    os.makedirs(slice_dir, exist_ok=True)
    for k in ABLATION_HEADERS:
        for v in df[k].unique():
            sub_df = df[df[k] == v]

            ablation_headers = [h for h in ABLATION_HEADERS if h != k]
            ncols = 2
            nrows = 1 + len(ablation_headers) // ncols
            fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 10))
            for ablation_header, ax in zip(ablation_headers, axes.ravel()):
                # Aggregate the dataset by maximum for this header
                idx = sub_df.groupby([ablation_header])[target_header].transform(max) == sub_df[target_header]
                sub_df_agg = sub_df[idx]
                sub_df_agg.index = sub_df_agg[ablation_header]
                sub_df_agg = sub_df_agg.sort_values(target_header, ascending=False)

                del sub_df_agg[ablation_header]
                try:
                    sns.boxplot(data=sub_df, x=ablation_header, y=target_header, ax=ax, order=sub_df_agg.index)
                    sns.swarmplot(data=sub_df, x=ablation_header, y=target_header, ax=ax, order=sub_df_agg.index,
                                  linewidth=1.0)
                except ValueError:
                    logger.exception('could not make swarm plot')
                    continue

                ax.set_title(ablation_header.replace('_', ' ').title())
                ax.set_xlabel('')

                for tick in ax.get_xticklabels():
                    tick.set_rotation(45)

            plt.suptitle(f"{k.replace('_', ' '.title())}: {v}", fontsize=20)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig(os.path.join(slice_dir, f'{k}_{v}.png'))
            plt.close(fig)

    with open(os.path.join(slice_dir, 'README.md'), 'w') as file:
        print(f'# Ablation Results\n', file=file)
        print(f'Output at {time.asctime()}', file=file)
        for k in ABLATION_HEADERS:
            print(f'\n## {k.replace("_", " ").title()}\n', file=file)
            for v in sorted(df[k].unique()):
                print(f'<img src="{k}_{v}.png" alt="{v}"/>\n', file=file)

    with open(os.path.join(HERE, 'README.md'), 'w') as file:
        print(f'# Ablation Results\n', file=file)
        print(f'Output at {time.asctime()}\n', file=file)
        for v in sorted(df['dataset'].unique()):
            print(f'<img src="summary/1D-slices/dataset_{v}.png" alt="{v}"/>\n', file=file)


@click.command()
def main():
    key = 'hits@10'
    if not os.path.exists(COLLATION_PATH):
        collate(key)
    make_plots(target_header=key)
    click.echo('done!')


if __name__ == '__main__':
    main()
