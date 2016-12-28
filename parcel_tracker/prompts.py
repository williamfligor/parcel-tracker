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

from gi.repository import Gtk
from gettext import gettext as _


class Prompt(Gtk.Dialog):
    def __init__(self, title, text):
        Gtk.Dialog.__init__(self, title, None, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        content_area = self.get_content_area()
        content_area.set_border_width(5)
        self.set_default_response(Gtk.ResponseType.OK)

        self.content_box = Gtk.VBox(False, 10)
        label = Gtk.Label(text)
        label.set_line_wrap(True)
        self.content_box.pack_start(label, False, False, 5)
        content_area.pack_start(self.content_box, False, False, 5)
        self.content_box.show()
        label.show()


def string(title=_("Input String"),
           text=_("Input a String:"),
           default_value=""):
    sp = StringPrompt(title, text, default_value)
    response = sp.run()
    val = sp.get_value()
    sp.destroy()
    return (response, val)


class StringPrompt(Prompt):
    def __init__(self,
                 title=_("Input String"),
                 text=_("Input a String:"),
                 default_value=""):
        Prompt.__init__(self, title, text)
        self._entry = Gtk.Entry()
        self._entry.set_text(default_value)
        self._entry.set_activates_default(True)
        self._entry.show()
        self.content_box.pack_end(self._entry, True, True, 5)

    def get_value(self):
        return self._entry.get_text()
