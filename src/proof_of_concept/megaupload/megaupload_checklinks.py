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

import captcha
import cons

class CheckLinks:
	""""""
	def check(self, url):
		""""""
		name = None
		size = 0
		unit = None
		try:
			for line in urllib2.urlopen(urllib2.Request(url)).readlines():
				if "<b>Filename:</b>" in line:
					name = line.split("<b>Filename:</b>")[1].split("</div>")[0].strip()
				elif "<b>Filesize:</b>" in line:
					tmp = line.split("<b>Filesize:</b>")[1].split("</div>")[0].split(" ")
					size = int(round(float(tmp[1])))
					unit = tmp[2]
			if name:
				if ".." in name:
					parser = captcha.CaptchaForm(url)
					if parser.link:
						name = parser.link.split("/").pop()
		except urllib2.URLError, e:
			print e
		return name, size, unit
