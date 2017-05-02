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
import cookielib

import logging
logger = logging.getLogger(__name__)

from core.download_plugin import DownloadPlugin
from core.recaptcha import Recaptcha
from core.url_open import URLOpen
import core.cons as cons
from check_links import CheckLinks 

BASE_URL = "http://www.filesonic.com/file"

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			cookie = cookielib.CookieJar()
			opener = URLOpen(cookie)
			file_id = url.split("/")[-2]
			form_action = "%s?start=1" % (url)
			
			if not wait_func():
				return
			
			it = opener.open(form_action)
			form_action = "%s?start=1" % it.geturl() #Get the redirect url
			end = form_action.split(".")[2].split("/")[0] #Get the .com replacement
			form_action2 = "%s/%s/%s?start=1" % (BASE_URL,file_id,file_id)
			form_action2 = form_action2.replace(".com",".%s" % end)
			form = urllib.urlencode([("foo","foo")]) #Force urllib2 to do a POST
			#FIXME : urlopen should be able to set custom headers
			headers = {"User-Agent": cons.USER_AGENT, "X-Requested-With": "XMLHttpRequest"}
			it = opener.opener.open(urllib2.Request(form_action2, None, headers), form)
			it_tmp = None

			#Loop until we get the captcha
			for loop in range(3):
				if not wait_func():
					return
				#it_tmp is set after a wait
				if it_tmp:
					it = it_tmp
				for line in it:
					if 'Recaptcha.create("' in line:
						tmp = line.split('"')[1].split('"')[0]
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
								form = urllib.urlencode([("recaptcha_challenge_field", challenge), ("recaptcha_response_field", response)])
								it = opener.open(form_action, form)
								#Get the link
								for line in it:
									if 'downloadLink' in line:
										it.next()
										return opener.open(it.next().split('href="')[1].split('"')[0])
				
					#Link already there
					elif 'downloadLink' in line:
						it.next()
						return opener.open(it.next().split('href="')[1].split('"')[0])
					
					#Need to wait
					elif "name='tm'" in line:
						tm = line.split("value='")[1].split("'")[0];
						tm_hash = it.next().split("value='")[1].split("'")[0];
						form = urllib.urlencode([("tm", tm), ("tm_hash", tm_hash)])
				
					#Need to wait
					elif "countDownDelay =" in line:
						wait = int(line.split("=")[1].split(";")[0])
						if wait < 60:
							if not wait_func(wait):
								return
							it_tmp = opener.open(form_action, form) #fetch the page
							#Next loop, reload the page
							break
						else:
							return self.set_limit_exceeded(wait)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		return CheckLinks().check_links(url)
