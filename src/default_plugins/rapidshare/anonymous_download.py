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

from check_links import CheckLinks

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen
from core.slots import Slots

#MAX_SIZE = 209796096
MAX_SIZE = None

API_URL = "/cgi-bin/rsapi.cgi?sub=download"

class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		link = None
		wait = 0
		try:
			tmp = url.split("/")
			opener = URLOpen()
			url = "%s&fileid=%s" % (API_URL,tmp[4])
			url = "%s&filename=%s" % (url,tmp[5])
			for line in opener.open("http://%s%s" % ("api.rapidshare.com",url)):
				print line
				if "DL:" in line:
					tmp = line.split("DL:")[1].split(",")
					link = "http://%s%s&dlauth=%s" % (tmp[0],url,tmp[1])
					wait = int(tmp[2])
					print link
			if not wait_func(wait):
				return
			if link:
				return URLOpen().open(link, content_range)
			else:
				return self.set_limit_exceeded()
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		return CheckLinks().check(url, MAX_SIZE)
