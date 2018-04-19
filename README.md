# Pistis


### Quality control plotting for long reads.

[![PyPI status](https://img.shields.io/pypi/v/pistis.svg)](https://pypi.python.org/pypi/pistis)
[![Build Status](https://travis-ci.org/mbhall88/pistis.svg?branch=master)](https://travis-ci.org/mbhall88/pistis)
[![GitHub license](https://img.shields.io/github/license/mbhall88/pistis.svg)](https://github.com/mbhall88/pistis/blob/master/LICENSE)
![Twitter Follow](https://img.shields.io/twitter/follow/mbhall88.svg?style=social&logo=twitter&label=Follow)

This package provides plotting designed to give you an idea of how your long read
sequencing data looks. It was conceived of and developed with nanopore reads in
mind, but there is not reason why PacBio reads can't be used.  


## Installation

Installation is fairly straightforward

```sh
pip3 install pistis
```

You can also use `pip` if you are running with python2.  
Or using a virtual
environment manager such as [conda](https://conda.io/docs/) or
[pipenv](https://docs.pipenv.org/) (my personal favourite).  

You should now be able to run `pistis` from the command line
```sh
pistis --help
```

## Usage

The main use case for `pistis` is as a command-line interface (CLI), but can also be
used in an interactive way, such as with a [Jupyter Notebook](https://jupyter.org/).  

#### CLI Usage
After installing and running the help menu you should see the following usage
options
```
pistis -h

Usage: pistis [OPTIONS]

  A package for sanity checking (quality control) your long read data.
  Feed it a fastq file and in return you will receive a PDF with four plots:

          1. GC content histogram with distribution curve for sample.

          2. Jointplot showing the read length vs. phred quality score for
          each         read. The interior representation of this plot can be
          altered with the         --kind option.

          3. Violin plot of the phred quality score at positional bins
          across all reads. The reads are binned into read positions 1, 2,
          3, 4, 5, 6, 7, 8, 9, 10, 11-20, 21-50, 51-100, 101-200, 201-300,
          301-1000, 1001-10000, and >10000. Plots from the start to the end
          of reads.

          4. Same as 3, but plots from the end of the read to the start.

  Additionally, if you provide a BAM/SAM file a histogram of the read
  percent identity will be added to the report.

Options:
  -f, --fastq PATH                Fastq file to plot. This can be gzipped.
  -o, --output PATH               Path to save the plot PDF as. If name is not
                                  specified, will use the name of the fastq
                                  (or bam) file with .pdf extension.
  -k, --kind [kde|scatter|hex]    The kind of representation to use for the
                                  jointplot of quality score vs read length.
                                  Accepted kinds are 'scatter', 'kde'
                                  (default), or 'hex'. For examples refer to h
                                  ttps://seaborn.pydata.org/generated/seaborn.
                                  jointplot.html
  --log_length / --no_log_length  Plot the read length as a log10
                                  transformation on the quality vs read length
                                  plot
  -b, --bam PATH                  SAM/BAM file to produce read percent
                                  identity histogram from.
  -h, --help                      Show this message and exit.
```
There are three different use cases - currently - for producing plots:  

**Fastq only** - This will return four plots:
  * A distribution plot of the GC content for each read.
  * A bivariate jointplot with read length on the y-axis and mean read quality
  score on the x-axis.
  * Two boxplots that show the distribution of quality scores at select positions
  and positional ranges. One plot shows the scores from the beginning of the
  read and the other from the end of the read.  

To use `pistis` in this way you just need a fastq file.

```sh
pistis -f /path/to/my.fastq -o /save/as/report.pdf
```

This will save the four plots to a file called `report.pdf` in directory `/save/as/`.
If you don't provide a `--output/-o` option the file will be saved in the current
directory with the basename of the fastq file. So in the above example it would be
saved as `my.pdf`.  
If you would prefer the read lengths in the bivariate plot of read length vs.
mean quality score then you can indicate this like so

```sh
pistis -f /path/to/my.fastq -o /save/as/report.pdf --no_log_length
```

Additionally, you can change the way the data is represented in the bivariate plot.
The default is a kernel density estimation plot (as in the below image), however you can
choose to use a [hex bin or scatter plot version instead](https://seaborn.pydata.org/generated/seaborn.jointplot.html).
In the running example, to use a scatter plot you would run the following

```sh
pistis -f /path/to/my.fastq -o /save/as/report.pdf --kind scatter
```

You can also provide a `gzip`ed fastq file without any extra steps

```sh
pistis -f /path/to/my.fastq.gz -o /save/as/report.pdf
```

**Examples**  
GC content:  
![gc content plot](https://github.com/mbhall88/pistis/blob/master/docs/imgs/pistis_gc_plot.png)

Read length vs. mean read quality score:  
![read length vs quality plot](https://github.com/mbhall88/pistis/blob/master/docs/imgs/pistis_qual_v_len.png)  

Base quality from the start of each read:  
![base quality from start plot](https://github.com/mbhall88/pistis/blob/master/docs/imgs/pistis_qual_start.png)  

Base quality from the end of each read:  
![base quality from end plot](https://github.com/mbhall88/pistis/blob/master/docs/imgs/pistis_qual_end.png)

---

**Fastq and BAM/SAM** - This will return the above four plots, plus a distribution
plot of each read's percent identity with the reference it is aligned to in the
[BS]AM file. Reads which are flagged as supplementary or secondary are not included.
The plot also includes a dashed vertical red line indicating the median
percent identity.  
Note: If using a BAM file, it must be sorted and indexed (i.e `.bai` file). See [`samtools`](http://www.htslib.org/doc/samtools.html)
for instructions on how to do this.

```sh
pistis -f /path/to/my.fastq  -b /path/to/my.bam -o /save/as/report.pdf
# or
pistis -f /path/to/my.fastq  -b /path/to/my.sam -o /save/as/report.pdf
```

**Example**  
Distribution of aligned read percent identity:  
![percent identity plot](https://github.com/mbhall88/pistis/blob/master/docs/imgs/pistis_perc_id.png)

---

**BAM/SAM only** - At this stage you will receive only the distribution
plot of each read's percent identity with the reference it is aligned to. In a
future release I aim to allow you to also get the other four fastq-only plots.

```sh
pistis -b /path/to/my.bam -o /save/as/report.pdf
```

As with the fastq-only method, if you don't provide a `--output/-o` option the file will be saved in the current
directory with the basename of the [BS]AM file. So in the above example it would be
saved as `my.pdf`.

#### Usage in a development environment

If you would like to use `pistis` within a development environment such as a
`jupyter notebook` or just a plain ol' python shell then take a look at [this example notebook](https://github.com/mbhall88/pistis/blob/master/examples/example_usage.ipynb)
for all the details.

## Credits

* This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage` project template](https://github.com/audreyr/cookiecutter-pypackage).  
* The two test data files (fastq and BAM) that I have use in this repository were
taken from [Wouter De Coster's `nanotest` repository](https://github.com/wdecoster/nanotest).
* Which in turn comes from [Nick Loman and Josh Quick](http://lab.loman.net/2017/03/09/ultrareads-for-nanopore/).  
* The example plots in this `README` were made using the entire fastq of basecalled
reads from the experiment in that [blog on "whale hunting"](http://lab.loman.net/2017/03/09/ultrareads-for-nanopore/).  
* The plot for the BAM file was obtained by running `pistis` on a BAM file generated
by mapping the fastq file to *E. coli* reference [NC_000913.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000913.3)
using Heng Li's [`minimap2`](https://github.com/lh3/minimap2) and `-x map-ont` option.

# Contributing

If you would like to contribute to this package you are more than welcome.  
**Please read through the [contributing guidelines](https://github.com/mbhall88/pistis/blob/master/CONTRIBUTING.rst) first**.
