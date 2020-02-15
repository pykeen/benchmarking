# -*- coding: utf-8 -*-

"""Manipulates HPO configs."""
import os
from typing import Iterable
import json
HERE = os.path.abspath(os.path.dirname(__file__))


def iterate_config_paths(root_directory: str) -> Iterable[str]:
    """."""

    root_directory = os.path.join(HERE, root_directory)

    """Iterate over all configuration paths."""
    for directory, b, filenames in os.walk(root_directory):
        for config in filenames:
            if not config.startswith('hpo'):
                continue
            path = os.path.join(directory, config)
            if not os.path.isfile(path) or not path.endswith('.json'):
                continue
            yield config, path

def remove_entry(config, key:str) -> None:
    del config[key]

if __name__ == '__main__':
    iterator = iterate_config_paths(root_directory='reduced_search_space')

    for config, path in iterator:
        with open(path) as file:
            config = json.load(file)

        remove_entry(config=config['training_kwargs'][''], key='batch_size')

        with open(path, 'w') as file:
            json.dump(config, file, indent=2)
