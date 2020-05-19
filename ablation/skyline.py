import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from collate import COLLATION_PATH, MODEL, SUMMARY_DIRECTORY

SKYLINE_DIRECTORY = os.path.join(SUMMARY_DIRECTORY, 'sizeplots')
os.makedirs(SKYLINE_DIRECTORY, exist_ok=True)


def main():
    """Collate all HPO results in a single table."""
    df = pd.read_csv(COLLATION_PATH, sep='\t')
    df['model'] = df['model'].map(lambda s: MODEL.get(s, s))
    it = tqdm(
        df.groupby(['dataset', 'optimizer']),
        desc=''
    )
    min_bytes = df['model_bytes'].min()
    max_bytes = df['model_bytes'].max()

    for (dataset, optimizer), sdf in it:
        fig, ax = plt.subplots(figsize=(8, 4))
        g = sns.scatterplot(
            x='model_bytes', y='hits@10', data=sdf,
            alpha=0.75, hue='model', hue_order=sorted(df['model'].unique()),
            ax=ax,
        )
        ax.set_xlim([min_bytes, max_bytes])
        ax.set_ylim([0.0, 1.0])
        g.set(xscale="log")
        g.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
        ax.set_xlabel('Model Size (bytes)')
        ax.set_title(f'{dataset} - {optimizer}')
        plt.tight_layout()
        plt.savefig(os.path.join(SKYLINE_DIRECTORY, f'{dataset}_{optimizer}.png'), dpi=300)
        plt.close(plt.gcf())


if __name__ == '__main__':
    main()
