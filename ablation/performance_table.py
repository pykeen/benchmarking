"""Generate a table of runtime per epoch for each trial of HPO."""
import os
import pathlib

import pandas
from tqdm import tqdm


def main():
    results_directory = pathlib.Path('.', 'results')
    output_directory = pathlib.Path('.', 'runtime')
    output_directory.mkdir(exist_ok=True, parents=True)
    directories = [
        pathlib.Path(directory)
        for directory, _, filenames in os.walk(results_directory)
        if 'study.json' in filenames
    ]

    directories = directories

    all_measurements = []
    all_params = []
    experiments = sorted(directories)
    progress = tqdm(experiments)
    for experiment_id, directory in enumerate(progress):
        progress.set_postfix(dict(part=directory.parts[1:3]))
        optuna_results_db = directory / "optuna_results.db"

        connection = f'sqlite:///{str(optuna_results_db)}'
        user_attributes_df = pandas.read_sql_table(
            table_name='trial_user_attributes',
            con=connection,
        )
        stop_data = user_attributes_df.loc[
            user_attributes_df['key'] == 'stopped_epoch'
            ].groupby(
            by='trial_id'
        ).agg(dict(
            value_json='first',
        )).reset_index().rename(
            columns=dict(
                value_json='stopped_epoch'
            ),
        )
        stop_data['stopped_epoch'] = pandas.to_numeric(stop_data['stopped_epoch'])

        trials_df = pandas.read_sql_table(
            table_name='trials',
            con=connection,
        )
        trials_df = trials_df[trials_df["state"] == "COMPLETE"][["trial_id", "datetime_start", "datetime_complete"]]
        trials_df["trial_time"] = trials_df["datetime_complete"] - trials_df["datetime_start"]
        trials_df = trials_df[["trial_id", "trial_time"]]
        measurement_df = pandas.merge(trials_df, stop_data, on="trial_id")
        measurement_df["epoch_time"] = measurement_df["trial_time"] / measurement_df["stopped_epoch"]
        measurement_df["experiment_id"] = experiment_id
        all_measurements.append(measurement_df[["trial_id", "experiment_id", "epoch_time"]].set_index(["experiment_id", "trial_id"]))

        param_df = pandas.read_sql_table(
            table_name='trial_params',
            con=connection,
        )

        study_df = pandas.read_sql_table(
            table_name='study_user_attributes',
            con=connection,
        )
        study_df = study_df[~study_df["key"].isin(["pykeen_version", "pykeen_git_hash", "metric"])][["key", "value_json"]].rename(columns=dict(key="param_name", value_json="param_value"))
        cat = [param_df[["trial_id", "param_name", "param_value"]]]
        for trial_id in param_df["trial_id"].unique():
            common_param_df = study_df.copy()
            common_param_df["trial_id"] = trial_id
            cat.append(common_param_df)
        param_df = pandas.concat(cat)
        param_df["experiment_id"] = experiment_id

        all_params.append(param_df.set_index(["experiment_id", "trial_id", "param_name"]))

    measurement = pandas.concat(all_measurements).reset_index()
    params = pandas.concat(all_params).reset_index()
    experiments = pandas.DataFrame(data=dict(output_directory=experiments))
    experiments.index.name = 'experiment_id'
    experiments = experiments.reset_index()

    measurement.to_csv(output_directory / 'measurement.tsv', index=False, sep='\t')
    params.to_csv(output_directory / 'params.tsv', index=False, sep='\t')
    experiments.to_csv(output_directory / 'experiments.tsv', index=False, sep='\t')


if __name__ == '__main__':
    main()
