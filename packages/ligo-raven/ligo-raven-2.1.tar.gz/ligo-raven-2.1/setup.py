#!/usr/bin/python

#
# Project Librarian: Alex Urban
#              Graduate Student
#              UW-Milwaukee Department of Physics
#              Center for Gravitation & Cosmology
#              <alexander.urban@ligo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from setuptools import setup, find_packages


setup(
    name='ligo-raven',
    version='2.1',
    url='http://gracedb.ligo.org',
    author='Alex Urban',
    author_email='alexander.urban@ligo.org',
    maintainer="Brandon Piotrzkowski",
    maintainer_email="brandon.piotrzkowski@ligo.org",
    description='Low-latency coincidence search between external triggers and GW candidates',
    license='GNU General Public License Version 3',
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics"
    ),
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    namespace_packages=['ligo'],
    scripts=[
        'bin/raven_query',
        'bin/raven_search',
        'bin/raven_skymap_overlap',
        'bin/raven_coinc_far',
        'bin/raven_calc_signif_gracedb'
    ],
    install_requires=[
        'numpy>=1.14.5',
        'healpy!=1.12.0',  # FIXME: https://github.com/healpy/healpy/pull/457
        'gracedb-sdk',
        'matplotlib',
        'astropy',
        'astropy-healpix',
        'scipy>=0.7.2',
        'ligo.skymap>=0.1.1',
        'python-ligo-lw!=1.8.0',
        'lscsoft-glue',
        'lxml',
        'voeventlib>=1.2'
    ],
    python_requires='>=3.6',
)
