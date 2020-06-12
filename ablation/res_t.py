
import os
import json
from tqdm import tqdm
HERE = os.path.dirname(__file__)
RESULTS = os.path.join(HERE, 'results')

directories = [
        (directory, filenames)
        for directory, _, filenames in os.walk(RESULTS)
        if 'study.json' in filenames
    ]

for directory, filenames in tqdm(directories):
    if 'hpo_config.json' not in filenames:
        continue
    hpo_config_path = os.path.join(directory, 'hpo_config.json')
    with open(hpo_config_path, 'r') as file:
        config = json.load(file)

    if config['pipeline']['dataset'].lower() == 'wn18rr' and config['pipeline']['optimizer'].lower() =='adadelta':
        print(hpo_config_path)
        exit(0)

    with open(os.path.join(directory, 'best_pipeline', 'pipeline_config.json')) as file:
        ppc = json.load(file)

    if ppc['pipeline']['model'].lower() == 'ermlp':
        print(ppc)
    if ppc['pipeline']['dataset'].lower() == 'wn18rr' and ppc['pipeline']['optimizer'].lower() =='adadelta':
        print("problem")
        exit(0)

