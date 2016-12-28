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


class HermesWorldTrackingService(TrackingService):
    """Hermes World Germany Service"""

    name = "Hermes World"
    url = 'https://tracking.hermesworld.com/SISYRestAPIWebApp/V1/sisy-rs/GetHistoryByID?id=%(number)s&lng=en&token=%(token)s'

    def _get_page(self):
        headers = {
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        }
        page = self._fetch_url('https://tracking.hermesworld.com/js/script.js', data=None, headers={}).decode('utf-8', 'ignore')
        token = re.findall(r"this.token = '(.*?)'", page, re.UNICODE)[0]

        url = self.url % {'number': self.number, 'token': token}
        return self._fetch_url(url, data=None, headers=headers)

    def _parse_page(self, js):
        js = json.loads(js)
        if 'status' not in js:
            return []
        js = js['status']
        res = []
        for record in js:
            res.append((
                record['statusDescription'].strip(),
                parsedate('{} {}'.format(record['statusDate'].strip(), record['statusTime'].strip()), dayfirst=True),
                '{} {}, {}'.format(record['zipCode'], record['countryCode'].strip(), record['city'].strip()),
            ))
        return res
