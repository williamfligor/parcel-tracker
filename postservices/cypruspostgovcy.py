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
from . import unescape, untagify

import re
from dateutil.parser import parse as parsedate


class CyprusPostGovCyService(TrackingService):
    """Cyprus Post"""

    name = "Cyprus Post"
    url = "http://ips.cypruspost.gov.cy/ipswebtrack/IPSWeb_item_events.asp?itemid=%(number)s&Submit=Submit"

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')

        res = re.search(r'<tr class=tabl1>.*</table>', html, re.DOTALL | re.UNICODE)
        if res is None:
            return []
        html = res.group(0)

        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL | re.UNICODE)

        results = []
        for date, country, location, description, extra in re.findall(r'<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*.*?</tr>', html, re.DOTALL | re.UNICODE):
            op = '%s %s' % (description, extra)
            op = unescape(untagify(op.encode('utf-8'))).decode('utf-8')
            loc = '%s %s' % (country, location)
            loc = unescape(untagify(loc.encode('utf-8'))).decode('utf-8')
            results.append((op, parsedate(date, dayfirst=True), loc))
        return results
