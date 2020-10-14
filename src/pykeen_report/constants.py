from pykeen.datasets import datasets
from pykeen.models import models

MODEL = {
    'unstructuredmodel': 'UM',
    'structuredembedding': 'SE',
}
for model_key, model_cls in models.items():
    if model_key not in MODEL:
        MODEL[model_key] = model_cls.__name__

DATASETS = {
    dataset_key: dataset_cls.__name__
    for dataset_key, dataset_cls in datasets.items()
}

LOSS = {
    'marginranking': 'MRL',
    'crossentropy': 'CEL',
    'bceaftersigmoid': 'BCEL',
    'softplus': 'SPL',
    'nssa': 'NSSAL',
}

TRAINING_LOOP = {
    'owa': 'sLCWA',
    'lcwa': 'LCWA',
}

REGULARIZER = {
    'no': 'No Reg.',
    'transh': 'No Reg.',
}

NEGATIVE_SAMPELR = {
    'basic': 'Basic',
}

GETTERS = {
    'hits@10': lambda metrics: metrics['hits_at_k']['avg']['10'],
}

ABLATION_HEADERS = [
    'dataset',
    'model',
    'loss',
    'optimizer',
    'training_approach',
    'inverse_relations',
]

BINARY_ABLATION_HEADERS = {
    'inverse_relations',
    'training_approach',
}

MODEL_BYTES = 'model_bytes'
