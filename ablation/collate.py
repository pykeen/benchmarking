import logging
import os
from typing import Collection, Optional

import click
import pandas as pd

import pykeen_report.utils

HERE = os.path.dirname(__file__)
RESULTS = os.path.join(HERE, 'results')
SUMMARY_DIRECTORY = os.path.join(HERE, 'summary')
os.makedirs(SUMMARY_DIRECTORY, exist_ok=True)

# Shut up about mapping triples, lol
logging.getLogger('pykeen.triples.triples_factory').setLevel(logging.ERROR)

COLLATION_PATH = os.path.join(SUMMARY_DIRECTORY, 'results.tsv')
CHECKLIST_TSV_PATH = os.path.join(SUMMARY_DIRECTORY, 'checklist.tsv')
CHECKLIST_LATEX_PATH = os.path.join(SUMMARY_DIRECTORY, 'checklist.tex')


def read_collation() -> pd.DataFrame:
    """Read the collated benchmarking results."""
    return pykeen_report.utils.read_ablation_collation(COLLATION_PATH)


def collate(key: str = 'hits@10', additional_metrics: Optional[Collection[str]] = None) -> pd.DataFrame:
    """Collate all results for a given metric."""
    return pykeen_report.utils.collate_ablation(
        results_directory=RESULTS,
        output_path=COLLATION_PATH,
        key=key,
        additional_metrics=additional_metrics,
    )


@click.command()
def main():
    """Collate the hits@10 metrics and output."""
    df = collate()
    pykeen_report.utils.make_checklist_df(
        df=df,
        output_csv_path=CHECKLIST_TSV_PATH,
        output_latex_path=CHECKLIST_LATEX_PATH,
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
