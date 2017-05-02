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
		""""""
		found = False
		try:
			cookie = self.get_cookie()
			if not wait_func():
				return
			opener = URLOpen(cookie)
			handler = opener.open(url, None, content_range)
			if not wait_func():
				return
			else:
				return handler
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		return CheckLinks().check_links(url)
