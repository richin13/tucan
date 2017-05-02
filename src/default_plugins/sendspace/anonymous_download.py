###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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

import urllib

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			link = None
			opener = URLOpen()
			form =  urllib.urlencode([('download','&nbsp;REGULAR DOWNLOAD&nbsp;')])
			for line in opener.open(url,form):
				if '<span id="spn_download_link">' in line:
					link = line.split('href="')[1].split('"')[0]
			if not link:
				return
			if not wait_func():
				return
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			try:
				handle = URLOpen().open(link, None, content_range)
			except Exception, e:
				return self.set_limit_exceeded()
			else:
				return handle

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		size_found = 0
		try:
			for line in URLOpen().open(url):
				if '<b>Name:</b>' in line:
					name = line.split('<b>Name:</b>')[1].split('<br>')[0].strip()
					tmp = line.split('<b>Size:</b> ')[1].split('   ')[0].strip()
					unit = tmp[-2:]
					size = int(round(float(tmp[:-2])))
					
					if size > 1024:
						if unit == "KB":
							size = size / 1024
							unit = "MB"
					break
		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
