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

import urllib
import urllib2
import cookielib

from HTMLParser import HTMLParser

from multipart_httphandler import MultipartHTTPHandler

HEADER = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20081114 Firefox/3.0.4"}

class UploadParser(HTMLParser):
	""""""
	def __init__(self, file_name, description):
		""""""
		HTMLParser.__init__(self)
		self.action = None
		self.id = None
		cookie = cookielib.CookieJar()
		simple_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

		req = urllib2.Request("http://www.gigasize.com/")
		handle = simple_opener.open(req)

		self.feed(handle.read())
		self.close()
		if self.action:
			print simple_opener.open(urllib2.Request("http://www.gigasize.com/upload_progress.php", urllib.urlencode([("sid", self.id), ("_", "")]), HEADER)).read()

			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), MultipartHTTPHandler())
			form = [("UPLOAD_IDENTIFIER", self.id), ("file_1", None), ("file_0", open(file_name, "rb")), ("titlel", ""), ("description", ""), ("numupfiles", ""), ("x", 78), ("y", 5), ("accept", 1)]
			handle = opener.open(urllib2.Request("http://www.gigasize.com%s" % self.action, form, HEADER))
			print simple_opener.open(urllib2.Request("http://www.gigasize.com/upload_progress.php", urllib.urlencode([("sid", self.id), ("_", "")]), HEADER)).read()

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "form":
			if attrs[0][1] == "multipart/form-data":
				self.action = attrs[1][1]
		elif tag == "input":
			if attrs[1][1] == "UPLOAD_IDENTIFIER":
				self.id = attrs[2][1]

if __name__ == "__main__":
	c = UploadParser("/home/crak/2009-03-03-210729_1024x600_scrot.png", "mierda")
