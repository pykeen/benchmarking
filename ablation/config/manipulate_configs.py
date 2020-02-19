# -*- coding: utf-8 -*-

"""Manipulates HPO configs."""
import json
import os
from typing import Dict

from ablation.config.check_correctnes_of_hpo_configs import MODEL_DIRECTORIES_TO_MODEL_NAME, iterate_config_paths

HERE = os.path.abspath(os.path.dirname(__file__))


def remove_entry(config: Dict, key: str) -> None:
    if key in config:
        del config[key]


def add_batch_size_kwargs_ranges(config):
    """."""
    config['batch_size'] = {
        "type": "int",
        "low": 7,
        "high": 9,
        "scale": 'power_two'
    }


def add_negative_samples_kwargs_ranges(config):
    """."""
    config['num_negs_per_pos'] = {
        "type": "int",
        "low": 1,
        "high": 100,
        "q": 1
    }


def add_automatic_memory_optimization(config: Dict) -> None:
    """."""
    config['automatic_memory_optimization'] = True


def add_eval_batch_size(config: Dict):
    """."""
    config['ablation']['evaluation_kwargs']['batch_size'] = None


def add_stopper(config: Dict) -> None:
    """."""
    config = config['ablation']
    if 'early_stopping' in config:
        del config['early_stopping']
        del config['early_stopping_kwargs']
    config['stopper'] = 'early'
    config['stopper_kwargs'] = {
        "frequency": 50,
        "patience": 2,
        "delta": 0.002
    }


def add_embedding_dimension(config: Dict) -> None:
    """."""
    model = config['ablation']['models'][0]
    embedding_dim = dict(
        type='int', low=6, high=8, scale='power_two'
    )
    config['ablation']['model_kwargs_ranges'][model]['embedding_dim'] = embedding_dim

    if 'relation_dim' in config['ablation']['model_kwargs_ranges'][model]:
        config['ablation']['model_kwargs_ranges'][model]['relation_dim'] = embedding_dim


if __name__ == '__main__':

    iterator = iterate_config_paths(root_directory='reduced_search_space')

    for model_name_normalized, dataset, hpo_approach, training_assumption, config_name, path in iterator:
        model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]
        with open(os.path.join(path, config_name), 'r') as file:
            try:
                config = json.load(file)
            except:
                raise Exception(f"{config_name} could not be loaded.")

        remove_entry(config=config['ablation']['training_kwargs'][model_name][training_assumption], key='batch_size')

        remove_entry(
            config=config['ablation']['training_kwargs'][model_name][training_assumption],
            key='sub_batch_size',
        )

        add_batch_size_kwargs_ranges(
            config['ablation']['training_kwargs_ranges'][model_name][training_assumption])

        if training_assumption.lower() == 'owa':
            add_negative_samples_kwargs_ranges(
                config=config['ablation']['negative_sampler_kwargs_ranges'][model_name]['BasicNegativeSampler']
            )
        add_automatic_memory_optimization(config=config['ablation']['model_kwargs'][model_name])

        add_eval_batch_size(config=config)

        add_stopper(config=config)

        add_embedding_dimension(config=config)

        with open(os.path.join(path, config_name), 'w') as file:
            json.dump(config, file, indent=2)
