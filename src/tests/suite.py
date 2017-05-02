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
import optparse
import unittest
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "../default_plugins/")))

LEVEL = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}

TEST_PREFIX = "test_"
TEST_SUFIX = ".py"
PATH_SEPARATOR = "/"

class Suite:
	""""""
	def __init__(self, path, method=None):
		""""""
		self.loader = unittest.TestLoader()
		self.test_files = []		
		if not path:
			path = os.listdir(".")
			
		self.recursive_walk_suites(path)
		
		if method:
			suite = []
			for tmp_suite in self.test_files:
				suite.append("%s.%s" %(tmp_suite, method))
		else:
			suite = self.test_files
		self.loaded_suite = self.loader.loadTestsFromNames(suite)

	def recursive_walk_suites(self, names, parent=""):
		""""""
		if not isinstance(names, list):
			if os.path.basename(names).startswith(TEST_PREFIX) and names.endswith(TEST_SUFIX):
				module_name = ".".join(names.split(TEST_SUFIX)[0].split(PATH_SEPARATOR))
				self.test_files.append(module_name)
		elif names:
			for path in names:
				path = os.path.join(parent, path)
				if os.path.isdir(path) and not os.path.basename(path).startswith("."):
					self.recursive_walk_suites(os.listdir(path), path)
				else:
					self.recursive_walk_suites(path)

if __name__ == '__main__':	
	parser = optparse.OptionParser()
	parser.add_option("-l", "--logging", dest="level", default="", help="set logger LEVEL (default=ERROR)", metavar="LEVEL")
	parser.add_option("-m", "--test-method", dest="method", default="", help="only test METHOD", metavar="METHOD")
	parser.add_option("-v", "--verbosity", dest="verbosity", default=1, help="set verbosity LEVEL (default=1)", metavar="LEVEL")
	options, args = parser.parse_args()

	logging.basicConfig(level=LEVEL.get(options.level.upper(), logging.ERROR))
	
	try:
		s = Suite(args, options.method)
	except Exception, e:
		print "Failed to load suite: %s" % e
	else:
		unittest.TextTestRunner(verbosity=int(options.verbosity)).run(s.loaded_suite)
