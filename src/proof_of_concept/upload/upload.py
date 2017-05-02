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

import urllib2
import logging
logger = logging.getLogger(__name__)

from poster.streaminghttp import StreamingHTTPHandler

class NewStreamingHTTPHandler(StreamingHTTPHandler):
	""""""
	def do_open(self, http_class, req):
		""""""
		if req.data:
			tmp = req.get_data()
			#Add some magic here
			req.data = tmp
		return urllib2.HTTPHandler.do_open(self, http_class, req)

def register_openers():
    """Register the streaming http handlers in the global urllib2 default
    opener object.

    Returns the created OpenerDirector object."""
    handlers = [NewStreamingHTTPHandler]

    opener = urllib2.build_opener(*handlers)

    urllib2.install_opener(opener)

    return opener
