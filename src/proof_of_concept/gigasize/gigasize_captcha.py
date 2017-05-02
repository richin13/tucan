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

import time
import urllib
import urllib2
import cookielib

from HTMLParser import HTMLParser

from tesseract import Tesseract

class FormParser(HTMLParser):
	""""""
	def __init__(self, data):
		""""""
		HTMLParser.__init__(self)
		self.form_action = None
		self.feed(data)
		self.close()
		print self.form_action

	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "form":
			if ((len(attrs) == 3) and (attrs[2][1] == "formDownload")):
				self.form_action = attrs[0][1]

if __name__ == "__main__":
	urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar())))
	urllib2.urlopen(urllib2.Request("http://www.gigasize.com/get.php/3196987695/p3x03sp.avi"))

	tes = Tesseract(urllib2.urlopen(urllib2.Request("http://www.gigasize.com/randomImage.php")).read(), True)
	captcha = tes.get_captcha(3)

	data = urllib.urlencode({"txtNumber": captcha, "btnLogin.x": "124", "btnLogin.y": "12", "btnLogin": "Download"})
	handle = urllib2.urlopen(urllib2.Request("http://www.gigasize.com/formdownload.php"), data)
	f = FormParser(handle.read())
	handle.close()
	if f.form_action:
		timer = 60
		while timer > 0:
			time.sleep(1)
			timer -= 1
			print timer
		data = urllib.urlencode({"dlb": "Download"})
		handle = urllib2.urlopen(urllib2.Request("http://www.gigasize.com" + f.form_action), data)
		while len(data) > 0:
			data = handle.read(1024)
			print data
		handle.close()
