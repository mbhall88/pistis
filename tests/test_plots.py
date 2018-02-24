"""Test functionality of the plots module."""
from __future__ import absolute_import
import pytest
import glob
import os
import copy
import pyfastaq
from typing import Tuple, List
import pandas as pd
from pistis import utils, plots

IMG_DIR = 'tests/images'
TEST_FASTQ = glob.glob('tests/data/*fastq*')[0]


@pytest.fixture
def get_test_data():
    """Generate a very small fastq dataset to use for plotting.

    Returns:
        A tuple containing gc content, read lengths, quality scores and quality
        scores per position from the start and end of the reads.
    """
    fastq = pyfastaq.sequences.file_reader(TEST_FASTQ, read_quals=True)
    records = []
    for i, read in enumerate(fastq):
        if i == 50:
            break
        records.append(copy.copy(read))
    return utils.collect_fastq_data(iter(records))


get_test_data.__annotations__ = {'return': Tuple[List[float], List[int],
                                                 List[float], pd.DataFrame,
                                                 pd.DataFrame]}


def test_gc_plot():
    """Test generation of GC content plot."""
    fname = os.path.join(IMG_DIR, 'gc_plot.png')
    expected_fname = os.path.join(IMG_DIR, 'gc_plot-expected.png')

    gc_data = get_test_data()[0]
    fig = plots.gc_plot(gc_data)
    fig.savefig(fname, format='png')
    assert open(expected_fname, 'rb').read() == open(fname, 'rb').read()


def test_length_vs_qual_plot():
    """Test generation of read length vs. quality score plot."""
    fname = os.path.join(IMG_DIR, 'len_v_qual.png')
    expected_fname = os.path.join(IMG_DIR, 'len_v_qual-expected.png')

    lengths, quality_scores = get_test_data()[1:3]
    fig = plots.length_vs_qual_plot(lengths, quality_scores)
    fig.savefig(fname, format='png')
    assert open(expected_fname, 'rb').read() == open(fname, 'rb').read()


def test_quality_per_position():
    """Test generation of the quality per position plots."""
    fname_start = os.path.join(IMG_DIR, 'qual_pos_start.png')
    expected_fname_start = os.path.join(IMG_DIR, 'qual_pos_start-expected.png')
    fname_end = os.path.join(IMG_DIR, 'qual_pos_end.png')
    expected_fname_end = os.path.join(IMG_DIR, 'qual_pos_end-expected.png')

    df_start, df_end = get_test_data()[3:]
    fig_start = plots.quality_per_position(df_start)
    fig_end = plots.quality_per_position(df_end, from_end='end')
    fig_start.savefig(fname_start, format='png')
    fig_end.savefig(fname_end, format='png')
    assert (open(expected_fname_start, 'rb').read() ==
            open(fname_start, 'rb').read())
    assert (open(expected_fname_end, 'rb').read() ==
            open(fname_end, 'rb').read())


def test_save_plots_to_pdf():
    """Test generation of PDF document containing all plots."""
    fname = os.path.join(IMG_DIR, 'report.pdf')
    # expected_fname = os.path.join(IMG_DIR, 'report-expected.pdf')
    (gc_content,
     read_lengths,
     mean_quality_scores,
     df_start,
     df_end) = get_test_data()
    plot1 = plots.gc_plot(gc_content)
    plot2 = plots.length_vs_qual_plot(read_lengths, mean_quality_scores)
    plot3 = plots.quality_per_position(df_start)
    plot4 = plots.quality_per_position(df_end, from_end='end')
    plots.save_plots_to_pdf([plot1, plot2, plot3, plot4], fname)
    # assert open(fname, 'rb').read() == open(expected_fname, 'rb').read()
    # Open report.pdf and report-expected.pdf and compare by eye. Currently no
    # test to compare two PDF documents.
