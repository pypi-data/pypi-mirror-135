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
Module containing time- and sky- coincidence search functions.
"""
__author__ = "Alex Urban <alexander.urban@ligo.org>"


# Imports.
import json
import os
import re
import sys

import healpy as hp
import numpy as np

from .gracedb_events import SE, ExtTrig
from gracedb_sdk import Client


#########################################################
# Functions implementing the actual coincidence search. #
#########################################################

def query(event_type, gpstime, tl, th, gracedb=None, group=None,
          pipelines=[], searches=[]):
    """ Query for coincident events of type event_type occurring within a
        window of [tl, th] seconds around gpstime. """

    # Perform a sanity check on the time window.
    if tl >= th:
        sys.stderr.write("ERROR: The time window [tl, th] must have tl < th.")
        sys.exit(1)

    # Initiate instance of GraceDb if not given.
    if gracedb is None:
        gracedb = Client('https://gracedb.ligo.org/api/')

    # Perform the GraceDB query.
    start, end = gpstime + tl, gpstime + th

    if event_type == 'External':  # Searching for external events
        arg = '{0} {1} .. {2}{3}'.format(event_type, start, end,
                                         ' MDC' if 'MDC' in searches else '')
        # Return list of graceids of coincident events.
        results = list(gracedb.events.search(query=arg))
        if pipelines:
            results = [event for event in results if event['pipeline']
                       in pipelines]
        if searches:
            results = [event for event in results if
                       event['search'] in searches]
        return results

    elif event_type == 'Superevent':  # Searching for superevents
        arg = '{0} .. {1}{2}'.format(start, end,
                                     ' MDC' if 'MDC' in searches else '')
        # Return list of coincident superevent_ids.
        results = list(gracedb.superevents.search(query=arg))
        if group:
            results = [superevent for superevent in results if
                       superevent['preferred_event_data']['group'] == group]
        return results


def search(gracedb_id, tl, th, gracedb=None, group=None, pipelines=None,
           searches=[], event_dict=None):
    """ Perform a search for neighbors coincident in time within
        a window [tl, th] seconds around an event. Uploads the
        results to the selected gracedb server. """

    # Identify neighbor types with their graceid strings.
    types = {'G': 'GW', 'E': 'External', 'S': 'Superevent',
             'T': 'Test'}
    groups = {'G': 'CBC Burst', 'E': 'External', 'S': 'Superevent'}

    # Initiate correct instance of GraceDb.
    if gracedb is None:
        gracedb = Client()

    # Load in event
    if 'S' in gracedb_id:
        event = SE(gracedb_id, gracedb=gracedb, event_dict=event_dict)
    else:
        event = ExtTrig(gracedb_id, gracedb=gracedb, event_dict=event_dict)

    # Grab any and all neighboring events.
    # Filter results depending on the group if specified.
    neighbors = query(groups[event.neighbor_type], event.gpstime, tl, th,
                      gracedb=gracedb, group=group, pipelines=pipelines,
                      searches=searches)

    # If no neighbors, report a null result.
    if not neighbors:
        if 'S' in gracedb_id:
            message = "RAVEN: No {0} {1}{2}candidates in window ".format(
                          types[event.neighbor_type],
                          str(pipelines) + ' ' if pipelines else '',
                          str(searches) + ' ' if searches else '')
            message += "[{0}, +{1}] seconds".format(tl, th)
        else:
            message = "RAVEN: No {0} {1}{2}candidates in window ".format(
                          types[event.neighbor_type],
                          str(group) + ' ' if group else '',
                          'MDC ' if 'MDC' in searches else '')
            message += "[{0}, +{1}] seconds".format(tl, th)
        event.submit_gracedb_log(message, tags=["ext_coinc"])

    # If neighbors are found, report each of them.
    else:
        for neighbor in neighbors:
            if event.neighbor_type == 'S':
                # search called on a external event
                deltat = event.gpstime - neighbor['t_0']
                superid = neighbor['superevent_id']
                extid = event.graceid
                tl_m, th_m = tl, th
                relat_word = ['before', 'after']
                exttrig = event
                se = SE(superid, gracedb=gracedb, event_dict=neighbor)
            else:
                # search called on a superevent
                deltat = event.gpstime - neighbor['gpstime']
                superid = event.graceid
                extid = neighbor['graceid']
                tl_m, th_m = -th, -tl
                relat_word = ['after', 'before']
                se = event
                exttrig = ExtTrig(extid, gracedb=gracedb, event_dict=neighbor)
            if deltat < 0:
                relat_word.reverse()
                deltat = abs(deltat)
            selink = 'superevents/'
            extlink = 'events/'
            gracedb_url = re.findall('(.*)api/', gracedb.url)[0]

            # Send message to external event
            message1 = "RAVEN: {0} {1}{2}candidate <a href='{3}{4}".format(
                types['S'],
                str(group) + ' ' if group else '',
                'MDC ' if 'MDC' in searches else '',
                gracedb_url, selink)
            message1 += "{0}'>{1}</a> within [{2}, +{3}] seconds".format(
                            superid, superid,
                            tl_m, th_m)
            message1 += ", about {0:.3f} second(s) {1} {2} event".format(
                            float(deltat),
                            relat_word[0],
                            types['E'])
            exttrig.submit_gracedb_log(message1, tags=["ext_coinc"])

            # Send message to superevent
            message2 = "RAVEN: {0} {1}{2}event <a href='{3}{4}".format(
                types['E'],
                str(pipelines) + ' ' if pipelines else '',
                str(searches) + ' ' if searches else '',
                gracedb_url, extlink)
            message2 += "{0}'>{1}</a> within [{2}, +{3}] seconds".format(
                            extid, extid, -th_m, -tl_m)
            message2 += ", about {0:.3f} second(s) {1} {2}".format(
                            float(deltat),
                            relat_word[1],
                            types['S'])
            se.submit_gracedb_log(message2, tags=["ext_coinc"])

    # Return search results.
    return neighbors


def skymap_overlap_integral(se_skymap, exttrig_skymap):
    """ Calculate the sky map overlap integral of the two sky maps. """

    nside_s = hp.npix2nside(len(se_skymap))
    nside_e = hp.npix2nside(len(exttrig_skymap))
    if nside_s > nside_e:
        exttrig_skymap = hp.ud_grade(exttrig_skymap, nside_out=nside_s)
    else:
        se_skymap = hp.ud_grade(se_skymap, nside_out=nside_e)
    se_norm = se_skymap.sum()
    exttrig_norm = exttrig_skymap.sum()
    if se_norm > 0 and exttrig_norm > 0:
        skymap_overlap_integral = (
            np.dot(se_skymap, exttrig_skymap)
            / se_norm / exttrig_norm
            * len(se_skymap))
        return skymap_overlap_integral
    else:
        message = ("RAVEN: ERROR: At least one sky map has a probability "
                   "density that sums to zero or less.")
        return message


def coinc_far(se_id, exttrig_id, tl, th, grb_search='GRB', se_fitsfile=None,
              ext_fitsfile='glg_healpix_all_bn_v00.fit', incl_sky=False,
              gracedb=None, far_grb=None, em_rate=None,
              se_dict=None, ext_dict=None):
    """ Calculate the significance of a gravitational wave candidate with the
        addition of an external astrophyical counterpart in terms of a
        coincidence false alarm rate. This includes a temporal and a
        space-time type. """

    # Create the SE and ExtTrig objects based on string inputs.
    se = SE(se_id, fitsfile=se_fitsfile, gracedb=gracedb, event_dict=se_dict)
    exttrig = ExtTrig(exttrig_id, fitsfile=ext_fitsfile, gracedb=gracedb,
                      event_dict=ext_dict)

    # Is the GW superevent candidate's FAR sensible?
    if not se.far:
        message = ("RAVEN: WARNING: This GW superevent candidate's FAR is a "
                   " NoneType object.")
        return message

    # The combined rate of independent GRB discovery by Swift, Fermi,
    # INTEGRAL, and AGILE MCAL
    # Fermi: 236/yr
    # Swift: 65/yr
    # INTEGRAL: ~5/yr
    # AGILE MCAL: ~5/yr
    gcn_rate = 310. / (365. * 24. * 60. * 60.)

    # Check if given an em rate first, intended for offline use
    if em_rate:
        temporal_far = (th - tl) * em_rate * se.far
    # Otherwise calculate FAR using vetted rate based on search
    elif grb_search in {'GRB', 'MDC'}:
        temporal_far = (th - tl) * gcn_rate * se.far

    elif grb_search == 'SubGRB':
        # Rate of subthreshold GRBs (rate of threshold plus rate of
        # subthreshold). Introduced based on an analysis done by
        # Peter Shawhan: https://dcc.ligo.org/cgi-bin/private/
        #                DocDB/ShowDocument?docid=T1900297&version=
        gcn_rate += 65. / (365. * 24. * 60. * 60.)
        temporal_far = (th - tl) * gcn_rate * se.far

    elif grb_search == 'SubGRBTargeted':
        # Max FARs considered in analysis
        if exttrig.inst == 'Fermi':
            far_gw_thresh = 1 / (3600 * 24)
            far_grb_thresh = 1 / 10000
        elif exttrig.inst == 'Swift':
            far_gw_thresh = 2 / (3600 * 24)
            far_grb_thresh = 1 / 1000
        else:
            raise AssertionError(("Only Fermi or Swift are valid "
                                  "pipelines for joint sub-threshold "
                                  "search"))
        # Map the product of uniformly drawn distributions to CDF
        # See https://en.wikipedia.org/wiki/Product_distribution
        z = (th - tl) * far_grb * se.far
        z_max = (th - tl) * far_grb_thresh * far_gw_thresh
        temporal_far = z * (1 - np.log(z/z_max))

    else:
        message = ("RAVEN: WARNING: Invalid search. RAVEN only considers "
                   "'GRB', 'SubGRB', and 'SubGRBTargeted'.")
        return message

    # Include sky coincidence if desired.
    if incl_sky:
        se_skymap = se.sky_map
        exttrig_skymap = exttrig.sky_map()
        skymap_overlap = skymap_overlap_integral(se_skymap, exttrig_skymap)
        if isinstance(skymap_overlap, str):
            return skymap_overlap
        try:
            spatiotemporal_far = temporal_far / skymap_overlap
        except ZeroDivisionError:
            message = ("RAVEN: WARNING: Sky maps minimally overlap. "
                       "Sky map overlap integral is {0:.2e}. "
                       "There is strong evidence against these events being "
                       "coincident.").format(skymap_overlap)
            return message
    else:
        spatiotemporal_far = None

    return {"temporal_coinc_far": temporal_far,
            "spatiotemporal_coinc_far": spatiotemporal_far,
            "preferred_event": se.preferred_event,
            "external_event": exttrig.graceid}


def calc_signif_gracedb(se_id, exttrig_id, tl, th, grb_search='GRB',
                        se_fitsfile=None,
                        ext_fitsfile='glg_healpix_all_bn_v00.fit',
                        incl_sky=False, gracedb=None, far_grb=None,
                        em_rate=None, se_dict=None, ext_dict=None):
    """ Calculates and uploads the coincidence false alarm rate
        of the given superevent to the selected gracedb server. """

    # Create the SE and ExtTrig objects based on string inputs.
    se = SE(se_id, fitsfile=se_fitsfile, gracedb=gracedb, event_dict=se_dict)
    exttrig = ExtTrig(exttrig_id, fitsfile=ext_fitsfile, gracedb=gracedb,
                      event_dict=ext_dict)

    # Create coincidence_far.json
    coinc_far_output = coinc_far(se_id, exttrig_id, tl, th,
                                 grb_search=grb_search,
                                 se_fitsfile=se_fitsfile,
                                 ext_fitsfile=ext_fitsfile,
                                 incl_sky=incl_sky, gracedb=gracedb,
                                 far_grb=far_grb, em_rate=em_rate,
                                 se_dict=se_dict, ext_dict=ext_dict)
    if isinstance(coinc_far_output, str):
        se.submit_gracedb_log(coinc_far_output, tags=["ext_coinc"])
        exttrig.submit_gracedb_log(coinc_far_output, tags=["ext_coinc"])
        raise ZeroDivisionError(coinc_far_output)
    coincidence_far = json.dumps(coinc_far_output)

    gracedb_events_url = re.findall('(.*)api/', se.gracedb.url)[0]
    link1 = 'events/'
    link2 = 'superevents/'

    with open('coincidence_far.json', 'w+') as fp:
        fp.write(coincidence_far)
        fp.flush()
        fp.seek(0)
        message = ("RAVEN: Computed coincident FAR(s) in Hz with external "
                   "trigger <a href='{0}").format(gracedb_events_url + link1)
        message += "{0}'>{1}</a>".format(exttrig.graceid, exttrig.graceid)
        se.submit_gracedb_log(message, filename='coincidence_far.json',
                              filecontents=coincidence_far,
                              tags=["ext_coinc"])

        message = ("RAVEN: Computed coincident FAR(s) in Hz with superevent "
                   "<a href='{0}").format(gracedb_events_url + link2)
        message += "{0}'>{1}</a>".format(se.graceid, se.graceid)
        exttrig.submit_gracedb_log(message, filename='coincidence_far.json',
                                   filecontents=coincidence_far,
                                   tags=["ext_coinc"])
    os.remove('coincidence_far.json')

    return coinc_far_output
