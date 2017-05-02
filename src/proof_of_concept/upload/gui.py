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
import sys
import time
import threading
import __builtin__
import gettext
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from tree import Tree

import cons
from input_files import InputFiles
import threading
from rapidshare import UploadParser

MIN_WIDTH = 250
MIN_HEIGHT = 200

class Gui(gtk.Window):
	""""""
	def __init__(self):
		""""""
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_title("%s - Version: %s" % (cons.TUCAN_NAME, cons.TUCAN_VERSION))
		self.set_size_request(MIN_WIDTH, MIN_HEIGHT)

		self.resize(900, 500)
		self.set_position(gtk.WIN_POS_CENTER)

		self.vbox = gtk.VBox()
		self.add(self.vbox)

		#trees
#		self.downloads = Tree()
		self.downloads = gtk.VBox()
		self.uploads = Tree()
#		self.uploads = gtk.VBox()
		self.add_button = gtk.Button("Add upload")
		self.add_button.connect("clicked", self.input_files, None)
		self.stop_button = gtk.Button("Stop upload")
		self.stop_button.connect("clicked", self.stop_upload, None)

		#pane
		self.pane = gtk.VPaned()
		self.vbox.pack_start(self.pane)
		self.pane.pack2(self.downloads, True)
		self.pane.pack1(self.uploads, True)
		self.vbox.pack_end(self.add_button, True)
		self.vbox.pack_end(self.stop_button, True)
		self.pane.set_position(self.get_size()[1])
		
		self.connect("delete_event", self.quit)
		self.show_all()
		
		self.upload = None
		self.pending_uploads = None
		self.th = []
		

	def add_upload(self, file_name):
		self.upload = UploadParser(file_name, "mierda", self.uploads.update)
		
	def stop_upload(self):
		pass
		
	def input_files(self,one,two):
		InputFiles(self)

		print self.pending_uploads
		#Append the results in the upload tree
		model = self.uploads.treeview.get_model()
		package_iter = model.append(None, [None, cons.STATUS_PEND,"shit","Upload package", 0, True, None, None, None, None, "/home/elie/you"])
		for res in self.pending_uploads:
			item_iter = model.append(package_iter, [None, cons.STATUS_PEND, None,res[0], 0, True, None,"%d %s" % (res[1],res[2]), None, None,res[3][0]])			
			self.uploads.treeview.expand_to_path(model.get_path(item_iter))
			self.th.append(threading.Thread(target=gui.add_upload, args = (res[0],)))
			self.th[-1].start()

	def quit(self,one,two):
		""""""
		self.close()

	def close(self):
		""""""
		self.destroy()
		gtk.main_quit()

		
if __name__ == "__main__":
	gobject.threads_init()
	gui = Gui()
	gtk.main()
