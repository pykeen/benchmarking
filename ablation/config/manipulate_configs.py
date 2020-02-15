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
        "q": 5
    }

def add_automatic_memory_optimization(config:Dict):
    """."""
    config['automatic_memory_optimization'] = True

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

        with open(os.path.join(path, config_name), 'w') as file:
            json.dump(config, file, indent=2)
