import json
import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pykeen.models import models

HERE = os.path.dirname(__file__)
RESULTS = os.path.join(HERE, 'results')
SUMMARY_DIRECTORY = os.path.join(HERE, 'summary')
os.makedirs(SUMMARY_DIRECTORY, exist_ok=True)

logger = logging.getLogger(__name__)

GETTERS = {
    'hits@10': lambda metrics: metrics['hits_at_k']['avg']['10']
}

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


def collate(key: str):
    df = pd.DataFrame([
        dict(searcher=searcher, **study)
        for model, dataset, searcher, study in iterate_studies(key=key)
    ])
    df = df.sort_values(ABLATION_HEADERS)
    df.to_csv(os.path.join(SUMMARY_DIRECTORY, 'results_test_mehdi.tsv'), sep='\t', index=False)


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


def _iter_model_dirs():
    for model in os.listdir(RESULTS):
        if model.startswith('_') or model.endswith('.py') or not os.path.isdir(os.path.join(RESULTS, model)):
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


def add_inverse_triples_info():
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

                    study_path = os.path.join(hpo_d, 'study.json')
                    if not os.path.exists(study_path):
                        logger.warning(f'missing study path: {hpo_d}')
                        continue

                    with open(study_path) as file:
                        study = json.load(file)

                    hpo_config_path = os.path.join(hpo_d, 'hpo_config.json')
                    if not os.path.exists(hpo_config_path):
                        logger.warning(f'missing hpo config path: {hpo_config_path}')
                        continue

                    with open(hpo_config_path) as file:
                        hpo_config = json.load(file)
                    try:
                        add_inverse_triples = hpo_config['pipeline']['dataset_kwargs']['create_inverse_triples']
                    except:
                        raise Exception(f'create_inverse_triples not in hpo config {hpo_config_path}')
                    study['create_inverse_triples'] = add_inverse_triples

                    with open(os.path.join(study_path), 'w') as file:
                        json.dump(study, file, indent=2)


def create_plots(target_header):
    df = pd.read_csv(os.path.join(SUMMARY_DIRECTORY, 'results_test_mehdi.tsv'), sep='\t')
    df['model'] = df['model'].map(lambda l: MODEL.get(l, l))
    df['loss'] = df['loss'].map(lambda l: LOSS.get(l, l))
    slice_dir = os.path.join(SUMMARY_DIRECTORY, '1D-slices_mehdi')
    os.makedirs(slice_dir, exist_ok=True)

    models = df['model'].unique()
    datasets = df['dataset'].unique()

    for dataset in datasets:
        # Get subframe for dataset
        subframe = df[df['dataset'] == dataset]
        models = subframe['model'].unique()
        num_models = len(models)
        num_rows = (num_models // 2)
        dif = num_models - (2 * num_rows)
        num_rows += dif
        i = 0
        fig, axes = plt.subplots(num_rows, 2, figsize=(14, 10))
        axes = axes.ravel()
        for model in subframe.groupby(['model']):
            y = model[1][target_header]
            x = np.arange(0, len(y))
            error = model[1][f'{target_header}_std']
            axes[i].errorbar(x, y, error, linestyle='None', marker='^')
            i +=1

        plt.savefig(os.path.join(slice_dir, f'{dataset}_all_models.png'))
        plt.close(fig)


def main():
    key = 'hits@10'
    # collate(key=key)
    create_plots(target_header=key)


if __name__ == '__main__':
    main()
