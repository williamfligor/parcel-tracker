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


class PostaSiService(TrackingService):
    """ Slovenian Posta """

    name = 'Posta.si'
    url = 'http://sledenje.posta.si/Default.aspx?tracenumber=%(number)s&lang=SI'

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search(r'Opis\s*</font></td></tr></table></td></tr></table><table[^>]*><tr><td><table[^>]*>(.*?)</table>', html)
        if res is None:
            return []
        html = res.group(1)
        result = []
        for res in re.findall(r'<tr[^>]*><td[^>]*><font[^>]*>(.*)</font></td><td[^>]*><font[^>]*>(.*)</font></td><td[^>]*><font[^>]*>(.*?)</font></td><td[^>]*><font[^>]*>(.*?)</font></td></tr>', html):
            result.append((res[3], datetime.strptime(res[0], '%d.%m.%Y'), res[1] + u' ' + res[2]))
        return result
