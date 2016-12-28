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

import json
from dateutil.parser import parse as parsedate


class PpxTrackComService(TrackingService):
    """ppxtrack.com"""
    url = "http://ppxtrack.com/api/ParcelTracking/%(number)s"
    name = "PpxTrack.com"

    def _fetch_url(self, url, data, headers, use_cookies=False):
        headers.update(Accept="application/json, text/javascript, */*; q=0.01")
        return super(PpxTrackComService, self)._fetch_url(url, data, headers, use_cookies)

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        data = json.loads(html)
        result = []
        for record in data['Stops']:
            result.append((record['Description'], parsedate(record['TimeStamp']), record['Location']))
        return result
