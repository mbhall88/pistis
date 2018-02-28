"""Tests for the utils module."""
from __future__ import absolute_import
import copy
import pytest
import pysam
from pistis import utils
from six.moves import zip

TEST_FASTQ = 'tests/data/reads.fastq.gz'


@pytest.fixture
def small_fastq():
    """Returns 5 records from test fastq file as an iterator.

    Returns:
        An iterator with 5 fastq records in it.
    """
    with pysam.FastxFile(TEST_FASTQ) as fastq:
        records = []
        idxs = (55, 100, 64, 98, 243)
        for i, read in enumerate(fastq):
            if i in idxs:
                records.append(copy.copy(read))

    return iter(records)


small_fastq.__annotations__ = {'return': iter}


def test_collect_fastq_data():
    """Test the collect_fastq_data function in utils module."""
    correct_lengths = [14665, 4700, 2351, 9155, 41207]
    correct_gc = [53.50153426525741, 48.319148936170214, 50.82943428328371,
                  47.657018022938286, 46.19846142645667]
    correct_quality_means = [15.806409819297647, 15.878297872340426,
                             15.629094002552106, 10.446204259967232,
                             10.431019001625938]
    correct_df_start_pos_1 = [13, 8, 8, 4, 2]
    correct_df_start_pos_4 = [4, 6, 8, 4, 2]
    correct_df_start_pos_11_20 = [12, 14, 9, 16, 17, 14, 10, 13, 13, 14, 15,
                                  8, 22, 25, 29, 28, 11, 11, 16, 9, 9, 9,
                                  12, 23, 12, 12, 10, 20, 17, 23, 13, 16, 16,
                                  10, 9, 15, 21, 22, 8, 10, 20, 13, 10, 10,
                                  6, 7, 7, 4, 14, 13, 29, 11, 20, 20, 24]
    correct_df_end_pos_3 = [3, 8, 6, 5, 5]
    correct_df_end_pos_10 = [23, 8, 10, 15, 6]
    correct_df_end_pos_11_20 = [29, 27, 22, 26, 26, 29, 27, 18, 14, 9, 12,
                                9, 8, 8, 20, 12, 10, 6, 10, 11, 15, 21,
                                9, 7, 5, 10, 17, 10, 12, 13, 7, 14, 5,
                                19, 13, 9, 9, 7, 6, 5, 14, 14, 18, 19,
                                9, 10, 12, 11, 17, 17, 16, 7, 4, 4, 6]
    fastq = small_fastq()
    (gc_content, read_lengths,
     mean_quality_scores, df_start, df_end) = utils.collect_fastq_data(fastq)

    assert all(x == y
               for x, y in zip(correct_lengths, read_lengths))
    assert all(pytest.approx(x) == y
               for x, y in zip(correct_gc, gc_content))
    assert all(pytest.approx(x) == y
               for x, y in
               zip(sorted(correct_quality_means), sorted(mean_quality_scores)))
    # test df start bins are correct
    assert all(x == y
               for x, y in
               zip(sorted(correct_df_start_pos_1), sorted(df_start['1'])))
    assert all(x == y
               for x, y in
               zip(sorted(correct_df_start_pos_4), sorted(df_start['4'])))
    assert all(x == y
               for x, y in zip(sorted(correct_df_start_pos_11_20),
                               sorted(df_start['11-20'])))
    # test df end bins are correct
    assert all(x == y
               for x, y in
               zip(sorted(correct_df_end_pos_3), sorted(df_end['3'])))
    assert all(x == y
               for x, y in
               zip(sorted(correct_df_end_pos_10), sorted(df_end['10'])))
    assert all(x == y
               for x, y in
               zip(sorted(correct_df_end_pos_11_20), sorted(df_end['11-20'])))


def test_gc_content():
    """Test GC content calculation works as expected"""
    tests = [
        ('cgCG', 1.0),
        ('tTaA', 0.0),
        ('GCAT', 0.5),
        ('GCATNN', 0.5),
        ('GCATNNS', 0.6),
        ('GCATNNSK', 0.5)
    ]
    for test, answer in tests:
        assert pytest.approx(utils.gc_content(test)) == answer
        assert (pytest.approx(utils.gc_content(test, as_decimal=False) ==
                              answer * 100))
