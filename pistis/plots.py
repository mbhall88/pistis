"""This module contains methods for making the quality control plots for
`pistis` and also for saving those plots into a single PDF document.
"""
from __future__ import absolute_import
from typing import List
import collections
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from six.moves import map


DPI = 300  # resolution for plots
FIGURE_SIZE = (11.7, 10)


def gc_plot(gc_content):
    """Generate a histogram with density curve over it for GC content of sample.

    Args:
        gc_content: A list of GC content for each read.

    Returns:
        A matplotlib figure object containing the plot.

    """
    bins = 100
    xlabel = 'GC content'
    ylabel = 'Proportion of reads'
    title = 'GC content of each read'
    # set the x-axis limits based on whether data is decimal or percentage
    xlim = (0, 100) if any(x > 1 for x in gc_content) else (0, 1.0)

    fig, axes = plt.subplots(dpi=DPI, figsize=FIGURE_SIZE)
    plot = sns.distplot(gc_content, bins=bins, ax=axes)
    plot.set(xlabel=xlabel, ylabel=ylabel, title=title, xlim=xlim)

    # remove top and right border of plot
    sns.despine()

    return fig


gc_plot.__annotations__ = {'gc_content': List[float],
                           'return': plt.Figure}


def length_vs_qual_plot(lengths, quality_scores, kind='scatter',
                        log_length=True):
    """Generates a plot of the read length against quality score for each read.

    Args:
        lengths: A list with each element being the length of a read.
        quality_scores: A list with each element being the mean Phred quality
        score for a read.
        kind: The way the points are represented on the plot. Options include
        hex bins, scatter points or kernel density estimatation ('hex',
        'scatter', and 'kde' respectively).
        log_length: Plot the length as a logarithm (base 10).

    Returns:
        A matplotlib figure object containing the plot.
    """
    # use slightly different plot styling for this plot compared to the others
    with sns.axes_style('whitegrid',
                        rc={"grid.linewidth": 0.25, 'grid.linestyle': '--'}):
        xlabel = 'Read Length (bp)'
        ylabel = 'Phred quality score'

        # jointplot require numpy array
        x_data = np.array(lengths)
        y_data = np.array(quality_scores)

        if log_length:
            x_data = np.log10(x_data)

        plot = sns.jointplot(x=x_data, y=y_data, kind=kind, space=0, size=3)

        # change the alpha of the scatter points
        if kind == 'scatter':
            plot.ax_joint.cla()
            plot.ax_joint.scatter(x_data, y_data, alpha=0.25)

        plot.set_axis_labels(xlabel=xlabel, ylabel=ylabel)

        # fix the y axis limits to reasonable phred scores
        quality_ticks = list(range(0, 50, 5))
        plot.ax_joint.set_yticks(quality_ticks)
        plot.ax_joint.set_yticklabels(quality_ticks)

        if log_length:  # format x-axis labels and ticks for log data
            log_ticks = [500, 1e3, 3e3, 5e3, 1e4, 3e4, 5e4, 1e5, 3e5, 5e5, 1e6,
                         1.5e6, 2e6]
            plot.ax_joint.set_xticks(np.log10(log_ticks))
            plot.ax_joint.set_xticklabels(list(map(int, log_ticks)),
                                          rotation=270)

        plot.fig.set(dpi=DPI, size_inches=FIGURE_SIZE)

    return plot.fig


length_vs_qual_plot.__annotations__ = {'lengths': List[int],
                                       'quality_scores': List[float],
                                       'kind': str,
                                       'log_length': bool,
                                       'return': plt.Figure}


def quality_per_position(data, from_end='start'):
    """Generate a violin plot of quality scores across positions in all reads.
    Each violin in the plot corresponds to a 'bin'. That is, all quality scores
    at that position (or positions if it is a range) across all reads.

    Args:
        data: An ordered dictionary where the keys are positions in the reads
        and the values are the quality scores at those positions.
        from_end: Which end of the read to plot from. 'start' or 'end'.

    Returns:
        A matplotlib figure object containing the plot.
    """
    if from_end.lower() == 'start':
        col_names = list(data.keys())
        values = list(data.values())
    elif from_end.lower() == 'end':
        col_names = list(data.keys())[::-1]
        values = list(data.values())[::-1]
    else:
        raise Exception("'start' and 'end' are the only options allowed for "
                        "plotting quality per position.")

    title = 'Quality score across reads, from the {}'.format(from_end)
    xlabel = 'Read position (bp)'
    ylabel = 'Phred Quality Score'

    fig, axes = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    plot = sns.boxplot(data=values, ax=axes, linewidth=0.5)
    plot.set(xlabel=xlabel, ylabel=ylabel, title=title)
    plot.set_xticklabels(col_names, rotation=45)
    sns.despine()

    return fig


quality_per_position.__annotations__ = {'data': collections.OrderedDict,
                                        'from_end': str,
                                        'return': plt.Figure}


def percent_identity(perc_indentities):
    """Plots read percent identity as a distribution/histogram plot.

    Args:
        perc_indentities: A list of the percentage identity figures.

    Returns:
        A matplotlib figure object containing the plot.
    """
    bins = 100
    xlabel = 'Read percent identity'
    ylabel = 'Proportion of reads'
    title = 'Read alignment percent identity'

    fig, axes = plt.subplots(dpi=DPI, figsize=FIGURE_SIZE)
    plot = sns.distplot(perc_indentities, bins=bins, ax=axes)

    # add a vertical dashed line at the median
    median = np.median(perc_indentities)
    plt.plot([median] * 2, [0, 1], linewidth=2, c='r', alpha=0.75,
             linestyle='--')
    xticks = plot.get_xticks().tolist()[1:-1]
    xticks.append(median.round(2))
    xticks.sort()
    plot.set(xlabel=xlabel, ylabel=ylabel, title=title, xticks=xticks,
             xticklabels=xticks)
    # remove top and right border of plot
    sns.despine()

    return fig


percent_identity.__annotations__ = {'gc_content': List[float],
                                    'return': plt.Figure}


def save_plots_to_pdf(plots, filename):
    """Saves a list of given plots to a single PDF document.

    Args:
        plots: A list of matplotlib figure objects.
        filename: The file name (and path) to save the PDF to.

    """
    pdf_doc = PdfPages(filename)

    for plot in plots:
        pdf_doc.savefig(plot)

    pdf_doc.close()


save_plots_to_pdf.__annotations__ = {'plots': List[plt.Figure],
                                     'filename': str,
                                     'return': None}
