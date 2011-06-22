import ctypes
import platform
import os

TYPES = {
 'Linux': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, ['.so', '.so64']),
 'Darwin': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, '.dylib'),
}
if platform.system() == 'Windows':
 TYPES['Windows'] = (ctypes.LibraryLoader(ctypes.WinDLL), ctypes.WINFUNCTYPE, '.dll')

def load_library(library, lib_path=''):
 which = TYPES[platform.system()]
 loader = which[0]
 ext = which[2]
 path = os.path.join(lib_path, library)
 if type(ext) == str:
  return loader.LoadLibrary('%s%s' % (path, ext))
 for n, i in enumerate(ext):
  try:
   loaded = loader.LoadLibrary('%s%s' % (path, i))
  except OSError:
   if n < len(ext):
    continue
   else:
    raise
 return loaded

def get_functype():
 return TYPES[platform.system()][1]
