# -*- coding: utf-8 -*-

"""Main module."""
from __future__ import division
import glob
import os
import argparse
import pyfastaq
import seaborn as sns
import utils, plots


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "fastq",
        help="Fastq file to generate plots for. Can be gzipped.",
        type=str)

    parser.add_argument(
        "-o", "--output",
        help="Where to save PDF of plots.",
        type=str,
        default=os.curdir)

    parser.add_argument(
        "--no_log_length",
        action='store_true',
        help="Plot length - on quality vs. read length plot - without log10 "
             "transformation.")

    return parser.parse_args()











def main():
    sns.set(style='whitegrid')
    fname = glob.glob('../../nanotest/*.fastq.gz')[0]
    fastq = pyfastaq.sequences.file_reader(fname, read_quals=True)
    (gc_content,
     read_lengths,
     mean_quality_scores,
     df_start, df_end) = utils.collect_fastq_data(fastq)

    save_as = 'foo.pdf'

    plot1 = plots.gc_plot(gc_content)
    plot2 = plots.length_vs_qual_plot(read_lengths, mean_quality_scores)
    plot3 = plots.quality_per_position(df_start, 'start')
    plot4 = plots.quality_per_position(df_end, 'end')
    plots.save_plots_to_pdf([plot1, plot2, plot3, plot4], save_as)



