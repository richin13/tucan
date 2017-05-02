#! /usr/bin/env python
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
import sys
import logging
import optparse

from core.dependencies import Dependencies

import core.pid_file as pid_file
import core.url_open as url_open
import core.config as config
import core.shared as shared
import core.cons as cons
import core.misc as misc

class Tucan:
	""""""
	def __init__(self):
		""""""
		#parse options
		parser = optparse.OptionParser()
		parser.add_option("-w", "--wizard", dest="wizard", help="setup: accounts, services, updates", metavar="TYPE")
		parser.add_option("-d", "--daemon", action="store_true", dest="daemon", default=False, help="no interaction interface (URL)")
		parser.add_option("-c", "--cli", action="store_true", dest="cli", default=False, help="command line interface (URL)")
		parser.add_option("-C", "--clean", action="store_true", dest="clean", default=False, help="remove ~/.tucan")
		parser.add_option("-i", "--input-links", dest="links_file", help="import links from FILE", metavar="FILE")
		parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print log to stdout")
		parser.add_option("-V", "--version", action="store_true", dest="version", default=False, help="print version and exit")
		self.options, self.args = parser.parse_args()

		if self.options.version:
			sys.exit("%s %s" % (cons.TUCAN_NAME, cons.TUCAN_VERSION))
			
		if self.options.clean:
			try:
				misc.remove_conf_dir()
			except Exception, e:
				sys.exit(e)

		if not os.path.exists(cons.CONFIG_PATH):
			os.mkdir(cons.CONFIG_PATH)

		#check for previous running instance
		self.pid_file = pid_file.PidFile(cons.PID_FILE)
		if self.pid_file.start():
			#config
			shared.configuration = config.Config()
			self.config = shared.configuration
			sys.path.append(cons.PLUGIN_PATH)

			#logging
			if os.path.exists(cons.LOG_FILE):
				if os.path.exists("%s.old" % cons.LOG_FILE):
					os.remove("%s.old" % cons.LOG_FILE)
				os.rename(cons.LOG_FILE, "%s.old" % cons.LOG_FILE)
			logging.basicConfig(level=logging.DEBUG, format=cons.LOG_FORMAT, filename=cons.LOG_FILE, filemode='w')
			self.logger = logging.getLogger(self.__class__.__name__)
		else:
			if self.options.wizard or self.options.daemon or self.options.cli:
				sys.exit("Already running or could not open ~/.tucan/tucan.pid")
			else:
				self.start_gui(False)
				sys.exit()

	def set_verbose(self, severity=logging.INFO):
		""""""
		console = logging.StreamHandler(sys.stdout)
		console.setLevel(severity)
		console.setFormatter(logging.Formatter('%(levelname)-7s %(name)s: %(message)s'))
		logging.getLogger("").addHandler(console)

	def start_ui(self):
		""""""
		misc.main_info(self.logger)

		shared.dependencies = Dependencies()

		if self.config.get_proxy_enabled():
			proxy_url, proxy_port = self.config.get_proxy()
			url_open.set_proxy(proxy_url, proxy_port)
		else:
			url_open.set_proxy(None)

		if self.options.wizard:
			self.set_verbose()
			self.start_wizard(self.options.wizard)
		elif self.options.daemon:
			self.set_verbose()
			if len(self.args) > 0:
				url = self.args[0]
			else:
				url = None
			self.start_daemon(self.options.links_file, url)
		elif self.options.cli:
			if len(self.args) > 0:
				url = self.args[0]
			else:
				url = None
			self.start_cli(self.options.links_file, url)
		else:
			if self.options.verbose:
				self.set_verbose()
			self.start_gui()

	def start_wizard(self, wizard_type):
		""""""
		from ui.console.wizard import Wizard
		from ui.console.no_ui import exception_hook

		#exception hook
		sys.excepthook = exception_hook

		w = Wizard()
		if wizard_type == "accounts":
			w.account_setup()
		elif wizard_type == "services":
			w.service_setup()
		elif wizard_type == "updates":
			w.update_setup()
		else:
			self.exit("TYPE should be one of: accounts, services or updates")
		
	def start_daemon(self, file, url):
		""""""
		from ui.console.no_ui import NoUi, exception_hook

		#exception hook
		sys.excepthook = exception_hook

		d = NoUi(file, url)
		d.run()

	def start_cli(self, file, url):
		""""""
		if cons.OS_WINDOWS:
			self.exit("No curses support.")
		else:
			from ui.console.no_ui import exception_hook
			from curses.wrapper import wrapper
			from ui.console.cli import Cli

			#exception hook
			sys.excepthook = exception_hook

			c = Cli(file, url)
			wrapper(c.run)

	def start_gui(self, unique=True):
		""""""
		message = "Use 'tucan --cli' for curses interface." 
		try:
			import pygtk
			pygtk.require('2.0')
			import gtk
			import gobject
		except:
			sys.exit("No GTK support. %s" % message)
		try:
			gtk.init_check()
		except:
			sys.exit("Could not connect to X server. %s" % message)
		try:
			from ui.gtk.gui import Gui, already_running, exception_hook
			from ui.gtk.recover import halt
		except Exception, e:
			#self.logger.exception(e)
			sys.exit("Tucan installed without GUI support. %s" % message)
			
		if unique:
			#recovery help
			sys.excepthook = exception_hook

			gobject.threads_init()
			try:
				shared.dependencies.set_recaptcha()
				Gui()
				gtk.main()
			except Exception, e:
				#self.logger.exception(e)
				self.logger.critical(e)
				halt(str(e))
		else:
			already_running()

	def exit(self, arg=0):
		""""""
		self.logger.debug("Exit: %s" % str(arg))
		self.pid_file.destroy()
		sys.exit(arg)

if __name__ == "__main__":
	tucan = Tucan()
	try:
		tucan.start_ui()
	except KeyboardInterrupt:
		tucan.exit("KeyboardInterrupt")
	except Exception, e:
		tucan.logger.exception(e)
		tucan.exit("Unhandled Error! Check the log file for details.")
	else:
		tucan.exit()
