import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from collate import COLLATION_PATH, SUMMARY_DIRECTORY

OUTPUT_PATH = os.path.join(SUMMARY_DIRECTORY, 'size_to_hits.png')


def main():
    """Collate all HPO results in a single table."""
    df = pd.read_csv(COLLATION_PATH, sep='\t')
    p = sns.scatterplot(x='model_bytes', y='hits@10', data=df, alpha=0.15)
    p.set(xscale="log")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)


if __name__ == '__main__':
    main()
