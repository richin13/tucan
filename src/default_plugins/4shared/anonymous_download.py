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

import logging
logger = logging.getLogger(__name__)

import cookielib

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen

WAIT = 20

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			tmp_link = None
			link = None
			wait = WAIT
			opener = URLOpen(cookielib.CookieJar())
			it = opener.open(url)
			for line in it:
				if "dbtn" in line:
					tmp_link = line.split('href="')[1].split('"')[0]
			if tmp_link:
				it = opener.open(tmp_link)
				for line in it:
					if "id='divDLStart'" in line:
						link = it.next().split("<a href='")[1].split("'")[0]
					elif '<div class="sec">' in line:
						wait = int(line.split(">")[1].split("<")[0])
			if not link:
				return
			elif not wait_func(wait):
				return
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			try:
				handle = opener.open(link)
			except Exception, e:
				return self.set_limit_exceeded()
			else:
				return handle

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		size_found = False
		try:
			it = URLOpen().open(url)
			for line in it:
				if '<span id="fileNameTextSpan">' in line:
					name = line.split('<span id="fileNameTextSpan">')[1].split('</span>')[0].strip()
					break
				elif '<div class="small lgrey" style="margin-bottom:5px">' in line:
					size_found = True
				elif size_found:
					size_found = False
					tmp = line.split("<b>")[1].split("</b>")[0].split()
					unit = tmp[1]
					if "," in tmp[0]:
						size = int(tmp[0].replace(",", ""))
					else:
						size = int(tmp[0])
					if size > 1024:
						if unit == "KB":
							size = size / 1024
							unit = "MB"
		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
