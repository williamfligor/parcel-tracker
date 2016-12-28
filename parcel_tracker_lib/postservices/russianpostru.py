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

import json
from dateutil.parser import parse as parsedate


class RussianpostRuService(TrackingService):
    """ Russian post """

    name = 'RussianPost.ru'
    url = 'https://www.pochta.ru/tracking?p_p_id=trackingPortlet_WAR_portalportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&barcodeList=%(number)s&postmanAllowed=true&_=1455882430642'

    def _get_page(self):
        self._fetch_url('https://www.pochta.ru/tracking', data=None, headers={}, use_cookies=True)
        return super(RussianpostRuService, self)._get_page()

    def _parse_page(self, js):
        js = json.loads(js)
        try:
            js = list(js['list'][0]['trackingItem']['trackingHistoryItemList'])
        except (TypeError, KeyError, AttributeError):
            return []

        result = []
        for row in js:
            date = parsedate(row['date'])
            op = row['humanStatus']
            location = filter(None, (row['index'], row['countryName'], row['cityName'], row['description']))
            location = u' '.join(unicode(l) for l in location)

            result.append((op, date, location))
        return result
