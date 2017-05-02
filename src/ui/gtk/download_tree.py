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
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from core.download_manager import DownloadManager

from tree import Tree

import core.shared as shared

class DownloadTree(Tree, DownloadManager):
	""""""
	def __init__(self):
		""""""
		DownloadManager.__init__(self, lambda x: x, [])
		Tree.__init__(self, [None], self)

		self.config = shared.configuration
		
	def manage_packages(self, packages, packages_info):
		""""""
		tmp_packages = []
		if not len(packages_info) > 0:
			default_path = self.config.get_downloads_folder()
			packages_info = [(default_path, name, None) for name, package_files in packages]
		#create directories and password files
		for info in packages_info:
			package_path = os.path.join(info[0].decode("utf-8"), info[1].replace(" ", "_"), "")
			if not os.path.exists(package_path):
				os.makedirs(package_path)
			if info[2]:
				f = open(package_path + "password.txt", "w")
				f.write(info[2] + "\n")
				f.close()
		#add packages to gui and manager
		for package_name, package_downloads in packages:
			info = packages_info[packages.index((package_name, package_downloads))]
			package_name = info[1].replace(" ", "_")
			package_path = os.path.join(info[0].decode("utf-8"), package_name, "")
			self.add_package(package_name, package_path, package_downloads, info[2])
			for download in package_downloads:
				tmp = []
				for service in download[2]:
					plugin, plugin_type = self.get_download_plugin(service)
					tmp.append((download[0][download[2].index(service)], plugin, plugin_type, service))
				self.add(package_path, download[1], tmp, download[3], download[4])

	def start_cb(self):
		"""Implementado solo para descargas"""
		model, paths = self.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if len(paths[0]) > 1:
				logger.info("Start file: %s" % self.download_manager.start(model.get_value(model.get_iter(paths[0]), 3)))
			else:
				logger.info("Start package.")
				for item in self.package_files(model.get_iter(paths[0])):
					self.start(item)

	def stop_cb(self):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if len(paths[0]) > 1:
				logger.info("Stop file: %s" % self.download_manager.stop(model.get_value(model.get_iter(paths[0]), 3)))
			else:
				logger.info("Stop package.")
				for item in self.downloads.package_files(model.get_iter(paths[0])):
					self.download_manager.stop(item)

	def clear_cb(self):
		"""Implementado solo para descargas"""
		files = self.downloads.clear()
		logger.info("Cleared: %s" % files)
		if len(files) > 0:
			self.download_manager.clear(files)

	def move_up_cb(self):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if not len(paths[0]) > 1:
				logger.info("Move up: %s" % self.downloads.move_up(model.get_iter(paths[0])))

	def move_down_cb(self):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if not len(paths[0]) > 1:
				logger.info("Move down: %s" % self.downloads.move_down(model.get_iter(paths[0])))

	def delete_cb(self):
		"""Implementado solo para descargas"""
		model, paths = self.treeview.get_selection().get_selected_rows()
		status = [cons.STATUS_STOP, cons.STATUS_PEND, cons.STATUS_ERROR]
		if len(paths) > 0:
			if len(paths[0]) > 2:
				name, link = self.delete_link(status, model.get_iter(paths[0]))
				if link:
					logger.warning("Remove %s: %s" % (link, self.download_manager.delete_link(name, link)))
			elif len(paths[0]) > 1:
				name = self.delete_file(status, model.get_iter(paths[0]))
				if name:
					logger.warning("Remove %s: %s" % (name, self.download_manager.clear([name])))
			else:
				files = self.delete_package(status, model.get_iter(paths[0]))
				if len(files) > 0:
					logger.warning("Remove package: %s" % self.download_manager.clear(files))
