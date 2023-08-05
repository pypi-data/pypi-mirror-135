from __future__ import print_function
from setuptools import setup, find_packages
import os
import io

PACKAGE = "lmgeo"
NAME = "Lmgeo"
DESCRIPTION = 'Python raster GIS library with low memory requirements.' 
AUTHOR = "Steven Hoek"
AUTHOR_EMAIL = 'dobedani@gmx.net'
URL = 'https://git.wur.nl/hoek008/lmgeo/'
LICENSE="LGPL"
VERSION = "1.0"

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md')

setup(
    name=NAME,
    version=VERSION,
    url=URL,
    download_url='https://git.wur.nl/hoek008/lmgeo/-/archive/master/lmgeo-master.tar.gz',
    license='LGPL',
    author=AUTHOR,
    install_requires=['pyshp>=2.1.0',
                      'pyproj>=1.9.5.1',
                      'numpy>=1.14.3',
                      'tifffile>=2019.3.18',
                      'tables>=3.5.2',
                      'netCDF4>=1.5.1.2',
                      'libtiff>=0.4.2'],
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    packages=find_packages(), 
    include_package_data=True,
    platforms='any',
    test_suite='lmgeo.tests.make_test_suite',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering']
)