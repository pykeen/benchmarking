import json
import logging
import os

import numpy as np
from pykeen.models import models

HERE = os.path.dirname(__file__)
RESULTS = os.path.join(HERE, 'results')
SUMMARY_DIRECTORY = os.path.join(HERE, 'summary')
os.makedirs(SUMMARY_DIRECTORY, exist_ok=True)

logger = logging.getLogger(__name__)

GETTERS = {
    'hits@10': lambda metrics: metrics['hits_at_k']['avg']['10']
}


def _iter_model_dirs():
    for model in os.listdir(RESULTS):
        if model.startswith('_') or model.endswith('.py') or not os.path.isdir(os.path.join(RESULTS, model)):
            continue
        if model not in models:
            raise KeyError(f'invalid model name: {model}')
        assert model in models, f'{model} not found'
        yield model, os.path.join(RESULTS, model)


def _iter_dataset_dirs():
    for model, d in _iter_model_dirs():
        for dataset in os.listdir(d):
            dataset_d = os.path.join(d, dataset)
            if not os.path.isdir(dataset_d):
                continue
            yield model, dataset, dataset_d

def add_inverse_triples_info():
    for model, dataset, d in _iter_dataset_dirs():
        for searcher in os.listdir(d):
            searcher_d = os.path.join(d, searcher)
            if not os.path.isdir(searcher_d):
                continue
            for ablation in os.listdir(searcher_d):
                ablation_d = os.path.join(searcher_d, ablation)
                if not os.path.isdir(ablation_d):
                    continue
                for hpo in os.listdir(ablation_d):
                    hpo_d = os.path.join(ablation_d, hpo)
                    if not os.path.isdir(hpo_d):
                        continue

                    study_path = os.path.join(hpo_d, 'study.json')
                    if not os.path.exists(study_path):
                        logger.warning(f'missing study path: {hpo_d}')
                        continue

                    with open(study_path) as file:
                        study = json.load(file)

                    hpo_config_path = os.path.join(hpo_d, 'hpo_config.json')
                    if not os.path.exists(hpo_config_path):
                        logger.warning(f'missing hpo config path: {hpo_config_path}')
                        continue

                    with open(hpo_config_path) as file:
                        hpo_config = json.load(file)
                    try:
                        add_inverse_triples = hpo_config['pipeline']['dataset_kwargs']['create_inverse_triples']
                    except:
                        raise Exception(f'create_inverse_triples not in hpo config {hpo_config_path}')
                    study['create_inverse_triples'] = add_inverse_triples

                    with open(os.path.join(study_path), 'w') as file:
                        json.dump(study, file, indent=2)


def main():
    key = 'hits@10'
    add_inverse_triples_info()


if __name__ == '__main__':
    main()
