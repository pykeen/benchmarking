# coding=utf-8
import json
import pathlib
from typing import Mapping, Optional

import pandas


def to_dot(d: Mapping, prefix: Optional[str] = None, sep: str = '.') -> Mapping[str, float]:
    result = {}
    for k, v in d.items():
        if prefix is not None:
            k = prefix + sep + k
        if isinstance(v, dict):
            result.update(to_dot(v, prefix=k))
        else:
            result[k] = v
    return result


if __name__ == '__main__':
    root = pathlib.Path(__file__).parent / 'results'
    data = []
    for run_label in root.iterdir():
        exp_name = run_label.name.split('_', maxsplit=1)[1]
        replicates_path = run_label / 'replicates'
        for i_replicate, replicate in enumerate(sorted(replicates_path.iterdir())):
            result_path = replicate / 'results.json'
            with result_path.open() as rf:
                result = to_dot(json.load(rf))
                result['experiment'] = exp_name
                result['i_replicate'] = i_replicate
                del result['losses']
                data.append(result)
    df = pandas.DataFrame(data=data)
    agg_cols = [col for col in df.columns if col.startswith('metrics') or col.startswith('times')]
    f_agg = {
        col: ['mean', 'std']
        for col in agg_cols
    }
    agg = df.groupby(by='experiment').agg(f_agg)
    for col in agg_cols:
        if '.mean_rank.' in col or col.startswith('times'):
            fmt = '{0:5.2f}'
            factor = 1
        else:
            fmt = '{0:.2f}'
            factor = 100
        agg[(col, 'mean_std')] = (factor * agg[(col, 'mean')]).apply(fmt.format) + '±' + (factor * agg[(col, 'std')]).apply(fmt.format)
    agg = agg.swapaxes(0, 1).swaplevel(0, 1).loc['mean_std'].swapaxes(0, 1)
    for dataset in ['fb15k', 'wn18']:
        selection = agg.loc[agg.index.str.endswith(dataset)].copy()
        selection.index = selection.index.str.replace('_' + dataset, '')
        print(dataset)
        print(selection.to_latex())
