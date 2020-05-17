import json
import os
from copy import deepcopy
from typing import Dict

from ablation.config.check_correctnes_of_hpo_configs import iterate_config_paths

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
    'structured_embedding': 'StructuredEmbedding',
    'transd': 'TransD',
    'transe': 'TransE',
    'transh': 'TransH',
    'transr': 'TransR',
    'tucker': 'TuckER',
    'unstructured_model': 'UnstructuredModel',
}


def split_configs(config: Dict, path: str, config_name: str):
    """."""
    model = config['ablation']['models'][0]
    config_bce = deepcopy(config)
    config_softplusloss = deepcopy(config)

    config_bce['ablation']['loss_functions'].remove('SoftplusLoss')
    del config_bce['ablation']['loss_kwargs'][model]['SoftplusLoss']
    del config_bce['ablation']['loss_kwargs_ranges'][model]['SoftplusLoss']

    config_softplusloss['ablation']['loss_functions'].remove('BCEAfterSigmoidLoss')
    del config_softplusloss['ablation']['loss_kwargs'][model]['BCEAfterSigmoidLoss']
    del config_softplusloss['ablation']['loss_kwargs_ranges'][model]['BCEAfterSigmoidLoss']

    parts_of_file_name = config_name.split('.json')

    config_name_adam_bce = f'{parts_of_file_name[0]}_bce.json'
    with open(os.path.join(path, config_name_adam_bce), 'w') as file:
        json.dump(config_bce, file, indent=2)

    config_name_adam_softplusloss = f'{parts_of_file_name[0]}_softplusloss.json'
    with open(os.path.join(path, config_name_adam_softplusloss), 'w') as file:
        json.dump(config_softplusloss, file, indent=2)

    os.remove(os.path.join(path, config_name))


def change_early_stopping_setting(config: Dict, training_assumption):
    """."""
    c = config['ablation']['stopper_kwargs']
    c['frequency'] = 10
    if training_assumption == 'owa':
        c['patience'] = 5
    if training_assumption == 'lcwa':
        c['patience'] = 2


def change_batch_size(config: Dict, model: str, training_assumption:str):
    config['ablation']['training_kwargs_ranges'][model][training_assumption]['batch_size']['low'] = 10
    config['ablation']['training_kwargs_ranges'][model][training_assumption]['batch_size']['high'] = 13


def change_neg_samples(config: Dict, model: str):
    config['ablation']['negative_sampler_kwargs_ranges'][model]['BasicNegativeSampler']['num_negs_per_pos']['high'] = 50


if __name__ == '__main__':
    iterator = iterate_config_paths(root_directory='adam')

    for model_name_normalized, dataset, hpo_approach, training_assumption, config_name, path in iterator:
        model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]

        with open(os.path.join(path, config_name), 'r') as file:
            try:
                config = json.load(file)
            except:
                raise Exception(f"{config_name} could not be loaded.")
        if dataset == 'yago310':
            change_early_stopping_setting(config=config, training_assumption=training_assumption)

            with open(os.path.join(path, config_name), 'w') as file:
                json.dump(config, file, indent=2)
