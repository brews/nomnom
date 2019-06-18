import os
import glob
import re

import numpy as np
import xarray as xr


def distance(lon1, lat1, lon2, lat2):
    """Greater-sphere distance (km) between two latlon points
    """
    earth_r = 6371
    startlat_r = np.deg2rad(lat1)
    stoplat_r = np.deg2rad(lat2)
    lon_dif = np.deg2rad(lon2 - lon1)
    lat_dif = np.deg2rad(lat2 - lat1)
    a = (np.sin(lat_dif/2.0) * np.sin(lat_dif/2.0)
        + np.cos(startlat_r) * np.cos(stoplat_r)
        * np.sin(lon_dif/2.0) * np.sin(lon_dif/2.0))
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return earth_r * c


def closest_xy(lat, lon, df):
    stacked = df.stack(xy=('x', 'y'))
    d = distance(lon, lat, stacked['lon'], stacked['lat'])
    min_val = d.unstack('xy').where(d.unstack('xy') == d.unstack('xy').min(), drop=True)
    return np.asscalar(min_val.x), np.asscalar(min_val.y)


def read_ensemblenpz(path):
    """Convert input DA ensemble NPZ file to xarray.Dataset"""
    d = np.load(path)
    # TODO(brews): Need to add metadata and reference_time. Maybe units.
    # TODO(brews): Do we need to worry about overflowing the float for time?
    # TODO(brews): Include other attrs that are in npz file.
    try:
        assert d['xbm'].ndim == 2 and d['xam'].ndim == 3
        ds = xr.Dataset({'xbm': (['y', 'x'], d['xbm']),
                         'xam': (['time', 'y', 'x'], d['xam'])},
                         coords = {'lat': (['y', 'x'], d['lat']),
                                   'lon': (['y', 'x'], d['lon']),
                                   'time': d['years'].astype(np.float)})
    except KeyError:
        assert d['xbv'].ndim == 2 and d['xav'].ndim == 3
        ds = xr.Dataset({'xbv': (['y', 'x'], d['xbv']),
                         'xav': (['time', 'y', 'x'], d['xav'])},
                        coords = {'lat': (['y', 'x'], d['lat']),
                                  'lon': (['y', 'x'], d['lon']),
                                  'time': d['years'].astype(np.float)})
    return ds


def global_wmean(da, latlon_dims=('y', 'x')):
    """Cos(lat) weighted global mean for an xarray.DataArray taken from an ensemblenpz"""
    # We are making some strong assumptions about the structure of da.
    wgts = np.cos(np.deg2rad(da.lat))
    if da.lat.ndim < 2 and da.lon.ndim < 2:
        wgts = np.stack([wgts] * len(da.lon)).T
    return (da * wgts).stack(z=latlon_dims).sum('z') / wgts.sum()


def list_ensemblefields(path):
    """Get list of ensemble fields at DA output path"""
    files = glob.glob(os.path.join(path, 'ensemble*.npz'))
    matches = [re.search('(ensemble_mean|ensemble_variance)_(\w+)\.npz$', s) for s in files]
    return list(set([m.groups()[1] for m in matches]))


def read_field(field, path='.'):
    """Get dataset of DA ensemble field at path"""
    files = glob.glob(os.path.join(path, 'ensemble*{0}.npz'.format(field)))
    ds = xr.merge([read_ensemblenpz(fl) for fl in files])
    ds.attrs['da_field'] = field
    return ds
