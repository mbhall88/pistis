"""Tests for `pistis` package."""
from __future__ import absolute_import
from click.testing import CliRunner
from pistis import pistis


def test_command_line_interface():
    """Test the CLI."""
    help_msgs = [
        'Show this message and exit.',
        '-k, --kind [kde|scatter|hex]',
        '-o, --output PATH',
        '--log_length / --no_log_length  Plot the read length as a log10',
        'Fastq file to plot. This can be gzipped.',
        'SAM/BAM file to produce read percent identity'
    ]
    runner = CliRunner()
    # test cli with no args passed
    result = runner.invoke(pistis.main)
    # assert result.exit_code == 2
    assert ('Either --fastq, --bam or both must be given as arguments.' in
            result.output)

    # test cli with help passed
    help_result = runner.invoke(pistis.main, ['--help'])
    assert help_result.exit_code == 0
    assert all(msg in help_result.output for msg in help_msgs)

    # test cli with bad fastq path passed
    bad_fastq = '../../test.fastq'
    bad_fastq_result = runner.invoke(pistis.main, ['--fastq', bad_fastq])
    assert bad_fastq_result.exit_code == 2
    assert ('Path "{}" does not exist.'.format(bad_fastq)
            in bad_fastq_result.output)

    # test cli with bad bam path passed
    bad_bam = '../../bad.bam'
    bad_bam_result = runner.invoke(pistis.main, ['--bam', bad_bam])
    assert bad_bam_result.exit_code == 2
    assert ('Path "{}" does not exist.'.format(bad_bam)
            in bad_bam_result.output)

    # test cli with bad kind argument
    kind = 'hownowbrowncow'
    bad_kind_result = runner.invoke(pistis.main, ['--kind', kind])
    assert bad_kind_result.exit_code == 2
    assert ('invalid choice: hownowbrowncow. (choose from kde, scatter, hex)'
            in bad_kind_result.output)
