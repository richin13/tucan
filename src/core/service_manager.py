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

import re
import sys
import logging
logger = logging.getLogger(__name__)

import cons
import shared

class Service:
	""""""
	def __init__(self, name, icon):
		""""""
		self.icon_path = icon
		self.name = name
		self.download_plugins = {}
		self.upload_plugins = {}
		
	def add_plugins(self, package, config):
		""""""
		plugins = 0
		#download plugins
		for plugin_module, plugin_name, plugin_type in config.get_download_plugins():
			logger.info("Loading: %s.%s, %i" % (package, plugin_module, config.get_update()))
			try:
				shared.dependencies.check(config.get_captcha(plugin_module))
				module = __import__("%s.%s" % (package, plugin_module), None, None, [''])
				self.download_plugins[plugin_type] = eval("module.%s(config, '%s')" % (plugin_name, plugin_module))
			except Exception, e:
				logger.error("%s.%s: %s" % (package, plugin_module, e))
			else:
				if plugin_type in [cons.TYPE_PREMIUM, cons.TYPE_USER]:
					if self.download_plugins[plugin_type].active:
						plugins += 1
				else:
					plugins += 1
		#upload plugins
		#for plugin_module, plugin_name, plugin_type in config.get_upload_plugins():
			#logger.info("Loading: %s.%s, %i" % (package, plugin_module, config.get_update()))
			#module = __import__("%s.%s" % (package, plugin_module), None, None, [''])
			#self.upload_plugins[plugin_type] = eval("module.%s(config, '%s')" % (plugin_name, plugin_module))
		return plugins

	def get_download_plugin(self):
		""""""
		plugins = self.download_plugins
		if cons.TYPE_PREMIUM in plugins:
			if plugins[cons.TYPE_PREMIUM].active:
				return plugins[cons.TYPE_PREMIUM], cons.TYPE_PREMIUM
		if cons.TYPE_USER in plugins:
			if plugins[cons.TYPE_USER].active:
				return plugins[cons.TYPE_USER], cons.TYPE_USER
		if cons.TYPE_ANONYMOUS in plugins:
			return plugins[cons.TYPE_ANONYMOUS], cons.TYPE_ANONYMOUS
			
	def get_upload_plugins(self):
		""""""
		result = []
		plugins = self.upload_plugins
		for plugin_type, plugin in plugins.items():
			if plugin_type in [cons.TYPE_PREMIUM, cons.TYPE_USER]:
				if plugin.active:
					result.append((plugin_type, plugin))
				else:
					logging.warning("%s has no active account!" % plugin.__module__)
			elif plugin_type == cons.TYPE_ANONYMOUS:
				result.append((plugin_type, plugin))
		return result

	def clean(self):
		""""""
		for plugin in self.download_plugins.values():
			plugin.stop_all()

class ServiceManager:
	""""""
	def __init__(self):
		""""""
		self.services = []
		if cons.PLUGIN_PATH not in sys.path:
			sys.path.append(cons.PLUGIN_PATH)
		for package, icon, service, enabled, config in shared.configuration.get_services():
			s = Service(service, icon)
			if enabled:
				if s.add_plugins(package, config):
					self.services.append(s)
		if len(self.services) == 0:
			logger.warning("No services loaded!")

	def get_download_plugin(self, service_name):
		""""""
		for service in self.services:
			if service.name == service_name:
				return service.get_download_plugin()

	def get_check_links(self, service_name):
		""""""
		plugin, type = self.get_download_plugin(service_name)
		return plugin.check_links, type
		
	def stop_all(self):
		""""""
		for service in self.services:
			service.clean()

	def filter_service(self, links):
		""""""
		services = {cons.TYPE_UNSUPPORTED: []}
		for link in links:
			found = False
			if "http://" in link:
				tmp = link.split("http://").pop()
				if "<" in tmp:
					tmp = tmp.split("<")[0]
				elif " " in tmp:
					tmp = tmp.split(" ")[0]
				elif "[" in tmp:
					tmp = tmp.split("[")[0]
				elif "'" in tmp:
					tmp = tmp.split("'")[0]
				link = "http://%s" % tmp
				for service in self.services:
					if link.find(service.name) > 0:
						found = True
						if service.name in services:
							services[service.name].append(link)
						else:
							services[service.name] = [link]
				if not found:
						services[cons.TYPE_UNSUPPORTED].append(link)
		return services

	def create_packages(self, dict):
		""""""
		packages = []
		files = []
		for service, links in dict.items():
			for link in links:
				found = False
				for tmp_link in files:
					if link[1] == tmp_link[1]:
						found = True
						if service not in tmp_link[2]:
							tmp_link[2].append(service)
							tmp_link[0].append(link[0])
							tmp_link[5].append(link[4])
				if not found:
					files.append(([link[0]], link[1], [service], link[2], link[3], [link[4]]))
		while len(files) > 0:
			tmp_name = []
			first = files[0]
			others = files[1:]
			for link in others:
				chars = re.split("[0-9]+", link[1])
				nums = re.split("[^0-9]+", link[1])
				tmp = ""
				for i in chars:
					if tmp+i == first[1][0:len(tmp+i)]:
						tmp += i
						for j in nums:
							if tmp+j == first[1][0:len(tmp+j)]:
								tmp += j
				tmp_name.append(tmp)
			final_name = ""
			for name in tmp_name:
				if len(name) > len(final_name):
					final_name = name
			if len(final_name) > 0:
				packages.append((final_name, [first]))
				del files[files.index(first)]
				tmp_list = []
				for link in files:
					if final_name in link[1]:
						tmp_list.append(link)
				for package_name, package_files in packages:
					if package_name == final_name:
						package_files += tmp_list
				for i in tmp_list:
					del files[files.index(i)]
			else:
				alone_name = first[1]
				if "." in alone_name:
					alone_name = alone_name.split(".")
					alone_name.pop()
					alone_name = ".".join(alone_name)
				packages.append((alone_name, [first]))
				del files[files.index(first)]
		return packages
