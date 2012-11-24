
def py2exe_datafiles():
 from glob import glob
 import os
 import sound_lib
 path = os.path.join(sound_lib.__path__[0], 'lib')
 results = []
 for d in os.listdir(path):
  dest_dir = os.path.join('sound_lib', 'lib', d)
  source = glob(os.path.join(path, d, '*.dll'))
  results.append((dest_dir, source))
 return results
