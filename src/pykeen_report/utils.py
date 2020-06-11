# -*- coding: utf-8 -*-

"""Utilities for collating experimental results."""

import json
import logging
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Type, Union

import pandas as pd
from tqdm import tqdm

from pykeen.datasets import DataSet, get_dataset
from pykeen.losses import Loss, get_loss_cls
from pykeen.models import get_model_cls, models
from pykeen.models.base import Model
from pykeen.regularizers import Regularizer, get_regularizer_cls
from pykeen.triples import TriplesFactory
from pykeen.utils import flatten_dictionary, resolve_device
from .constants import DATASETS, GETTERS, LOSS, MODEL, MODEL_BYTES, NEGATIVE_SAMPELR, REGULARIZER

__all__ = [
    'get_model_size',
]

logger = logging.getLogger(__name__)


def collate_ablation(
    *,
    results_directory: str,
    output_path: str,
    key: str,
) -> pd.DataFrame:
    """Collate all results for a given metric.

    :param key: The metric which you care about. Should be the same one against which you
     optimized
    """
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
        for directory, _, filenames in os.walk(results_directory)
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
    df.to_csv(output_path, sep='\t', index=False)
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


def read_ablation_collation(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep='\t')
    df['model'] = df['model'].map(lambda l: MODEL.get(l.lower(), l))
    df['loss'] = df['loss'].map(lambda l: LOSS.get(l.lower(), l))
    df['regularizer'] = df['regularizer'].map(lambda l: REGULARIZER.get(l.lower(), l))
    df['dataset'] = df['dataset'].map(lambda l: DATASETS.get(l.lower(), l))
    df['optimizer'] = df['optimizer'].map(str.capitalize)
    df['training_loop'] = df['training_loop'].map(str.upper)
    df['negative_sampler'] = df['negative_sampler'].map(
        lambda l: NEGATIVE_SAMPELR.get(l.lower(), l) if pd.notna(l) else 'None'
    )
    df['create_inverse_triples'] = df['create_inverse_triples'].map(lambda s: 'True' if s else 'False')
    return df


def make_checklist_df(df: pd.DataFrame, output_csv_path=None, output_latex_path=None) -> pd.DataFrame:
    """Make a checklist dataframe.

    :param df: A collated dataframe from :func:`read_collation`
    """
    experiments = {model: {} for model in models}
    for model, dataset in df[['model', 'dataset']].values:
        experiments[model][dataset] = True
    rv = pd.DataFrame(experiments).fillna(False).transpose()

    if output_csv_path:
        rv.to_csv(output_csv_path, sep='\t')
    if output_latex_path:
        rv.to_latex(output_latex_path)
    return rv


def get_model_size(  # noqa: C901
    *,
    dataset: Union[None, str, Type[DataSet]] = None,
    dataset_kwargs: Optional[Mapping[str, Any]] = None,
    training_triples_factory: Optional[TriplesFactory] = None,
    testing_triples_factory: Optional[TriplesFactory] = None,
    validation_triples_factory: Optional[TriplesFactory] = None,
    model: Union[str, Type[Model]],
    model_kwargs: Optional[Mapping[str, Any]] = None,
    loss: Union[None, str, Type[Loss]] = None,
    loss_kwargs: Optional[Mapping[str, Any]] = None,
    regularizer: Union[None, str, Type[Regularizer]] = None,
    regularizer_kwargs: Optional[Mapping[str, Any]] = None,
    **_kwargs,
) -> int:
    """Make a model instance, similarly to how the pipelin is started, then return the model size."""
    device = resolve_device('cpu')
    training_triples_factory, testing_triples_factory, validation_triples_factory = get_dataset(
        dataset=dataset,
        dataset_kwargs=dataset_kwargs,
        training_triples_factory=training_triples_factory,
        testing_triples_factory=testing_triples_factory,
        validation_triples_factory=validation_triples_factory,
    )

    if model_kwargs is None:
        model_kwargs = {}

    if regularizer is not None:
        regularizer_cls = get_regularizer_cls(regularizer)
        model_kwargs['regularizer'] = regularizer_cls(
            device=device,
            **(regularizer_kwargs or {}),
        )

    if loss is not None:
        loss_cls = get_loss_cls(loss)
        model_kwargs['loss'] = loss_cls(**(loss_kwargs or {}))

    model = get_model_cls(model)
    model_instance: Model = model(
        random_seed=0,
        preferred_device=device,
        triples_factory=training_triples_factory,
        **model_kwargs,
    )
    return model_instance.num_parameter_bytes


def collate_experiments(root: Path, output: str) -> pd.DataFrame:
    data = []
    for run_label in tqdm(list(root.iterdir()), desc='Collating reproductions'):
        if run_label.name in {'.DS_Store'}:
            continue
        _date, _reference, model, dataset = run_label.name.split('_')

        # get size
        with (run_label / 'configuration_copied.json').open() as file:
            config = json.load(file)
        model_size = get_model_size(**config['pipeline'])

        for replicate in (run_label / 'replicates').iterdir():
            with (replicate / 'results.json').open() as rf:
                result = flatten_dictionary(json.load(rf))
            result.update(dict(
                # reference=reference,
                model=get_model_cls(model).__name__,
                dataset=dataset,
                replicate=int(replicate.name.split('-')[1]),
                model_bytes=model_size,
            ))
            del result['losses']
            data.append(result)

    df = pd.DataFrame(data=data)
    df = df.set_index(['dataset', 'model', 'replicate']).reset_index()
    df.to_csv(output, sep='\t', index=False)
    return df
