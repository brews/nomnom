import collections
import logging


log = logging.getLogger(__name__)
cleaning_delegator = collections.defaultdict(list)


def clean(da_field):
    """Decorator to register functions for cleaning data assimilation output
    """
    def decor(func):
        cleaning_delegator[da_field].append(func)
        return func
    return decor


def bcad_to_bp(df, varname='time'):
    """Convert time units from BC/AD to years before present
    """
    out = df.copy()
    out[varname] = 1950 - out[varname]
    return out


def kelvin_to_celsius(df, varname='xam'):
    """Convert temperature from kelvin to celsius
    """
    out = df.copy()
    out[varname] = out[varname] - 273.15
    return out


def cleaning_default(da_output):
    """Default function to clean units and populate metadata for da_output
    """
    return da_output


@clean('pr_sfc_Adec')
@clean('wap_700hPa_Adec')
@clean('sos_sfc_Odec')
@clean('zg_500hPa_Adec')
@clean('prw_int_Adec')
@clean('psl_sfc_Adec')
def fieldplot_temps(da_output):
    out = da_output.copy()
    out = bcad_to_bp(out)
    return out


@clean('ts_sfc_Adec')
@clean('tas_sfc_Adec')
@clean('tos_sfc_Odec')
def fieldplot_temps(da_output):
    out = da_output.copy()
    out = bcad_to_bp(out)
    out = kelvin_to_celsius(out)
    return out


def unit_cleaning(da_output):
    """Convert units and populate metadata for da_output
    """
    log.debug('Cleaning units and metadata')
    out = da_output.copy()
    cleanfuns = cleaning_delegator.get(da_output.attrs['da_field'], [cleaning_default])

    for fun in cleanfuns:
        out = fun(out)

    return out

