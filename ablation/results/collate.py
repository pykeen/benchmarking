"""CLI For HPO results."""

import json
import os
import time

import click
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from poem.utils import flatten_dictionary

HERE = os.path.abspath(os.path.dirname(__file__))

ablation_headers = [
    'model',
    'loss',
    'optimizer',
    'training_loop',
]


@click.command()
def main():
    """Collate all HPO results in a single table."""
    results = list(_iterate_results())
    df = pd.DataFrame(results)

    result_dir = os.path.join(HERE, '_results')
    os.makedirs(result_dir, exist_ok=True)

    df['model'] = df['model'].map(_clean_model)
    df['loss'] = df['loss'].map(_clean_loss)

    df = df.sort_values(ablation_headers)
    df.to_csv(os.path.join(result_dir, 'results.tsv'), sep='\t', index=False)

    target_header = 'best_trial_evaluation'

    for dataset in df.dataset.unique():
        sub_df = df[df.dataset == dataset]
        dataset_dir = os.path.join(result_dir, dataset)
        os.makedirs(dataset_dir, exist_ok=True)

        for ablation_header in ablation_headers:
            # Show distributions

            # Aggregate the dataset by maximum for this header
            idx = sub_df.groupby([ablation_header])[target_header].transform(max) == sub_df[target_header]
            sub_df_agg = sub_df[idx]
            sub_df_agg.index = sub_df_agg[ablation_header]
            sub_df_agg = sub_df_agg.sort_values(target_header, ascending=False)

            # sns.barplot(
            #     data=sub_df_agg,
            #     x=ablation_header,
            #     y=target_header,
            # )
            # plt.xticks(
            #     rotation=45,
            #     horizontalalignment='right',
            #     fontweight='light',
            #     fontsize='x-large'
            # )
            # plt.tight_layout()
            # plt.savefig(os.path.join(result_dir, f'{dataset}_{ablation_header}.png'))

            del sub_df_agg[ablation_header]
            sub_df_agg.to_csv(
                os.path.join(dataset_dir, f'{ablation_header}.tsv'),
                sep='\t',
            )

            f, ax = plt.subplots(figsize=(7, 6))

            sns.boxplot(data=sub_df, x=ablation_header, y=target_header, ax=ax, order=sub_df_agg.index)
            sns.swarmplot(data=sub_df, x=ablation_header, y=target_header, ax=ax, linewidth=1.0, order=sub_df_agg.index)
            if len(sub_df_agg.index) > 4:
                plt.xticks(
                    rotation=45,
                    horizontalalignment='right',
                    fontweight='light',
                    fontsize='x-large'
                )
            ax.set_title(f'{dataset} - {ablation_header}')
            ax.set_xlabel('')
            plt.tight_layout()
            plt.savefig(os.path.join(dataset_dir, f'{ablation_header}.png'))

    with open(os.path.join(result_dir, 'README.md'), 'w') as file:
        print('# HPO Ablation Results\n', file=file)
        print(f'Output at {time.asctime()}\n', file=file)
        for dataset in df.dataset.unique():
            print(f'## {dataset}\n', file=file)
            for ablation_header in ablation_headers:
                print(f'### {dataset} {ablation_header}\n', file=file)
                print(
                    f'<img src="{dataset}/{ablation_header}.png"'
                    f' alt="{dataset} {ablation_header}"'
                    f' height="300" />\n',
                    file=file,
                )


def _clean_model(x):
    if x == 'unstructuredmodel':
        return 'um'
    elif x == 'structuredembedding':
        return 'se'
    return x


def _clean_loss(x):
    if x == 'negativesamplingselfadversarial':
        return 'nssa'
    return x


def _iterate_results():
    for directory, _, file_names in os.walk(HERE):
        if 'hpo_config.json' not in file_names or 'best_pipeline_config.json' not in file_names:
            continue

        with open(os.path.join(directory, 'best_pipeline_config.json')) as file:
            r = json.load(file)

        yield {
            **flatten_dictionary(r['metadata']),
            **flatten_dictionary(r['pipeline']),
        }


if __name__ == '__main__':
    main()
