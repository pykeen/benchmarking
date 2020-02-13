# -*- coding: utf-8 -*-

"""Validates the HPO configs."""

import json
import os
from typing import Dict, Iterable

HERE = os.path.abspath(os.path.dirname(__file__))

MODEL_DIRECTORIES_TO_MODEL_NAME = {
    'complex': 'ComplEx',
    'conve': 'ConvE',
    'convkb': 'ConvKB',
    'distmult': 'DistMult',
    'ermlp': 'ERMLP',
    'hole': 'HolE',
    'kg2e': 'KG2E',
    'ntn': 'NTN',
    'proje': 'ProjE',
    'rescal': 'RESCAL',
    'rgcn': 'RGCN',
    'rotate': 'RotatE',
    'simple': 'SimplE',
    'structuredembedding': 'StructuredEmbedding',
    'transd': 'TransD',
    'transe': 'TransE',
    'transh': 'TransH',
    'transr': 'TransR',
    'tucker': 'TuckER',
    'um': 'UnstructuredModel',
}

DATASET_NAMES = ['fb15k237', 'kinships', 'wn18rr', 'yago310', 'examples']

NUM_LCWA_CONFIGS = 1
NUM_OWA_CONFIGS = 4

REDUCED = 'reduced'
REDUCED_EMBEDDING_SETTING = {
    "type": "int",
    "low": 64,
    "high": 192,
    "q": 64,
}

REDUCED_SETTING = {
    'embedding': REDUCED_EMBEDDING_SETTING,
}

SETTING = {
    REDUCED: REDUCED_SETTING,
}


def iterate_config_paths(root_directory: str) -> Iterable[str]:
    """Iterate over all configuration paths."""
    root_directory = os.path.join(HERE, root_directory)
    for model in os.listdir(root_directory):
        # Check, whether model is valid
        if model.startswith('.'):
            break

        assert model in MODEL_DIRECTORIES_TO_MODEL_NAME, f'Model {model} is unknown'
        model_directory = os.path.join(root_directory, model)

        # Check, whether required datasets are defined
        datasets = os.listdir(model_directory)

        assert len(datasets) == len(DATASET_NAMES) and [dataset in datasets for dataset in DATASET_NAMES], \
            f'It is excepted that configurations for \'examples\', \'fb15k237\', \'kinships\', \'wn18rr\' and' \
                f' \'yago310\' are prvovided, but got' \
                f' {datasets[0]}, {datasets[1]}, {datasets[2]}, {datasets[3]} and {datasets[4]}.'

        for dataset in datasets:
            if dataset not in DATASET_NAMES and dataset != 'examples':
                raise Exception(f"Dataset {dataset} is unknown.")

            if dataset == 'examples':
                continue

            # Check, whether correct HPO approach is defined
            hpo_approach_directory = os.path.join(root_directory, model_directory, dataset)
            hpo_approach = os.listdir(hpo_approach_directory)

            assert len(
                hpo_approach) == 1 and hpo_approach[0] == 'random', \
                "Currently, only random search is allowed as HPO approach."

            # Check, whether correct training assumptions are defined
            training_assumption_directory = os.path.join(
                root_directory,
                model_directory,
                dataset,
                hpo_approach[0],
            )
            training_assumptions = os.listdir(training_assumption_directory)
            assert len(training_assumptions) == 2 and 'lcwa' in training_assumptions and 'owa' in training_assumptions, \
                f'It is expected that only configurations for LCWA and OWA are provided, but got ' \
                    f'{training_assumptions[0]} and {training_assumptions[1]}'

            for training_assumption in training_assumptions:
                configs_directory = os.path.join(
                    root_directory,
                    model_directory,
                    dataset,
                    hpo_approach[0],
                    training_assumption,
                )
                configs = os.listdir(configs_directory)

                # Check, whether correct number of configurations are defined
                if training_assumption == 'lcwa':
                    assert len(configs) == NUM_LCWA_CONFIGS, "More than one LCWA config provided."
                else:
                    assert training_assumption == 'owa' and len(
                        configs) == NUM_OWA_CONFIGS, f'For owa exactly {NUM_OWA_CONFIGS} configurations' \
                        f' are required, but {len(configs)} were provided'

                for config in configs:
                    yield model, dataset, hpo_approach, training_assumption, config, configs_directory


def check_embedding_setting(configuration: json, model: str, setting: Dict):
    """."""
    relevant_part = configuration['ablation']['model_kwargs_ranges']
    configured_embedding = relevant_part[MODEL_DIRECTORIES_TO_MODEL_NAME[model]]['embedding_dim']
    embedding_setting = setting['embedding']
    keys = configured_embedding.keys()
    assert len(keys) == len(embedding_setting.keys()) and [k in embedding_setting for k in keys]
    for k in keys:
        assert configured_embedding[k] == embedding_setting[k], f'expected {k} is {embedding_setting[k]},' \
            f'but got {configured_embedding}'


if __name__ == '__main__':
    iterator = iterate_config_paths(root_directory='reduced_search_space')

    for model, dataset, hpo_approach, training_assumption, config_name, path in iterator:
        with open(os.path.join(path, config_name)) as file:
            configuration = json.load(file)
            check_embedding_setting(configuration=configuration, model=model, setting=REDUCED_SETTING)
