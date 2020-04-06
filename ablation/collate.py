import json
import logging
import os
from copy import deepcopy
from typing import Any, Iterable, Mapping

import pandas as pd

from pykeen.models import models

HERE = os.path.dirname(__file__)
RESULTS = os.path.join(HERE, 'results')
SUMMARY_DIRECTORY = os.path.join(HERE, 'summary')
os.makedirs(SUMMARY_DIRECTORY, exist_ok=True)

COLLATION_PATH = os.path.join(SUMMARY_DIRECTORY, 'results.tsv')

GETTERS = {
    'hits@10': lambda metrics: metrics['hits_at_k']['avg']['10']
}

ABLATION_HEADERS = [
    'dataset',
    'model',
    'loss',
    'optimizer',
    'training_loop',
    'create_inverse_triples',
]

logger = logging.getLogger(__name__)


def get_which_experiments_are_done_df() -> pd.DataFrame:
    experiments = {model: {} for model in models}

    for model, dataset, dataset_directory in _iter_dataset_dirs():
        experiments[model][dataset] = True
        if not os.path.exists(os.path.join(dataset_directory, 'random')):
            print(model, dataset, 'missing random folder')

    return pd.DataFrame(experiments).fillna(False).transpose()


def collate(key: str) -> pd.DataFrame:
    df = pd.DataFrame([
        dict(searcher=searcher, **study)
        for _model, _dataset, searcher, _ablation, _hpo, directory in _iterate_hpo_dirs()
        for study in iterate_studies_from_hpo_directory(directory, key=key)
    ])
    columns = [
        'searcher',
        'dataset',
        'create_inverse_triples',
        'model',
        'loss',
        'regularizer',
        'optimizer',
        'training_loop',
        'negative_sampler',
        'replicate',
        key,
    ]

    df = df[columns].sort_values(columns)
    df.to_csv(COLLATION_PATH, sep='\t', index=False)
    return df


def iterate_studies_from_hpo_directory(directory: str, key: str) -> Iterable[Mapping[str, Any]]:
    study_path = os.path.join(directory, 'study.json')
    if not os.path.exists(study_path):
        logger.warning(f'missing study path: {directory}')
        return

    with open(study_path) as file:
        study = json.load(file)

    for _delete_key in ['metric', 'pykeen_git_hash', 'pykeen_version', 'evaluator']:
        del study[_delete_key]

    replicates_directory = os.path.join(directory, 'best_pipeline', 'replicates')
    if not os.path.exists(replicates_directory):
        logger.warning(f'Can not find {replicates_directory}')
        return

    for replicate in os.listdir(replicates_directory):
        yv = deepcopy(study)
        yv['replicate'] = int(replicate.split('-')[1])

        replicate_results_path = os.path.join(replicates_directory, replicate, 'results.json')
        with open(replicate_results_path) as file:
            replicate_results = json.load(file)
        yv[key] = GETTERS[key](replicate_results['metrics'])

        yield yv


def _iterate_hpo_dirs():
    for model, dataset, searcher, ablation, ablation_d in _iterate_ablation_dirs():
        for hpo in os.listdir(ablation_d):
            hpo_d = os.path.join(ablation_d, hpo)
            if not os.path.isdir(hpo_d):
                continue
            # example:
            # ('complex', 'kinships', 'random',
            # '2020-03-11-13-37_4615dc5b-5d2b-4a50-aa3b-3a19f219b5dc_hpo_complex_kinships_lcwa_adadelta',
            # '0000_kinships_complex', <path>)
            yield model, dataset, searcher, ablation, hpo, hpo_d


def _iterate_ablation_dirs():
    for model, dataset, searcher, searcher_d in _iterate_searcher_dirs():
        for ablation in os.listdir(searcher_d):
            ablation_d = os.path.join(searcher_d, ablation)
            if not os.path.isdir(ablation_d):
                continue
            # example:
            # ('complex', 'kinships', 'random',
            # '2020-03-11-13-37_4615dc5b-5d2b-4a50-aa3b-3a19f219b5dc_hpo_complex_kinships_lcwa_adadelta',
            # <path>)
            yield model, dataset, searcher, ablation, ablation_d


def _iterate_searcher_dirs():
    for model, dataset, dataset_d in _iter_dataset_dirs():
        for searcher in os.listdir(dataset_d):
            searcher_d = os.path.join(dataset_d, searcher)
            if not os.path.isdir(searcher_d):
                continue
            # example: ('complex', 'kinships', 'random', <path>)
            yield model, dataset, searcher, searcher_d


def _iter_dataset_dirs():
    for model, model_d in _iter_model_dirs():
        for dataset in os.listdir(model_d):
            dataset_d = os.path.join(model_d, dataset)
            if not os.path.isdir(dataset_d):
                continue
            # example: ('complex', 'kinships', <path>)
            yield model, dataset, dataset_d


def _iter_model_dirs():
    for model in os.listdir(RESULTS):
        model_d = os.path.join(RESULTS, model)
        if not os.path.isdir(model_d) or model.startswith('_') or model.endswith('.py'):
            continue
        if model not in models:
            raise KeyError(f'invalid model name: {model}')
        # example: ('complex', <path>)
        yield model, model_d


def main():
    """Collate the hits@10 metrics and output."""
    collate('hits@10')
    # df = df.sort_values(ABLATION_HEADERS)
    checkist_df = get_which_experiments_are_done_df()
    checkist_df.to_csv(os.path.join(SUMMARY_DIRECTORY, 'checklist.tsv'), sep='\t')


if __name__ == '__main__':
    main()
