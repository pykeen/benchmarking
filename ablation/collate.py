import json
import logging
import os
from copy import deepcopy
from typing import Any, Iterable, Mapping

import click
import pandas as pd
from tqdm import tqdm

from pykeen.datasets import datasets
from pykeen.models import models
from src.utils import get_model_size

HERE = os.path.dirname(__file__)
RESULTS = os.path.join(HERE, 'results')
SUMMARY_DIRECTORY = os.path.join(HERE, 'summary')
os.makedirs(SUMMARY_DIRECTORY, exist_ok=True)

# Shut up about mapping triples, lol
logging.getLogger('pykeen.triples.triples_factory').setLevel(logging.ERROR)

COLLATION_PATH = os.path.join(SUMMARY_DIRECTORY, 'results.tsv')

MODEL = {
    'unstructuredmodel': 'UM',
    'structuredembedding': 'SE',
}
for model_key, model_cls in models.items():
    if model_key not in MODEL:
        MODEL[model_key] = model_cls.__name__

DATASETS = {
    dataset_key: dataset_cls.__name__
    for dataset_key, dataset_cls in datasets.items()
}

LOSS = {
    'marginranking': 'MR',
    'crossentropy': 'CE',
    'bceaftersigmoid': 'BCE',
    'softplus': 'SoftPlus',
    'nssa': 'NSSA',
}

REGULARIZER = {
    'no': 'No Reg.',
    'transh': 'No Reg.',
}

GETTERS = {
    'hits@10': lambda metrics: metrics['hits_at_k']['avg']['10'],
}

ABLATION_HEADERS = [
    'dataset',
    'model',
    'loss',
    'optimizer',
    'training_loop',
    'create_inverse_triples',
]

BINARY_ABLATION_HEADERS = {
    'create_inverse_triples',
    'training_loop',
}

MODEL_BYTES = 'model_bytes'

logger = logging.getLogger(__name__)


def read_collation() -> pd.DataFrame:
    df = pd.read_csv(COLLATION_PATH, sep='\t')
    df['model'] = df['model'].map(lambda l: MODEL.get(l.lower(), l))
    df['loss'] = df['loss'].map(lambda l: LOSS.get(l.lower(), l))
    df['regularizer'] = df['regularizer'].map(lambda l: REGULARIZER.get(l.lower(), l))
    df['dataset'] = df['dataset'].map(lambda l: DATASETS.get(l.lower(), l))
    df['optimizer'] = df['optimizer'].map(str.capitalize)
    df['training_loop'] = df['training_loop'].map(str.upper)
    df['create_inverse_triples'] = df['create_inverse_triples'].map(lambda s: 'True' if s else 'False')
    return df


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
        MODEL_BYTES,
        'replicate',
        'training_time',
        'evaluation_time',
        key,
    ]

    directories = [
        (directory, filenames)
        for directory, _, filenames in os.walk(RESULTS)
        if 'study.json' in filenames
    ]

    rows = []
    for directory, filenames in tqdm(directories):
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

    with open(os.path.join(directory, 'best_pipeline', 'pipeline_config.json')) as file:
        ppc = json.load(file)

    if 'create_inverse_triples' not in study:
        study['create_inverse_triples'] = ppc['pipeline']['dataset_kwargs']['create_inverse_triples']

    try:
        study[MODEL_BYTES] = get_model_size(**ppc['pipeline'])
    except TypeError as e:
        logger.warning('could not instantiate part of model: %s', e)
        logger.warning('study:\n%s\n', json.dumps(study, indent=2))
        study[MODEL_BYTES] = None

    with open(hpo_config_path) as file:
        hpo_config = json.load(file)

    study.setdefault('create_inverse_triples', False)
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
        yv['training_time'] = replicate_results['times']['training']
        yv['evaluation_time'] = replicate_results['times']['evaluation']
        yield yv


@click.command()
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
    logging.basicConfig(level=logging.INFO)
    main()
