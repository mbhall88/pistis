# -*- coding: utf-8 -*-

"""Main module."""
from __future__ import division
import pyfastaq
import os
import seaborn as sns
from pistis import utils, plots
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
SEABORN_STYLE = 'whitegrid'
REQUIRED_EXT = '.pdf'


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('fastq', nargs=1,
                type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option('--output', '-o',
              type=click.Path(dir_okay=True, resolve_path=True),
              help="Filepath to save the plot PDF as. If name is not specified,"
                   " will use the name of the fastq file with .pdf extension.")
@click.option('--kind', '-k', default='kde',
              type=click.Choice(['kde', 'scatter', 'hex']),
              help="The kind of representation to use for the jointplot of "
                   "quality score vs read length. Suggested kinds are 'scatter', "
                   "'kde' (default), or 'hex'. For examples of these refer to "
                   "https://seaborn.pydata.org/generated/seaborn.jointplot.html")
@click.option('--log_length/--no_log_length', default=True,
              help="Plot the read length as a log10 transformation on the "
                   "quality vs read length plot")
def main(fastq, output, kind, log_length):
    """A package for sanity checking (quality control) your long read data.
        Feed it a fastq file and in return you will receive a PDF with four plots:\n
            1. GC content histogram with distribution curve for sample.\n
            2. Jointplot showing the read length vs. phred quality score for each
            read. The interior representation of this plot can be altered with the
            --kind option.\n
            3. Violin plot of the phred quality score at positional bins across all reads. The reads are binned into read positions 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11-20, 21-50, 51-100, 101-200, 201-300, 301-1000, 1001-10000, and >10000. Plots from the start to the end of reads.\n
            4. Same as 3, but plots from the end of the read to the start.\n

    FASTQ: Fastq file to plot. This can be gzipped.
    """
    sns.set(style=SEABORN_STYLE)

    # read in the fastq file to a generator object
    fastq_file = pyfastaq.sequences.file_reader(fastq, read_quals=True)

    # collect the data needed for plotting
    (gc_content,
     read_lengths,
     mean_quality_scores,
     df_start,
     df_end) = utils.collect_fastq_data(fastq_file)

    # if the specified output is a directory, default pdf name is fastq name.
    if os.path.isdir(output):
        # get the basename of the fastq file and add pdf extension
        basename = os.path.splitext(os.path.basename(fastq))[0]
        filename = basename + REQUIRED_EXT
        save_as = os.path.join(output, filename)
    else:  # if file name is provided in output, make sure it has correct ext.
        extension = os.path.splitext(output)
        if extension.lower() != REQUIRED_EXT:
            save_as = output + REQUIRED_EXT
        else:
            save_as = output

    # generate plots and save
    plot1 = plots.gc_plot(gc_content)
    plot2 = plots.length_vs_qual_plot(read_lengths, mean_quality_scores,
                                      log_length=log_length, kind=kind)
    plot3 = plots.quality_per_position(df_start, 'start')
    plot4 = plots.quality_per_position(df_end, 'end')
    plots.save_plots_to_pdf([plot1, plot2, plot3, plot4], save_as)

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
