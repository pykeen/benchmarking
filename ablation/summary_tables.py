"""Generate the summary."""

import pandas as pd
from tabulate import tabulate

from collate import collate_hpo_experiments, read_collation


def main():
    hpo_df = collate_hpo_experiments()
    elapsed = pd.to_datetime(hpo_df['datetime_complete']) - pd.to_datetime(hpo_df['datetime_start'])
    total_elapsed = elapsed.sum()
    total_hours = round(total_elapsed / pd.Timedelta('1 hour'))

    best_replicates_df = read_collation()

    total_training_time = best_replicates_df['training_time'].sum()
    total_evaluation_time = best_replicates_df['evaluation_time'].sum()
    total_replicates_time = pd.Timedelta(seconds=total_training_time + total_evaluation_time)
    replicates_hours = round(total_replicates_time / pd.Timedelta('1 hour'))

    columns = [
        'searcher', 'dataset',
        'inverse_relations',
        'model', 'loss', 'regularizer', 'optimizer', 'training_approach',
        'negative_sampler',
    ]
    configurations = len(best_replicates_df[columns].drop_duplicates().index)

    sdf = best_replicates_df[columns].nunique().reset_index()

    rows = [
        (k.replace('_', ' ').title() + 's', v)
        for k, v in sdf.values
        if v > 1 and k != 'inverse_relations'
    ]

    rows.extend([
        ('HPO Configurations', configurations),
        ('HPO Experiments', len(hpo_df.index)),
        ('HPO Compute Hours', total_hours),
        ('Replicate Experiments', len(best_replicates_df.index)),
        ('Replicate Compute Hours', replicates_hours),
    ])
    print(tabulate(rows, headers=['header', 'count'], tablefmt='github'))


if __name__ == '__main__':
    main()
