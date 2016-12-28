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


class BelpostByService(TrackingService):
    """Belpochta"""

    name = "Belpost.by"
    url = "http://search.belpost.by/ajax/search"
    post = "item=%(number)s&internal=%(internal)s"

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        result = []
        for res in re.findall(r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>', html, re.DOTALL | re.UNICODE):
            result.append((re.sub('<[^>]*>', '', res[1]), parsedate(res[0], dayfirst=True), ''))
        return result

    def fetch(self):
        self.additional_fields = {'internal': '1'}
        data = super(BelpostByService, self).fetch()
        self.additional_fields = {'internal': '2'}
        data += super(BelpostByService, self).fetch()
        return data
