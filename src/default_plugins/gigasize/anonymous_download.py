###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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
import cookielib
logger = logging.getLogger(__name__)

import urllib
import random

import Image

from core.tesseract import Tesseract
from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen
import core.cons as cons

import time

WAIT = 30 #Default, also parsed in the page if possible
BASE_URL = "http://www.gigasize.com"


class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			url = url.split("&")[0]
			cookie = cookielib.CookieJar()
			opener = URLOpen(cookie)
			
			if not wait_func():
				return
			
			retry = 5
			while retry:
				it = opener.open(url)
				img_url = None
				for line in it:
					if "<iframe src='" in line:
						img_url = line.split("'")[1].split("'")[0]
					elif 'name="fileId"' in line:
						file_id = line.split('value="')[1].split('"')[0]
				if not img_url:
					return self.set_limit_exceeded()
				it = opener.open(img_url)
				for line in it:
					if 'AdsCaptcha Challenge' in line:
						img_url = line.split('src="')[1].split('"')[0]
					elif 'class="code">' in line:
						code = line.split('">')[1].split("<")[0]

				tes = Tesseract(opener.open(img_url).read())
				captcha = tes.get_captcha()
				captcha = "".join([c for c in captcha if c.isdigit()]) #keep only the numbers
	
				data = urllib.urlencode([("fileId", file_id),("adscaptcha_response_field", captcha),("adscaptcha_challenge_field", code), ("adUnder", "")])
				it = opener.open("%s/getoken" % BASE_URL, data)
				captcha = False
				for line in it:
					if '"status":1' in line:
						captcha = True
				#captcha is valid
				if captcha:
					if not wait_func(WAIT):
						return
					it = opener.open("%s/formtoken" % BASE_URL)
					for line in it:
						token = line
					rnd = "".join([str(random.randint(1,9)) for i in range(16)])
					data = urllib.urlencode([("fileId", file_id),("token", token),("rnd", rnd)])
					it = opener.open("%s/getoken" % BASE_URL, data)
					for line in it:
						if '"status":1' in line:
							link = line.split('":"')[1].split('"')[0].replace("\\","")
					return opener.open(link)
				retry -= 1
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			url = url.split("&")[0]
			it = URLOpen().open(url)
			for line in it:
				if '<div class="fileInfo">' in line:
					name = it.next().split("</strong>")[0].split(">")[-1].strip()
					it.next()
					tmp = it.next().split("</strong>")[0].split(">")[-1].strip()
					if cons.UNIT_KB in tmp:
						unit = cons.UNIT_KB
						size = int(float(tmp.split(cons.UNIT_KB)[0]))
					elif cons.UNIT_MB in tmp:
						unit = cons.UNIT_MB
						size = int(float(tmp.split(cons.UNIT_MB)[0]))
					elif cons.UNIT_GB in tmp:
						unit = cons.UNIT_GB
						size = int(float(tmp.split(cons.UNIT_GB)[0]))
		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
