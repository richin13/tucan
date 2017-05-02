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
import urllib2

import logging
logger = logging.getLogger(__name__)

from core.download_plugin import DownloadPlugin
from core.recaptcha import Recaptcha
from core.url_open import URLOpen

BASE_URL = "http://easy-share.com"
WAIT = 20

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			wait = WAIT
			opener = URLOpen()
			it = opener.open(url)
			first_wait = False
			#Check for first wait
			for line in it:
				if 'var wf =' in line:
					try:
						wait = int(line.split("=")[1].split(";")[0].strip())
						first_wait = True
					except Exception, e:
						logger.exception("%s: %s" % (url, e))
						return
				break
			#Necessary to loop to reload the page, due to the wait
			for loop in range(3):
				if not wait_func():
					return
				#First wait
				if first_wait:
					if not wait_func(wait):
						return
					data = urllib.urlencode([("free", "Regular Download")])
					url = "%sbilling?%s" % (url,data)
					it = opener.open(url,data)
				#No first wait
				else:
					it = opener.open(url)
				for line in it:
					if 'name="id"' in line:
						file_id = line.split('value="')[1].split('"')[0]
					elif 'id="dwait"' in line:
						it.next()
						it.next()
						tmp = it.next()
						#The download is possible
						if "form" in tmp:
							form_action = tmp.split('action="')[1].split('"')[0]
						#Necessary to wait
						else:
							it.next()
							it.next()
							wait = int(it.next().split("'")[1].split("'")[0])
							if wait < 60:
								if not wait_func(wait):
									return
								#Next loop, reload the page
								break
							else:
								return self.set_limit_exceeded(wait)
					elif 'Recaptcha.create("' in line:
						tmp = line.split('"')[1].split('"')[0]
						recaptcha_link = "http://www.google.com/recaptcha/api/challenge?k=%s" % tmp
						if not wait_func():
							return
						c = Recaptcha(BASE_URL, recaptcha_link)
						challenge, response = c.solve_captcha()
						if response:
							if not wait_func():
								return
						
							#Submit the input to the recaptcha system
							form = urllib.urlencode([("recaptcha_challenge_field", challenge), ("recaptcha_response_field", response), ("recaptcha_shortencode_field", "undefined")])
							handle = opener.open(form_action, form, content_range)
							if not handle.info().getheader("Content-Type") == "text/html":
								#Captcha is good
								return handle
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			it = URLOpen().open(url)
			for line in it:
				if '<span class="txtorange">' in line:
					tmp = it.next()
					name = tmp.split("<")[0].strip()
					tmp = tmp.split(">(")[1].split(")")[0]
					if "KB" in tmp:
						size = int(round(float(tmp.split("KB")[0])))
						unit = "KB"
					elif "MB" in tmp:
						size = float(tmp.split("MB")[0])
						if int(round(size)) > 0:
							size = int(round(size))
							unit = "MB"
						else:
							size = int(round(1024 * size))
							unit = "KB"
					elif "GB" in tmp:
						size = int(round(float(tmp.split("GB")[0])))
						unit = "GB"
		except urllib2.HTTPError:
			pass
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
