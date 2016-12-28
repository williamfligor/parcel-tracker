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
import datetime
import urllib
from dateutil.parser import parse as parsedate


class CorreosDeMexicoGobMxService(TrackingService):
    """Correos de México post service"""

    name = 'Correos de México'
    url = 'http://www.correosdemexico.gob.mx/lservicios/seguimientoen/emsportalen.aspx'

    def _get_page(self):
        url = 'http://www.correosdemexico.gob.mx/English/Paginas/track.aspx'
        page = self._fetch_url(url, data=None, headers={}, use_cookies=True).decode('iso-8859-1')
        url = 'http://www.correosdemexico.gob.mx/lservicios/seguimientoen/emsportalen.aspx'
        page = self._fetch_url(url, data=None, headers={}, use_cookies=True).decode('iso-8859-1')
        viewstate = urllib.quote(re.findall(r'name="__VIEWSTATE".*?value="([^"]*)"', page, re.DOTALL | re.IGNORECASE | re.UNICODE)[0], '')
        eventvalidation = urllib.quote(re.findall(r'name="__EVENTVALIDATION".*?value="([^"]*)"', page, re.DOTALL | re.IGNORECASE | re.UNICODE)[0], '')
        self.post = '&'.join(['__EVENTTARGET=',
                              '__EVENTARGUMENT=',
                              '__VIEWSTATE=%(viewstate)s',
                              '__EVENTVALIDATION=%(eventvalidation)s',
                              'txtNGuia=%(number)s',
                              'cboanio=%(year)s',
                              'btnFind.x=32',
                              'btnFind.y=5'])
        self.additional_fields = {
            'viewstate': viewstate,
            'eventvalidation': eventvalidation,
            'year': datetime.date.today().year
        }
        return super(CorreosDeMexicoGobMxService, self)._get_page()

    def _parse_page(self, html):
        html = html.decode('iso-8859-1')
        res = re.search(r'<tr class="dgHeader">(.*?)</table>', html, re.DOTALL | re.UNICODE)
        if res is None:
            return []
        html = res.group(1)
        results = []
        for date, time, place, event in re.findall(r'<tr class="dgNormal".*?<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>', html, re.UNICODE | re.DOTALL):
            date = parsedate('{} {}'.format(date, time), dayfirst=True)
            results.append((event, date, place))
        return results
