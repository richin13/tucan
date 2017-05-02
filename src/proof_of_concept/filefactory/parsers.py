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
import logging
logger = logging.getLogger(__name__)

import sys
sys.path.append("/home/crak/tucan/trunk")

from url_open import URLOpen, set_proxy

set_proxy(None)

BASE_URL = "http://www.filefactory.com%s"

class Parser:
	def __init__(self, url):
		""""""
		self.link = None
		first_link = None
		captcha_url = None
		captcha_id = None
		try:
			opener = URLOpen()
			for line in opener.open(url).readlines():
				if '<a class="download" href="' in line:
					first_link = BASE_URL % line.split('<a class="download" href="')[1].split('">')[0]
			if first_link:
				while not self.link:
					for line in opener.open(first_link).readlines():
						if '<input id="captchaID" name="captchaID" type="hidden" value="' in line:
							captcha_id = line.split('<input id="captchaID" name="captchaID" type="hidden" value="')[1].split('"/>')[0]
						elif '<a class="captchaReload ajax" target="captchaReload" href="' in line:
							captcha_url = BASE_URL % line.split('<a class="captchaReload ajax" target="captchaReload" href="')[1].split('">')[0]
					if captcha_url:
						logger.info("Captcha url: %s" % captcha_url)
						for i in range(25):
							self.image_string = URLOpen().open(captcha_url).read()
							tes = Tesseract(self.image_string, self.filter_image)
							captcha = tes.get_captcha().strip()
							if len(captcha) == 4:
								tmp = [i for i in captcha]
								for i in tmp:
									if i in CORRECTION.keys():
										tmp[tmp.index(i)] = CORRECTION[i]
								captcha = "".join(tmp)
								logger.warning("Captcha: %s" % captcha)
								data = urllib.urlencode([("captchaID", captcha_id),("captchaText", captcha)])
								for line in opener.open(first_link, data).readlines():
									if '" class="download">CLICK HERE to download for free with Filefactory Basic</a></p>' in line:
										self.link = line.split('<p><a href="')[1].split('" class="download">CLICK HERE to download for free with Filefactory Basic</a></p>')[0]
								if self.link:
									break
		except Exception, e:
			print e
			logger.exception("%s :%s" % (url, e))

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None
		try:
			for line in URLOpen().open(url).readlines():
				if '<span href="" class="last">' in line:
					name = line.split('<span href="" class="last">')[1].split('</span>')[0]
					if ".." in name:
						tmp = url.split("/").pop().split("_")
						name = ".".join(tmp)
				elif "file uploaded" in line:
					tmp = line.split("file uploaded")[0].split("<span>")[1].split(" ")
					size = int(float(tmp[0]))
					if size == 0:
						size = 1
					unit = tmp[1]
			if not name:
				name = url
				size = -1
		except Exception, e:
			name = url
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit

if __name__ == "__main__":
	c = Parser("http://www.filefactory.com/file/cc646e/n/Music_Within_2007_Sample_avi")
	#print CheckLinks().check("http://www.filefactory.com/file/cc646e/n/Music_Within_2007_Sample_avi")
