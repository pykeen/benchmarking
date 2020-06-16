"""Generate the summary."""

import pandas as pd
from tabulate import tabulate

from collate import HPO_RUNS_RESULTS_PATH, read_collation


def main():
    hpo_df = pd.read_csv(HPO_RUNS_RESULTS_PATH, sep='\t')
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
        # 'create_inverse_triples',
        'model', 'loss', 'regularizer', 'optimizer', 'training_loop',
        'negative_sampler',
    ]
    configurations = len(best_replicates_df[columns].drop_duplicates().index)

    sdf = best_replicates_df[columns].nunique().reset_index()

    rows = [
        (k.replace('_', ' ').title() + 's', v)
        for k, v in sdf.values
        if v > 1
    ]

    rows.extend([
        ('Replicates Compute Hours', replicates_hours),
        ('HPO Compute Hours', total_hours),
        ('Configurations', configurations),
        ('Experiments', len(best_replicates_df.index)),
    ])
    print(tabulate(rows, headers=['header', 'count'], tablefmt='github'))


if __name__ == '__main__':
    main()
