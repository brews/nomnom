import collections
import logging

import tqdm
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pylab as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs

import nomnom.api.utils as utils


log = logging.getLogger(__name__)
plot_delegator = collections.defaultdict(list)


def site_map(assim_proxies, ax=None, jitter=True):
    """Simple global site map, given an iterable of proxy named tuples.
    """
    if ax is None:
        ax = plt.gca(projection=ccrs.Robinson())
    ax.set_global()
    ax.add_feature(cfeature.LAND, facecolor='#B0B0B0', zorder=0)
    ax.outline_patch.set_linewidth(0.5)

    # Break site latlons into proxy type groups.
    latlon = collections.defaultdict(list)
    for p in assim_proxies:
        latlon[p.proxy_type].append((p.lat, p.lon))

    # Plot by proxy type, sorted.
    ptypes = list(latlon.keys())
    # ptypes.sort()
    for k in ptypes:
        v = latlon[k]
        lat, lon = zip(*v)

        if jitter:
            lon += np.random.randn(len(lon)) * 0.75
            lat += np.random.randn(len(lat)) * 0.75

        ax.scatter(x=lon, 
                   y=lat, 
                   s=50, facecolors='none', 
                   edgecolors= 'C' + str(ptypes.index(k)),
                   marker='.', transform=ccrs.Geodetic(), label=str(k))
    return ax


def daplot(da_field):
    """Decorator to register functions for plotting data assimilation output"""
    def decor(func):
        plot_delegator[da_field].append(func)
        return func
    return decor


def fieldplot_default(da_output, fig=None):
    if fig is None:
        fig = plt.figure(figsize=(6.5, 9))

    title_str = str(da_output.attrs['da_field'])

    ax1 = plt.subplot2grid((4, 2), (0, 0), colspan=2)
    ax2 = plt.subplot2grid((4, 2), (1, 0), colspan=2)
    ax3 = plt.subplot2grid((4, 2), (2, 0), projection=ccrs.Robinson())
    ax4 = plt.subplot2grid((4, 2), (2, 1), projection=ccrs.Robinson())
    ax5 = plt.subplot2grid((4, 2), (3, 0), projection=ccrs.Robinson())

    mean_global = utils.global_wmean(da_output)
    mean_global.xam.plot(label='DA global ensemble mean', ax=ax1)
    ax1.set_title(title_str)
    ax1.grid(True)
    ax1.legend()

    lh = da_output.sel(time=slice(3000, 1000)).mean(dim='time')
    mh = da_output.sel(time=slice(8000, 6000)).mean(dim='time')
    lgm = da_output.sel(time=slice(22000, 20000)).mean(dim='time')

    da_output.xam.mean(dim='x').plot(y='y', ax=ax2)
    ax2.grid(True)

    cb_kws = {'orientation': 'horizontal'}

    lh.xam.plot.pcolormesh('lon', 'lat', ax=ax3,
                           transform=ccrs.PlateCarree(),
                           cbar_kwargs=cb_kws)
    ax3.set_title('LH')
    ax3.coastlines()

    (mh.xam - lh.xam).plot.pcolormesh('lon', 'lat', ax=ax4,
                                      transform=ccrs.PlateCarree(),
                                      cbar_kwargs=cb_kws)
    ax4.set_title('MH - LH')
    ax4.coastlines()

    (lgm.xam - lh.xam).plot.pcolormesh('lon', 'lat', ax=ax5,
                                       transform=ccrs.PlateCarree(),
                                       cbar_kwargs=cb_kws)
    ax5.set_title('LGM - LH')
    ax5.coastlines()

    return fig


@daplot('tas_sfc_Adec')
@daplot('tos_sfc_Odec')
def fieldplot_keytemps(da_output, fig=None):
    if fig is None:
        fig = plt.figure(figsize=(6.5, 9))

    title_str = str(da_output.attrs['da_field'])

    ax1 = plt.subplot2grid((4, 2), (0, 0), colspan=2)
    ax2 = plt.subplot2grid((4, 2), (1, 0), colspan=2)
    ax3 = plt.subplot2grid((4, 2), (2, 0), projection=ccrs.Robinson())
    ax4 = plt.subplot2grid((4, 2), (2, 1), projection=ccrs.Robinson())
    ax5 = plt.subplot2grid((4, 2), (3, 0), projection=ccrs.Robinson())

    mean_global = utils.global_wmean(da_output)
    mean_global.xam.plot(label='DA global ensemble mean', ax=ax1)
    ax1.set_title(title_str)
    ax1.grid(True)
    ax1.legend()

    lh = da_output.sel(time=slice(3000, 1000)).mean(dim='time')
    mh = da_output.sel(time=slice(8000, 5000)).mean(dim='time')
    lgm = da_output.sel(time=slice(22000, 19000)).mean(dim='time')

    da_output.xam.mean(dim='x').plot(y='y', ax=ax2)
    ax2.grid(True)

    cb_kws = {'orientation': 'horizontal'}

    lh.xam.plot.pcolormesh('lon', 'lat', ax=ax3,
                           transform=ccrs.PlateCarree(),
                           cbar_kwargs=cb_kws)
    ax3.set_title('LH')
    ax3.coastlines()

    (mh.xam - lh.xam).plot.pcolormesh('lon', 'lat', ax=ax4,
                                      transform=ccrs.PlateCarree(),
                                      cbar_kwargs=cb_kws)
    ax4.set_title('MH - LH')
    ax4.coastlines()

    (lgm.xam - lh.xam).plot.pcolormesh('lon', 'lat', ax=ax5,
                                       transform=ccrs.PlateCarree(),
                                       cbar_kwargs=cb_kws)
    ax5.set_title('LGM - LH')
    ax5.coastlines()

    return fig


@daplot('tas_sfc_Adec')
@daplot('tos_sfc_Odec')
def fieldplot_keytemps_timeseries(da_output, fig=None):
    if fig is None:
        fig = plt.figure(figsize=(6.5, 9))

    title_str = str(da_output.attrs['da_field'])

    ax1 = plt.subplot(4, 1, 1)

    natlantic_latlon = (56.23914915, -48.07422501)
    xy = utils.closest_xy(*natlantic_latlon, da_output)
    nearest_point = da_output.sel(x=xy[0], y=xy[1])
    ax1.errorbar(y=nearest_point.xam.values, x=nearest_point.time.values,
                 yerr=nearest_point.xav.values, label='N. Atlantic')
    ax1.set_title(title_str)
    ax1.grid(True)
    ax1.legend()

    ax2 = plt.subplot(4, 1, 2)

    eeqpac_latlon = (0.1, -90.1)
    xy = utils.closest_xy(*eeqpac_latlon, da_output)
    nearest_point = da_output.sel(x=xy[0], y=xy[1])
    ax2.errorbar(y=nearest_point.xam.values, x=nearest_point.time.values,
                 yerr=nearest_point.xav.values, label='E. Eq. Pacific')
    ax2.grid(True)
    ax2.legend()

    ax3 = plt.subplot(4, 1, 3)

    maui_latlon = (20.77473733, -156.26197385)
    xy = utils.closest_xy(*maui_latlon, da_output)
    nearest_point = da_output.sel(x=xy[0], y=xy[1])
    ax3.errorbar(y=nearest_point.xam.values, x=nearest_point.time.values,
                 yerr=nearest_point.xav.values, label='Maui')
    ax3.grid(True)
    ax3.legend()

    ax4 = plt.subplot(4, 1, 4)

    socean_latlon = (-64.742719, -12.345419)
    xy = utils.closest_xy(*socean_latlon, da_output)
    nearest_point = da_output.sel(x=xy[0], y=xy[1])
    ax4.errorbar(y=nearest_point.xam.values, x=nearest_point.time.values,
                 yerr=nearest_point.xav.values, label='S. Ocean')
    ax4.grid(True)
    ax4.legend()

    return fig


def proxyplot(assim_proxies, fig=None):
    """Plots for the assimilated_proxies numpy array in DA output"""
    if fig is None:
        fig = plt.figure(figsize=(6.5, 9))

    title_str = 'Assimilated proxies'

    type_time = collections.defaultdict(list)
    time_all = []
    for p in assim_proxies:
        ptype = p.proxy_type
        ptime = np.array(p.years)
        ptime = 1950 - ptime  # BCAD to yr BP
        type_time[ptype].extend(list(ptime))
        time_all.extend(list(ptime))

    n_bins = 20 # len(set(time_all))  # This doesn't work 'cause is time not binned time.

    ax1 = plt.subplot(2, 1, 1, projection=ccrs.Robinson())
    ax1 = site_map(assim_proxies, ax=ax1)
    ax1.set_title(title_str)

    ax2 = plt.subplot(2, 1, 2)

    lab = list(type_time.keys())
    val = list(type_time.values())

    ax2.hist(val, bins=n_bins, stacked=True, label=lab)
    ax2.yaxis.grid(True)
    ax2.set_ylabel('Proxy sample count')
    ax2.set_xlabel('Time (Cal year BP)')
    ax2.legend()

    return fig


def write_reportpdf(pdf_path, *da_output, assim_proxies=None):
    log.debug('Writing DA report')

    with PdfPages(pdf_path) as pdf:

        if assim_proxies is not None:
            fig = plt.figure(figsize=(6.5, 9))
            fig = proxyplot(assim_proxies, fig=fig)
            fig.tight_layout()
            pdf.savefig(bbox_inches='tight')
            plt.close()

        for d in tqdm.tqdm(da_output):
            plotfuns = plot_delegator.get(d.attrs['da_field'], [fieldplot_default])

            for fun in plotfuns:
                fig = plt.figure(figsize=(6.5, 9))
                fig = fun(d, fig=fig)
                fig.tight_layout()
                pdf.savefig(bbox_inches='tight')
                plt.close()

        log.debug('DA report saved to {}'.format(pdf_path))
