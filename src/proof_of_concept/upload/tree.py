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

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango

import cons

import threading

class Tree(gtk.VBox):
	""""""
	def __init__(self):
		""""""
		gtk.VBox.__init__(self)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.treeview = gtk.TreeView(gtk.TreeStore(gtk.gdk.Pixbuf, str, str, str, int, bool, str, str, str, str, str))
		scroll.add(self.treeview)
		self.pack_start(scroll)

		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(True)

		#tree columns
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, False)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)

		tree_name = gtk.TreeViewColumn('Name')
		name_cell = gtk.CellRendererText()
		name_cell.set_property("width-chars", 60)
		name_cell.set_property("ellipsize", pango.ELLIPSIZE_MIDDLE)
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 3)
		self.treeview.append_column(tree_name)

		tree_progress = gtk.TreeViewColumn('Progress')
		tree_progress.set_min_width(150)
		progress_cell = gtk.CellRendererProgress()
		tree_progress.pack_start(progress_cell, True)
		tree_progress.add_attribute(progress_cell, 'value', 4)
		tree_progress.add_attribute(progress_cell, 'visible', 5)
		self.treeview.append_column(tree_progress)

		tree_current_size = gtk.TreeViewColumn('Current Size')
		current_size_cell = gtk.CellRendererText()
		tree_current_size.pack_start(current_size_cell, False)
		tree_current_size.add_attribute(current_size_cell, 'text', 6)
		self.treeview.append_column(tree_current_size)

		tree_total_size = gtk.TreeViewColumn('Total Size')
		total_size_cell = gtk.CellRendererText()
		tree_total_size.pack_start(total_size_cell, False)
		tree_total_size.add_attribute(total_size_cell, 'text', 7)
		self.treeview.append_column(tree_total_size)

		tree_speed = gtk.TreeViewColumn('Speed')
		speed_cell = gtk.CellRendererText()
		tree_speed.pack_start(speed_cell, False)
		tree_speed.add_attribute(speed_cell, 'text', 8)
		self.treeview.append_column(tree_speed)

		tree_time = gtk.TreeViewColumn('Time Left')
		time_cell = gtk.CellRendererText()
		tree_time.pack_start(time_cell, False)
		tree_time.add_attribute(time_cell, 'text', 9)
		self.treeview.append_column(tree_time)

		tree_plugins = gtk.TreeViewColumn('Plugin')
		plugins_cell = gtk.CellRendererText()
		tree_plugins.pack_start(plugins_cell, False)
		tree_plugins.add_attribute(plugins_cell, 'text', 10)
		self.treeview.append_column(tree_plugins)

		#icons
		self.package_icon = self.treeview.render_icon(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU)
		self.active_service_icon = self.treeview.render_icon(gtk.STOCK_YES, gtk.ICON_SIZE_MENU)
		self.unactive_service_icon = self.treeview.render_icon(gtk.STOCK_NO, gtk.ICON_SIZE_MENU)
		self.correct_icon = self.treeview.render_icon(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
		self.failed_icon = self.treeview.render_icon(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)
		self.wait_icon = self.treeview.render_icon(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
		self.active_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU)
		self.pending_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_MENU)
		self.stoped_icon = self.treeview.render_icon(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_MENU)
		self.icons = {cons.STATUS_CORRECT: self.correct_icon, cons.STATUS_ERROR: self.failed_icon, cons.STATUS_WAIT: self.wait_icon, cons.STATUS_ACTIVE: self.active_icon, cons.STATUS_PEND: self.pending_icon, cons.STATUS_STOP: self.stoped_icon}
		

		
		model = self.treeview.get_model()
		package_iter = model.append(None, [self.package_icon, cons.STATUS_PEND,"shit","some name", 0, True, None, None, None, None, "/home/elie/you"])
		item_iter = model.append(package_iter, [self.pending_icon, cons.STATUS_PEND, None,"you", 0, True, None, "ohoh", None, None, "tucan"])
		self.treeview.expand_to_path(model.get_path(item_iter))


	def update(self,progress,file_name):
		model = self.treeview.get_model()
		package_iter = model.get_iter_root()

		while package_iter:
			file_iter = model.iter_children(package_iter)
			while file_iter:
				if model.get_value(file_iter,3) == file_name:
					model.set_value(file_iter, 4, progress)
					break
				file_iter = model.iter_next(file_iter)
			package_iter = model.iter_next(package_iter)
#		if self.progress < 100:
#			self.progress = self.progress + 10
#			return True
		
		
