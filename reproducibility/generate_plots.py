# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import seaborn as sns

from pykeen.datasets import datasets
from utils import get_df

HERE = os.path.abspath(os.path.dirname(__file__))
PLOTS_DIRECTORY = os.path.join(HERE, 'plots')
os.makedirs(PLOTS_DIRECTORY, exist_ok=True)

sns.set_style('whitegrid')


def make_dataset_plots(m: str = 'metrics.hits_at_k.avg.10'):
    u = {
        m: ('hits_at_10', 'Hits@10', {}),
        'times.training': ('time', 'Time (s)', {'xscale': 'log'}),
    }

    df = get_df()
    df['dataset'] = df['dataset'].map(lambda s: datasets[s].__name__)

    for x, (op, label, setters) in u.items():
        g = sns.catplot(
            x=x,
            y='model',
            data=df,
            col='dataset',
            col_wrap=2,
            kind='bar',
            order=sorted(df['model'].unique()),
        )
        g.set_titles(template='{col_name}', size=20)
        g.set_ylabels('')
        g.set_xlabels(label)
        g.set(**setters)
        g.fig.tight_layout()
        g.savefig(os.path.join(PLOTS_DIRECTORY, f'overview_{op}.pdf'))
        g.savefig(os.path.join(PLOTS_DIRECTORY, f'overview_{op}.png'), dpi=300)
        plt.close(g.fig)

    g = sns.FacetGrid(
        data=df,
        col='dataset',
        col_wrap=2,
        hue='model',
        hue_order=sorted(df['model'].unique()),
        legend_out=True,
    )
    g.map(sns.scatterplot, 'times.training', m, alpha=0.5)
    g.set_titles(template='{col_name}')
    g.set(xscale='log', xlabel='Time (s)', ylabel='Hits@10')
    g.fig.tight_layout()
    g.savefig(os.path.join(PLOTS_DIRECTORY, f'overview_scatter.pdf'))
    g.savefig(os.path.join(PLOTS_DIRECTORY, f'overview_scatter.png'), dpi=300)
    plt.close(g.fig)


if __name__ == '__main__':
    make_dataset_plots()
