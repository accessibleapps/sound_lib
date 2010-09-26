from pybass import *
from ctypes import *
from functools import update_wrapper

class BassError (Exception): pass

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

class SoundOutput(object):

 def __init__ (self, device=-1, frequency=44100, flags=BASS_DEVICE_3D, window=0, clsid=None):
  if platform.system() == 'Linux' and device == -1: #Bass wants default device set to 1 on linux
   device = 1
  BASS_Init(device, frequency, flags, window, clsid)

 def get_volume (self):
  volume = BASS_GetConfig(BASS_CONFIG_GVOL_STREAM)
  if volume:
   volume = volume / 100.0
  return volume

 def set_volume (self, volume):
  #Pass in a float 0.0 to 100.0 and watch the volume magically change
  bass_call(BASS_SetConfig, BASS_CONFIG_GVOL_STREAM, int(round(volume*100, 2)))

 volume = property(fget=get_volume, fset=set_volume)


class SoundInput(object):

 def __init__ (self, device=-1):
  if platform.system() == 'Linux' and device == -1: #Bass wants default device set to 1 on linux
   device = 1
  bass_call(BASS_RecordInit, device)

