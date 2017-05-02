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

import socket
import urllib2
import logging
logger = logging.getLogger(__name__)

from poster.encode import multipart_encode
from poster.streaminghttp import StreamingHTTPHandler

import shared
import cons

def set_proxy(url, port=0):
	""""""
	if url:
		shared.proxy = {"http": "%s:%i" % (url, port)}
		socket.setdefaulttimeout(60)
		logger.info("Using proxy: %s:%i" % (url, port))
	else:
		if shared.proxy:
			shared.proxy = None
			logger.info("Proxy Disabled.")
		socket.setdefaulttimeout(30)

class URLOpen:
	""""""
	def __init__(self, cookie=None):
		""""""
		handlers = [urllib2.HTTPCookieProcessor(cookie)]
		if shared.proxy:
			handlers.append(urllib2.ProxyHandler(shared.proxy))
		self.opener = urllib2.build_opener(*handlers)

	def open(self, url, form=None, range=None, keep_alive=False, referer=False):
		""""""
		headers = {"User-Agent": cons.USER_AGENT}
		if range:
			headers["Range"] = "bytes=%s-" % range
		if keep_alive:
			headers["Connection"] = "Keep-alive"
		if referer:
			headers["Referer"] = referer
		if form:
			return self.opener.open(urllib2.Request(url, None, headers), form)
		else:
			return self.opener.open(urllib2.Request(url, None, headers))

class MultipartEncoder:
	""""""
	def __init__(self, url, form, boundary=None, cookie=None):
		""""""
		self.url = url
		self.form = form
		self.boundary = boundary

		handlers = [StreamingHTTPHandler]
		if shared.proxy:
			handlers.append(urllib2.ProxyHandler(shared.proxy))
		if cookie:
			handlers.append(urllib2.HTTPCookieProcessor(cookie))
		self.opener = urllib2.build_opener(*handlers)

	def open(self, callback):
		""""""
		datagen, headers = multipart_encode(self.form, self.boundary, callback)
		headers["User-Agent"] = cons.USER_AGENT
		return self.opener.open(urllib2.Request(self.url, datagen, headers))
