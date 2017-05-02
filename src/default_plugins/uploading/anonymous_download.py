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
import cookielib

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen

JS_URL = "http://uploading.com/files/get/?JsHttpRequest=0-xml"
WAIT = 60 

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			opener = URLOpen(cookielib.CookieJar())
			#First req to get to the timer
			it = opener.open(url)
			for line in it:
				if '"page pageDownloadAvm"' in line:
					try:
						form_action = it.next().split('"')[1].split('"')[0]
						it.next()
						#action = it.next().split('value="')[1].split('"')[0]
						file_id = it.next().split('value="')[1].split('"')[0]
						code = it.next().split('value="')[1].split('"')[0]
						break
					except:
						return self.set_limit_exceeded()
			form = urllib.urlencode([("action", "second_page"), ("file_id", file_id), ("code", code)])
			#Second req to get to the timer
			it = opener.open(form_action, form)
			for line in it:
				if 'id="timeadform"' in line:
					form_action = line.split('"')[1].split('"')[0]
					it.next()
					#action = it.next().split('value="')[1].split('"')[0]
					file_id = it.next().split('value="')[1].split('"')[0]
					code = it.next().split('value="')[1].split('"')[0]
					break
			if not wait_func(WAIT):
				return
			#Ajax req to get the link
			data = urllib.urlencode([("action", "get_link"), ("file_id", file_id), ("code", code), ("pass", "undefined")])
			tmp = opener.open(JS_URL, data).read()
			if 'link' in tmp:
				link = tmp.split('"link":"')[1].split('"')[0]
				link = urllib.unquote(link).replace("\\", "")
				return opener.open(link, None, content_range)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		size_found = 0
		try:
			it = URLOpen().open(url)
			for line in it:
				if '#383737' in line:
					name = it.next().split('>')[1].split('<')[0].strip()
					tmp = it.next().split('>')[1].split('<')[0].strip()
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
