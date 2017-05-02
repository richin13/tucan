###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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
import cookielib

import logging
logger = logging.getLogger(__name__)

from core.download_plugin import DownloadPlugin
from core.recaptcha import Recaptcha
from core.url_open import URLOpen
from check_links import CheckLinks

BASE_URL = "http://fileserve.com"

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			#Remove the filename from the url
			tmp = url.split("/file/")[1].split("/")[0]
			url = "%s/file/%s" % (BASE_URL,tmp)
			
			file_id = url.split("/")[-1].strip("/")
			cookie = cookielib.CookieJar()
			opener = URLOpen(cookie)
			
			form = urllib.urlencode([("checkDownload", "check")])
			#If the limit is exceeded
			if '"fail":"timeLimit"' in opener.open(url,form).read():
				return self.set_limit_exceeded()
				
			it = opener.open(url)
			for line in it:
				if 'reCAPTCHA_publickey=' in line:
					tmp = line.split("'")[1].split("'")[0]
					recaptcha_link = "http://www.google.com/recaptcha/api/challenge?k=%s" % tmp
					if not wait_func():
						return
					c = Recaptcha(BASE_URL, recaptcha_link)
					for retry in range(3):
						challenge, response = c.solve_captcha()
						if response:
							if not wait_func():
								return
							
							#Submit the input to the recaptcha system
							form = urllib.urlencode([("recaptcha_challenge_field", challenge), ("recaptcha_response_field", response), ("recaptcha_shortencode_field",file_id)])
							recaptcha_url = "%s/checkReCaptcha.php" % BASE_URL
							
							#Captcha is good
							if "success" in opener.open(recaptcha_url,form).read():
								form = urllib.urlencode([("downloadLink", "wait")])
								wait = int(opener.open(url,form).read()[-2:])
								if not wait_func(wait):
									return
								form = urllib.urlencode([("downloadLink", "show")])
								opener.open(url,form).read()
								form = urllib.urlencode([("download", "normal")])
								return opener.open(url,form)#,content_range)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		return CheckLinks().check_links(url)
