# -*- coding: utf-8 -*-

"""Manipulates HPO configs."""
import json
import os
from copy import deepcopy
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


def set_optimizer(config: Dict, optimizer: str, model: str):
    """."""
    config = config['ablation']
    config['optimizers'] = [optimizer]
    config['optimizer_kwargs'][model] = {
        optimizer: {
            "weight_decay": 0.0
        }
    }

    config['optimizer_kwargs_ranges'][model] = {
        optimizer: {
            "lr": {
                "type": "float",
                "low": 0.001,
                "high": 0.1,
                "scale": "log"
            }
        }
    }

    return config


def set_crossentropy_loss(config: Dict, model: str):
    """."""
    config = config['ablation']
    config['loss_functions'] = ['CrossEntropyLoss']
    config['loss_kwargs'][model] = {
        'CrossEntropyLoss': {}
    }

    config['loss_kwargs_ranges'][model] = {
        'CrossEntropyLoss': {}
    }


def split_lcwa_configs(config: Dict, path: str, config_name: str):
    """."""
    model = config['ablation']['models'][0]
    config_adam = deepcopy(config)
    config_crossentropy = deepcopy(config)
    config_adadelta = deepcopy(config)

    set_optimizer(config=config_adam, optimizer='adadelta', model=model)

    set_optimizer(config=config_adadelta, optimizer='adadelta', model=model)

    set_crossentropy_loss(config=config_crossentropy, model=model)

    parts_of_file_name = config_name.split('.json')

    config_name_adam = f'{parts_of_file_name[0]}_adam.json'
    with open(os.path.join(path, config_name_adam), 'w') as file:
        json.dump(config_adam, file, indent=2)

    config_name_adadelta = f'{parts_of_file_name[0]}_adadelta.json'
    with open(os.path.join(path, config_name_adadelta), 'w') as file:
        json.dump(config_adadelta, file, indent=2)

    config_name_crossentropy = f'{parts_of_file_name[0]}_crossentropy.json'
    with open(os.path.join(path, config_name_crossentropy), 'w') as file:
        json.dump(config_crossentropy, file, indent=2)

    os.remove(os.path.join(path, config_name))


def add_inverse_triples_setting(config: Dict):
    """."""
    config['ablation']['create_inverse_triples'] = [True, False]


def add_embedding_dimension(config: Dict) -> None:
    """."""
    model = config['ablation']['models'][0]
    embedding_dim = dict(
        type='int', low=6, high=8, scale='power_two'
    )
    config['ablation']['model_kwargs_ranges'][model]['embedding_dim'] = embedding_dim

    if 'relation_dim' in config['ablation']['model_kwargs_ranges'][model]:
        config['ablation']['model_kwargs_ranges'][model]['relation_dim'] = embedding_dim


def specify_batch_normalization(config: Dict, model: str):
    """."""
    config['ablation']['model_kwargs'][model]['apply_batch_normalization'] = False


if __name__ == '__main__':

    # iterator = iterate_config_paths(root_directory='reduced_search_space')
    #
    # for model_name_normalized, dataset, hpo_approach, training_assumption, config_name, path in iterator:
    #     model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]
    #     with open(os.path.join(path, config_name), 'r') as file:
    #         try:
    #             config = json.load(file)
    #         except:
    #             raise Exception(f"{config_name} could not be loaded.")
    #     if training_assumption == 'owa' and 'mrl' in config_name:
    #         crossentropy_config = deepcopy(config)
    #         set_crossentropy_loss(config=crossentropy_config, model=model_name)
    #         parts_of_file_name = config_name.split('.json')
    #         config_name_crossentropy = f'{parts_of_file_name[0]}_crossentropy.json'
    #         config_name_crossentropy = re.sub('_mrl', '', config_name_crossentropy)
    #
    #         with open(os.path.join(path, config_name_crossentropy), 'w') as file:
    #             json.dump(crossentropy_config, file, indent=2)

    # iterator = iterate_config_paths(root_directory='reduced_search_space')
    #
    # for model_name_normalized, dataset, hpo_approach, training_assumption, config_name, path in iterator:
    #     model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]
    #     with open(os.path.join(path, config_name), 'r') as file:
    #         try:
    #             config = json.load(file)
    #         except:
    #             raise Exception(f"{config_name} could not be loaded.")
    #     if training_assumption == 'lcwa':
    #         split_lcwa_configs(config=config, path=path, config_name=config_name)

    # exit(0)

    iterator = iterate_config_paths(root_directory='reduced_search_space')

    # for model_name_normalized, dataset, hpo_approach, training_assumption, config_name, path in iterator:
    #     model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]
    #     with open(os.path.join(path, config_name), 'r') as file:
    #         try:
    #             config = json.load(file)
    #         except:
    #             raise Exception(f"{config_name} could not be loaded.")
    #
    #     if 'nssal' in config_name:
    #         if 'NegativeSamplingSelfAdversarialLoss' in config['ablation']['loss_kwargs'][model_name]:
    #             del config['ablation']['loss_kwargs'][model_name]['NegativeSamplingSelfAdversarialLoss']
    #             del config['ablation']['loss_kwargs_ranges'][model_name]['NegativeSamplingSelfAdversarialLoss']
    #     else:
    #         continue
    #
    #     with open(os.path.join(path, config_name), 'w') as file:
    #         json.dump(config, file, indent=2)
    #
    # exit(0)

    # for model_name_normalized, dataset, hpo_approach, training_assumption, config_name, path in iterator:
    #     model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]
    #     with open(os.path.join(path, config_name), 'r') as file:
    #         try:
    #             config = json.load(file)
    #         except:
    #             raise Exception(f"{config_name} could not be loaded.")
    #
    #     if dataset == 'yago310':
    #         if 'adadelta' in config_name or 'adadelta' in config_name:
    #             continue
    #         set_optimizer(config=config, optimizer='adadelta',model=model_name)
    #         with open(os.path.join(path, config_name), 'w') as file:
    #             json.dump(config, file, indent=2)
    #
    #
    #
    # exit(0)

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

        add_inverse_triples_setting(config=config)

        if model_name == 'TuckER':
            specify_batch_normalization(config=config, model=model_name)

        with open(os.path.join(path, config_name), 'w') as file:
            json.dump(config, file, indent=2)
