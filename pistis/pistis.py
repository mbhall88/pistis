"""Main module. This module creates the command line interface for `pistis` and
coordinates reading in data, running functions from the `utils` module to
parse the data into the form required by the `plots` module. It then plots this
data and writes it to a PDF report."""
from __future__ import division
from __future__ import absolute_import
import os
import pysam
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import click
from pistis import utils, plots

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
SEABORN_STYLE = 'whitegrid'
REQUIRED_EXT = '.pdf'


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--fastq', '-f',
              type=click.Path(exists=True, dir_okay=False,
                              resolve_path=True),
              help="Fastq file to plot. This can be gzipped.")
@click.option('--output', '-o', default='.',
              type=click.Path(dir_okay=True, resolve_path=True,
                              writable=True),
              help="Path to save the plot PDF as. If name is not specified,"
                   " will use the name of the fastq (or bam) file with .pdf "
                   "extension.")
@click.option('--kind', '-k', default='scatter',
              type=click.Choice(['kde', 'scatter', 'hex']),
              help="The kind of representation to use for the jointplot of "
                   "quality score vs read length. Accepted kinds are 'scatter'"
                   "(default), 'kde', or 'hex'. For examples refer to "
                   "https://seaborn.pydata.org/generated/seaborn.jointplot.html")
@click.option('--log_length/--no_log_length', default=True,
              help="Plot the read length as a log10 transformation on the "
                   "quality vs read length plot")
@click.option('--bam', '-b',
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              help="SAM/BAM file to produce read percent identity histogram "
                   "from.")
def main(fastq, output, kind, log_length, bam):
    """A package for sanity checking (quality control) your long read data.
        Feed it a fastq file and in return you will receive a PDF with four plots:\n
            1. GC content histogram with distribution curve for sample.\n
            2. Jointplot showing the read length vs. phred quality score for each
            read. The interior representation of this plot can be altered with the
            --kind option.\n
            3. Violin plot of the phred quality score at positional bins across all reads. The reads are binned into read positions 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11-20, 21-50, 51-100, 101-200, 201-300, 301-1000, 1001-10000, and >10000. Plots from the start to the end of reads.\n
            4. Same as 3, but plots from the end of the read to the start.\n
    Additionally, if you provide a BAM/SAM file a histogram of the read percent
    identity will be added to the report.
    """
    if not any([fastq, bam]):
        raise click.MissingParameter("Either --fastq, --bam or both must be "
                                     "given as arguments.")
    sns.set(style=SEABORN_STYLE)

    # if the specified output is a directory, default pdf name is fastq name.
    if os.path.isdir(output):
        # get the basename of the fastq file and add pdf extension
        basename, ext = os.path.splitext(os.path.basename(fastq or bam))
        # if file is gzipped, need to also strip fastq extension
        if ext == '.gz':
            basename = os.path.splitext(os.path.basename(basename))[0]

        filename = basename + REQUIRED_EXT
        save_as = os.path.join(output, filename)
    else:  # if file name is provided in output, make sure it has correct ext.
        extension = os.path.splitext(output)[-1]
        if extension.lower() != REQUIRED_EXT:
            save_as = output + REQUIRED_EXT
        else:
            save_as = output

    plots_for_report = []
    if fastq:
        with pysam.FastxFile(fastq) as fastq_file:
            # collect the data needed for plotting
            (gc_content,
             read_lengths,
             mean_quality_scores,
             bins_from_start,
             bins_from_end) = utils.collect_fastq_data(fastq_file)

        # generate plots
        plots_for_report.extend([
            plots.gc_plot(gc_content),
            plots.length_vs_qual_plot(read_lengths, mean_quality_scores,
                                      log_length=log_length, kind=kind),
            plots.quality_per_position(bins_from_start, 'start'),
            plots.quality_per_position(bins_from_end, 'end')
        ])
    if bam:
        # generate read percent identity plot
        perc_identities = utils.sam_percent_identity(bam)
        plots_for_report.append(plots.percent_identity(perc_identities))

    plots.save_plots_to_pdf(plots_for_report, save_as)

    return 0


main.__annotations__ = {'fastq': click.Path,
                        'output': click.Path,
                        'kind': str,
                        'log_length': bool,
                        'return': int}

if __name__ == "__main__":
    import sys

    sys.exit(main())
