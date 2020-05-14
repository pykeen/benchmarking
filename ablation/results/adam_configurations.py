import os
from typing import Iterable

HERE = os.path.abspath(os.path.dirname(__file__))
import json

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

MODEL_NAME_TO_DIRECTORIES = {val: key for key, val in MODEL_DIRECTORIES_TO_MODEL_NAME.items()}

DATASET_NAMES = ['fb15k237', 'kinships', 'wn18rr', 'yago310', 'examples']


def iterate_config_paths() -> Iterable[str]:
    """Iterate over all configuration paths."""
    root_directory = HERE
    for model in os.listdir(root_directory):
        # Check, whether model is valid
        if model.startswith('.'):
            continue

        # assert model in MODEL_DIRECTORIES_TO_MODEL_NAME, f'Model {model} is unknown'
        model_directory = os.path.join(root_directory, model)

        if model_directory.endswith('.py'):
            continue
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

            for training_assumption in training_assumptions:
                configs_directory = os.path.join(
                    root_directory,
                    model_directory,
                    dataset,
                    hpo_approach[0],
                    training_assumption,
                )
                configs = os.listdir(configs_directory)

                for config in configs:
                    yield model, dataset, hpo_approach, training_assumption, config, configs_directory


def remove_adadelta_configurations(root, config, config_name, model_name_normalized):
    """."""
    ADADELTA = 'adadelta'
    if ADADELTA in config_name.lower():
        os.remove(os.path.join(root, config_name))

    optimizers = config['ablation']['optimizers']
    if ADADELTA in optimizers:
        config['ablation']['optimizers'].remove(ADADELTA)
        del config['ablation']['optimizer_kwargs'][
            MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]][ADADELTA]

        del config['ablation']['optimizer_kwargs_ranges'][
            MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]][ADADELTA]


if __name__ == '__main__':
    iterator = iterate_config_paths()

    for model_name_normalized, dataset, hpo_approach, training_assumption, config_name, path in iterator:
        model_name = MODEL_DIRECTORIES_TO_MODEL_NAME[model_name_normalized]
        with open(os.path.join(path, config_name), 'r') as file:
            try:
                config = json.load(file)
            except:
                raise Exception(f"{config_name} could not be loaded.")

        remove_adadelta_configurations(
            root=path,
            config=config,
            config_name=config_name,
            model_name_normalized=model_name_normalized,
        )

        if 'adadelta' in config_name:
            continue
        with open(os.path.join(path, config_name), 'w') as file:
            json.dump(config, file, indent=2)
