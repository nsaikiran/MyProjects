from distutils.core import setup
import py2exe
import os,sys

# Find GTK+ installation path
__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]

setup(
    name = 'ChatRoomClient',
    description = 'By Team-09 of SG-06 of Batch 2010',
    version = '1.0',

    windows = [
                  {
                      'script': 'ChatRoomClient.py'
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
                      'includes': 'cairo, pango, gio, pangocairo, atk, gobject',
			"dll_excludes": ["POWRPROF.dll", "MSWSOCK.dll"]
                  }
              },

     data_files=[
                    #If using GTK+'s built in SVG support, uncomment these
                   os.path.join('C:\GTK', 'bin', 'gdk-pixbuf-query-loaders.exe'),
                  # os.path.join('C:\GTK', '..', 'runtime', 'bin', 'libxml2-2.dll'),
               ]
)
