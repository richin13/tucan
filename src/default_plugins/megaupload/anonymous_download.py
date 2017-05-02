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
from core.tesseract import Tesseract

import core.cons as cons

WAIT = 45

CAPTCHACODE = "captchacode"
MEGAVAR = "megavar"

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		link = None
		wait = WAIT
		try:
			for line in URLOpen().open(url).readlines():
				if 'id="downloadlink"' in line:
					link = line.split('href="')[1].split('"')[0]
				if "count=" in line:
					wait = int(line.split("=")[1].split(";")[0])
			if not link:
				return
			elif not wait_func(WAIT):
				return
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			try:
				handle = URLOpen().open(link, None, content_range)
			except:
				return self.set_limit_exceeded()
			else:
				return handle

	def check_links(self, url):
		""""""
		return CheckLinks().check(url)
