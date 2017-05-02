###############################################################################
## Tucan Project
##
## Copyright (C) 2011      Ali Shah
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

BASE_URL = "http://oron.com"
GLOBAL_WAIT = 60 #Default, also parsed in the page 

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		"""
		Oron links usually look like this:
			http://www.oron.com/file_id/file_name.foo.html
		However, by testing it seems that the server pulls the file name out by
		using the file_id, which is some sort of hash. 
		So the same file can aswell be accessed by: 
			http://www.oron.com/file_id/file_name.foo.html.html
		and 
			http://www.oron.com/file_id/file_name.foo.html.html(.html)*
		So we use check_links to get the file name form the HTML page, its 
		slower, but more accurate as we cannot rely on the url passed here
		"""
		file_id   = url.split("/")[3]
		file_name = self.check_links(url)[0]
		encoded_str = urllib.urlencode({
			"op"          : "download1",
			"usr_login"   : "",
			"id"          : file_id,
			"name"        : file_name,
			"referer"     : "",
			"method_free" : "+Regular+Download+"})
		opener = URLOpen()

		"""
		The url we are currently trying to open is the origin (referring) URL 
		preceding the post
		"""
		web_page = opener.open(url, encoded_str, False, url)


		for retry in range(3):
			if not wait_func():
				return

			for line in web_page:
				if '<input type="hidden" name="rand" value="' in line:
					rand_value = line.split('value="')[1].split('"')[0]
					break

			if not rand_value:
				logger.warning("Oron Plugin: No random value in download page- template changed?");
				return self.set_limit_exceeded(wait)

			for line in  web_page:
				if '<span id="countdown">' in line:
					wait_length  = line.split('<span id="countdown">')[1].split('<')[0]
					if not wait_func(int(wait_length)):
						return

				"""
				Check for longer limits
				"""
				if '<p class="err"' in line:
					parse_line = line.split('>')[1].split('<')[0]
					seconds = 0 
					minutes = 0
					hours   = 0
					prev_word = ''

					for word in parse_line.split(' '):

						if  word == 'hour,' or word == 'hours,':
							hours = int(prev_word)
                             
						elif  word == 'minute,' or word == 'minutes,':
							minutes = int(prev_word)

						elif  word == 'second' or word == 'seconds':
							seconds = int(prev_word)
							break
						else:
							prev_word = word

					seconds = seconds + (minutes * 60) + (hours * 3600)
					return self.set_limit_exceeded(seconds)
				
				if  'http://api.recaptcha.net/challenge?' in line:
					recaptcha_link = line.split('src="')[1].split('"')[0]
					if not wait_func():
						return
					c = Recaptcha(BASE_URL, recaptcha_link)
					challenge, response = c.solve_captcha()
					if response:
						if not wait_func():
							return

						#Submit the input to the recaptcha system
						form =  urllib.urlencode({
								"op"                        : "download2",
								"id"                        : file_id,
								"rand"                      : rand_value,
								"referer"                   : url,
								"method_free"               : "+Regular+Download+",
								"method_premium"            : "",
								"recaptcha_challenge_field" : challenge,
								"recaptcha_response_field"  : response,
								"down_direct"               : 1			
								})
						download_page = opener.open(url, form, None, False, url)
						#Get the link and return it
						for line in download_page:
							if 'Download File' in line:
								return opener.open(line.split('href="')[1].split('"')[0])

		return

	def check_links(self, url):
		return CheckLinks().check_links(url)
