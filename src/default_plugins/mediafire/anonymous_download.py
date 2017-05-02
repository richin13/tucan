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

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		try:
			pkr = None
			cookie = cookielib.CookieJar()
			opener = URLOpen(cookie)
			res = ""
			#Open the first page
			page = opener.open(url).readlines()
			for line in page:
				#Get pKr
				if "pKr='" in line:
					pkr = line.split("'")[1].split("'")[0]
				#Get the last block to unescape
				if "unescape" in line:
					tmp = line.split("break;}")[-1]
					tmp = tmp.split("var cb")[0]
					tmp = self.split_eval(tmp)
				
					#Eval the block until it's plain text
					res = self.decrypt(tmp)

			id_func = res.split("(")[0] #Name of the function containig the id refering to the div that contains the real link

			pk1 = res.split("'")[3].split("'")[0]
			qk = res.split("'")[1].split("'")[0] #Public ID of the file

			it = iter(page)
			for line in it:
				#Line containing the function to parse
				if id_func in line:
					#Try to get the crypted block
					tmp = line.split(id_func)[1].split("setTimeout")[0].split('"none";')[1]
					tmp = self.split_eval(tmp)

					#Eval until it's plain text
					res = self.decrypt(tmp)


			div_id = res.split('getElementById("')[1].split('"')[0]

			data = urllib.urlencode([("qk",qk), ("pk1", pk1), ("r", pkr),])

			form_action = "http://www.mediafire.com/dynamic/download.php?%s" %data

			#Parse the GET
			res = opener.open(form_action, data)
			line = " ".join(res)
			#Long line containing the js
			if "var" in line:
				#Decrypt the table containig the final dl var
				tmp = line.split("function dz()")[0].split(";")[2:-1]
				tmp = ";".join(tmp)
				tmp = self.split_eval(tmp)
				table = self.decrypt(tmp)
				#Result is plain text
				if "http://download" in line:
					#Get all the dl links (even the fake ones)
					var = line.split('mediafire.com/" +')
					#Get the number of the server
					serv = line.split("http://download")[1].split(".")[0]
					#Get the name of the file
					name = var[1].split('+')[1].split("/")[2].split('"')[0].strip("\\")
					
					it = iter(var)
					#Find the real link among the fake ones
					for tmp in it:
						#Real link
						if div_id in tmp:
							tmp = it.next()
							tmp = tmp.split('+')[0]
							#Get the final dl var in the table
							dl = table.split(tmp+"=")[1].split(";")[0].strip("'")
				#Result is encrypted
				else:
					tmp = line.split("case 15:")[1]
					tmp = tmp.split("break;")[0]
					tmp = tmp.split("eval(")
					#Decrypt until the real link is found
					for t in tmp:
						if "unescape" in t:
							t = self.split_eval(t)
							res = self.decrypt(t,div_id)
							if len(res) == 3:
								serv = res[0]
								var = res[1]
								name = res[2]
								break
					dl = table.split(var+"=")[1].split(";")[0].strip("'")
			url = "http://download%s.mediafire.com/%sg/%s/%s" % (serv,dl,qk,name)
			try:
				handle = opener.open(url, None, content_range)
			except Exception, e:
				return self.set_limit_exceeded()
			else:
				return handle
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
				if 'download_file_title" style="margin:20px 0;">' in line:
					name = line.split('download_file_title" style="margin:20px 0;">')[1].split('<')[0].strip()
					tmp = line.split('color:#777;">')[1].split('<')[0].strip("()")
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
		
		
	def split_eval(self,tmp):
		if tmp.count("eval(") == 1:
			res = tmp.split("eval(")[0]
		else:
			res = tmp.replace('eval("',"")
			res = res.split("eval(")[0]
			res = res.replace("\\","")
		return res

	def decrypt(self,tmp,div=None):
		for j in range(10):
			res = ""
			try:
				bond = tmp.split("');")[1].split(";")[0].split("=")[1]
			#Happens sometimes, unecessary to continue at this point
			except:
				return []
			coef = tmp.split(")^")[1]
			coef = coef.split(")")[0]
			coef = coef.split("^")
			esc = urllib.unquote(tmp.split("unescape('")[1].split("');")[0])
			for i in range(int(bond)):
				ordt = int(esc[i*2:i*2+2],16)
				for a in coef:
					ordt = ordt^int(a)
				res = "%s%s" %(res,chr(ordt))
			
			#When the second request is encrypted
			if "http://download" in res:
				if div:
					if div in res:
						serv = res.split("http://download")[1].split(".")[0]
						var = res.split('" +')[1].split("+")[0]
						name = "g/".join(res.split('g/')[1:]).split("\\")[0].split("/")[1]
						return [serv, var, name]

			#Plain text
			if "unescape" not in res:
				return res
			else:
				tmp = self.split_eval(res)
