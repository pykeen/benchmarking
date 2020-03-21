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
RESULTS = os.path.join(HERE, 'results')
SUMMARY_DIRECTORY = os.path.join(HERE, 'summary')
os.makedirs(SUMMARY_DIRECTORY, exist_ok=True)

logger = logging.getLogger(__name__)


def _iter_model_dirs():
    for model in os.listdir(RESULTS):
        if model.startswith('_') or model.endswith('.py') or not os.path.isdir(model):
            continue
        if model not in models:
            raise KeyError(f'invalid model name: {model}')
        assert model in models, f'{model} not found'
        yield model, os.path.join(RESULTS, model)


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
    df = pd.DataFrame([
        dict(searcher=searcher, **study)
        for model, dataset, searcher, study in iterate_studies(key=key)
    ])
    df = df.sort_values(ABLATION_HEADERS)
    df.to_csv(os.path.join(SUMMARY_DIRECTORY, 'results.tsv'), sep='\t', index=False)


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


ABLATION_HEADERS = [
    'dataset',
    'model',
    'loss',
    'optimizer',
    'training_loop',
]

MODEL = {
    'unstructuredmodel': 'um',
    'structuredembedding': 'se',
}

LOSS = {
    'marginranking': 'mr',
    'crossentropy': 'ce',
}


def make_plots(*, target_header: str):
    """Collate all HPO results in a single table."""
    df = pd.read_csv(os.path.join(SUMMARY_DIRECTORY, 'results.tsv'), sep='\t')
    df['model'] = df['model'].map(lambda l: MODEL.get(l, l))
    df['loss'] = df['loss'].map(lambda l: LOSS.get(l, l))
    _write_1d_sliced_summaries(df=df, target_header=target_header)

    for k in ['loss', 'optimizer', 'training_loop']:
        values = df[k].unique()

        if len(values) == 2:
            _write_2d_sliced_summaries(df, target_header, 'dataset', 'model', k)
        else:
            for value in values:
                _write_2d_sliced_summaries(df, target_header, 'dataset', 'model', k, value)
                _write_2d_sliced_summaries(df, target_header, 'model', 'dataset', k, value)


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
            sdf[val] = [val if x else 'other' for x in sdf[slice_3] == val]
            hue = val
        else:
            hue = slice_3
        sns.violinplot(
            data=sdf,
            x=slice_2,
            y=target_header,
            split=True,
            ax=ax,
            cut=0,
            hue=hue,
        )
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

            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            ablation_headers = [h for h in ABLATION_HEADERS if h != k]
            for ablation_header, ax in zip(ablation_headers, axes.ravel()):
                # Aggregate the dataset by maximum for this header
                idx = sub_df.groupby([ablation_header])[target_header].transform(max) == sub_df[target_header]
                sub_df_agg = sub_df[idx]
                sub_df_agg.index = sub_df_agg[ablation_header]
                sub_df_agg = sub_df_agg.sort_values(target_header, ascending=False)

                del sub_df_agg[ablation_header]

                sns.boxplot(data=sub_df, x=ablation_header, y=target_header, ax=ax, order=sub_df_agg.index)
                sns.swarmplot(data=sub_df, x=ablation_header, y=target_header, ax=ax, linewidth=1.0,
                              order=sub_df_agg.index)

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


def main():
    key = 'hits@10'
    # collate(key=key)
    make_plots(target_header=key)


if __name__ == '__main__':
    main()
