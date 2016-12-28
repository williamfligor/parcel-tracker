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

class CorreiosComService(TrackingService):
    """ Brazilian postal service Correios - www.correios.com """

    name = "Correios"
    url = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_LINGUA=001&P_TIPO=001&P_COD_UNI=%(number)s'
    def _parse_page(self, html):
        html = html.decode('ISO-8859-1', 'ignore')
        res = re.findall(r'<tr><td rowspan=.*?>(.*?)</td><td>(.*?)</td><td><FONT COLOR=".*?">(.*?)</font></td></tr>(?:\s*?<tr><td colspan=2>(.*?)</td></tr>)?',
                         html, re.DOTALL|re.IGNORECASE|re.UNICODE)
        result = []
        for (date, post, op, obs) in res:
            resdate = parsedate(date, dayfirst=True)
            respost = u' '.join(post.split())
            if obs:
                resop = u' '.join(op.split() + [u'-'] + obs.split())
            else:
                resop = u' '.join(op.split())
            result.append((resop, resdate, respost))
        return result

