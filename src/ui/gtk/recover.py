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

import sys
import subprocess
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from report import Report
from core.misc import remove_conf_dir

import core.cons as cons
import media
import gui

def halt(message):
	""""""
	for window in gtk.window_list_toplevels():
		if isinstance(window, gui.Gui):
			window.stop_all()
		window.hide()
	gobject.idle_add(show_recover, message)
	gtk.main()

def show_recover(message):
	"""Needed for windows"""
	r = Recover(message)
	r.run()

class Recover(gtk.Dialog):
	""""""
	def __init__(self, message):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon(self.render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DND))
		self.set_title("%s - %s" % (cons.TUCAN_NAME, ("Recover Help")))
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_modal(True)
		self.set_resizable(False)

		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, True, False, 5)
		aspect = gtk.AspectFrame()
		hbox.pack_start(aspect)
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		image = gtk.image_new_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG)
		hbox.pack_start(image)
		label = gtk.Label("An unexpected error forced Tucan to exit.")
		hbox.pack_start(label)
		label.set_width_chars(35)
		label.set_line_wrap(True)

		self.expander = gtk.Expander("Show details")
		self.vbox.pack_start(self.expander, True, True, 5)
		frame = gtk.Frame()
		self.expander.add(frame)
		frame.set_border_width(10)
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.buffer = gtk.TextBuffer()
		self.buffer.set_text(message)
		textview = gtk.TextView(self.buffer)
		scroll.add(textview)
		textview.set_wrap_mode(gtk.WRAP_WORD)
		textview.set_editable(False)
		textview.set_cursor_visible(False)


		hbox = gtk.HButtonBox()
		self.vbox.pack_start(hbox, True, True, 5)
		hbox.set_layout(gtk.BUTTONBOX_SPREAD)
		button = gtk.Button("Remove Configuration")
		hbox.pack_start(button)
		button.connect("clicked", self.remove_conf)
		button = gtk.Button("Report Problem")
		hbox.pack_start(button)
		button.connect("clicked", self.report_problem)

		#action area
		button = gtk.Button(None, gtk.STOCK_QUIT)
		self.action_area.pack_start(button)
		button.connect("clicked", self.close)
		button = gtk.Button("Restart ")
		self.action_area.pack_start(button)
		button.connect("clicked", self.restart)
		button.set_image(gtk.image_new_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_BUTTON))

		self.connect("response", self.close)
		self.show_all()
		self.set_focus(button)
		self.set_urgency_hint(True)

	def remove_conf(self, button):
		""""""
		button.set_sensitive(False)
		try:
			remove_conf_dir()
		except Exception, e:
			self.buffer.set_text(str(e))
			self.expander.set_expanded(True)

	def report_problem(self, button):
		""""""
		Report(self)

	def restart(self, button):
		""""""
		logging.shutdown()
		command = "%stucan.py" % cons.PATH
		subprocess.Popen(["python", command])
		self.close()

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
		gtk.main_quit()
		sys.exit()

if __name__ == "__main__":
	show_recover("puta mierda")
