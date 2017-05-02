###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import media
import core.cons as cons

class HistoryView(gtk.Dialog):
	""""""
	def __init__(self, parent, history, services):
		""""""
		gtk.Dialog.__init__(self)
		self.set_transient_for(parent)
		self.set_icon(self.render_icon(gtk.STOCK_INDEX, gtk.ICON_SIZE_MENU))
		self.set_title(("History View"))
		self.set_size_request(600,400)

		self.history = history
		self.services = services
		self.icons = {}

		# treeview
		frame = gtk.Frame()
		self.vbox.pack_start(frame)
		frame.set_border_width(10)
		label = gtk.Label()
		label.set_markup("<b>%s</b>" % ("Downloads"))
		frame.set_label_widget(label)
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.store = gtk.ListStore(str, bool, gtk.gdk.Pixbuf, str, str, str, str)
		self.treeview = gtk.TreeView(self.store)
		scroll.add(self.treeview)

		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(False)

		tree_played = gtk.TreeViewColumn('Played')
		played_cell = gtk.CellRendererToggle()
		played_cell.connect("toggled", self.toggled)
		tree_played.pack_start(played_cell, True)
		tree_played.add_attribute(played_cell, 'active', 1)
		self.treeview.append_column(tree_played)

		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 2)
		tree_icon.set_property('min-width', 32)
		self.treeview.append_column(tree_icon)

		tree_date = gtk.TreeViewColumn('Date') 
		date_cell = gtk.CellRendererText()
		tree_date.pack_start(date_cell, True)
		tree_date.add_attribute(date_cell, 'text', 3)
		self.treeview.append_column(tree_date)

		tree_name = gtk.TreeViewColumn('Name') 
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 4)
		tree_name.set_property('min-width', 180)
		self.treeview.append_column(tree_name)

		tree_size = gtk.TreeViewColumn('Size') 
		size_cell = gtk.CellRendererText()
		tree_size.pack_start(size_cell, True)
		tree_size.add_attribute(size_cell, 'text', 6)
		self.treeview.append_column(tree_size)

		#fill store
		total_size, num_files, history = self.history.get_all()
		for id, played, link, date, name, size in history:
			self.store.append((id, played, self.get_icon(link), date, name, link, size))

		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, False, False, 10)
		label = gtk.Label()
		label.set_markup("<b>Total:</b> %s Files - %s" % (num_files, total_size))
		hbox.pack_start(label, False, False, 15)

		#action area
		close_button = gtk.Button(None, gtk.STOCK_CLOSE)
		self.action_area.pack_start(close_button)
		close_button.connect("clicked", self.close)

		self.treeview.connect("button-press-event", self.mouse_menu)
		self.connect("response", self.close)
		self.show_all()
		self.run()

	def mouse_menu(self, widget, event):
		"""right button"""
		if event.button == 3:
			model, paths = self.treeview.get_selection().get_selected_rows()
			if len(paths) > 0:
				subitem = gtk.ImageMenuItem(gtk.STOCK_COPY)
				subitem.connect("activate", self.copy_clipboard)
				menu = gtk.Menu()
				menu.append(subitem)
				menu.show_all()
				menu.popup(None, None, None, event.button, event.time)

	def copy_clipboard(self, button):
		""""""
		model, iter = self.treeview.get_selection().get_selected()
		if iter:
			clipboard = gtk.Clipboard()
			clipboard.clear()
			clipboard.set_text(model.get_value(iter, 5))

	def toggled(self, button, path):
		""""""
		model = self.treeview.get_model()
		if button.get_active():
			active = False
		else:
			active = True
		id = model.get_value(model.get_iter(path), 0)
		self.history.set_played(id, active)
		model.set_value(model.get_iter(path), 1, active)

	def get_icon(self, link):
		""""""
		try:
			service = ""
			for name, path in self.services:
				if name in link:
					service = name
			if service not in self.icons:
				for name, path in self.services:
					if service == name:
						self.icons[service] = gtk.gdk.pixbuf_new_from_file_at_size(path, 16, 16)
			return self.icons[service]
		except:
			return gtk.gdk.pixbuf_new_from_file_at_size(media.ICON_MISSING, 16, 16)

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
