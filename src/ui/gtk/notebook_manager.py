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

from upload_tree import UploadTree
from download_tree import DownloadTree
from input_files import InputFiles
from input_links import InputLinks

import core.shared as shared

import media

class NotebookManager(gtk.VBox):
	""""""
	def __init__(self):
		""""""
		gtk.VBox.__init__(self)
		self.download_manager = DownloadTree()
		self.upload_manager = UploadTree()
		
		#toolbar
		toolbar = gtk.Toolbar()
		self.pack_start(toolbar, False)
		toolbar.set_style(gtk.TOOLBAR_BOTH)
		
		tool_buttons = [
		(_("Add Downloads"), media.ICON_DOWNLOAD, lambda x: self.add_downloads),
		(_("Add Uploads"), media.ICON_UPLOAD, lambda x: self.add_uploads),
		(None, None, None),
		(_("Clear Complete"), media.ICON_CLEAR, lambda x: x.clear_cb),
		(None, None, None),
		(_("Move Up"), media.ICON_UP, lambda x: x.move_up_cb),
		(_("Move Down"), media.ICON_DOWN, lambda x: x.move_down_cb),
		(None, None, None),
		(_("Start Selected"), media.ICON_START, lambda x: x.start_cb),
		(_("Stop Selected"), media.ICON_STOP, lambda x: x.stop_cb),
		]
		
		for name, icon_path, get_callback in tool_buttons:
			if name == None:
				item = gtk.SeparatorToolItem()
			else:
				icon = gtk.image_new_from_file(icon_path)
				item = gtk.ToolButton(icon, name)
				item.connect("clicked", self.manage_callbacks, get_callback)
			toolbar.insert(item, -1)

		#notebook
		self.notebook = gtk.Notebook()
		self.pack_start(self.notebook)
		self.notebook.set_show_tabs(False)
		self.control_buttons = {}
		self.button_box = gtk.HBox()
		self.pack_start(self.button_box, False)
		self.download_id = self.add_page(self.download_manager, gtk.STOCK_GO_DOWN, _("Show Downloads"))
		self.upload_id = self.add_page(self.upload_manager, gtk.STOCK_GO_UP, _("Show Uploads"))

		#statusbar
		
	def add_page(self, page, stock, tooltip):
		""""""
		page_id = self.notebook.append_page(page)
		button = gtk.ToggleButton()
		if not page_id:
			button.set_active(True)
		self.button_box.pack_start(button, True, True, 5)
		button.set_tooltip_text(tooltip)
		button.set_image(gtk.image_new_from_stock(stock, gtk.ICON_SIZE_MENU))
		button.connect("released", lambda button: button.set_active(True))
		button.connect("pressed", self.toggle, page_id)
		self.control_buttons[page_id] = button
		return page_id
		
	def toggle(self, button, page_id):
		""""""
		if not button.get_active():
			self.notebook.set_current_page(page_id)
			for child in self.button_box.get_children():
				if button != child:
					child.set_active(False)

	def show_page(self, page_id):
		""""""
		if page_id in self.control_buttons:
			button = self.control_buttons[page_id]
			self.toggle(button, page_id)
			button.set_active(True)

	def manage_callbacks(self, button, get_callback):
		""""""
		page = self.notebook.get_nth_page(self.notebook.get_current_page())
		get_callback(page)()

	def add_downloads(self, content=None):
		""""""
		default_path = shared.configuration.get_downloads_folder()
		self.enable_clipboard(False)
		InputLinks(self, default_path, self.filter_service, self.get_check_links, self.create_packages, self.manage_packages, content)
		self.enable_clipboard(True)

	def add_uploads(self):
		""""""
		self.enable_clipboard(False)
		InputFiles(self, SERVICES, self.manager.add_package)
		self.enable_clipboard(False)
