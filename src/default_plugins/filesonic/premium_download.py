###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2011 Elie Melois eliemelois@gmail.com
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

import re

class PremiumDownload(DownloadPlugin, Accounts):
	""""""
	def __init__(self, config, section):
		""""""
		Accounts.__init__(self, config, section, PremiumCookie())
		DownloadPlugin.__init__(self, config, section)

	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			cookie = self.get_cookie()
			if not wait_func():
				return

			#Dirty hack due to issue #46
			#We should add support for services that don't need cookies
			user =  cookie._cookies['.filesonic.com']['/']['enc'].comment
			password = cookie._cookies['.filesonic.com']['/']['enc'].comment_url
			
			#Filesonic API doc : http://api.filesonic.com/user#FSApi_Link-getDownloadLink
			regex = '/file/(([a-z][0-9]+/)?[0-9]+)(/.*)?$' #Given by the Filesonic API doc
			matches = re.split(regex, url)
			
			if(len(matches) > 1):
				file_id = matches[1].replace("/","-") #Extract the id in the given format
			else:
				return
			
			url = "http://api.filesonic.com/link?method=getDownloadLink&u=%s&p=%s&ids=%s" % (user, password, file_id)
			link = None
			for line in URLOpen().open(url):
				if '"url"' in line:
					link = line.split('"url":"')[1].split('"')[0].replace("\\","")
					
			if not wait_func():
				return
			
			if not link:
				return
			else:
				return URLOpen().open(link, None, content_range)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		return CheckLinks().check_links(url)
