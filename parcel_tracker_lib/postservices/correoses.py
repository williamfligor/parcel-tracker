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

class CorreosEsService(TrackingService):
    """ Spanish postal service Correos - correos.es """

    name = "Correos.es"
    url = 'http://correos.es/comun/Localizador/track.asp'
    post = 'idiomaWeb=ENG&numero=%(number)s&imageField.x=0&imageField.y=0'

    def _parse_page(self, html):
        html = html.decode('utf-8', 'ignore')
        res = re.search(r'<table id="Table2".*?(<tr class="txtCabeceraTabla" align="center">.*?)</table>', html, re.DOTALL)
        if res is None:
            return []
        html = res.group(1)

        result = []
        for date, action in re.findall(r'<td[^>]*>(.*?)</td>\s*<td.*?<span[^>]*>(.*?)</span>', html, re.DOTALL):
            result.append((action.strip(), parsedate(date.strip(), dayfirst=True), ""))
        return result
