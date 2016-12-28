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
from dateutil.parser import parse as parsedate


class TransgroupComService(TrackingService):
    """Transgroup HWBs transgroup.com service"""
    name = "Transgroup"
    url = "http://transtatus.transgroup.com/GetStatus.aspx?hwb=%(number)s"

    def _parse_page(self, html):
        results = []
        try:
            js = json.loads(html)
            for status in js['statuses']:
                pieces = status['datetime'].split(' ')
                dt = parsedate('{} {}'.format(pieces[0], pieces[1]), dayfirst=False)
                loc = '' if len(pieces) == 2 else ' '.join(pieces[2:])
                results.append((status['status'], dt, loc))
        except:
            pass
        return results
