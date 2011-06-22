import ctypes
import collections
import platform
import os

TYPES = {
 'Linux': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, ['.so', '.so64']),
 'Darwin': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, '.dylib'),
}
if platform.system() == 'Windows':
 TYPES['Windows'] = (ctypes.LibraryLoader(ctypes.WinDLL), ctypes.WINFUNCTYPE, '.dll')

class LibraryLoadError(Exception): pass

def load_library(library, lib_path=None):
 if not isinstance(lib_path, collections.Sequence):
  lib_path = [lib_path]
 for p in lib_path:
  path = os.path.join(p, library)
  libs = _find_libs(path)
  for p in libs:
   if not os.path.exists(p):
    libs.remove(p)
  lib = _do_load(libs)
  if lib is not None:
   return lib
 raise LibraryLoadError('unable to load %r' % library)

def _find_libs(path):
 ext = TYPES[platform.system()][2]
 possible_files = []
 if isinstance(ext, basestring):
  possible_files.append('%s%s' % (path, ext))
 elif isinstance(ext, collections.Sequence):
  for i in ext:
   possible_files.append('%s%s' % (path, i))
 return possible_files

def _do_load(files_to_try):
 loader = TYPES[platform.system()][0] 
 loaded = None
 for n, f in enumerate(files_to_try):
  try:
   loaded = loader.LoadLibrary(f)
  except OSError:
   if n >= len(files_to_try) - 1:
    raise
 return loaded

def get_functype():
 return TYPES[platform.system()][1]
