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

import os
import time

import pygtk
pygtk.require('2.0')
import gtk
import pango
import gobject

from file_chooser import FileChooser
from message import Message

from core.base_types import create_upload_package

import media
import core.cons as cons
import core.misc as misc

class InputFiles(gtk.Dialog):
	""""""
	def __init__(self, parent, upload_services, add_package):
		""""""
		gtk.Dialog.__init__(self)
		self.set_transient_for(parent)
		self.set_icon_from_file(media.ICON_UPLOAD)
		self.set_title(("Input Files"))
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_size_request(600, 500)

		self.history_path = cons.DEFAULT_PATH
		
		self.add_package = add_package

		main_hbox = gtk.HBox()
		self.vbox.pack_start(main_hbox)

		self.file_icon = self.render_icon(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
		self.correct_icon = self.render_icon(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
		self.incorrect_icon = self.render_icon(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)

		#package treeview
		frame = gtk.Frame()
		main_hbox.pack_start(frame, True)
		frame.set_border_width(5)
		
		hbox = gtk.HBox()
		frame.set_label_widget(hbox)
		hbox.pack_start(gtk.image_new_from_file(media.ICON_PACKAGE))
		self.package_entry = gtk.Entry(50)
		hbox.pack_start(self.package_entry)
		self.package_entry.set_width_chars(25)
		self.package_entry.set_text("package-%s" % time.strftime("%Y%m%d%H%M%S"))

		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		#(icon, name, size, normalized_size, path, service_name, plugin_type)
		self.package_treeview = gtk.TreeView(gtk.TreeStore(gtk.gdk.Pixbuf, str, int, str, str, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT))
		scroll.add(self.package_treeview)

		self.package_treeview.set_rules_hint(True)
		self.package_treeview.set_headers_visible(False)

		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.package_treeview.append_column(tree_icon)

		tree_name = gtk.TreeViewColumn('Name') 
		name_cell = gtk.CellRendererText()
		name_cell.set_property("width-chars", 36)
		name_cell.set_property("ellipsize", pango.ELLIPSIZE_MIDDLE)
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		self.package_treeview.append_column(tree_name)

		tree_size = gtk.TreeViewColumn('Size') 
		size_cell = gtk.CellRendererText()
		tree_size.pack_start(size_cell, False)
		tree_size.add_attribute(size_cell, 'text', 3)
		self.package_treeview.append_column(tree_size)

		service_vbox = gtk.VBox()
		main_hbox.pack_start(service_vbox, False, False)

		# services treeview
		frame = gtk.Frame()
		service_vbox.pack_start(frame)
		frame.set_size_request(170, -1)
		frame.set_border_width(5)
		frame.set_label_widget(gtk.image_new_from_file(media.ICON_PREFERENCES_SERVICES))
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		#(icon, service_name, selected, Service, plugins_vbox)
		services = gtk.ListStore(gtk.gdk.Pixbuf, str, bool, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT)
		self.services_treeview = gtk.TreeView(services)
		self.services_treeview.get_selection().connect("changed", self.select_service)
		scroll.add(self.services_treeview)

		self.services_treeview.set_rules_hint(True)
		self.services_treeview.set_headers_visible(False)

		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.services_treeview.append_column(tree_icon)

		tree_name = gtk.TreeViewColumn('Name') 
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		self.services_treeview.append_column(tree_name)

		tree_add = gtk.TreeViewColumn('Add')
		add_cell = gtk.CellRendererToggle()
		add_cell.connect("toggled", self.toggled)
		tree_add.pack_start(add_cell, True)
		tree_add.add_attribute(add_cell, 'active', 2)
		self.services_treeview.append_column(tree_add)

		#plugins
		self.plugins_frame = gtk.Frame()
		service_vbox.pack_start(self.plugins_frame, False, False)
		self.plugins_frame.set_size_request(160, 100)
		self.plugins_frame.set_border_width(5)

		for service in upload_services:
			icon = gtk.gdk.pixbuf_new_from_file(service.icon_path)
			name = service.name.split(".")[0]
			selected = False
			first = None
			vbox = gtk.VBox()
			available_plugins = service.get_upload_plugins()
			if available_plugins:
				for plugin_type, plugin in available_plugins:
					first = gtk.RadioButton(first, plugin_type)
					func = lambda x, y, z: self.activate(x.get_active(), y, z)
					first.connect("toggled", func, service, vbox)
					tooltip = "Max File Size: %s" % misc.normalize(plugin.max_size, "%.0f%s")
					first.set_tooltip_text(tooltip)
					vbox.pack_start(first, False, False, 1)
				vbox.show_all()
				services.append([icon, name, selected, service, vbox])
		
		#choose path
		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, False, False, 5)
		path_button = gtk.Button(None, gtk.STOCK_OPEN)
		path_button.set_size_request(90,-1)
		hbox.pack_start(path_button, False, False, 5)
		path_button.connect("clicked", self.choose_files)
		path_label = gtk.Label(("Choose files to upload."))
		hbox.pack_start(path_label, False, False, 5)
		aspect = gtk.AspectFrame()
		hbox.pack_start(aspect, True, True)
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		clear_button = gtk.Button(None, gtk.STOCK_CLEAR)
		clear_button.set_size_request(160,-1)
		hbox.pack_start(clear_button, False, False, 5)
		clear_button.connect("clicked", self.clear)

		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		add_button = gtk.Button(None, gtk.STOCK_ADD)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(add_button)
		cancel_button.connect("clicked", self.close)
		add_button.connect("clicked", self.add_files)

		self.connect("response", self.close)
		self.show_all()
		self.set_focus(path_button)
		self.run()

	def clear(self, button):
		""""""
		self.package_treeview.get_model().clear()

	def select_service(self, selection):
		""""""
		model, service_iter = selection.get_selected()
		if service_iter:
			if self.plugins_frame.get_child():
				self.plugins_frame.remove(self.plugins_frame.get_child())
			self.plugins_frame.add(model.get_value(service_iter, 4))

	def add_files(self, button):
		""""""
		files = []
		package_model = self.package_treeview.get_model()
		services_model = self.services_treeview.get_model()
		
		file_iter = package_model.get_iter_root()
		while file_iter:
			services = []
			service_iter = package_model.iter_children(file_iter)
			while service_iter:
				plugin_type = package_model.get_value(service_iter, 6)
				if plugin_type:
					service_name = package_model.get_value(service_iter, 5)
					plugin_info = package_model.get_value(service_iter, 1)
					services.append((service_name, plugin_type, plugin_info))
				service_iter = package_model.iter_next(service_iter)
			if services:
				size = package_model.get_value(file_iter, 2)
				path = package_model.get_value(file_iter, 4)
				files.append((path, size, services))
			file_iter = package_model.iter_next(file_iter)
		if files:
			self.add_package(create_upload_package(files, self.package_entry.get_text()))
			self.close()
		else:
			title = _("Nothing to add")
			message = _("There aren't files to add.\nSelected services must support file size.")
			m = Message(self, cons.SEVERITY_INFO, title, message, both=True)
			if not m.accepted:
				self.close()

	def toggled(self, button, path):
		""""""
		active = True
		if button.get_active():
			active = False
		button.set_active(active)

		model = self.services_treeview.get_model()		
		iter = model.get_iter(path)
		model.set_value(iter, 2, active)

		service = model.get_value(iter, 3)
		vbox = model.get_value(iter, 4)
		
		self.activate(active, service, vbox)
		
	def activate(self, add, service, vbox):
		""""""
		model = self.package_treeview.get_model()
		plugin_type = self.get_selected_plugin(service, vbox)
		
		iters = []
		file_iter = model.get_iter_root()
		while file_iter:
			if add:	
				iters.append(file_iter)
			else:
				iter = model.iter_children(file_iter)
				while iter:
					if service.name == model.get_value(iter, 5):
						model.remove(iter)
						break
					iter = model.iter_next(iter)
			file_iter = model.iter_next(file_iter)
		if add and iters:
			self.add_service(model, iters, service, plugin_type)

	def choose_files(self, button):
		""""""
		f = FileChooser(self, self.on_choose, self.history_path, True)
		self.history_path = f.history_path

	def on_choose(self, choosed_path):
		""""""
		package_model = self.package_treeview.get_model()
		services_model = self.services_treeview.get_model()
		paths = []
		if os.path.isfile(choosed_path):
			paths.append(choosed_path)
		elif os.path.isdir(choosed_path):
			for path in os.listdir(choosed_path):
				path = os.path.join(choosed_path, path)
				if os.path.isfile(path):
					paths.append(path)
		iters = []
		for path in paths:
			if path not in [row[4] for row in package_model]:
				size = os.stat(path).st_size
				row = [self.file_icon, os.path.basename(path), size, misc.normalize(size), path, None, None]
				iter = package_model.append(None, row)
				iters.append(iter)
		for row in services_model:
			if row[2]:
				service = row[3]
				plugin_type = self.get_selected_plugin(service, row[4])
				self.add_service(package_model, iters, service, plugin_type)
	
	def get_selected_plugin(self, service, vbox):
		""""""
		for button in vbox.get_children():
			if button.get_active():
				return button.get_label()

	def add_service(self, package_model, iters, service, choosed_type):
		""""""
		available_plugins = service.get_upload_plugins()
		if available_plugins:
			for plugin_type, plugin in available_plugins:
				if choosed_type == plugin_type:
					break
			checked = plugin.check_files([package_model.get_value(iter, 4)  for iter in iters])
			i = 0
			for iter in iters:
				if checked[i]:
					icon = self.correct_icon
					t = plugin_type
				else:
					icon = self.incorrect_icon
					t = None
				package_model.append(iter, [icon, plugin.__module__, 0, None, None, service.name, t])
				self.package_treeview.expand_row(package_model.get_path(iter), True)
				i += 1

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
