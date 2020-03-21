import json
import logging
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from pykeen.models import models

HERE = os.path.dirname(__file__)

logger = logging.getLogger(__name__)


def _iter_model_dirs():
    for model in os.listdir(HERE):
        if model.startswith('_') or model.endswith('.py') or not os.path.isdir(model):
            continue
        if model not in models:
            raise KeyError(f'invalid model name: {model}')
        assert model in models, f'{model} not found'
        yield model, os.path.join(HERE, model)


def _iter_dataset_dirs():
    for model, d in _iter_model_dirs():
        for dataset in os.listdir(d):
            dataset_d = os.path.join(d, dataset)
            if not os.path.isdir(dataset_d):
                continue
            yield model, dataset, dataset_d


def iterate_studies(key: str):
    for model, dataset, d in _iter_dataset_dirs():
        for searcher in os.listdir(d):
            searcher_d = os.path.join(d, searcher)
            if not os.path.isdir(searcher_d):
                continue
            for ablation in os.listdir(searcher_d):
                ablation_d = os.path.join(searcher_d, ablation)
                if not os.path.isdir(ablation_d):
                    continue
                for hpo in os.listdir(ablation_d):
                    hpo_d = os.path.join(ablation_d, hpo)
                    if not os.path.isdir(hpo_d):
                        continue
                    study = get_results_from_hpo_directory(hpo_d, key=key)
                    if study is None:
                        continue
                    yield model, dataset, searcher, study


def collate(key: str):
    return pd.DataFrame([
        dict(searcher=searcher, **study)
        for model, dataset, searcher, study in iterate_studies(key=key)
    ])


GETTERS = {
    'hits@10': lambda metrics: metrics['hits_at_k']['avg']['10']
}


def get_results_from_hpo_directory(hpo_experiment_directory: str, key: str):
    study_path = os.path.join(hpo_experiment_directory, 'study.json')
    if not os.path.exists(study_path):
        logger.warning(f'missing study path: {hpo_experiment_directory}')
        return

    with open(study_path) as file:
        study = json.load(file)

    for _delete_key in ['metric', 'pykeen_git_hash', 'pykeen_version']:
        del study[_delete_key]

    metrics = []
    replicates_directory = os.path.join(hpo_experiment_directory, 'best_pipeline', 'replicates')
    if not os.path.exists(replicates_directory):
        raise FileNotFoundError
    for replicate in os.listdir(replicates_directory):
        replicate_results_path = os.path.join(replicates_directory, replicate, 'results.json')
        with open(replicate_results_path) as file:
            replicate_results = json.load(file)
        metrics.append(GETTERS[key](replicate_results['metrics']))

    study[key] = np.mean(metrics).round(5)
    study[f'{key}_std'] = np.std(metrics).round(5)

    return study


def get_which_experiments_are_done_df() -> pd.DataFrame:
    experiments = {model: {} for model in models}

    for model, dataset, dataset_directory in _iter_dataset_dirs():
        experiments[model][dataset] = True
        if not os.path.exists(os.path.join(dataset_directory, 'random')):
            print(model, dataset, 'missing random folder')

    return pd.DataFrame(experiments).fillna(False).transpose()


ablation_headers = [
    'model',
    'loss',
    'optimizer',
    'training_loop',
]


def make_plots(*, df: pd.DataFrame, target_header: str):
    """Collate all HPO results in a single table."""
    result_dir = os.path.join(HERE, '_results')
    os.makedirs(result_dir, exist_ok=True)

    df = df.sort_values(ablation_headers)
    df.to_csv(os.path.join(result_dir, 'results.tsv'), sep='\t', index=False)

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


def main():
    key = 'hits@10'
    df = collate(key=key)
    make_plots(df=df, target_header=key)


if __name__ == '__main__':
    main()
