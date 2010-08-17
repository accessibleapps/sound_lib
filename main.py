from pybass import *
from ctypes import *

class BassError (Exception): pass

def bass_call(function, *args):
 """Makes a call to bass and raises an exception if it fails."""
 res = function(*args)
 if res == 0 or res == -1:
  raise BassError(BASS_ErrorGetCode())
 return res

def bass_call_0(function, *args):
 """Makes a call to bass and raises an exception if it fails.  Does not consider 0 an error."""
 res = function(*args)
 if res == -1:
  raise BassError(BASS_ErrorGetCode())
 return res

