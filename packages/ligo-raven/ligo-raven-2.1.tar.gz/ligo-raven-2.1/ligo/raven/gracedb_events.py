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

"""
Module to define functions and attributes corresponding
to both gravitational-wave candidates and external triggers.
"""
__author__ = "Alex Urban <alexander.urban@ligo.org>"


# Imports.
import healpy as hp
import tempfile

from gracedb_sdk import Client
from ligo.skymap.io import fits


#######################################################
# Define object classes for GWs and external triggers #
#######################################################

class ExtTrig(object):
    """ Instance of an external trigger event (e.g. gamma-ray burst) """
    def __init__(self, graceid, gracedb=None, event_dict=None,
                 fitsfile='glg_healpix_all_bn_v00.fit'):
        self.graceid = graceid
        self.fits = fitsfile  # name of fits file
        self.neighbor_type = 'S'  # by default, look for superevents

        # Initiate correct instance of GraceDb.
        if gracedb is None:
            self.gracedb = Client()
        else:
            self.gracedb = gracedb

        # Check if event dictionary provided, otherwise
        # get other properties from GraceDb.
        if event_dict:
            event = event_dict
        else:
            event = self.gracedb.events[graceid].get()
        self.inst = event['pipeline']  # instrument that detected the event
        self.gpstime = float(event['gpstime'])  # event time in GPS seconds

    def submit_gracedb_log(self, message, filename=None, filecontents=None,
                           tags=[]):
        """ Wrapper for gracedb.logs() for this event """
        self.gracedb.events[self.graceid].logs.create(
            comment=message,
            filename=filename,
            filecontents=filecontents,
            tags=tags)

    def sky_map(self):
        """ Returns a numpy array equivalent to the one that would get written
            to a FITS file for this event, with resolution nside """
        kwargs = {'mode': 'w+b'}
        with tempfile.NamedTemporaryFile(**kwargs) as skymapfile:
            skymap = \
                self.gracedb.events[self.graceid].files[self.fits].get().read()
            skymapfile.write(skymap)
            skymapfile.flush()
            skymapfile.seek(0)
            self.skymap = hp.read_map(skymapfile.name)
        return self.skymap


class SE(object):
    """Instance of a superevent"""
    def __init__(self, superevent_id, event_dict=None, gracedb=None,
                 fitsfile=None):
        self.graceid = superevent_id
        self.neighbor_type = 'E'
        self.fits = fitsfile  # name of fits file

        if gracedb is None:
            self.gracedb = Client()
        else:
            self.gracedb = gracedb

        # Check if event dictionary provided, otherwise
        # get other properties from GraceDb.
        if event_dict:
            superevent = event_dict
        else:
            superevent = self.gracedb.superevents[superevent_id].get()
        self.preferred_event = superevent['preferred_event']
        self.far = superevent['far']
        self.gpstime = superevent['t_0']

        if self.fits:
            # self.sky_map = fits.read_sky_map( self.fits )
            kwargs = {'mode': 'w+b'}
            with tempfile.NamedTemporaryFile(**kwargs) as skymapfile:
                skymap = \
                    self.gracedb.events[self.graceid].files[self.fits].get()
                skymap = skymap.read()
                skymapfile.write(skymap)
                skymapfile.flush()
                skymapfile.seek(0)
                skymap = fits.read_sky_map(skymapfile.name, moc=False)[0]
                self.sky_map = skymap

    def submit_gracedb_log(self, message, filename=None, filecontents=None,
                           tags=[]):
        """ Wrapper for gracedb.logs() for this event """
        self.gracedb.superevents[self.graceid].logs.create(
            comment=message,
            filename=filename,
            filecontents=filecontents,
            tags=tags)
