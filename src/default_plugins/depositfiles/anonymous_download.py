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

WAIT = 60 #Default, also parsed in the page if possible
BASE_URL = "http://depositfiles.com/en/files/"

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			wait = WAIT
			link = None
			opener = URLOpen()
			#Transform the url into an english one
			url = "%s%s" % (BASE_URL, url.split("/files/")[1].split("/")[0])
			form =  urllib.urlencode([('gateway_result','1')])
			for line in opener.open(url,form):
				#Try to get WAIT from the page
				if 'download_waiter_remain' in line:
					try:
						tmp = line.split(">")[2].split("<")[0]
						tmp = int(tmp)
					except Exception, e:
						pass
					else:
						if tmp > 0:
							wait = tmp
				elif "$('#download_container').load('" in line:
					try:
						tmp = line.split("load('")[1].split("'")[0]
						url = "%s%s" % ("http://depositfiles.com", tmp)
					except Exception, e:
						pass
					if not wait_func(wait + 1):
						return
					#Due to a bug in DepositFiles, sometimes it returns "Invalid params"
					#If it's the case, retry, 10 times and set limit exceeded
					for attempt in range(10):
						for line in opener.open(url):
							if "Invalid" in line:
								if not wait_func():
									return
								break
							elif "action" in line:
								link = line.split('"')[1].split('"')[0]
								break
						if link:
							break
				elif 'html_download_api-limit_interval' in line:
					tmp = int(line.split(">")[1].split("<")[0])
					return self.set_limit_exceeded(tmp)
			if not link:
				return self.set_limit_exceeded()
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			try:
				#No content-range support
				handle = URLOpen().open(link)
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
				if '<div class="info">' in line:
					name = it.next().split('="')[1].split('">')[0].strip()
					tmp = it.next().split('>')[2].split('<')[0].strip()
					unit = tmp[-2:]
					size = int(round(float(tmp[:-2].replace("&nbsp;",""))))
					
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
