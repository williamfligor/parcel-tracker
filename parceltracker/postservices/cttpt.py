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


class CttPtService(TrackingService):
    """Portuguese ctt.pt post"""

    name = "ctt.pt"
    url = "http://www.ctt.pt/feapl_2/app/open/objectSearch/objectSearch.jspx"
    post = "pesqObjecto.objectoId=%(number)s&showResults=true"

    def _get_page(self):
        self._fetch_url("http://www.ctt.pt/feapl_2/app/open/objectSearch/objectSearch.jspx?lang=01", data=None, headers={}, use_cookies=True)
        return super(CttPtService, self)._get_page()

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search(r'<h2>Resultados</h2>.*?<tr id="details_0".*?</thead>(.*?)</table>', html, re.UNICODE | re.DOTALL)
        if res is None:
            return []
        html = res.group(1)

        results = []
        curdate = None
        for date, time, action, place in re.findall(
            r'<tr>\s*(?:<tr class="group">\s*<td colspan="5">(.*?)</td>\s*</tr>)?\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>.*?</td>\s*<td>(.*?)</td>\s*<td>.*?</td>\s*</tr>',
            html, re.UNICODE | re.DOTALL
        ):
            if date:
                curdate = date
            date = parsedate('{}, {}'.format(curdate.strip(), time.strip()))
            results.append((action.strip(), date, place.strip()))
        return results
