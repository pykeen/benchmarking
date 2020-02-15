# -*- coding: utf-8 -*-

"""Manipulates HPO configs."""
import json
import os
from typing import Iterable

from ablation.config.check_correctnes_of_hpo_configs import MODEL_DIRECTORIES_TO_MODEL_NAME

HERE = os.path.abspath(os.path.dirname(__file__))


def iterate_config_paths(root_directory: str) -> Iterable[str]:
    """."""

    root_directory = os.path.join(HERE, root_directory)
    for model in os.listdir(root_directory):
        if model.startswith('.'):
            continue
        assert model in MODEL_DIRECTORIES_TO_MODEL_NAME, f'Model {model} is unknown'
        model_directory = os.path.join(root_directory, model)
        datasets = os.listdir(model_directory)

        for dataset in datasets:
            if dataset.startswith('examples'):
                continue
            dataset_directory = os.path.join(model_directory, dataset)
            for directory, b, filenames in os.walk(dataset_directory):
                for config in filenames:
                    if not config.startswith('hpo'):
                        continue
                    path = os.path.join(directory, config)
                    if not os.path.isfile(path) or not path.endswith('.json'):
                        continue
                    yield config, path, model


def remove_entry(config, key: str) -> None:
    if key in config:
        del config[key]

def remove_batch_size():
    """."""
    iterator = iterate_config_paths(root_directory='reduced_search_space')

    for config, path, model_name in iterator:
        model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name]
        try:
            with open(path) as file:
                config = json.load(file)
        except:
            raise Exception(f"Cannot load {path}")

        if 'lcwa' in config['ablation']['training_kwargs'][model_name]:
            remove_entry(config=config['ablation']['training_kwargs'][model_name]['lcwa'], key='batch_size')
        elif 'owa' in config['ablation']['training_kwargs'][model_name]:
            remove_entry(config=config['ablation']['training_kwargs'][model_name]['owa'], key='batch_size')
        else:
            print(config['ablation']['training_kwargs'][model_name])
            raise Exception(f"Key error in {config['ablation']['training_kwargs'][model_name]} for {path}")

        with open(path, 'w') as file:
            json.dump(config, file, indent=2)

def remove_sub_batch_size():
    """."""
    iterator = iterate_config_paths(root_directory='reduced_search_space')

    for config, path, model_name in iterator:
        model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name]
        try:
            with open(path) as file:
                config = json.load(file)
        except:
            raise Exception(f"Cannot load {path}")

        if 'lcwa' in config['ablation']['training_kwargs'][model_name]:
            remove_entry(config=config['ablation']['training_kwargs'][model_name]['lcwa'], key='sub_batch_size')
        elif 'owa' in config['ablation']['training_kwargs'][model_name]:
            remove_entry(config=config['ablation']['training_kwargs'][model_name]['owa'], key='sub_batch_size')
        else:
            print(config['ablation']['training_kwargs'][model_name])
            raise Exception(f"Key error in {config['ablation']['training_kwargs'][model_name]} for {path}")

        with open(path, 'w') as file:
            json.dump(config, file, indent=2)
if __name__ == '__main__':
    remove_batch_size()
    remove_sub_batch_size()
