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

class UkrposhtaComService(TrackingService):
    """ Ukrainian post """

    name = "Ukrposhta.com"
    url = 'http://services.ukrposhta.com/barcodestatistic/Default.aspx?culture=en'
    referer = url
    __boundary = '--kekeke'
    post_type = 'multipart/form-data; boundary=' + __boundary

    def __init__(self, *kargs, **kwargs):
        super(UkrposhtaComService, self).__init__(*kargs, **kwargs)
        postdata = []
        postdata.append('--' + self.__boundary)
        postdata.append('Content-Disposition: form-data; name="%s"' % '__VIEWSTATE')
        postdata.append('')
        postdata.append('/wEPDwUKMTY4MjI1MTAyMw9kFgJmD2QWAgIDDxYCHgdlbmN0eXBlBRNtdWx0aXBhcnQvZm9ybS1kYXRhFgYCAQ8WAh4FY2xhc3MFBmxvZ29VS2QCBQ8PF'
                        + 'gIeBFRleHQFaNCS0ZbQtNGB0YLQtdC20LXQvdC90Y8g0L/QtdGA0LXRgdC40LvQsNC90L3RjyDQv9C+0YjRgtC+0LLQuNGFINCy0ZbQtNC/0YDQsNCy0L'
                        + 'vQtdC90YwgKNGB0L/QuNGB0LrQsNC80LgpZGQCBw9kFiYCAw8PFgIfAgUe0KjQsNC90L7QstC90ZYg0LrQu9GW0ZTQvdGC0LghZGQCBQ8WAh4JaW5uZXJ'
                        + 'odG1sBa0C0JLQuCDQvNC+0LbQtdGC0LUg0LTRltC30L3QsNGC0LjRgdGPINC/0YDQviDQvNGW0YHRhtC10LfQvdCw0YXQvtC00LbQtdC90L3RjyDQv9C+'
                        + '0YjRgtC+0LLQuNGFINCy0ZbQtNC/0YDQsNCy0LvQtdC90YwgKNGB0L/QuNGB0LrQsNC80LgpLCDRidC+INGA0L7Qt9GI0YPQutGD0Y7RgtGM0YHRjywg0'
                        + 'YMg0LHRg9C00Ywt0Y/QutC40Lkg0LfRgNGD0YfQvdC40Lkg0LTQu9GPINCS0LDRgSDRh9Cw0YEuPGJyIC8+PGJyIC8+DQrQhtC90YTQvtGA0LzQsNGG0Z'
                        + 'bRjiDQvNC+0LbQvdCwINC+0YLRgNC40LzQsNGC0Lgg0L/RgNC+OjxiciAvPmQCBw8WAh8DBbQCLSDQstC90YPRgtGA0ZbRiNC90ZYg0YDQtdGU0YHRgtG'
                        + 'A0L7QstCw0L3RliDQv9C+0YjRgtC+0LLRliDQstGW0LTQv9GA0LDQstC70LXQvdC90Y8sINGJ0L4g0L/QtdGA0LXRgdC40LvQsNGO0YLRjNGB0Y8g0LIg'
                        + '0LzQtdC20LDRhSDQo9C60YDQsNGX0L3QuDs8YnIgLz4NCi0g0LzRltC20L3QsNGA0L7QtNC90ZYg0YDQtdGU0YHRgtGA0L7QstCw0L3RliDQv9C+0YjRg'
                        + 'tC+0LLRliDQstGW0LTQv9GA0LDQstC70LXQvdC90Y8sINGJ0L4g0L/QtdGA0LXRgdC40LvQsNGO0YLRjNGB0Y8g0LfQsCDQvNC10LbRliDQo9C60YDQsN'
                        + 'GX0L3QuC48YnIgLz5kAgkPDxYCHwIFVtCU0LvRjyDQvtGC0YDQuNC80LDQvdC90Y8g0LTQvtCy0ZbQtNC60L7QstC+0Zcg0ZbQvdGE0L7RgNC80LDRhtG'
                        + 'W0Zcg0L3QsNGC0LjRgdC90ZbRgtGMZGQCCw8WBB4EaHJlZgVGRG93bmxvYWRJbmZvLmFzcHg/aGlkZGVuU2Vzc2lvbklkPTJlYWNhZDc1LTJmZmMtNDU5'
                        + 'Ni1iMmNjLTRlODdhNTI5OTIzNB8DBQbQotGD0YJkAg0PDxYCHwIFmwHQl9Cw0LLQsNC90YLQsNC20YLQtSDRhNCw0LnQuyDQtyDRiNGC0YDQuNGF0LrQv'
                        + 'tC00LDQvNC4INC30LAg0LTQvtC/0L7QvNC+0LPQvtGOINC60L3QvtC/0LrQuCAi0J7QsdC30L7RgCIg0YLQsCDQvdCw0YLQuNGB0L3RltGC0Ywg0LrQvd'
                        + 'C+0L/QutGDICLQn9C+0YjRg9C6ImRkAg8PDxYCHwIFXdCc0LDQutGB0LjQvNCw0LvRjNC90L4g0LTQvtC/0YPRgdGC0LjQvNCwINC60ZbQu9GM0LrRltG'
                        + 'B0YLRjCDQt9Cw0L/QuNGB0ZbQsiDRgyDRhNCw0LnQu9GWIDI0MGRkAhMPDxYCHwIFCtCf0L7RiNGD0LpkZAIVDxYCHgVzdHlsZQUoY29sb3I6UmVkO21h'
                        + 'cmdpbi1sZWZ0OjIwcHg7ZGlzcGxheTpub25lOxYCAgEPDxYCHwIFO9Ck0LDQudC7INC80LDRlCDQvdC10L/RgNCw0LLQuNC70YzQvdC1INGA0L7Qt9GI0'
                        + 'LjRgNC10L3QvdGPZGQCFw8WAh8FBShjb2xvcjpSZWQ7bWFyZ2luLWxlZnQ6MjBweDtkaXNwbGF5Om5vbmU7FgICAQ8PFgIfAgWQAdCi0LXQutGB0YLQvt'
                        + 'Cy0LjQuSDRhNCw0LnQuyDQvdC1INCy0ZbQtNC/0L7QstGW0LTQsNGUINGE0L7RgNC80LDRgtGDLiDQl9Cw0LLQsNC90YLQsNC20YLQtSDQv9GA0LjQutC'
                        + '70LDQtCDRhNCw0LnQu9GDINC3INC90LDRiNC+0LPQviDRgdCw0LnRgtGDLmRkAhkPZBYEAgEPDxYCHwIFhAHQmtGW0LvRjNC60ZbRgdGC0Ywg0YjRgtGA'
                        + '0LjRhdC60L7QtNGW0LIg0LIg0YTQsNC50LvRliDQv9C10YDQtdCy0LjRidGD0ZQg0LzQsNC60YHQuNC80LDQu9GM0L3QviDQtNC+0LfQstC+0LvQtdC90'
                        + 'LUg0LfQvdCw0YfQtdC90L3RjzpkZAIDDw8WAh8CBQMyNDBkZAIbDxYCHwUFKGNvbG9yOlJlZDttYXJnaW4tbGVmdDoyMHB4O2Rpc3BsYXk6bm9uZTsWAg'
                        + 'IBDw8WAh8CBYEBWG1sINGE0LDQudC7INC90LUg0LLRltC00L/QvtCy0ZbQtNCw0ZQg0YTQvtGA0LzQsNGC0YMuINCX0LDQstCw0L3RgtCw0LbRgtC1INC'
                        + '/0YDQuNC60LvQsNC0INGE0LDQudC70YMg0Lcg0L3QsNGI0L7Qs9C+INGB0LDQudGC0YMuZGQCHQ8WAh4HVmlzaWJsZWcWAgIBDw8WAh8CBTvQoNC10LfR'
                        + 'g9C70YzRgtCw0YLQuCDQstGW0LTRgdGC0LXQttC10L3QvdGPINC90LAgMTAuMDcuMjAxMmRkAh8PPCsADQIADxYEHgtfIURhdGFCb3VuZGceC18hSXRlb'
                        + 'UNvdW50AgNkARAWBGYCAQICAgMWBDwrAAUBABYCHgpIZWFkZXJUZXh0BRHQqNGC0YDQuNGFINC60L7QtDwrAAUBABYCHwkFO9CG0L3QtNC10LrRgSDQvN'
                        + 'GW0YHRhtGPINCy0LjQutC+0L3QsNC90L3RjyDQvtC/0LXRgNCw0YbRltGXPCsABQEAFgIfCQUR0JrQvtC0INC/0L7QtNGW0Zc8KwAFAQAWAh8JBQjQntC'
                        + '/0LjRgRYEAgYCBgIGAgYWAmYPZBYIAgEPZBYIZg9kFgJmDxUBDVJRMzA0MTc2NjY5R0JkAgEPZBYCZg8VAQEgZAICD2QWAmYPFQEBIGQCAw9kFgJmDxUB'
                        + 'tAHQlNCw0L3RliDQv9GA0L4g0LLRltC00L/RgNCw0LLQu9C10L3QvdGPINC30LAg0L3QvtC80LXRgNC+0LwgUlEzMDQxNzY2NjlHQiDQvdCwINC00LDQv'
                        + 'dC40Lkg0YfQsNGBINCy0ZbQtNGB0YPRgtC90ZYsINGC0L7QvNGDINGJ0L4g0L3QtSDQt9Cw0YDQtdGU0YHRgtGA0L7QstCw0L3RliDQsiDRgdC40YHRgt'
                        + 'C10LzRli5kAgIPZBYIZg9kFgJmDxUBDVJCMDQxNjk3MDg3VUFkAgEPZBYCZg8VAQUwMzkyMmQCAg9kFgJmDxUBBTcwODAxZAIDD2QWAmYPFQHEAgogICA'
                        + 'gINCS0ZbQtNC/0YDQsNCy0LvQtdC90L3RjyDQt9CwINC90L7QvNC10YDQvtC8IFJCMDQxNjk3MDg3VUEg0LLRltC00L/RgNCw0LLQu9C10L3QtSAxMy4w'
                        + 'NS4yMDEyINC3INC80ZbRgdGG0Y8g0LzRltC20L3QsNGA0L7QtNC90L7Qs9C+INC/0L7RiNGC0L7QstC+0LPQviDQvtCx0LzRltC90YMg0KPQutGA0LDRl'
                        + '9C90Lgg0JrQuNGX0LIg0JTQntCf0J8g0KbQtdGFIOKEljIg0LzQttC9INCg0IYtMiDQstC40YXRltC0INC/0LjRgdGM0Lwg0LrQvtGAINGA0L7QsSDQty'
                        + 'DRltC90LTQtdC60YHQvtC8IDAzOTIyINC30LAg0LzQtdC20ZYg0KPQutGA0LDRl9C90LguCiAgIGQCAw9kFghmD2QWAmYPFQEAZAIBD2QWAmYPFQEBIGQ'
                        + 'CAg9kFgJmDxUBASBkAgMPZBYCZg8VAacB0JTQsNC90ZYg0L/RgNC+INCy0ZbQtNC/0YDQsNCy0LvQtdC90L3RjyDQt9CwINC90L7QvNC10YDQvtC8ICDQ'
                        + 'vdCwINC00LDQvdC40Lkg0YfQsNGBINCy0ZbQtNGB0YPRgtC90ZYsINGC0L7QvNGDINGJ0L4g0L3QtSDQt9Cw0YDQtdGU0YHRgtGA0L7QstCw0L3RliDQs'
                        + 'iDRgdC40YHRgtC10LzRli5kAgQPDxYCHwZoZGQCIQ8WBh8EBV5Eb3dubG9hZC5hc3B4P0ZpbGVOYW1lPU91dHB1dEJhcmNvZGVzLnhtbCZoaWRkZW5TZX'
                        + 'NzaW9uSWQ9MmVhY2FkNzUtMmZmYy00NTk2LWIyY2MtNGU4N2E1Mjk5MjM0HwMFINCX0LHQtdGA0LXQs9GC0Lgg0LIgeG1sINGE0LDQudC7HwUFCWRpc3B'
                        + 'sYXk6O2QCIw8WBh8EBUdEb3dubG9hZEV4Y2VsLmFzcHg/aGlkZGVuU2Vzc2lvbklkPTJlYWNhZDc1LTJmZmMtNDU5Ni1iMmNjLTRlODdhNTI5OTIzNB8D'
                        + 'BSDQl9Cx0LXRgNC10LPRgtC4INCyIHhscyDRhNCw0LnQux8FBQlkaXNwbGF5OjtkAiUPFgYfBAV5RG93bmxvYWRUZXh0LmFzcHg/RmlsZU5hbWU9T3V0c'
                        + 'HV0QmFyY29kZXMudHh0JlNlc3Npb249dHJ1ZSZUeHQ9ZmFsc2UmaGlkZGVuU2Vzc2lvbklkPTJlYWNhZDc1LTJmZmMtNDU5Ni1iMmNjLTRlODdhNTI5OT'
                        + 'IzNB8DBS/Ql9Cx0LXRgNC10LPRgtC4INCyINGC0LXQutGB0YLQvtCy0LjQuSDRhNCw0LnQux8FBQlkaXNwbGF5OjtkAicPFgYfBAVBRGVmYXVsdC5hc3B'
                        + '4P2hpZGRlblNlc3Npb25JZD0yZWFjYWQ3NS0yZmZjLTQ1OTYtYjJjYy00ZTg3YTUyOTkyMzQfAwUt0J3QsNC30LDQtCDQtNC+INC/0L7RiNGD0LrQvtCy'
                        + '0L7RlyDRhNC+0YDQvNC4HwZnZAIpDw8WBB8CBVDQlNGP0LrRg9GU0LzQviDQktCw0Lwg0LfQsCDQutC+0YDQuNGB0YLRg9Cy0LDQvdC90Y8g0L3QsNGI0'
                        + 'L7RjiDQv9C+0YHQu9GD0LPQvtGOIR8GZ2RkGAEFIGN0bDAwJGNlbnRlckNvbnRlbnQkTGlzdEJhcmNvZGVzDzwrAAoBCAIBZLl2R+IB0PiDE33q4DV4Q5'
                        + 'Q4VAZj')
        postdata.append('--' + self.__boundary)
        postdata.append('Content-Disposition: form-data; name="%s"' % 'ctl00$centerContent$hiddenSessionGuid')
        postdata.append('')
        postdata.append('88844977-d9c9-44cb-a4f8-6eee96e95c0a')
        postdata.append('--' + self.__boundary)
        postdata.append('Content-Disposition: form-data; name="%s"' % 'ctl00$centerContent$btnUpload')
        postdata.append('')
        postdata.append('Search')
        postdata.append('--' + self.__boundary)
        postdata.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('ctl00$centerContent$fileUploadXmlBarcodes', 'a.txt'))
        postdata.append('Content-Type: text/plain')
        postdata.append('')
        postdata.append('%(number)s\r\n')
        postdata.append('--' + self.__boundary + '--')
        postdata.append('')
        self.post = '\r\n'.join(postdata)

    def __get_operation_name(self, opcode):
        opcode = int(opcode)
        __common_opcodes = {
            10101: 'Acceptance',
            20701: 'Income',
            20801: 'Dispatching',
            20901: 'Transmission for delivery',
            21501: 'Transmission for delivery',
            31119: 'Not handed over during delivery',
            31205: 'Return to sender’s address: incomplete address',
            31206: 'Return to sender’s address: no addressee in indicated address',
            31207: 'Return to sender’s address: according to addressee’s written refusal',
            31208: 'Return to sender’s address: according to sender’s written request',
            31209: 'Return to sender’s address: according to addressee’s written request',
            31210: 'Return to sender’s address: no request',
            31213: 'Return to sender’s address: end of a set storage period',
            31414: 'Transmission for storage: end of a set storage period',
            31415: 'Transmission for storage: refusal of receipt according to sender’s request',
            41002: 'Handing over personally to an addressee',
            41003: 'Handing over to a family member',
            41004: 'Handing over by warrant',
            41022: 'Transmission for courier delivery',
            51118: 'Not indicated in income',
            51119: 'Handing over is impossible',
            51120: 'Storage',
        }
        if opcode in __common_opcodes:
            return __common_opcodes[opcode]
        if opcode >= 31201 and opcode <= 31204:
            return 'Return to sender’s address'
        if opcode >= 31219 and opcode <= 31299:
            return 'Return to sender’s address'
        if opcode >= 31301 and opcode <= 31399:
            return 'Re-forwarding to new address'
        if opcode >= 31401 and opcode <= 31410:
            return 'Transmission for storage'
        if opcode >= 31416 and opcode <= 31499:
            return 'Transmission for storage'
        if opcode >= 51101 and opcode <= 51115:
            return 'Handing over is impossible'
        if opcode >= 51121 and opcode <= 51199:
            return 'Handing over is impossible'
        if opcode >= 60701 and opcode <= 60799:
            return 'Import: income to Ukrainian exchange office'
        if opcode >= 70801 and opcode <= 70899:
            return 'Export: dispatching abroad from Ukrainian exchange office'
        if opcode >= 80801 and opcode <= 80899:
            return 'Transmission for customs control'
        if opcode >= 90801 and opcode <= 90899:
            return 'Dispatching from exchange office to Ukrainian postal facility'
        return 'Unknown operation'

    def _parse_page(self, html):
        html = html.decode('utf-8')
        res = re.search('%s\s*</td>\s*<td>\s*(\d{5})\s*</td>\s*<td>\s*(\d{5})\s*</td>\s*<td>\s*(.*?)\s*</td>' % self.number, html)
        if res is None:
            return []
        operation = self.__get_operation_name(res.group(2))
        postindex = res.group(1)
        dateres = re.search('(\d{2}\.\d{2}\.\d{4})', res.group(3))
        if dateres is None:
            date = None
        else:
            date = datetime.strptime(dateres.group(1), '%d.%m.%Y')

        locationres = re.search(u'[A-Z0-9№-]+ [A-Z0-9№-]+( [A-Z0-9№-]+)*', res.group(3))
        if locationres is None:
            location = 'Unknown location'
        else:
            location = locationres.group(0)

        return [(operation, date, location)]
