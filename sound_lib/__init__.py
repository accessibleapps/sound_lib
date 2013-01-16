import platform

def find_datafiles():
 from glob import glob
 import os
 import sound_lib
 path = os.path.join(sound_lib.__path__[0], 'lib')
 results = []
 system = platform.system()
 if system == 'Windows':
  file_ext = '*.dll'
 elif system == 'Darwin':
  file_ext = '*.dylib'
 else:
  file_ext = '*.so'

 for d in os.listdir(path):
  dest_dir = os.path.join('sound_lib', 'lib', d)

  source = glob(os.path.join(path, d, file_ext))
  results.append((dest_dir, source))
 return results
