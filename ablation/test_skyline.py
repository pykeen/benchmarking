from collate import read_collation

from pykeen_report.plot import make_sizeplots_trellised

if __name__ == '__main__':
    df = read_collation()

    make_sizeplots_trellised(
        df=df,
        target_x_header='model_bytes',
        target_y_header='hits@10',
        output_directory='/tmp/plot_tmp',
    )
