import collections

import numpy as np


def read_assimilated_proxies(fl):
    """Read assimilated_proxies.npy and return list of named tuples.
    """
    x = np.load(fl)
    Proxy = collections.namedtuple('Proxy', ['name', 'proxy_type', 'lat', 'lon', 'years', 'sensitivity'])

    out = []
    for entry in x:
        for k, v in entry.items():
            
            ptype = str(k).split('_')
            if 'mgca' in ptype:
                cleaned_type = ' '.join(ptype[1:-1])
            else:
                cleaned_type = ' '.join(ptype[1:])

            p = Proxy(name=str(v[0]), proxy_type=cleaned_type,
                      lat=float(v[1]), lon=float(v[2]), 
                      years=np.array(v[3]),
                      sensitivity=str(v[4]))
            out.append(p)
    return out