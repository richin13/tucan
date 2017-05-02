from distutils.core import setup
import py2exe

setup(
    name = 'Tucan Manager',
    description = 'Download Manager',
    version = '1.0',

    windows = [
                  {
                      'script': 'tucan.py',
                      'icon_resources': [(1, "tucan.ico")],

                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings, core',
                      'includes': 'gio,cairo, pango, pangocairo, atk, gobject, urllib2, Image, ImageOps, core, PIL'
                  }
              },
			  
	zipfile = None,
)
