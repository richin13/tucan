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

import hashlib
import urllib
import urllib2

from HTMLParser import HTMLParser

HEADER = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20081114 Firefox/3.0.4"}

CAPTCHACODE = "captchacode"
MEGAVAR = "megavar"

URL = "http://www.megaupload.com/?d=7H602RK1"
QUERY = "http://tucanquery.appspot.com/query"
ADD = "http://tucanquery.appspot.com/add"

class CaptchaParser(HTMLParser):
	""""""
	def __init__(self, data):
		""""""
		HTMLParser.__init__(self)
		self.located = False
		self.captcha = None
		self.captchacode = ""
		self.megavar = ""
		self.feed(data)
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "td":
			if self.get_starttag_text() == '<TD width="100" align="center" height="40">':
				self.located = True
		elif tag == "img":
			if self.located:
				self.located = False
				self.captcha = attrs[0][1]
		elif tag == "input":
			if attrs[1][1] == CAPTCHACODE:
				self.captchacode = attrs[2][1]
			elif attrs[1][1] == MEGAVAR:
				self.megavar = attrs[2][1]

class CaptchaForm(HTMLParser):
	""""""
	def __init__(self, url, captcha, captchacode, megavar):
		""""""
		HTMLParser.__init__(self)
		self.link = None
		self.located = False
		if captcha:
			self.feed(urllib2.urlopen(urllib2.Request(url, urllib.urlencode([(CAPTCHACODE, captchacode), (MEGAVAR, megavar), ("captcha", captcha)]), HEADER)).read())
			self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if ((self.located) and (attrs[0][0] == "href")):
				self.located = False
				self.link = attrs[0][1]
		elif tag == "div":
			if ((len(attrs) > 1) and (attrs[1][1] == "downloadlink")):
				self.located = True

class CaptchaSolve(gtk.Dialog):
	""""""
	def __init__(self):
		""""""
		gtk.Dialog.__init__(self)
		self.set_title("Megaupload Captcha")
		self.set_size_request(300,200)

		self.image = gtk.Image()
		self.vbox.pack_start(self.image)

		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, False, False, 10)
		self.label = gtk.Label()
		hbox.pack_start(self.label)

		self.entry = gtk.Entry()
		hbox.pack_start(self.entry, False, False, 10)
		self.entry.set_width_chars(5)
		self.entry.set_max_length(4)
		self.entry.set_activates_default(True)
		self.entry.connect("activate", self.store_captcha)

		self.megavar = ""
		self.captchacode = ""
		self.new_captcha()

		button = gtk.Button(None, gtk.STOCK_REFRESH)
		self.action_area.pack_start(button)
		button.connect("clicked", self.new_captcha)
		button = gtk.Button(None, gtk.STOCK_ADD)
		self.action_area.pack_start(button)
		button.connect("clicked", self.store_captcha)

		self.connect("response", self.close)
		self.show_all()
		self.run()

	def store_captcha(self, widget=None):
		""""""
		solution = self.entry.get_text()
		if len(solution) == 4:
			try:
				int(solution[3])
			except:
				print "Last char is not a number."
			else:
				f = CaptchaForm(URL, solution.lower(), self.captchacode, self.megavar)
				print f.link
				if f.link:
					if self.add_captcha(self.captcha, solution.lower()):
						self.new_captcha()
				else:
					self.entry.set_text("")
					self.set_focus(self.entry)

	def new_captcha(self, widget=None):
		""""""
		found = ""
		captcha = None
		while found != None:
			p = CaptchaParser(urllib2.urlopen(urllib2.Request(URL, None, HEADER)).read())
			if p.captcha:
				self.captchacode = p.captchacode
				self.megavar = p.megavar
				captcha = p.captcha.split("gencap.php?")[1].split(".gif")[0]
				loader = gtk.gdk.PixbufLoader("gif")
				handle = urllib2.urlopen(urllib2.Request(p.captcha, None, HEADER))
				if handle.info()["Content-Type"] == "image/gif":
					data = handle.read()
					captcha = hashlib.md5(data).hexdigest()
					loader.write(data)
					loader.close()
					self.image.set_from_pixbuf(loader.get_pixbuf())
					self.entry.set_text("")
					self.set_focus(self.entry)
					found = self.query_captcha(captcha)
		self.captcha = captcha
		print p.captcha
		self.label.set_text("Solve Captcha: %s" % p.captcha.split("gencap.php?")[1].split(".gif")[0])

	def close(self, widget=None, other=None):
		""""""
		self.destroy()

	def query_captcha(self, captcha):
		""""""
		response = urllib2.urlopen(urllib2.Request(QUERY), urllib.urlencode([("key", captcha)])).read()
		print "Captcha requested: %s %s" % (captcha, response)
		if len(response) > 0:
			return response

	def add_captcha(self, captcha, solution):
		""""""
		data = urllib.urlencode([("key", captcha), ("value", solution)])
		response = urllib2.urlopen(urllib2.Request(ADD), data).read()
		if len(response) > 0:
			print "Captcha added: %s %s" % (captcha, solution)
			return True

if __name__ == "__main__":
	c = CaptchaSolve()
	print c.query_captcha("56b797d1ffd5438eed0d8403ed7f21de")
