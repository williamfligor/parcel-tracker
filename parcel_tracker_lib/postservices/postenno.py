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


class PostenNoService(TrackingService):
    """ Posten Norge """

    name = "Posten.no"
    url = 'http://sporing.bring.no/sporing.json?q=%(number)s&lang=en'
    # TESTPACKAGE-AT-PICKUPPOINT is a valid tracking number for testing

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        try:
            html = json.loads(html)
            html = html['consignmentSet'][0]['packageSet'][0]['eventSet']
        except Exception, e:
            self.logger.exception(e)
            return []
        if html is None:
            return []
        result = []
        for item in html:
          result.append((item['description'], datetime.strptime(item['displayDate'] + ' ' + item['displayTime'], '%d.%m.%Y %H:%M'), item['postalCode'] + ' ' + item['city']))
        return result
