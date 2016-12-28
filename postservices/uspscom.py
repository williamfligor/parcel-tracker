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


class UspsComService(TrackingService):
    """ USPS """

    name = "USPS.com"
    url = 'https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=%(number)s&qtc_senddate1=&qtc_zipcode1='

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search(r'<table[^>]*id="tc-hits".*?<tbody[^>]*>(.*?)</tbody>', html, re.DOTALL | re.UNICODE)
        if res is None:
            return []
        html = res.group(1)
        result = []
        for res in re.findall(r'<td class="date-time">\s*<p>(.*?)</p>\s*</td>\s*<td class="status">\s*(<!--.*?-->)?\s*<p[^>]*>\s*(<span[^>]*>)?(.*?)<.*?\s*(</p)?\s*</td>\s*<td class="location">\s*<p>(.*?)</td>', html, re.DOTALL | re.UNICODE):
            opdate, operation, location = (
                re.sub('\s+',
                       ' ',
                       unescape(untagify(x.strip())).replace('\n', ' '),
                       flags=re.UNICODE)
                for x in (res[0], res[3], res[5])
            )
            opdate = parsedate(opdate)
            result.append((operation, opdate, location))
        return result
