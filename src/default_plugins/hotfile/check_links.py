###############################################################################
## Tucan Project
## Copyright (C)    2008-2010 Fran Lupion crak@tucaneando.com
##                       2011 Ali Shah ahshah@airpost.net
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
from core.url_open import URLOpen
logger = logging.getLogger(__name__)

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		if url is None:
			return None

		name   = None
		size   = -1
		unit   = None
		status = -1
		
		"""
		Split the string by '/':
		Hotfile urls are always of this form:
			http://hotfile.com/dl/ID/KEY/filename.html
		Thus we should get the (0 based) 4th & 5th entry in the returned list
		"""
		split_str = url.split('/')
		if len(split_str) is not 7:
			return None

		link_id  = split_str[4]
		link_key = split_str[5]
		del split_str
		check_link_url = ("http://api.hotfile.com/?action=checklinks&ids=" + link_id + 
						  "&keys=" + link_key + "&fields=name,size,status")
		""" print ("Check link url: {0}".format(check_link_url))  """
		try: 
			link_name_size_status = URLOpen().open(check_link_url).readline()
			link_name_size_status_list = link_name_size_status.split(',')
			name   = link_name_size_status_list[0]
			""" Hotfile glitch: sometimes removed files do not have size information """
			if ( len(link_name_size_status_list[1]) != 0):
				size   = int(link_name_size_status_list[1]) / 1024

			status = int(link_name_size_status_list[2])
			unit = "KB"
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
			
		if status != 1:
			""" print ("Link is down! {0} {1}|".format(type(status), status)) """
			return None, -1, None
		else:
			return name, size, unit
