import json

with open('/Users/mali/PycharmProjects/pykeen_experimental_results/try_and_error/config.json') as json_file:
    data = json.load(json_file)
    bs = data['ablation']['evaluation_kwargs']['batch_size']
    print(bs)
    print(bs is None)