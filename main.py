from pybass import *
from ctypes import *

class BassError (Exception): pass

def bass_call (function, *args):
 res = function(*args)
 if res == 0 or res == -1:
  raise BassError(BASS_ErrorGetCode())
 return res
