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
    'embedding_dim': REDUCED_EMBEDDING_SETTING,
}

SETTING = {
    REDUCED: REDUCED_SETTING,
}

DEFINED_REGULARIZERS = ['NoRegularizer']
NUM_REGULARIZERS = 1
REGULARIZER_KWARGS = {
    'NoRegularizer': {}
}
REGULARIZER_KWARGS_RANGES = {
    'NoRegularizer': {}
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


def filter_provided_setting(model_name: str, provided_setting: Dict, key_of_interest: str) -> Dict:
    """"""
    provided_setting = {model_name:
        {
            key: value for key, value in provided_setting.items() if key == key_of_interest
        }
    }

    return provided_setting


def create_expected_setting(model_name: str, key: str) -> Dict:
    """."""
    expected_setting = {model_name: {key: REDUCED_SETTING[key]}}

    return expected_setting


if __name__ == '__main__':
    iterator = iterate_config_paths(root_directory='reduced_search_space')

    for model_name_normalized, dataset, hpo_approach, training_assumption, config_name, path in iterator:
        with open(os.path.join(path, config_name)) as file:
            configuration = json.load(file)
            ablation_setting = configuration['ablation']
            model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]

            # check embedding setting
            provided_setting = ablation_setting['model_kwargs'][model_name]
            assert 'embedding_dim' not in provided_setting, f'Embedding dimension provided' \
                f' in model_kwargs for {config_name}'

            provided_setting = ablation_setting['model_kwargs_ranges'][model_name]
            provided_setting = filter_provided_setting(
                model_name=model_name,
                provided_setting=provided_setting,
                key_of_interest='embedding_dim',
            )
            expected_setting = create_expected_setting(model_name=model_name, key='embedding_dim')
            assert expected_setting == provided_setting, f'Error in embedding setting' \
                f' for configuration {config_name}.'

            # check regularization setting
            provided_regularizers = ablation_setting['regularizers']
            provided_setting_kwargs = ablation_setting['regularizer_kwargs']
            provided_setting_kwargs_ranges = ablation_setting['regularizer_kwargs_ranges']
            if model_name == 'TransH':
                expected_regularizers = ['TransH']
                expected_setting_kwargs = {
                    "TransH": {
                        "TransH": {
                            "epsilon": 1e-5
                        }
                    }
                }
                expected_setting_kwargs_ranges = {
                    "TransH": {
                        "TransH": {
                            "weight": {
                                "type": "float",
                                "low": 0.01,
                                "high": 0.3,
                                "scale": "log"
                            }
                        }
                    }
                }
            else:
                expected_regularizers = ['NoRegularizer']
                expected_setting_kwargs = {
                    model_name: {
                        "NoRegularizer": {}
                    }
                }
                expected_setting_kwargs_ranges = expected_setting_kwargs

            assert expected_regularizers == provided_regularizers, f'Wrong regularizers defiend in {config_name}.'
            assert expected_setting_kwargs == provided_setting_kwargs, f'Regularizer arguments provided' \
                f' in regularizer_kwargs for {config_name}'

            assert expected_setting_kwargs_ranges == provided_setting_kwargs_ranges, f'Regularizer arguments provided' \
                f' in regularizer_kwargs_ranges for {config_name}'

            # Check correctness of negative sampling setting for OWA
            if training_assumption.lower() == 'owa':
                provided_setting_kwargs = ablation_setting['negative_sampler_kwargs']
                provided_setting_kwargs_ranges = ablation_setting['negative_sampler_kwargs_ranges']
                expected_setting_kwargs = {
                    model_name: {
                        "BasicNegativeSampler": {}
                    }
                }
                expected_setting_kwargs_ranges = {
                    model_name: {
                        "BasicNegativeSampler": {
                            "num_negs_per_pos": {
                                "type": "int",
                                "low": 1,
                                "high": 100,
                                "q": 10
                            }
                        }
                    }
                }
                assert expected_setting_kwargs == provided_setting_kwargs, f'Negative saompler arguments provided' \
                    f' in negative_sampler_kwargs for {config_name}.'

                assert expected_setting_kwargs_ranges == provided_setting_kwargs_ranges, f'Error in ' \
                    f' negative_sampler_kwargs_ranges for {config_name}.'
