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

class TntService(TrackingService):
    """TNT service"""

    name = 'TNT'
    url = 'http://www.tnt.com/webtracker/tracking.do'
    post = 'cons=%(number)s'

    def _parse_page(self, html):
        html = html.decode('utf-8')
        res = re.search(r'<table[^>]*class="appTable">.*?<table[^>]*class="appTable">.*?</tr>(.*?)</tbody>', html, re.DOTALL)
        if res is None:
            return []
        return [
                (oper.strip(), parsedate('%s %s' % (date.strip(), time.strip())), loc.strip())
                for date, time, loc, oper
                in re.findall(r'<tr.*?<td[^>]*>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>', res.group(1), re.DOTALL)
                ]
