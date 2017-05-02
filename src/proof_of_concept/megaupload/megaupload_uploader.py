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
		self.up_action = None
		self.up_done_action = None
		self.id = None

		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), MultipartHTTPHandler)

		self.feed(opener.open(urllib2.Request("http://www.megaupload.com/", {})).read())
		self.close()
		if self.up_action and self.up_done_action:
			print self.up_action
			print self.up_done_action

			req = urllib2.Request(self.up_action, {}, HEADER)
			handle1 = opener.open(req)
			print handle1.readline()

			form = {"filecount": "", 'multifile_0"; filename="': "", "UPLOAD_IDENTIFIER": self.id, "sessionid": self.id , "file": open(file_name, "rb"), "toemail": "", "fromemail": "", "message": description, "multiemail": "", "password": "", "url": "", "accept": "on"}
			req = urllib2.Request(self.up_done_action, form, HEADER)
			handle2 = opener.open(req)

			print "mierda", req.get_data()
			data = " "
			while data:
				data = handle2.readline()
				print data
			"""
			for line in handle.readlines():
				if "downloadurl" in line:
					print line
			"""

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "form":
			if attrs[2][1] == "multipart/form-data":
				self.up_done_action = attrs[3][1]
			elif attrs[1][1] == "uploadprogress":
				self.up_action = attrs[3][1]
		elif tag == "input":
			if attrs[1][1] == "UPLOAD_IDENTIFIER":
				self.id = attrs[2][1]

if __name__ == "__main__":
	c = UploadParser("/home/crak/2009-02-10-231803_1024x600_scrot.png", "mierda")
