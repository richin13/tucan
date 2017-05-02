###############################################################################
## Tucan Project
## Copyright (C)      2011 Ali Shah    ahshah@airpost.net
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
import urllib2
from core.url_open import URLOpen
logger = logging.getLogger(__name__)

class CheckLinks():
	""""""
	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			it = URLOpen().open(url)
			for line in it:
				if 'Filename:' in line:
					name = line.split(">")[1].split("<")[0]
					line = it.next()
					size_and_units = []
					size_and_units = line.split(":")[1].split("<")[0].lstrip().rstrip().split(" ")
					size = float(size_and_units[0])
					unit = size_and_units[1].upper()
					if 'B' == unit:
						size = size / 1024
						unit = "KB"
					break
		# Oron responds to unknown files as HTTP 404s followed by a redirect
		except urllib2.HTTPError as http_error:
			if http_error.code != 404:
				logger.warning("Oron::check_links: Received unexpected HTTP error code: %s" % http_error.code)
			return None, -1, None

		except Exception, e:
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
