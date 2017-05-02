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

import HTMLParser
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import core.cons as cons
import media

def check_text(clipboard, selection_data):
	""""""
	urls = []
	tmp = clipboard.wait_for_text()
	if tmp:
		for line in tmp.split("\n"):
			if "http://" in line:
				urls.append(line.strip())
	return urls

def check_contents(clipboard, selection_data):
	""""""
	if cons.OS_OSX:
		return check_osx_html(clipboard, selection_data)
	elif cons.OS_WINDOWS:
		return check_html(clipboard, selection_data, "HTML Format", "utf8")
	else:
		return check_html(clipboard, selection_data, "text/html", "utf16")

def check_osx_html(clipboard, selection_data):
	""""""
	urls = []
	target = "public.rtf"
	if target  in list(selection_data):
		selection = clipboard.wait_for_contents(target)
		if selection:
			for line in str(selection.data.decode("utf8", "ignore")).split("\n"):
				if '{HYPERLINK "' in line:
					urls.append(line.split('{HYPERLINK "')[1].split('"}')[0])
	return urls


def check_html(clipboard, selection_data, target, codec):
	""""""
	urls = []
	if target in list(selection_data):
		selection = clipboard.wait_for_contents(target)
		if selection:
			for line in str(selection.data.decode(codec, "ignore")).split("\n"):
				try:
					parser = ClipParser()
					parser.feed(line)
				except HTMLParser.HTMLParseError:
					parser.reset()
				else:
					urls += parser.urls
	return urls

class ClipParser(HTMLParser.HTMLParser):
	""""""
	def __init__(self):
		""""""
		HTMLParser.HTMLParser.__init__(self)
		self.urls = []

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			for ref, link in attrs:
				if ref == "href":
					self.urls.append(link)

class Clipboard:
	""""""
	def __init__(self, parent_window, callback, set_hint, services):
		""""""
		self.handler_id = None
		self.parent = parent_window
		self.enabled = False
		self.old_content = ""
		self.len_old = 0
		self.monitor_open = False
		self.content_callback = callback
		self.hint = set_hint
		self.services = services

	def enable(self):
		""""""
		if cons.OS_WINDOWS or cons.OS_OSX:
			self.enabled = True
			tmp = gtk.clipboard_get().wait_for_text()
			if tmp:
				self.old_content = tmp
				self.len_old = len(tmp)
			gobject.timeout_add_seconds(1, self.check_clipboard)
		else:
			self.handler_id = gtk.clipboard_get().connect("owner-change", self.poll_clipboard)

	def disable(self):
		""""""
		if cons.OS_WINDOWS or cons.OS_OSX:
			self.enabled = False
		else:
			if self.handler_id:
				gtk.clipboard_get().disconnect(self.handler_id)

	def check_supported(self, urls):
		""""""
		links = []
		for url in urls:
			for name in self.services:
				if url.find(name) > 0:
					links.append(url)
					break
		return links

	def show_monitor(self, clipboard, selection_data, data):
		""""""
		html_links = self.check_supported(check_contents(clipboard, selection_data))
		text_links = self.check_supported(check_text(clipboard, selection_data))
		if len(html_links) > 0 or len(text_links) > 0:
			if cons.OS_WINDOWS or cons.OS_OSX:
				monitor = ClipboardMonitor(self.parent, html_links, text_links)
			else:
				monitor = ClipboardMonitor(None, html_links, text_links)
			content = monitor.get_content()
			if content:
				self.hint(True)
				self.content_callback(None, content)
				self.hint(False)
		self.monitor_open = False

	def check_clipboard(self):
		"""Windows and OSX support"""
		if not self.monitor_open:
			clipboard = gtk.clipboard_get()
			tmp = clipboard.wait_for_text()
			if tmp:
				len_tmp = len(tmp)
				if len(tmp) != self.len_old:
					self.old_content = tmp
					self.len_old = len_tmp
					self.poll_clipboard(clipboard)
				else:
					for i in range(len_tmp):
						if tmp[i] != self.old_content[i]:
							self.old_content = tmp
							self.len_old = len_tmp
							self.poll_clipboard(clipboard)
							break
		if self.enabled:
			return True

	def poll_clipboard(self, clipboard, event=None):
		""""""
		if not self.monitor_open:
			self.monitor_open = True
			clipboard.request_targets(self.show_monitor)


class ClipboardMonitor(gtk.Dialog):
	""""""
	def __init__(self, parent, html, text):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon(self.render_icon(gtk.STOCK_PASTE, gtk.ICON_SIZE_MENU))
		self.set_title("%s - %s" % (cons.TUCAN_NAME, ("Clipboard Monitor")))
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_modal(True)
		self.set_size_request(400,200)
		if parent:
			self.set_transient_for(parent)

		self.html_buffer = gtk.TextBuffer()
		self.html_buffer.insert_at_cursor("\n".join(html) + "\n")
		self.text_buffer = gtk.TextBuffer()
		self.text_buffer.insert_at_cursor("\n".join(text) + "\n")
		self.all_buffer = gtk.TextBuffer()
		self.all_buffer.insert_at_cursor("\n".join(html+text) + "\n")

		self.notebook = gtk.Notebook()
		self.vbox.pack_start(self.notebook)
		for tab, buffer in [("HTML", self.html_buffer),  ("TEXT", self.text_buffer),  ("ALL", self.all_buffer)]:
			frame = gtk.Frame()
			self.notebook.append_page(frame, gtk.Label(tab))
			frame.set_border_width(10)
			hbox = gtk.HBox()
			frame.add(hbox)
			scroll = gtk.ScrolledWindow()
			hbox.pack_start(scroll, True, True)
			scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
			textview = gtk.TextView(buffer)
			scroll.add(textview)
			textview.set_wrap_mode(gtk.WRAP_CHAR)

		self.content = None

		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		self.action_area.pack_start(cancel_button)
		button = gtk.Button("Check")
		self.action_area.pack_start(button)
		pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(media.ICON_CHECK, 24, 24)
		button.set_image(gtk.image_new_from_pixbuf(pixbuf))
		button.connect("clicked", self.set_content)
		cancel_button.connect("clicked", self.close)

		self.connect("response", self.close)
		self.show_all()

		#must be after show_all
		if len(html) > 0:
			self.notebook.set_current_page(0)
		else:
			self.notebook.set_current_page(1)

		self.run()


	def set_content(self, button=None):
		""""""
		buffer = [self.html_buffer, self.text_buffer, self.all_buffer][self.notebook.get_current_page()]
		start, end = buffer.get_bounds()
		self.content = buffer.get_text(start, end)
		self.close()

	def get_content(self):
		""""""
		result = self.content
		self.content = None
		return result

	def close(self, widget=None, other=None):
		""""""
		self.html_buffer.set_text("")
		self.text_buffer.set_text("")
		self.all_buffer.set_text("")
		self.destroy()
