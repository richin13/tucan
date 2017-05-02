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

import os
import socket
import sys
import stat
import mimetypes
import mimetools
import httplib
import urllib
import urllib2

CHUNK_SIZE = 4096
CRLF = '\r\n'

#class MultipartHTTPHandler(urllib2.HTTPCookieProcessor):
class MultipartHTTPHandler(urllib2.HTTPHandler):
	"""Based on urllib2_file-0.2 Fabien SEISEN"""

	handler_order = urllib2.HTTPHandler.handler_order - 10

	def get_content_type(self, filename):
		""""""
		return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

	def send_data(self, data, boundary, sock=None):
		"""if sock is None, juste return the estimate size"""
		length = 0
		for key, value in data:
			if hasattr(value, 'read'):
				file_size = os.fstat(value.fileno())[stat.ST_SIZE]
				length += file_size

				name = os.path.basename(value.name)

				buffer = []
				buffer.append("--%s" % boundary)
				buffer.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, name))
				buffer.append("Content-Type: %s" % self.get_content_type(name))
				buffer.append("")
				buffer.append("")
				buffer = CRLF.join(buffer)
				length += len(buffer)

				if sock:
					sock.send(buffer)
					size = 0
					chunk = "None"
					while chunk:
						chunk = value.read(CHUNK_SIZE)
						size += len(chunk)
						print int((float(size)/file_size)*100)
						sock.send(chunk)
					value.close()
			elif value == None:
				buffer = []
				buffer.append("--%s" % boundary)
				buffer.append('Content-Disposition: form-data; name="%s"; filename=""' % key)
				buffer.append("Content-Type: application/octet-stream")
				buffer.append("")
				buffer.append("")
				buffer = CRLF.join(buffer)
				length += len(buffer)
			else:
				buffer = []
				buffer.append("--%s" % boundary)
				buffer.append('Content-Disposition: form-data; name="%s"' % key)
				buffer.append("")
				buffer.append("%s" % value)
				buffer.append("")

				buffer = CRLF.join(buffer)
				length += len(buffer)

				if sock:
					sock.send(buffer)

		buffer = []
		buffer.append("")
		buffer.append("--%s--" % boundary)
		buffer.append("")
		buffer = CRLF.join(buffer)
		length += len(buffer)

		if sock:
			sock.send(buffer)
		return length

	def http_open(self, req):
		""""""
		return self.do_open(httplib.HTTPConnection, req)

	def do_open(self, http_class, req):
		""""""
		data = req.get_data()
		
		files = False
		for key, value in data:
			if hasattr(value, 'read'):
				files = True

		host = req.get_host()
		# parse host:port
		h = http_class(host) 
		if req.has_data():
			h.putrequest('POST', req.get_selector())
			if not 'Content-type' in req.headers:
				if files:
					boundary = mimetools.choose_boundary()
					length = self.send_data(data, boundary)
					h.putheader('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
					h.putheader('Content-length', str(length))
		else:
			h.putrequest('GET', req.get_selector())

		scheme, sel = urllib.splittype(req.get_selector())
		sel_host, sel_path = urllib.splithost(sel)
		h.putheader('Host', sel_host or host)

		for name, value in self.parent.addheaders:
			name = name.capitalize()
			if name not in req.headers:
				h.putheader(name, value)

		for key, value in req.headers.items():
			h.putheader(key, value)

		h.endheaders()
		if req.has_data():
			if files:
				print self.send_data(data, boundary, h)
		#addinfo
		try:
			r = h.getresponse()
			r.recv = r.read
			fp = socket._fileobject(r, close=True)
			resp = urllib.addinfourl(fp, r.msg, req.get_full_url())
			resp.code = r.status
			resp.msg = r.reason
			return resp

		except socket.error, err:
			raise URLError(err)
