# nomnom
Quick and dirty lab-internal tools to parse Last Millennium Reanalysis (LMR) data assimilation (DA) output.

This project is under activate development.


## Quick example

From a terminal, run:

```bash
nomnom report --dapath /path_to/lmr_output/r0 --pdfpath da_report.pdf
```

This reads LMR DA directory output and then writes a quick and dirty PDF, handy for quality control.

You can read more options with `--help`, like:

```bash
nomnom --help

nomnom report --help
```


## Installation

To install **nomnom** from GitHub with pip, run:

```bash
$ pip install git+https://github.com/brews/nomnom.git#egg=nomnom
```


## Support and development

Please feel free to report bugs and issues, or view the source code on GitHub (https://github.com/brews/nomnom).


## License

**nomnom** is available under the Open Source GPLv3 (https://www.gnu.org/licenses).