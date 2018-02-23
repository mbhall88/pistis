import glob
import pytest
import pyfastaq
from pistis import utils

TEST_FASTQ = glob.glob('data/*fastq*')[0]

@pytest.fixture
def small_fastq() -> iter:
    """Returns 5 records from test fastq file as an iterator.

    Returns:
        An iterator with 5 fastq records in it.
    """
    fastq = pyfastaq.sequences.file_reader(TEST_FASTQ, read_quals=True)
    small_list = []
    count = 0
    for record in fastq:
        small_list.append(record)
        count += 1
        if count > 5:
            break
    return iter(small_list)
