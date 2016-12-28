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


class PrivpakSchenkerNuService(TrackingService):
    """Swedish "Schenker PrivPak" service"""

    name = "privpak.schenker.nu"
    url = 'http://privpakportal.schenker.nu/TrackAndTrace/packagesearch.aspx?packageid=%(number)s&referenceid='

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search(r'<table[^>]*class="result".*?</th>\s*(<tr.*?)</table>', html, re.DOTALL)

        if res is None:
            return []
        html = res.group(1)
        result = []
        for res in re.findall('<tr[^>]*>\s*<td[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>', html, re.DOTALL):
            location, opdate, action = (x.strip() for x in res)
            opdate = parsedate(opdate)

            action = re.sub('\s+', ' ', action)
            location = re.sub('\s+', ' ', location)
            result.append((action, opdate, location))
        return result


class SchenkerNuService(TrackingService):
    """Swedish "Schenker" service"""

    name = "was.schenker.nu"
    url = 'https://was.schenker.nu/ctts-a/com.dcs.servicebroker.http.HttpXSLTServlet?request.service=CTTSTYPEA&request.method=search&clientid=&language=sv&country=SE&reference_type=*DWB&reference_number=%(number)s'

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search(r'<table.*?class="lightBlueBackground".*?<td class="tableheadline">.*?</tr>(.*?)\s*<tr>', html, re.DOTALL)

        if res is None:
            return []
        html = res.group(1)
        result = []
        for res in re.findall(r'<tr.*?<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>.*?</tr>', html, re.DOTALL | re.IGNORECASE | re.UNICODE):
            action, location, country, date = (x.replace('&nbsp;', " ").replace('<br/>', "").strip() for x in res)
            opdate = parsedate(date)
            action = re.sub('<.*?>', '', re.sub('\s+', ' ', action))
            location = re.sub('\s+', ' ', '%s, %s' % (location, country))

            result.append((action, opdate, location))
        return result
