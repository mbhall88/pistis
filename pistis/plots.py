import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from typing import List

DPI = 300  # resolution for plots
FIGURE_SIZE = (11.7, 8.27)  # A4 size


def gc_plot(gc_content: List[float]) -> plt.Figure:
    """Generate a histogram with density curve over it for GC content of sample.

    Args:
        gc_content: A list of GC content for each read.

    Returns:
        A matplotlib figure object containing the plot.

    """
    bins = 100
    xlabel = 'GC content'
    ylabel = 'Number of reads'
    title = 'GC content of each read'
    # set the x-axis limits based on whether data is decimal or percentage
    xlim = (0, 100) if any(x > 1 for x in gc_content) else (0, 1.0)

    fig, axes = plt.subplots(dpi=DPI, figsize=FIGURE_SIZE)
    plot = sns.distplot(gc_content, bins=bins, ax=axes)
    plot.set(xlabel=xlabel, ylabel=ylabel, title=title, xlim=xlim)

    # remove top and right border of plot
    sns.despine()

    return fig


def length_vs_qual_plot(lengths: List[int], quality_scores: List[float],
                        kind='kde', log_length=True) -> plt.Figure:
    """Generates a plot of the read length against quality score for each read.

    Args:
        lengths: A list with each element being the length of a read.
        quality_scores: A list with each element being the mean Phred quality
        score for a read.
        kind: The way the points are represented on the plot. The default (kde)
        is a kernel density estimate. Other options include hex bins, or
        single points ('hex' and 'scatter' respectively).
        log_length: Plot the length as a logarithm (base 10).

    Returns:
        A matplotlib figure object containing the plot.
    """
    # use slightly different plot styling for this plot compared to the others
    with sns.axes_style('whitegrid',
                        rc={"grid.linewidth": 0.5, 'grid.linestyle': '--'}):
        xlabel = 'Read Length (bp)'
        ylabel = 'Phred quality score'
        size = (8, 8)  # if you use A4 the axes seem to run off the PDF

        # jointplot require numpy array
        x_data = np.array(lengths)
        y_data = np.array(quality_scores)

        if log_length:
            x_data = np.log10(x_data)

        p = sns.jointplot(x=x_data, y=y_data, kind=kind, space=0, size=3)
        p.set_axis_labels(xlabel=xlabel, ylabel=ylabel)

        if log_length:  # format x-axis labels and ticks for log data
            log_ticks = [500, 1e3, 3e3, 5e3, 1e4, 3e4, 5e4, 1e5, 3e5, 5e5, 1e6,
                         1.5e6]
            p.ax_joint.set_xticks(np.log10(log_ticks))
            p.ax_joint.set_xticklabels(map(int, log_ticks), rotation=270)

        p.fig.set(dpi=DPI, size_inches=size)

    return p.fig


def quality_per_position(data: pd.DataFrame, from_end='start') -> plt.Figure:
    """Generate a violin plot of quality scores across positions in all reads.
    Each violin in the plot corresponds to a 'bin'. That is, all quality scores
    at that position (or positions if it is a range) across all reads.

    Args:
        data: A Pandas DataFrame where the columns are positions in the reads
        and the values are the quality scores at those positions.
        from_end: Which end of the read to plot from. 'start' or 'end'.

    Returns:
        A matplotlib figure object containing the plot.
    """
    if from_end.lower() == 'start':
        col_names = data.columns
    elif from_end.lower() == 'end':
        col_names = data.columns[::-1]
    else:
        raise Exception("'start' and 'end' are the only options allowed for "
                        "plotting quality per position.")

    title = 'Quality score across reads, from the {}'.format(from_end)
    xlabel = 'Read position (bp)'
    ylabel = 'Phred Quality Score'
    cut = 0  # cuts the violin plot at max and min values (doesn't extrapolate)

    fig, axes = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    plot = sns.violinplot(data=data, ax=axes, order=col_names,
                          cut=cut, linewidth=0.5)
    plot.set(xlabel=xlabel, ylabel=ylabel, title=title)
    plot.set_xticklabels(plot.get_xticklabels(), rotation=45)
    sns.despine()

    return fig


def save_plots_to_pdf(plots: List[plt.Figure], filename: str):
    """Saves a list of given plots to a single PDF document.

    Args:
        plots: A list of matplotlib figure objects.
        filename: The file name (and path) to save the PDF to.

    """
    pdf_doc = PdfPages(filename)

    for plot in plots:
        pdf_doc.savefig(plot)

    pdf_doc.close()
