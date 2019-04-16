from setuptools import setup, find_packages

setup(
    name='nomnom',
    version='0.0.1a',
    license='GPLv3',
    description='Quick and dirty tools to parse Last Millennium Reanalysis (LMR) data assimilation output ',

    author='S. Brewster Malevich',
    author_email='malevich@email.arizona.edu',
    url='https://github.com/brews/nomnom',

    packages=find_packages(),
    install_requires=['numpy', 'xarray', 'click', 'cartopy', 'matplotlib', 'tqdm'],

    entry_points={
        'console_scripts': [
            'nomnom = nomnom.cli:nomnom_cli',
        ]
    },
)