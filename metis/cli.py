# -*- coding: utf-8 -*-

"""Console script for metis."""

import click


@click.command()
@click.argument('fastq',
                help="Fastq file to plot. This can be gzipped.")
@click.option('--output', '-o',
              help="Filepath to save the plot PDF as.")
def main(fastq, output):
    """A package for sanity checking (quality control) your long read data.
    Feed it a fastq file and in return you will receive a PDF with four plots:
        1. GC content histogram with distribution curve for sample.
        2. Jointplot showing the read length vs. phred quality score for each
        read. The interior representation of this plot can be altered with the
        --kind option.
        3. Violin plot of the phred quality score at positional bins across all
        reads. The reads are binned into read positions 1, 2, 3, 4, 5, 6, 7, 8,
        9, 10, 11-20, 21-50, 51-100, 101-200, 201-300, 301-1000, 1001-10000, and
        >10000. Plots from the start to the end of reads.
        4. Same as 3, but plots from the end of the read to the start.
    """
    click.Path(exists=True, file_okay=True, dir_okay=True, resolve_path=True)
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
