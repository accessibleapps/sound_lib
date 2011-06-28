from glob import glob
import os
from main import BassError

import channel
import effects
import input
import listener
import music
import output
import recording
import stream

def py2exe_datafiles():
 path = os.path.join(__path__[0], 'lib')
 results = []
 for d in os.listdir(path):
  dest_dir = os.path.join('lib', d)
  source = glob(os.path.join(path, d, '*.dll'))
  results.append((dest_dir, source))
 return results
