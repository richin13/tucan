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

import urllib2
import math

from HTMLParser import HTMLParser

class CaptchaParser(HTMLParser):
	""""""
	def __init__(self, url):
		""""""
		HTMLParser.__init__(self)
		self.captcha = None
		self.form_action = None
		self.form_d = None
		self.form_imagecode = None
		self.form_megavar = None
		self.feed(urllib2.urlopen(urllib2.Request(url)).read())
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "img":
			if attrs[0][0]  == "src":
				if attrs[0][1].find("capgen") > 0:
				    self.captcha = attrs[0][1]
		elif tag == "form":
			if attrs[0][1] == "POST":
				self.form_action = attrs[1][1]
		elif tag == "input":
			if attrs[1][1] == "d":
				self.form_d = attrs[2][1]
			if attrs[1][1] == "imagecode":
				self.form_imagecode= attrs[2][1]
			if attrs[1][1] == "megavar":
				self.form_megavar = attrs[2][1]

class UrlParser(HTMLParser):
	""""""
	def __init__(self, data):
		""""""
		HTMLParser.__init__(self)
		self.tmp_url = None
		self.url_pos = None
		self.data = data
		self.feed(self.data)
		self.close()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if ('class', 'downloadhtml') in attrs:
				self.url_pos = self.getpos()
			elif  ('onclick', 'loadingdownload();') in attrs:
				self.tmp_url = attrs[0][1]

	def get_url(self):
		""""""
		vars = {}
		data = self.data.split("\n")

		tmp = data[self.url_pos[0]].split(" ")
		vars[tmp[1]] = chr(int(tmp[3].split("-")[1].split(")")[0]))

		tmp = data[self.url_pos[0]+1].split(" ")
		vars[tmp[1]] = tmp[3].split("\'")[1] + chr(int(math.sqrt(int(tmp[5].split("sqrt(")[1].split(")")[0]))))

		tmp = self.tmp_url.split(" + ")
		return tmp[0].split("\'")[0] + vars[tmp[1]] + vars[tmp[2]] + tmp[3].split("\'")[1]

if __name__ == "__main__":
	f = open("source.html", "r")
	c = UrlParser(f.read())
	print c.get_url()
