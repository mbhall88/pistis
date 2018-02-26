"""This module contains functions to aid in the parsing of data into the
formats required to produce the quality plots for `pistis`.
"""
from __future__ import division
from __future__ import absolute_import
from typing import List, Tuple, Iterable
import collections
import numpy as np
from six.moves import zip


def bin_quality_scores_by_position(quality_scores):
    """Bins quality scores based on their position in the sequence.

    Args:
        quality_scores: list of list of Phred quality scores for a read.
        shape: This should be the a tuple of  M x N where M is the number of
        reads in the top level list i.e len(quality_scores) and N is the length
        of the longest read in the fastq file.

    Returns:
        A Pandas DataFrame where each column corresponds to a postitional bin
        and the values in that column are quality scores for all reads at that
        position(s).

    """
    bin_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11-20',
                 '21-50', '51-100', '101-200', '201-300', '301-500']
    # Array holding the starting index for each bin.
    bin_starts = np.append(np.arange(11),
                           np.array([21, 51, 101, 201, 301, 501]))

    bins = collections.OrderedDict()
    for read_scores in quality_scores:
        for i, (start_idx, bin_name) in enumerate(zip(bin_starts[:-1],
                                                      bin_names)):
            if bin_name not in bins.keys():
                bins[bin_name] = []
            bins[bin_name].extend(read_scores[start_idx: bin_starts[i + 1]])

    return bins


bin_quality_scores_by_position.__annotations__ = {
    'quality_scores': List[List[float]],
    'return': collections.OrderedDict
}


def collect_fastq_data(fastq):
    """Given a fastq filename, gets the GC content, mean quality scores, read
    length, and quality at certain positional bins - for each read.

    Args:
        fastq: An iterable fastq object.

    Returns:
        A tuple of:
            - GC content as a list of values, which each value being GC content
            for a read.
            - List of lengths for each read.
            - List where each value is the mean Phred quality score for a read.
            - A Pandas DataFrame where each column corresponds to a postitional
            bin and the values in that column are quality scores for all reads
            at that position(s) from the start of each read.
            - A Pandas DataFrame where each column corresponds to a postitional
            bin and the values in that column are quality scores for all reads
            at that position(s) from the end of each read.
    """
    gc_content = []
    read_lengths = []
    mean_quality_scores = []
    all_quality_scores = []
    longest_read = 0
    for record in fastq:
        gc_content.append(record.gc_content(as_decimal=False))
        length = len(record.seq)
        read_lengths.append(length)
        __, q_scores = record.to_Fasta_and_qual()
        all_quality_scores.append(q_scores)
        mean_quality_scores.append(sum(q_scores) / length)
        if length > longest_read:
            longest_read = length

    # dataframe of quality scores at each positional bin from start of read
    bins_from_start = bin_quality_scores_by_position(all_quality_scores)

    # reverse each list within the list of all quality scores so as to get the
    # dataframe of quality scores at each positional bin from the END of reads
    reversed_quality_scores = [[score for score in read_scores[::-1]]
                               for read_scores in all_quality_scores]
    bins_from_end = bin_quality_scores_by_position(reversed_quality_scores)

    return (gc_content, read_lengths, mean_quality_scores, bins_from_start,
            bins_from_end)


collect_fastq_data.__annotations__ = {'fastq': Iterable,
                                      'return': Tuple[List[float], List[int],
                                                      List[float],
                                                      collections.OrderedDict,
                                                      collections.OrderedDict]}
