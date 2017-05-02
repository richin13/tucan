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

import urllib2
import logging
logger = logging.getLogger(__name__)

from premium_cookie import PremiumCookie
from anonymous_download import AnonymousDownload

from core.download_plugin import DownloadPlugin
from core.accounts import Accounts
from core.service_config import SECTION_PREMIUM_DOWNLOAD, ServiceConfig
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
		auth_string = self.get_cookie()
		if not wait_func():
			return

		encoded_link = 'http://api.hotfile.com/?action=getdirectdownloadlink&link=' + url + auth_string
		logger.info("Encoded link %s" % (encoded_link))
		opener = URLOpen()
		handler = opener.open(encoded_link)
		actual_link = handler.readline()
		return opener.open(actual_link)	

	def check_links(self, url):
		return CheckLinks().check(url)
