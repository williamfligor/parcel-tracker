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
import urllib
from dateutil.parser import parse as parsedate


class IParcelComService(TrackingService):
    """i-parcel.com service"""

    name = "i-parcel"
    url = "https://tracking.i-parcel.com/Home/Index?__EVENTVALIDATION=%(eventvalidation)s&trackingnumber=%(number)s"

    def _get_page(self):
        page = self._fetch_url('https://tracking.i-parcel.com/Home/Index?trackingnumber=INVALID', data=None, headers={}, use_cookies=True).decode('utf-8')
        eventvalidation = urllib.quote(re.findall(r'name="__EVENTVALIDATION".*?value="([^"]*)"', page, re.DOTALL | re.IGNORECASE | re.UNICODE)[0], '')
        self.additional_fields = {
            'eventvalidation': eventvalidation,
        }
        return super(IParcelComService, self)._get_page()

    def _parse_page(self, html):
        html = html.decode('utf-8')
        res = re.search(r"<thead><b>Details.*?<tbody>(.*?)</tbody>", html, re.UNICODE | re.DOTALL)
        if res is None:
            return []
        html = res.group(1)
        results = []
        for action, date, city, state, country in re.findall(r'<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>', html, re.UNICODE | re.DOTALL):
            results.append((
                action.strip(),
                parsedate(date, dayfirst=False),
                ', '.join(filter(bool, (country, state, city)))
            ))
        return results
