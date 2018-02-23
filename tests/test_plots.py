import pytest
import glob
import os
import copy
import pyfastaq
from pistis import utils, plots


IMG_DIR = 'tests/images'
TEST_FASTQ = glob.glob('tests/data/*fastq*')[0]


@pytest.fixture
def get_test_data():
    fastq = pyfastaq.sequences.file_reader(TEST_FASTQ, read_quals=True)
    records = []
    for i, read in enumerate(fastq):
        if i == 50:
            break
        records.append(copy.copy(read))
    return utils.collect_fastq_data(iter(records))


def test_gc_plot():
    fname = os.path.join(IMG_DIR, 'gc_plot.png')
    expected_fname = os.path.join(IMG_DIR, 'gc_plot-expected.png')
    gc_data = get_test_data()[0]
    fig = plots.gc_plot(gc_data)
    fig.savefig(fname, format='png')
    assert open(expected_fname, 'rb').read() == open(fname, 'rb').read()

def test_length_vs_qual_plot():
    fname = os.path.join(IMG_DIR, 'len_v_qual.png')
    expected_fname = os.path.join(IMG_DIR, 'len_v_qual-expected.png')
    lengths, quality_scores = get_test_data()[1:3]
    fig = plots.length_vs_qual_plot(lengths, quality_scores)
    fig.savefig(fname, format='png')
    assert open(expected_fname, 'rb').read() == open(fname, 'rb').read()