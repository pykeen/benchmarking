import logging
import os
import random
import time

import click
import numpy as np
import seaborn as sns

from collate import COLLATION_PATH, HERE, SUMMARY_DIRECTORY, collate, read_collation
from pykeen_report import plot as pkp

logger = logging.getLogger(__name__)


def make_plots(
    *,
    target_header: str,
    make_png: bool = True,
    make_pdf: bool = True,
):
    """Collate all HPO results in a single table."""
    df = read_collation()

    for k in ['searcher', 'evaluator']:
        if k in df.columns:
            del df[k]

    sns.set_style("whitegrid")
    summary_1d_directory = os.path.join(SUMMARY_DIRECTORY, '1D-slices')
    os.makedirs(summary_1d_directory, exist_ok=True)
    pkp.write_1d_sliced_summaries(
        df=df, target_header=target_header, output_directory=summary_1d_directory,
        make_pdf=make_pdf, make_png=make_png,
    )
    with open(os.path.join(HERE, 'README.md'), 'w') as file:
        print(f'# Ablation Results\n', file=file)
        print(f'Output at {time.asctime()}\n', file=file)
        for v in sorted(df['dataset'].unique()):
            print(f'<img src="summary/1D-slices/dataset_{v}.png" alt="{v}"/>\n', file=file)

    sns.set_style("darkgrid")
    dataset_optimizer_directory = os.path.join(SUMMARY_DIRECTORY, 'dataset_optimizer_model_summary')
    os.makedirs(dataset_optimizer_directory, exist_ok=True)
    pkp.write_dataset_optimizer_model_summaries(
        df=df, target_header=target_header, output_directory=dataset_optimizer_directory,
        make_pdf=make_pdf, make_png=make_png,
    )
    pkp.write_1d_sliced_summaries_stratified(
        df=df, target_header=target_header, output_directory=SUMMARY_DIRECTORY,
        make_pdf=make_pdf, make_png=make_png,
    )
    pkp.write_2d_summaries(
        df=df, target_header=target_header, output_directory=SUMMARY_DIRECTORY,
        make_pdf=make_pdf, make_png=make_png,
    )

    sizeplot_dir = os.path.join(SUMMARY_DIRECTORY, 'sizeplots')
    os.makedirs(sizeplot_dir, exist_ok=True)
    pkp.make_sizeplots_trellised(
        df=df, target_header=target_header, output_directory=sizeplot_dir,
        make_pdf=make_pdf, make_png=make_png,
    )


@click.command()
def main():
    key = 'hits@10'
    if not os.path.exists(COLLATION_PATH):
        collate(key)
    # Plotting should be deterministic
    np.random.seed(5)
    random.seed(5)
    make_plots(target_header=key)
    click.echo('done!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
