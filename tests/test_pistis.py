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
        'FASTQ: Fastq file to plot.'
    ]
    runner = CliRunner()
    # test cli with no args passed
    result = runner.invoke(pistis.main)
    assert result.exit_code == 2
    assert 'Error: Missing argument "fastq"' in result.output

    # test cli with help passed
    help_result = runner.invoke(pistis.main, ['--help'])
    assert help_result.exit_code == 0
    assert all(msg in help_result.output for msg in help_msgs)

    # test cli with bad fastq path passed
    bad_fastq = '../../test.fastq'
    bad_fastq_result = runner.invoke(pistis.main, [bad_fastq])
    assert bad_fastq_result.exit_code == 2
    assert ('Path "{}" does not exist.'.format(bad_fastq)
            in bad_fastq_result.output)

    # test cli with bad kind argument
    kind = 'hownowbrowncow'
    bad_kind_result = runner.invoke(pistis.main, ['--kind', kind])
    assert bad_kind_result.exit_code == 2
    assert ('invalid choice: hownowbrowncow. (choose from kde, scatter, hex)'
            in bad_kind_result.output)
