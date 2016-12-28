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
from dateutil.parser import parse as parsedate


class CanparComService(TrackingService):
    """Canpar Courier"""

    name = "Canpar"
    url = "http://www.canpar.com/en/track/TrackingAction.do?locale=en&type=0&reference=%(number)s"

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        result = []

        res = re.search(r"<table[^>]*class='events'[^>]*>(.*?)</table>", html, re.DOTALL | re.UNICODE)
        if res is None:
            return []
        html = res.group(1)
        for (date, action, location, _) in re.findall(r'<tr[^>]*>\s*<td[^>]*>([^<]*)</td>\s*<td[^>]*>([^<]*)</td>\s*<td[^>]*>([^<]*)</td>\s*<td[^>]*>([^<]*)</td>\s*</tr>', html, re.DOTALL | re.UNICODE):
            result.append((
                re.sub('\s+', ' ', action.strip()),
                parsedate(date),
                re.sub('\s+', ' ', location.strip()),

            ))
        return result
