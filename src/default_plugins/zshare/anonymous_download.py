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

import logging
logger = logging.getLogger(__name__)

import urllib
import cookielib

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen

WAIT = 50 #Default, also parsed in the page if possible

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			link = None
			cookie = cookielib.CookieJar()
			opener = URLOpen(cookie)
			if "/video/" in url:
				url = url.replace("/video/", "/download/")
			elif "/audio/" in url:
				url = url.replace("/audio/", "/download/")
			elif "/image/" in url:
				url = url.replace("/image/", "/download/")
			try:
				form = urllib.urlencode([("download", 1)])
				for line in opener.open(url,form):
					if 'link_enc=new Array' in line:
						tmp = line.strip().split("var link_enc=new Array(")[1].split(");")[0]
						link = tmp.replace("','","").replace("'","")
					#Try to get WAIT from the page
					if 'document|important' in line:
						try:
							tmp = line.split("here|")[1].split("|class")[0]
							tmp = int(tmp)
						except ValueError:
							pass
						else:
							if tmp > 0:
								WAIT = tmp
						break
			except Exception, e:
				logger.exception("%s :%s" % (url, e))
				
			if not link:
				return
			if not wait_func(WAIT):
				return
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			try:
				handle = opener.open(link, None, content_range)
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
			it = URLOpen().open(url)
			for line in it:
				if 'File Name:' in line:
					name = it.next().split('>')[1].split('<')[0]
				if 'File Size:' in line:
					tmp = line.split('>')[3].split('<')[0]
					if "KB" in tmp:
						size = int(round(float(tmp.split("KB")[0])))
						unit = "KB"
					elif "MB" in tmp:
						size = float(tmp.split("MB")[0])
						if int(round(size)) > 0:
							size = int(round(size))
							unit = "MB"
						else:
							size = int(round(1024 * size))
							unit = "KB"
					elif "GB" in tmp:
						size = int(round(float(tmp.split("GB")[0])))
						unit = "GB"
		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
