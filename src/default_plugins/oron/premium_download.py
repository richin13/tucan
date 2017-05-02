###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Ali Shah ahshah@airpost.net
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

from premium_cookie import PremiumCookie

from core.accounts import Accounts
from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen
from check_links import CheckLinks 

class PremiumDownload(DownloadPlugin, Accounts):
	""""""
	def __init__(self, config, section):
		""""""
		Accounts.__init__(self, config, section, PremiumCookie())
		DownloadPlugin.__init__(self, config, section)

	def link_parser(self, url, wait_func, content_range=None):
		"""
		See comment in anonymous_download.py for how oron links generally look
		like. Premimum accounts still have to suffer by having to post the random
		value at the bottom of the html page. There is also a download page that 
		one has to parse to figure out what the actual direct download link is
		"""
		file_id   = url.split("/")[3]
		file_name = self.check_links(url)[0]

		try:
			cookie = self.get_cookie()
			if not wait_func():
				return
			opener = URLOpen(cookie)
			web_page = opener.open(url, None, content_range)

			if not wait_func():
				return

			rand_value = None
			for line in web_page:
				if '<input type="hidden" name="rand" value="' in line:
					rand_value = line.split('value="')[1].split('"')[0]
					break
			if not rand_value:
				logger.error("Oron.premium_download: could not find random value in " \
				             "download page. Premimum format changed?")

			form = urllib.urlencode({
				"op"              :"download2",
				"id"              : file_id,
				"rand"            : rand_value,
				"referer"         : "",
				"method_free"     : "",
				"method_premium"  : "1",
				"down_direct"     : "1"})

			download_page =  opener.open(url, form, content_range)
			direct_link = None
			for line in download_page:
				if 'Download File</a></td>' in line:
					direct_link = line.split('a href="')[1].split('" class="')[0]

			if not direct_link:
				return

			return opener.open(direct_link)

		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		return CheckLinks().check_links(url)
