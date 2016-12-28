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
from datetime import datetime


class SwisspostChService(TrackingService):
    """ Swiss Post """

    name = "SwissPost.ch"
    url = 'https://www.post.ch/EasyTrack/submitParcelData.do?p_language=en&VTI-GROUP=1&directSearch=false&formattedParcelCodes=%(number)s'

    def _parse_page(self, html):
        res = re.search(r'<tbody>[\s\n\r]*(<tr class="(row_fullview_tablerow_grey)?">[\s\n\r]*<td class="event_date">.*?)</tbody>', html, re.DOTALL)
        if res is None:
            return []
        html = res.group(1)
        results = []
        for res in re.findall(r'<td\s*class="event_date"><span.*?</span>(.*?)</td>.*?<td class="event_time">(.*?)</td>.*?<td class="event_event">(.*?)</td>.*?<td class="event_city">(.*?)</td>', html, re.DOTALL):
            resdate = re.sub('<([^ ]*)[^>]*>.*?</\1>', '', res[0].strip() + " " + res[1].strip())
            resdate = datetime.strptime(resdate, '%d.%m.%Y %H:%M')
            operation = re.sub('<([^ ]*)[^>]*>.*?</\\1>', '', res[2])
            results.append((operation, resdate, res[3].strip()))
        return results
