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


class CanadaPostCaService(TrackingService):
    """ Canada Post service - www.canadapost.ca """

    name = "CanadaPost"
    url = 'https://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber?execution=e1s1'
    post = 'tapByTrackSearch:trackSearch:trackNumbers=%(number)s&tapByTrackSearch:trackSearch:submit_button=Track&autoScroll=&tapByTrackSearch:trackSearch_SUBMIT=1&javax.faces.ViewState='

    def _get_page(self):
        self._fetch_url('https://www.canadapost.ca/cpotools/apps/track/personal/findByTrackNumber?execution=e1s1',
                        data=None,
                        headers={'Referer': 'https://www.canadapost.ca/cpo/mc/default.jsf?LOCALE=en'},
                        use_cookies=True)
        return super(CanadaPostCaService, self)._get_page()

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search(r'<div id="eventList1">(.*?)</div>', html, re.DOTALL | re.UNICODE)
        if res is None:
            return []
        html = res.group(1)

        result = []
        res = re.findall(
            r'<fieldset[^>]*>.*?'
            r'<strong>Date.*?value="([^"]+)".*?'
            r'<strong>Time[^<]*</strong>([^<]*).*?'
            r'<strong>Location[^<]*</strong>([^<]*).*?'
            r'<strong>Description[^<]*</strong>([^<]*).*?'
            r'.*?</fieldset>',
            html,
            re.DOTALL | re.UNICODE
        )
        for (date, time, place, op) in res:
            resdate = parsedate('%s %s' % (date, time))
            op = re.sub(r'[<\n].*', '', op, flags=re.UNICODE | re.DOTALL)
            result.append((op.strip(), resdate, place.strip()))
        return result
