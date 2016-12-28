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

import locale
from locale import gettext as _
locale.textdomain('parcel-tracker')

from gi.repository import Gtk, Pango, GLib  # pylint: disable=E0611
import json
import gevent
import logging
import sys
logger = logging.getLogger('parcel_tracker')

from parcel_tracker_lib import Window
from parcel_tracker.AboutParcelTrackerDialog import AboutParcelTrackerDialog
from parcel_tracker.PreferencesParcelTrackerDialog import PreferencesParcelTrackerDialog
from parcel_tracker import prompts, post_fetcher


# See parcel_tracker_lib.Window.py for more details about how this class works
class ParcelTrackerWindow(Window):
    __gtype_name__ = "ParcelTrackerWindow"
    (LIST_NAME, LIST_POSTCODE, LIST_DATETIME, LIST_UNREAD, LIST_TECHNICAL, LIST_UPDATED) = range(6)
    (DETAILS_DATETIME, DETAILS_PLACE, DETAILS_OPERATION, DETAILS_TECHNICAL) = range(4)

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the main window"""
        super(ParcelTrackerWindow, self).finish_initializing(builder)

        def hide(*kargs, **kwargs):
            self.hide()
            return True
        self.connect("delete_event", hide)

        self.AboutDialog = AboutParcelTrackerDialog
        self.PreferencesDialog = PreferencesParcelTrackerDialog

        # Currently updating tasks
        self.updating = 0

        self.parcels = json.loads(self.settings['parcels'])

        # Fix fields if needed
        for code, parcel in self.parcels.iteritems():
            for requiredfield in ["name"]:
                if requiredfield not in parcel:
                    del self.parcels[code]
            for nullablefield in ["date", "unread", "updated"]:
                if nullablefield not in parcel:
                    parcel[nullablefield] = None
            for mapfield in ["news"]:
                if mapfield not in parcel:
                    parcel[mapfield] = {}

        # Code for other initialization actions should be added here.
        self.setup_parcelslist_view()
        self.setup_parcelinfo_view()
        self.setup_events()
        self.fill_parcels_list()

        def gevent_loop_idle():
            """Idle job for gevent could successfully switch threads"""
            try:
                gevent.sleep(0.01)
            except:
                Gtk.main_quit()
                exc_info = sys.exc_info()
                try:
                    gevent.hub.MAIN.throw(*exc_info)
                except AttributeError:
                    gevent.hub.get_hub().throw(*exc_info)
            GLib.idle_add(gevent_loop_idle)
        gevent_loop_idle()
        gevent.spawn(self.update_parcels)

    def on_destroy(self, widget, data=None):
        self.save_parcels()
        Window.on_destroy(self, widget, data)

    def save_parcels(self):
        self.settings.set_value('parcels', GLib.Variant.new_string(json.dumps(self.parcels)))

    def update_parcels(self, spawn_future=True):
        """This method updates all parcel states and schedules the next run"""
        for postcode, parcel in self.parcels.iteritems():
            self.update_progress_indicator()
            self.updating += post_fetcher.fetch_parcel(postcode, parcel, self.redraw_list)
        self.save_parcels()
        if spawn_future:
            update_period = self.settings.get_value("update-period").get_int32()
            gevent.spawn_later(update_period, self.update_parcels)

    def update_progress_indicator(self):
        indicator = self.builder.get_object("update_status")
        if self.updating > 0:
            indicator.set_property("active", True)
            indicator.set_property("has_tooltip", True)
        else:
            indicator.set_property("active", False)
            indicator.set_property("has_tooltip", False)

    def redraw_list(self):
        """Update parcels list and redraw the selected parcel info"""
        self.fix_parcels_list()
        selection = self.builder.get_object("trackedparcels_treeview").get_selection()
        self.display_parcel(selection)
        self.updating -= 1
        self.update_progress_indicator()

    def insert_parcel_to_list(self, code, parcel):
        """Insert parcel short info to the ListStore of the user parcels"""
        store = self.builder.get_object("parcels_store")
        name = parcel['name']
        unread = parcel['unread']
        latest_date = parcel['date']
        updated = parcel['updated']
        store.append([name, code, latest_date, unread, False, updated])
        self.fix_parcels_list()

    def fill_parcels_list(self):
        """Load the list of tracked parcels and their states"""
        store = self.builder.get_object("parcels_store")
        store.clear()
        [self.insert_parcel_to_list(code, parcel) for code, parcel in self.parcels.iteritems()]
        self.fix_parcels_list()

    def fix_parcels_list(self):
        """Fix the parcels list - add or remove technical line if needed"""
        store = self.builder.get_object("parcels_store")
        # To empty store we add the technical message
        if len(store) == 0:
            store.append([_("No tracked packages"), None, None, False, True, None])
            self.builder.get_object("trackedparcels_treeview").set_sensitive(False)
            return
        # In one-row store we check if the message is already technical
        if len(store) == 1 and store[0][self.LIST_TECHNICAL] is True:
            self.builder.get_object("trackedparcels_treeview").set_sensitive(False)
            return
        # Otherwise we remove the technical row if any
        for i in store:
            self.builder.get_object("trackedparcels_treeview").set_sensitive(True)
            if i[self.LIST_TECHNICAL] is True:
                store.remove(i.iter)
            else:
                parcel = self.parcels[i[self.LIST_POSTCODE]]
                i[self.LIST_UNREAD] = parcel['unread']
                i[self.LIST_DATETIME] = "" if parcel['date'] is None else parcel['date']
        self.update_indicator()

    def refresh_parcelinfo_store(self, postcode):
        store = self.builder.get_object("parcelinfo_store")
        store.clear()
        try:
            parcel_history = self.parcels[postcode]['news']
            if len(parcel_history):
                for hashname, row in parcel_history.iteritems():
                    store.append([row[1], row[2], row[0], False])
            else:
                store.append([_("Parcel info has never been received yet"), None, None, True])
        except KeyError:
            store.append([_("Parcel details are not available"), None, None, True])

    def display_parcel(self, selection):
        model, path = selection.get_selected_rows()
        if not len(path):
            self.builder.get_object("parcelinfo_vbox").set_visible(False)
            self.builder.get_object("removeparcel_button").set_sensitive(False)
            return

        path = path[0]
        i = model.get_iter(path)
        postcode = model.get_value(i, self.LIST_POSTCODE)
        self.refresh_parcelinfo_store(postcode)
        model.set_value(i, self.LIST_UNREAD, False)
        self.parcels[postcode]['unread'] = False
        self.update_indicator()
        self.builder.get_object("parcelinfo_vbox").set_visible(True)
        self.builder.get_object("removeparcel_button").set_sensitive(True)

    def add_parcel(self, button):
        input = self.builder.get_object("parcel_input")
        postcode = input.get_text().strip()
        clicked, text = prompts.string(title=_("Parcel name"), text=_("Enter the short description of your package"))
        text = text.strip()
        if clicked != Gtk.ResponseType.OK or text == "":
            return
        parcel = {
            'name': text,
            'unread': False,
            'date': None,
            'news': {},
            'updated': None
        }
        self.parcels[postcode] = parcel
        input.set_text("")
        self.insert_parcel_to_list(postcode, parcel)
        self.save_parcels()
        post_fetcher.fetch_parcel(postcode, parcel, self.redraw_list)

    def remove_parcel(self, button):
        selection = self.builder.get_object("trackedparcels_treeview").get_selection()
        model, path = selection.get_selected_rows()
        path = path[0]
        i = model.get_iter(path)
        postcode = model.get_value(i, self.LIST_POSTCODE)
        model.remove(i)
        if postcode in self.parcels:
            del self.parcels[postcode]
        self.fix_parcels_list()
        self.save_parcels()

    def setup_parcelinfo_view(self):
        view = self.builder.get_object("parcelinfo_treeview")
        date_column = Gtk.TreeViewColumn()
        place_column = Gtk.TreeViewColumn()
        operation_column = Gtk.TreeViewColumn()

        bgcolor = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL).to_color()

        def datetime_renderer_func(col, cell, m, i, _):
            technical = m.get_value(i, self.DETAILS_TECHNICAL) is True
            line = m.get_value(i, self.DETAILS_DATETIME)
            if not technical:
                line = "<span style=\"italic\" foreground=\"gray\">%s</span>" % line
            else:
                cell.set_property("xalign", 0)
            cell.set_property("markup", line)

        def items_sort_func(m, i1, i2, _):
            val1 = m.get_value(i1, self.DETAILS_DATETIME)
            val2 = m.get_value(i2, self.DETAILS_DATETIME)
            if val1 > val2:
                return 1
            elif val1 < val2:
                return -1
            else:
                return 1

        # Datetime
        cell_datetime = Gtk.CellRendererText()
        cell_datetime.set_property("background-gdk", bgcolor)
        date_column.pack_start(cell_datetime, False)
        date_column.set_cell_data_func(cell_datetime, datetime_renderer_func)

        # Place
        cell_place = Gtk.CellRendererText()
        cell_place.set_property("background-gdk", bgcolor)
        place_column.pack_start(cell_place, False)
        place_column.add_attribute(cell_place, "text", self.DETAILS_PLACE)

        # Operation
        cell_operation = Gtk.CellRendererText()
        cell_operation.set_property("background-gdk", bgcolor)
        operation_column.pack_start(cell_operation, False)
        operation_column.add_attribute(cell_operation, "text", self.DETAILS_OPERATION)

        view.append_column(date_column)
        view.append_column(place_column)
        view.append_column(operation_column)
        store = view.get_model()
        store.set_sort_column_id(0, Gtk.SortType.DESCENDING)
        store.set_default_sort_func(items_sort_func)
        store.set_sort_func(0, items_sort_func)

    def setup_parcelslist_view(self):
        view = self.builder.get_object("trackedparcels_treeview")
        column = Gtk.TreeViewColumn()

        def unread_renderer_func(col, cell, m, i, _):
            has_unread = m.get_value(i, self.LIST_UNREAD)
            title = m.get_value(i, self.LIST_NAME)
            if has_unread:
                cell.set_property("background", "orange")
            else:
                cell.set_property("background", "white")
            cell.set_property("text", "")

        def title_renderer_func(col, cell, m, i, _):
            technical = m.get_value(i, self.LIST_TECHNICAL) is True
            line = m.get_value(i, self.LIST_NAME)
            if not technical:
                line = "<b>%s</b>\n<span style=\"italic\" foreground=\"gray\">%s</span>" % (line, m.get_value(i, self.LIST_POSTCODE))
            cell.set_property("markup", line)
            if technical:
                cell.set_property("xalign", 0.5)
            else:
                cell.set_property("xalign", 0)
            cell.set_property("ellipsize", Pango.EllipsizeMode.END)
            cell.set_property("width", 250)

        def datetime_renderer_func(col, cell, m, i, _):
            val = m.get_value(i, self.LIST_DATETIME)
            if val is not None:
                cell.set_property("markup", " <span underline=\"low\" weight=\"ultralight\">%s</span>" % val)
            else:
                cell.set_property("text", None)

        def items_sort_func(m, i1, i2, _):
            val1 = m.get_value(i1, self.LIST_DATETIME)
            val2 = m.get_value(i2, self.LIST_DATETIME)
            if val1 > val2:
                return 1
            elif val1 < val2:
                return -1
            else:
                return 1

        # Does it have unread news
        cell_unread = Gtk.CellRendererText()
        column.pack_start(cell_unread, False)
        column.set_cell_data_func(cell_unread, unread_renderer_func)
        # Name and postcode
        cell_title = Gtk.CellRendererText()
        column.pack_start(cell_title, False)
        column.set_cell_data_func(cell_title, title_renderer_func)
        # Datetime
        cell_datetime = Gtk.CellRendererText()
        #cell_datetime.set_property("background-gdk", bgcolor)
        cell_datetime.set_property("yalign", 1.0)
        column.pack_end(cell_datetime, False)
        column.set_cell_data_func(cell_datetime, datetime_renderer_func)
        view.append_column(column)

        store = view.get_model()
        store.set_sort_column_id(0, Gtk.SortType.DESCENDING)
        store.set_default_sort_func(items_sort_func)
        store.set_sort_func(0, items_sort_func)

    def setup_events(self):
        def tooltip_func(view, x, y, keyboard_tip, tooltip):
            try:
                result, __, __, m, path, i = view.get_tooltip_context(x, y, keyboard_tip)
                if not result:
                    return False
            except TypeError:
                return False
            text = m.get_value(i, self.LIST_UPDATED)
            if text is None:
                text = _("Never")
            tooltip.set_markup(_("Latest info on this parcel was updated on: <b>%s</b>") % text)
            view.set_tooltip_row(tooltip, path)
            return True

        def update_addparcel_sensitivity(entry):
            button = self.builder.get_object("addparcel_button")
            text = entry.get_text().strip()
            if text == "" or text in self.parcels:
                button.set_sensitive(False)
            else:
                button.set_sensitive(True)

        view = self.builder.get_object("trackedparcels_treeview")
        view.connect("query-tooltip", tooltip_func)

        selection = view.get_selection()
        selection.set_mode(Gtk.SelectionMode.BROWSE)
        selection.connect("changed", self.display_parcel)

        self.builder.get_object("removeparcel_button").connect("clicked", self.remove_parcel)
        self.builder.get_object("addparcel_button").connect("clicked", self.add_parcel)
        self.builder.get_object("parcel_input").connect("changed", update_addparcel_sensitivity)
        self.builder.get_object("update_all").connect("clicked", lambda x: self.update_parcels(False))
        self.builder.get_object("parcel_input").connect("activate", lambda x: self.builder.get_object("addparcel_button").clicked())

    def update_indicator(self):
        if not self.indicator:
            return
        unread = any([x['unread'] for x in self.parcels.values()])
        if unread:
            self.indicator.setNewMessages()
        else:
            self.indicator.unsetNewMessages()
