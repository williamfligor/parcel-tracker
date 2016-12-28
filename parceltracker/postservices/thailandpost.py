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


class ThailandPostCoThService(TrackingService):
    """Thailand Post service"""

    name = 'ThailandPost'
    url = 'http://track.thailandpost.co.th/trackinternet/Default.aspx?lang=en'
    post = '__EVENTTARGET=Login&__VIEWSTATE=%(viewstate)s&__EVENTVALIDATION=%(eventvalidation)s&TextBarcode=%(number)s&Login.y=6&Login.x=48'

    def __init__(self, number):
        super(ThailandPostCoThService, self).__init__(number)
        self.additional_fields = {}

    def _get_page(self):
        page = self._fetch_url(self.url, data=None, headers={}, use_cookies=True).decode('cp874', 'ignore')
        viewstate = urllib.quote(re.findall(r'name="__VIEWSTATE".*?value="([^"]*)"', page, re.DOTALL | re.IGNORECASE | re.UNICODE)[0], '')
        eventvalidation = urllib.quote(re.findall(r'name="__EVENTVALIDATION".*?value="([^"]*)"', page, re.DOTALL | re.IGNORECASE | re.UNICODE)[0], '')

        self.additional_fields.update({
            'viewstate': viewstate,
            'eventvalidation': eventvalidation,
        })
        return super(ThailandPostCoThService, self)._get_page()

    def _parse_page(self, html):
        html = html.decode('cp874', 'ignore')
        res = re.search(r'<b>Description</b>.*?</tr>(.*?)</table>', html, re.DOTALL | re.IGNORECASE | re.UNICODE)
        if res is None:
            return []
        html = res.group(1)

        results = []
        for (date, location, action) in re.findall(r'<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>', html, re.DOTALL | re.IGNORECASE | re.UNICODE):
            location = re.sub('</?font[^>]*>', '', location)
            action = re.sub('</?font[^>]*>', '', action)
            date = re.sub('</?font[^>]*>', '', date)
            date = ' '.join(date.split(' <br> '))
            date = parsedate(date)
            results.append((action, date, location))
        return results
