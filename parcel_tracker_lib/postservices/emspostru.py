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

import json
from datetime import datetime


class EmspostRuService(TrackingService):
    """ Russian EMS Post """

    name = "EMSPost.ru"
    url = 'http://emspost.ru/tracking.aspx/TrackOne'
    post = '{"id":"%(number)s"}'
    referer = 'http://emspost.ru/ru/tracking/'
    post_type = 'application/json; charset=utf-8'

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        try:
            html = json.loads(html)
            html = html['d']['Operations']
        except Exception, e:
            self.logger.exception(e)
            return []
        if html is None:
            return []
        result = []
        for item in html:
            result.append((item['opStatus'], datetime.strptime(item['opDateTime'], '%d.%m.%Y %H:%M'), item['opAddressDescription']))
        return result
