# -*- coding: utf-8 -*-

import logging
import os
import random
from collections import Counter
from typing import Optional

import click
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from collate import COLLATION_PATH, SUMMARY_DIRECTORY, collate, read_collation
from pykeen_report import plot as pkp
from pykeen_report.constants import MODEL_BYTES

sns.set(font_scale=2, style='whitegrid')


def make_plots(
    *,
    df: Optional[pd.DataFrame] = None,
    target_header: str,
    output_directory: str,
    make_pngs: bool = True,
    make_pdfs: bool = True,
):
    if df is None:
        df = read_collation()
    del df['training_time']
    del df['evaluation_time']
    del df['model_bytes']
    del df['searcher']  # always same
    loss_loops = set(map(tuple, df[['loss', 'training_approach']].values))
    loss_loops_counter = Counter(loss for loss, _ in loss_loops)
    loss_mult = {loss for loss, count in loss_loops_counter.items() if count > 1}
    df['loss_training_approach'] = [
        (
            f'{loss} ({training_approach})'
            if loss in loss_mult
            else loss
        )
        for loss, training_approach in df[['loss', 'training_approach']].values
    ]

    it = tqdm(df.groupby(['dataset', 'optimizer']), desc='Making dataset/optimizer figures')
    for (dataset, optimizer), sub_df in it:
        it.write(f'creating trellised barplots: dataset/optimizer ({dataset}/{optimizer})')
        pkp.write_experimental_heatmap(
            df=sub_df,
            dataset=dataset,
            optimizer=optimizer,
            target_header=target_header,
            output_directory=output_directory,
            name=f'{dataset}_{optimizer}_heat',
        )
        pkp.write_dataset_optimizer_barplots(
            df=sub_df,
            dataset=dataset,
            optimizer=optimizer,
            target_header=target_header,
            output_directory=output_directory,
            name=f'{dataset}_{optimizer}',
            make_pngs=make_pngs,
            make_pdfs=make_pdfs,
        )

        # Loss / Model / (Training Loop Chart | Inverse)
        for hue in ('training_approach', 'inverse_relations'):
            it.write(f'creating barplot: loss/model/{hue} barplot')
            pkp.make_loss_plot_barplot(
                df=sub_df,
                target_header=target_header,
                hue=hue,
                output_directory=output_directory,
                dataset=dataset,
                name=f'{dataset}_{optimizer}_model_loss_{hue}',
                make_pngs=make_pngs,
                make_pdfs=make_pdfs,
            )

        y, col, hue = 'loss', 'model', 'training_approach',
        it.write(f'creating barplot: {y}/{col}/{hue}')
        pkp.plot_3d_barplot(
            df=sub_df,
            dataset=dataset,
            optimizer=optimizer,
            y=y,
            hue=hue,
            col=col,
            target_header=target_header,
            slice_dir=output_directory,
            name=f'{dataset}_{optimizer}_{y}_{col}_{hue}',
            make_pngs=make_pngs,
            make_pdfs=make_pdfs,
        )

        gkey = [c for c in sub_df.columns if c not in {target_header, 'replicate'}]
        gdf = sub_df.groupby(gkey)[target_header].median().reset_index()

        # 2-way plots
        for y, hue in [
            ('loss_training_approach', 'inverse_relations'),
            ('loss', 'inverse_relations'),
            ('loss', 'training_approach'),
            ('training_approach', 'inverse_relations'),
        ]:
            it.write(f'creating barplot: {y}/{hue} aggregated')
            # Aggregated
            pkp.make_2way_boxplot(
                df=gdf,
                target_header=target_header,
                y=y,
                hue=hue,
                slice_dir=output_directory,
                dataset=dataset,
                name=f'{dataset}_{optimizer}_{y}_{hue}_agg',
                make_pngs=make_pngs,
                make_pdfs=make_pdfs,
            )

            it.write(f'creating barplot: {y}/{hue}')
            pkp.make_2way_boxplot(
                df=sub_df,
                target_header=target_header,
                y=y,
                hue=hue,
                slice_dir=output_directory,
                dataset=dataset,
                name=f'{dataset}_{optimizer}_{y}_{hue}',
                make_pngs=make_pngs,
                make_pdfs=make_pdfs,
            )

    it = tqdm(df.groupby('dataset'), desc=f'Making 1D slice plots for dataset')
    for dataset, sub_df in it:
        it.write(f'creating summary chart for {dataset}')
        pkp.make_summary_chart(
            df=sub_df,
            target_header=target_header,
            slice_dir=output_directory,
            dataset=dataset,
            make_pngs=make_pngs,
            make_pdfs=make_pdfs,
            name=dataset,
        )

        gkey = [c for c in sub_df.columns if c not in {target_header, 'replicate'}]
        gdf = sub_df.groupby(gkey)[target_header].median().reset_index()

        it.write(f'creating summary chart for {dataset} (aggregated)')
        pkp.make_summary_chart(
            df=gdf,
            target_header=target_header,
            slice_dir=output_directory,
            dataset=dataset,
            make_pngs=make_pngs,
            make_pdfs=make_pdfs,
            name=f'{dataset}_agg',
        )


def make_sizeplots(
    *,
    output_directory: str,
    target_y_header: str,
    make_pngs: bool = True,
    make_pdf: bool = True,
) -> None:
    df = read_collation()
    sns.set(style='whitegrid')
    for target_x_header in (MODEL_BYTES, 'training_time'):
        pkp.make_sizeplots_trellised(
            df=df, target_x_header=target_x_header, target_y_header=target_y_header,
            output_directory=output_directory,
            make_png=make_pngs,
            make_pdf=make_pdf,
            name=f'trellis_scatter_{target_x_header}',
        )


@click.command()
def main():
    key = 'hits@10'
    if not os.path.exists(COLLATION_PATH):
        collate(key)
    # Plotting should be deterministic
    np.random.seed(5)
    random.seed(5)

    output_directory = os.path.join(SUMMARY_DIRECTORY, 'paper')
    os.makedirs(output_directory, exist_ok=True)

    make_plots(target_header=key, output_directory=output_directory)
    make_sizeplots(output_directory=output_directory, target_y_header=key)
    click.echo('done!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
