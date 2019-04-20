import os

import click

import nomnom.api.units
import nomnom.api.utils
import nomnom.api.qcreport.plot as daplot
import nomnom.api.assimilated_proxies as proxies


# Main entry point
@click.group(context_settings={'help_option_names': ['-h', '--help']})
def nomnom_cli():
    """Parse output from Last Millennium Reanalysis (LMR) data assimilation (DA)
    """
    pass


@nomnom_cli.command(help='Write PDF report from DA output directory')
@click.option('--dapath', help='Path to directory with DA output files')
@click.option('--outpdf', help='Where to write output PDF file')
def report(dapath, outpdf):
    """Produce PDF report from data assimilation output directory
    """
    target_fields = nomnom.api.utils.list_ensemblefields(dapath)
    target_fields.sort()

    out_fields = []
    for f in target_fields:
        out_fields.append(nomnom.api.utils.read_field(f, dapath))

    out_fields = [nomnom.api.units.unit_cleaning(f) for f in out_fields]

    try:
        assim_proxies = proxies.read_assimilated_proxies(os.path.join(dapath, 'assimilated_proxies.npy'))
    except FileNotFoundError:
        assim_proxies = None

    daplot.write_reportpdf(outpdf, *out_fields, assim_proxies=assim_proxies)
