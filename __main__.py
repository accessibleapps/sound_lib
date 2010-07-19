from pybass import *
from ctypes import *

def bass_call (function, *args):
 res = function(*args)
 if res == 0 or res == -1:
  raise SoundOutputError(BASS_ErrorGetCode())
 return res
