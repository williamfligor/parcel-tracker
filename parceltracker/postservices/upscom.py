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


class UpsComService(TrackingService):
    """ UPS """

    name = "UPS"
    url = 'https://wwwapps.ups.com/WebTracking/detail'
    post = 'loc=en_US&USER_HISTORY_LIST=&progressIsLoaded=N&refresh_sii=&showSpPkgProg1=true&datakey=line1&HIDDEN_FIELD_SESSION=%(session)s&multiship=true&descValue%(number)s=&trackNums=%(number)s'

    def _get_page(self):
        super(UpsComService, self)._fetch_url('http://www.ups.com/?Site=Corporate&cookie=us_en_home&setCookie=yes', None, {})
        return super(UpsComService, self)._fetch_url(
            'https://wwwapps.ups.com/WebTracking/track?%(params)s&trackNums=%(number)s&track.x=Track'
                % {"params": "HTMLVersion=5.0&loc=en_US&Requester=UPSHome&WBPM_lid=homepage%2Fct1.html_pnl_trk", "number": self.number},
            None,
            {"Cookie": self.cookie})

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search('<div id="collapse3".*?<table[^>]*>(.*?)</table>', html, re.DOTALL)
        if res is None:
            return []
        html = res.group(1)
        result = []
        for res in re.findall('<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>([^<]*)</', html, re.DOTALL):
            location, opdate, optime, action = (x.strip() for x in res)
            optime = optime.replace('.M.', 'M')  # A.M. -> AM
            opdate = parsedate('%s %s' % (opdate, optime))
            action = re.sub('\s+', ' ', action)
            location = re.sub('\s+', ' ', location)
            result.append((action, opdate, location))
        return result
