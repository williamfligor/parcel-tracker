#!/usr/bin/env python
# -*- coding: utf-8 -*-

### BEGIN LICENSE
# Copyright © 2012-2016 Vsevolod Velichko <torkvema@gmail.com>
# Copyright © 2012 Carlos da Costa <c.costa@outlook.com>
# Copyright © 2012-2013 Erik Christiansson <erik@christiansson.net>
# Copyright © 2013 Pål Sollie <sollie@sparkz.no>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from . import TrackingService

import re
import json
from dateutil.parser import parse as parsedate


class DhlActiveTrackingService(TrackingService):
    """DHL Active Tracking service"""

    name = 'DHL Active Tracking'
    url = 'https://activetracing.dhl.com/DatPublic/datSelection.do'
    post = 'search=consignmentId&at=cons_ordercode&valueShipmentOrderField=%(number)s&focus=search2&searchConsignmentId=track'

    def _parse_page(self, html):
        html = html.decode('utf-8')

        res = re.search(r'<table[^>]*id="sendungsHistorieOne"[^>]*>(.*?)</table>', html, re.DOTALL)
        if res is None:
            return []
        html = res.group(1)
        return [(r[0], parsedate(r[2]), r[1]) for r in re.findall(r'<tr[^>]*>\s*<td[^>]*>.*?</td>\s*<td[^>]*>\s*(.*?)\s*</td>\s*<td[^>]*>\s*<a[^>]*>\s*(.*?)\s*</a>\s*</td>\s*<td[^>]*>\s*(.*?)\s*</td>\s*</tr>', html, re.DOTALL)]


class DhlDeService(TrackingService):
    """DHL Germany service"""

    name = 'DHL Germany'
    url = 'http://nolp.dhl.de/nextt-online-public/set_identcodes.do?lang=en&idc=%(number)s&rfn=&extendedSearch=true'

    def _parse_page(self, html):
        html = html.decode('utf-8')
        res = re.search(r'<tr>\s*<th>Date/Time</th>.*?<tbody>(.*?)</tbody>', html, re.DOTALL | re.UNICODE)
        if res is None:
            return []
        html = res.group(1)
        html = re.sub(r'<!--.*?-->', '', html, re.DOTALL)
        html = re.sub(r'<div[^>]*>', '', html)
        html = re.sub(r'</div>', '', html)
        results = []
        for res in re.findall(r'<tr[^>]*>\s*<td[^>]*>\s*(.*?)\s*</td>\s*<td[^>]*>\s*(.*?)\s*</td>\s*<td[^>]*>\s*(.*?)\s*</td>\s*</tr>', html, re.DOTALL):
            date = re.sub(r'\s+', ' ', res[0].strip())
            date = date[4:-1].strip()  # remove DOW from start and 'h' from end
            date = parsedate(date, dayfirst=True)
            location = re.sub(r'\s+', ' ', res[1].strip())
            operation = re.sub(r'\s+', ' ', res[2].strip())
            results.append((operation, date, location))

        return results


class DhlmultishippingSeService(TrackingService):
    """DHL shipments that are not parcels"""
    name = 'DHLMultishipping.se'
    url = 'http://www.dhlmultishipping.se/customers/dhl/parcelevents_status.jsp?consignmentNo=%(number)s&lang=en'

    def _parse_page(self, html):
        html = html.decode('utf-8')
        res = re.search(r'<table[^>]*>.*?</tr>(.*?)</table>', html, re.DOTALL)
        if res is None:
            return []
        html = res.group(1)
        results = []
        for res in re.findall(r'<tr[^>]*>.*?<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>', html, re.DOTALL):
            action = res[1].strip()
            date = parsedate(res[3].strip())
            location = res[4].strip()
            results.append((action, date, location))
        return results


class DhlComService(TrackingService):
    """DHL Global service"""

    name = 'DHL Global'
    url = 'http://www.dhl.com/shipmentTracking?AWB=%(number)s&countryCode=g0&languageCode=en'

    def _parse_page(self, js):
        js = json.loads(js)
        try:
            js = list(js['results'][0]['checkpoints'])
        except (TypeError, KeyError, AttributeError):
            return []

        results = []
        for res in reversed(js):
            loc = res['location']
            date = parsedate('%s, %s' % (res['time'], res['date']))
            op = res['description']

            results.append((op, date, loc))

        return results
