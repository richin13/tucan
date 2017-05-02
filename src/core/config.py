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
import uuid
import shutil
import logging
logger = logging.getLogger(__name__)

from ConfigParser import SafeConfigParser

import service_config
import cons
import shared

CONF = "tucan.conf"

COMMENT = """# Tucan Manager's default configuration.
# Dont change anything unless you really know what are doing, 
# instead use the preferences dialog of the GUI."""

SECTION_MAIN = "main"
SECTION_SERVICES = "services"
SECTION_UI = "ui"
SECTION_ADVANCED = "advanced"

#main options
OPTION_VERSION = "version"
OPTION_UUID = "uuid"

OPTION_LANGUAGE = "language"
OPTION_MAX_DOWNLOADS = "max_downloads"
OPTION_MAX_DOWNLOAD_SPEED = "max_download_speed"
#OPTION_MAX_UPLOADS = "max_uploads"
OPTION_DOWNLOADS_FOLDER = "downloads_folder"

#ui options
OPTION_TRAY_CLOSE = "tray_close"
OPTION_CLIPBOARD_MONITOR = "clipboard_monitor"
OPTION_WINDOW_SETTINGS = "window_settings"
OPTION_ADVANCED_PACKAGES = "advanced_packages"
OPTION_SHOW_UPLOADS = "show_uploads"

#advanced options
OPTION_AUTO_UPDATE = "auto_update"
OPTION_ENABLE_PROXY = "enable_proxy"
OPTION_PROXY_URL = "proxy_url"
OPTION_PROXY_PORT = "proxy_port"

DEFAULTS = {SECTION_MAIN: {OPTION_VERSION: cons.TUCAN_VERSION, OPTION_LANGUAGE: "en", OPTION_MAX_DOWNLOADS: "5", OPTION_MAX_DOWNLOAD_SPEED: "0", OPTION_DOWNLOADS_FOLDER: cons.DEFAULT_PATH.encode("utf-8")}
	, SECTION_SERVICES: {}
	, SECTION_UI: {OPTION_TRAY_CLOSE: "False", OPTION_CLIPBOARD_MONITOR: "True", OPTION_WINDOW_SETTINGS: "-1,-1,-1,-1", OPTION_ADVANCED_PACKAGES: "False",OPTION_SHOW_UPLOADS: "False"}
	, SECTION_ADVANCED: {OPTION_AUTO_UPDATE: "True", OPTION_ENABLE_PROXY: "False", OPTION_PROXY_URL: "", OPTION_PROXY_PORT: "0"}}

class Config(SafeConfigParser):
	""""""
	def __init__(self):
		""""""
		SafeConfigParser.__init__(self)
		self.configured = True
		if not os.path.exists(cons.CONFIG_PATH + CONF):
			self.create_config()
			self.configured = False
		else:
			self.read(cons.CONFIG_PATH + CONF)
			if not self.check_config():
				self.create_config()
				self.configured = False
		if not os.path.exists(cons.PLUGIN_PATH):
			shutil.copytree(cons.DEFAULT_PLUGINS, cons.PLUGIN_PATH)
			for service in os.listdir(cons.PLUGIN_PATH):
				if os.path.isdir(os.path.join(cons.PLUGIN_PATH, service)):
					path = os.path.join(cons.PLUGIN_PATH, service, "")
					package, icon, name, enabled, config = self.service(path)
					if name:
						self.set(SECTION_SERVICES, name, path.encode("utf-8"))
			self.save()

	def check_config(self):
		""""""
		for section, options in DEFAULTS.items():
			if self.has_section(section):
				if section == SECTION_MAIN:
					if self.has_option(section, OPTION_VERSION):
						if self.get(section, OPTION_VERSION) != cons.TUCAN_VERSION:
							shutil.rmtree(cons.PLUGIN_PATH)
							return False
					else:
						shutil.rmtree(cons.PLUGIN_PATH)
						return False
				for option, value in options.items():
					if option not in [option for option, value in self.items(section)]:
						return False
			else:
				return False
		return True

	def create_config(self):
		""""""
		for section, options in DEFAULTS.items():
			if not self.has_section(section):
				self.add_section(section)
			for option, value in options.items():
				self.set(section, option, value)
		#set uuid
		self.set(SECTION_MAIN, OPTION_UUID, str(uuid.uuid1()))
		self.save()

	def get_version(self):
		""""""
		if self.has_option(SECTION_MAIN, OPTION_VERSION):
			return self.get(SECTION_MAIN, OPTION_VERSION)

	def get_uuid(self):
		""""""
		if self.has_option(SECTION_MAIN, OPTION_UUID):
			return self.get(SECTION_MAIN, OPTION_UUID)
		else:
			new_uuid = str(uuid.uuid1())
			self.set(SECTION_MAIN, OPTION_UUID, new_uuid)
			self.save()
			return new_uuid

	def get_languaje(self):
		""""""
		return self.get(SECTION_MAIN, OPTION_LANGUAGE)

	def set_languaje(self, value):
		""""""
		self.set(SECTION_MAIN, OPTION_LANGUAGE, value)

	def get_max_downloads(self):
		""""""
		return self.getint(SECTION_MAIN, OPTION_MAX_DOWNLOADS)

	def set_max_downloads(self, value):
		""""""
		self.set(SECTION_MAIN, OPTION_MAX_DOWNLOADS, str(value))
		shared.max_downloads = value

	def get_max_download_speed(self):
		""""""
		return self.getint(SECTION_MAIN, OPTION_MAX_DOWNLOAD_SPEED)

	def set_max_download_speed(self, value):
		""""""
		self.set(SECTION_MAIN, OPTION_MAX_DOWNLOAD_SPEED, str(value))
		shared.max_download_speed = value

	def get_downloads_folder(self):
		""""""
		if self.has_option(SECTION_MAIN, OPTION_DOWNLOADS_FOLDER):
			return self.get(SECTION_MAIN, OPTION_DOWNLOADS_FOLDER).decode("utf-8")
		else:
			return cons.DEFAULT_PATH

	def set_downloads_folder(self, path):
		""""""
		self.set(SECTION_MAIN, OPTION_DOWNLOADS_FOLDER, path.encode("utf-8"))

	def get_tray_close(self):
		""""""
		return self.getboolean(SECTION_UI, OPTION_TRAY_CLOSE)

	def set_tray_close(self, value):
		""""""
		self.set(SECTION_UI, OPTION_TRAY_CLOSE, str(value))

	def get_clipboard_monitor(self):
		""""""
		return self.getboolean(SECTION_UI, OPTION_CLIPBOARD_MONITOR)

	def set_clipboard_monitor(self, value):
		""""""
		self.set(SECTION_UI, OPTION_CLIPBOARD_MONITOR, str(value))

	def get_window_settings(self):
		""""""
		if self.has_option(SECTION_UI, OPTION_WINDOW_SETTINGS):
			tmp = self.get(SECTION_UI, OPTION_WINDOW_SETTINGS)
			try:
				x, y, w, h = tmp.split(",")
				x = int(x)
				y = int(y)
				w = int(w)
				h = int(h)
			except:
				logger.warning("Wrong window settings!: %s" % tmp)
				return -1, -1, -1, -1
			return x, y, w, h
		else:
			return -1, -1, -1, -1

	def set_window_settings(self, x, y, w, h):
		""""""
		self.set(SECTION_UI, OPTION_WINDOW_SETTINGS, "%i,%i,%i,%i" % (x, y, w, h))

	def get_advanced_packages(self):
		""""""
		return self.getboolean(SECTION_UI, OPTION_ADVANCED_PACKAGES)

	def set_advanced_packages(self, value):
		""""""
		self.set(SECTION_UI, OPTION_ADVANCED_PACKAGES, str(value))

	def get_show_uploads(self):
		""""""
		return self.getboolean(SECTION_UI, OPTION_SHOW_UPLOADS)

	def set_show_uploads(self, value):
		""""""
		self.set(SECTION_UI, OPTION_SHOW_UPLOADS, str(value))

	def get_auto_update(self):
		""""""
		return self.getboolean(SECTION_ADVANCED, OPTION_AUTO_UPDATE)

	def set_auto_update(self, value):
		""""""
		self.set(SECTION_ADVANCED, OPTION_AUTO_UPDATE, str(value))

	def get_proxy_enabled(self):
		""""""
		return self.getboolean(SECTION_ADVANCED, OPTION_ENABLE_PROXY)

	def set_proxy_enabled(self, value):
		""""""
		self.set(SECTION_ADVANCED, OPTION_ENABLE_PROXY, str(value))

	def get_proxy(self):
		""""""
		result = "", 0
		if self.has_section(SECTION_ADVANCED):
			if self.getboolean(SECTION_ADVANCED, OPTION_ENABLE_PROXY):
				result = self.get(SECTION_ADVANCED, OPTION_PROXY_URL), self.getint(SECTION_ADVANCED, OPTION_PROXY_PORT)
		return result

	def set_proxy(self, url, port):
		""""""
		self.set(SECTION_ADVANCED, OPTION_PROXY_URL, url)
		self.set(SECTION_ADVANCED, OPTION_PROXY_PORT, str(port))

	def get_services(self):
		""""""
		result = []
		for service, path in self.items(SECTION_SERVICES):
			result.append(self.service(path.decode("utf-8")))
		return sorted(result)

	def service(self, path):
		""""""
		result = path, None, None, None, None
		config = service_config.ServiceConfig(path)
		if config.check_config():
			icon = config.get_icon()
			name = config.get(service_config.SECTION_MAIN, service_config.OPTION_NAME)
			enabled = config.getboolean(service_config.SECTION_MAIN, service_config.OPTION_ENABLED)
			result = os.path.split(os.path.split(path)[0])[1], icon, name, enabled, config
		return result

	def save(self, comment=True):
		""""""
		f = open(cons.CONFIG_PATH + CONF, "w")
		if comment:
			f.write(COMMENT + "\n\n")
		self.write(f)
		f.close()

if __name__ == "__main__":
	c = Config()
	print c.configured
