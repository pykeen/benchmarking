import json
import logging
import os
from copy import deepcopy
from typing import Any, Iterable, Mapping

import pandas as pd
from tqdm import tqdm

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


def collate(key: str = 'hits@10') -> pd.DataFrame:
    """Collate all results for a given metric."""
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

    rows = []
    for directory, d, filenames in tqdm(os.walk(RESULTS)):
        if 'study.json' not in filenames:
            continue
        if 'hpo_config.json' not in filenames:
            logger.warning('missing hpo config in %s', directory)
            continue
        for study in iterate_studies_from_hpo_directory(directory, key=key):
            rows.append(study)

    if not rows:
        raise RuntimeError('NO RESULTS')

    df = pd.DataFrame(rows)
    df = df[columns].sort_values(columns)
    df.to_csv(COLLATION_PATH, sep='\t', index=False)
    return df


def iterate_studies_from_hpo_directory(directory: str, key: str) -> Iterable[Mapping[str, Any]]:
    study_path = os.path.join(directory, 'study.json')
    if not os.path.exists(study_path):
        logger.warning('missing study path: %s', directory)
        return

    hpo_config_path = os.path.join(directory, 'hpo_config.json')
    if not os.path.exists(hpo_config_path):
        logger.warning('missing hpo config: %s', directory)
        return

    with open(study_path) as file:
        study = json.load(file)

    with open(hpo_config_path) as file:
        hpo_config = json.load(file)

    study['searcher'] = hpo_config['optuna']['sampler']

    for _delete_key in ['metric', 'pykeen_git_hash', 'pykeen_version', 'evaluator']:
        del study[_delete_key]

    replicates_directory = os.path.join(directory, 'best_pipeline', 'replicates')
    if not os.path.exists(replicates_directory):
        logger.warning('Can not find %s', replicates_directory)
        return

    for replicate in os.listdir(replicates_directory):
        yv = deepcopy(study)
        yv['replicate'] = int(replicate.split('-')[1])

        replicate_results_path = os.path.join(replicates_directory, replicate, 'results.json')
        with open(replicate_results_path) as file:
            replicate_results = json.load(file)
        yv[key] = GETTERS[key](replicate_results['metrics'])

        yield yv


def main():
    """Collate the hits@10 metrics and output."""
    df = collate()

    experiments = {model: {} for model in models}
    for model, dataset in df[['model', 'dataset']].values:
        experiments[model][dataset] = True
    checklist_df = pd.DataFrame(experiments).fillna(False).transpose()
    checklist_df.to_csv(os.path.join(SUMMARY_DIRECTORY, 'checklist.tsv'), sep='\t')
    checklist_df.to_latex(os.path.join(SUMMARY_DIRECTORY, 'checklist.tex'))


if __name__ == '__main__':
    main()
