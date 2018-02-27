"""This module contains functions to aid in the parsing of data into the
formats required to produce the quality plots for `pistis`.
"""
from __future__ import division
from __future__ import absolute_import
from typing import List, Tuple, Iterable
from collections import OrderedDict
import numpy as np
from six.moves import zip


BIN_NAMES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11-20',
             '21-50', '51-100', '101-200', '201-300']
BIN_STARTS = np.append(np.arange(11), np.array([21, 51, 101, 201, 301]))


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
            - An ordered dictionary where each key corresponds to a postitional
            bin and the values are quality scores for all reads at that
            position(s) from the start of each read.
            - An ordered dictionary where each key corresponds to a postitional
            bin and the values are quality scores for all reads at that
            position(s) from the end of each read.
    """
    gc_content = []
    read_lengths = []
    mean_quality_scores = []
    bins_from_start = OrderedDict((name, []) for name in BIN_NAMES)
    bins_from_end = OrderedDict((name, []) for name in BIN_NAMES)
    for record in fastq:
        gc_content.append(record.gc_content(as_decimal=False))
        length = len(record.seq)
        read_lengths.append(length)
        __, q_scores = record.to_Fasta_and_qual()
        mean_quality_scores.append(sum(q_scores) / length)
        # bin the quality scores for the read from start and end by position
        for i, (start_idx, bin_name) in enumerate(zip(BIN_STARTS[:-1],
                                                      BIN_NAMES)):
            slice_from_start = q_scores[start_idx: BIN_STARTS[i + 1]]
            slice_from_end = q_scores[-BIN_STARTS[i + 1]: -start_idx or None]
            bins_from_start[bin_name].extend(slice_from_start)
            bins_from_end[bin_name].extend(slice_from_end)

    return (gc_content, read_lengths, mean_quality_scores, bins_from_start,
            bins_from_end)


collect_fastq_data.__annotations__ = {'fastq': Iterable,
                                      'return': Tuple[List[float], List[int],
                                                      List[float], OrderedDict,
                                                      OrderedDict]}
