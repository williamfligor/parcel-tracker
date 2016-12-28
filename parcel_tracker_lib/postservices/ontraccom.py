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

from . import TrackingService, unescape, untagify

import re
from dateutil.parser import parse as parsedate


class OnTracComService(TrackingService):
    """OnTrac"""

    name = "OnTrac"
    url = 'https://www.ontrac.com/trackingres.asp?tracking_number=%(number)s'

    def _get_page(self):
        page = super(OnTracComService, self)._get_page().decode('utf-8', 'ignore')
        res = re.search('trackingdetail\.asp\?[^"]+', page)
        if res is None:
            return ""
        return self._fetch_url("https://www.ontrac.com/" + res.group(0), None, {})

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search('<div id="trkdetail">.*?<table.*?<table[^>]*>(.*?)</table>', html, re.DOTALL | re.UNICODE)
        if res is None:
            return []
        html = res.group(1)
        result = []
        for res in re.findall('<tr[^>]*?>\s*<td[^<]*?<p>(.*?)</td>\s*<td[^<]*?<p>(.*?)</td>\s*<td[^<]*?<p>(.*?)</td>', html, re.DOTALL | re.UNICODE):
            action, date, location = (untagify(unescape(x)).strip() for x in res)
            date = parsedate(date)
            result.append((action, date, location))
        return result
