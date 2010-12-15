from pybass import *
from ctypes import *
from functools import update_wrapper

class BassError (Exception):
 """Error that is raised when there is a problem with a Bass call."""

 def __init__(self, code, description):
  self.code = code
  self.description = description

 def __str__(self):
  return '%d, %s' % (self.code, self.description)

def bass_call(function, *args):
 """Makes a call to bass and raises an exception if it fails."""
 res = function(*args)
 if res == 0 or res == -1:
  code = BASS_ErrorGetCode()
  raise BassError(code, get_error_description(code))
 return res

def bass_call_0(function, *args):
 """Makes a call to bass and raises an exception if it fails.  Does not consider 0 an error."""
 res = function(*args)
 if res == -1:
  code = BASS_ErrorGetCode()
  raise BassError(code, get_error_description(code))
 return res

def update_3d_system(func):
 def update_3d_system_wrapper(*args, **kwargs):
  val = func(*args, **kwargs)
  bass_call( BASS_Apply3D)
  return val
 update_wrapper(update_3d_system_wrapper, func)
 return update_3d_system_wrapper

