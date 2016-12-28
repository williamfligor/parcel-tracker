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


class PostdanmarkDkService(TrackingService):
    """ Danmark post """

    name = 'PostDanmark.dk'
    url = 'http://www.postdanmark.dk/tracktrace/TrackTrace.do?i_lang=INE&i_stregkode=%(number)s'

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search(r'<tbody>(.*?)</tbody>', html, re.DOTALL)
        if res is None:
            return []
        html = res.group(1)
        results = []
        for res in re.findall(r'<tr>.*?<td[^>]*>(.*?)</td>.*?<td[^>]*>(.*?)</td>.*?<td[^>]*>(.*?)</td>.*?</tr>', html, re.DOTALL):
            results.append((res[2], parsedate(res[0] + u' ' + res[1]), ''))
        return results

