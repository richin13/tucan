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

import os.path
import tempfile
import tarfile
import random
import urllib2
import logging
logger = logging.getLogger(__name__)

from ConfigParser import SafeConfigParser

from url_open import URLOpen
from service_config import ServiceConfig

import config
import cons
import shared

SECTION_MAIN = "main"
SECTION_UPDATES = "updates"
OPTION_VERSION = "version"

FORJA = "https://forja.rediris.es/svn/cusl3-tucan/branches/update_manager/0.3.10/"
BTD = "http://build-tucan-doc.googlecode.com/svn/branches/update_manager/0.3.10/"

SERVERS = [BTD, FORJA]
UPDATE_FILE = "updates.conf"
EXTENSION = ".tar.gz"

class RemoteInfo(SafeConfigParser):
	""""""
	def __init__(self, server, fd):
		""""""
		SafeConfigParser.__init__(self)
		self.readfp(fd)
		self.server = server
		self.version = self.get(SECTION_MAIN, OPTION_VERSION)
		self.services = self.items(SECTION_UPDATES)

class ServiceUpdate:
	""""""""
	def __init__(self, info=None):
		"""urllib2 does not support proxy and https"""
		self.config = shared.configuration
		self.remote_outdated = False
		self.remote_version = None
		self.updates = None
		self.remote_info = info

	def get_updates(self):
		""""""
		self.updates = {}
		tmp = SERVERS
		random.shuffle(tmp)
		if not self.remote_info:
			for server in tmp:
				try:
					logger.debug("Update Server: %s" % server)
					fd = URLOpen().open("%s%s" % (server, UPDATE_FILE))
				except Exception, e:
					logger.exception(e)
				else:
					self.remote_info = RemoteInfo(server, fd)
					break
		if self.remote_info:
			self.remote_version = self.remote_info.version
			self.local_services = self.config.get_services()
			if self.check_version():
				for remote_service, remote_version in self.remote_info.services:
					archive = "%s%s" % (self.remote_info.server, remote_service.split(".")[0] + EXTENSION)
					#get local version
					found = False
					for local_service in self.local_services:
						if local_service[2] == remote_service:
							found = True
							local_version = local_service[4].get_update()
							if int(remote_version) > local_version:
								self.updates[local_service[2]] = local_service[0], archive, local_service[1]
					if not found:
						self.updates[remote_service] = remote_service.split(".")[0], archive, None
				if len(self.updates) > 0:
					return True
					
	def check_version(self):
		"""remote version should not be smaller than local version"""
		try:
			remote = self.remote_version.split(" ")[0].split(".")
			local = cons.TUCAN_VERSION.split(" ")[0].split(".")
			for i in range(len(remote)):
				if int(local[i]) > int(remote[i]):
					logger.info("Remote version older than local.")
					self.remote_outdated = True
					return
		except:
			logger.info("RC releases have no updates.")
			self.remote_outdated = True
		else:
			return True

	def install_service(self, service_name, service_dir, archive):
		""""""
		logger.warning("Updating: %s" % service_name)
		try:
			#Get the state of the plugin before the update
			if self.config.has_option(config.SECTION_SERVICES, service_name):
				enabled = self.config.service(os.path.join(cons.PLUGIN_PATH, service_dir, ""))[3]
			fd = tempfile.TemporaryFile()
			fd.write(URLOpen().open(archive).read())
			fd.seek(0)
			tar_package = tarfile.open("", 'r:gz', fd)
			tar_package.extractall(cons.PLUGIN_PATH)
			tar_package.close()
			fd.close()
			if not self.config.has_option(config.SECTION_SERVICES, service_name):
				self.config.set(config.SECTION_SERVICES, service_name, os.path.join(cons.PLUGIN_PATH, service_dir, ""))
			else:
				#Set the previous state of the plugin
				self.config.service(os.path.join(cons.PLUGIN_PATH, service_dir, ""))[4].enable(enabled)
		except Exception, e:
			logger.exception(e)
		else:
			return True
